"""Opt-in TwelveLabs backend for StreamRAG.

By default StreamRAG talks to VideoDB (see ``app.py``). This module provides an
alternative, opt-in backend powered by TwelveLabs:

* **Marengo** handles retrieval. ``search()`` runs a multimodal (visual + audio)
  search over an index and returns the same ``{compilationVideo, chunks}`` shape
  the VideoDB path returns, so the OpenAPI action and GPT prompt are unchanged.
* **Pegasus** handles answers. ``get_video()`` uses video understanding to
  generate a description for an individual video instead of a raw transcript.

To switch StreamRAG over to TwelveLabs set two env vars (see ``.env.sample``)::

    VIDEO_SEARCH_PROVIDER=twelvelabs
    TWELVELABS_API_KEY=tlk_...
    TWELVELABS_INDEX_ID=<your index id>

When ``VIDEO_SEARCH_PROVIDER`` is unset (or anything other than ``twelvelabs``)
this module is never imported and behavior is identical to upstream.

Create an index and upload videos with the TwelveLabs SDK once, up front::

    from twelvelabs import TwelveLabs
    client = TwelveLabs(api_key="tlk_...")
    index = client.indexes.create(
        index_name="streamrag",
        models=[{"model_name": "marengo3.0", "model_options": ["visual", "audio"]},
                {"model_name": "pegasus1.2", "model_options": ["visual", "audio"]}],
    )
    task = client.tasks.create(index_id=index.id, video_url="https://...")
    client.tasks.wait_for_done(task_id=task.id)

Grab a free API key at https://twelvelabs.io (generous free tier).
"""

import os

from twelvelabs import TwelveLabs

# Marengo model used for both search and (text) embeddings.
MARENGO_MODEL = os.getenv("TWELVELABS_MARENGO_MODEL", "marengo3.0")
# Pegasus model used for video understanding / answers.
PEGASUS_MODEL = os.getenv("TWELVELABS_PEGASUS_MODEL", "pegasus1.2")
# Search modalities; Marengo indexes are typically created with visual + audio.
SEARCH_OPTIONS = ["visual", "audio"]


class TwelveLabsError(Exception):
    """Raised when the TwelveLabs backend is misconfigured."""


def _index_id():
    index_id = os.getenv("TWELVELABS_INDEX_ID")
    if not index_id:
        raise TwelveLabsError(
            "TWELVELABS_INDEX_ID is not set. Create an index and upload videos "
            "with the TwelveLabs SDK, then set TWELVELABS_INDEX_ID."
        )
    return index_id


def get_client():
    """Create a TwelveLabs client from ``TWELVELABS_API_KEY``."""
    api_key = os.getenv("TWELVELABS_API_KEY")
    if not api_key:
        raise TwelveLabsError("TWELVELABS_API_KEY is not set.")
    return TwelveLabs(api_key=api_key)


def list_videos():
    """Mirror ``app.list_videos``: return ``{"videos": [...]}``."""
    client = get_client()
    index_id = _index_id()
    videos = []
    for vid in client.indexes.videos.list(index_id=index_id):
        meta = getattr(vid, "system_metadata", None)
        videos.append(
            {
                "id": vid.id,
                "title": getattr(meta, "filename", None) or vid.id,
                "url": getattr(meta, "video_url", None),
                "length": round(float(getattr(meta, "duration", 0) or 0)),
            }
        )
    return {"videos": videos}


def get_video(video_id):
    """Mirror ``app.get_video`` but answer with Pegasus video understanding.

    Instead of a raw transcript we ask Pegasus to summarize the video, which is
    the "answers" half of the integration. The summary is returned in the same
    ``transcript`` field so the existing OpenAPI schema and GPT prompt work
    unchanged.
    """
    client = get_client()
    res = client.analyze(
        model_name=PEGASUS_MODEL,
        video_id=video_id,
        prompt="Summarize this video, including the key topics and notable moments.",
        max_tokens=2048,
    )
    return {
        "video": {
            "id": video_id,
            "title": video_id,
            "url": None,
            "length": None,
            "transcript": res.data or "",
        }
    }


def search(query):
    """Mirror ``app.search_videos``: return ``{"compilationVideo", "chunks"}``.

    Marengo multimodal search returns ranked clips. Each clip becomes a chunk
    with its transcription text and thumbnail. TwelveLabs does not stitch a
    compilation video, so ``compilationVideo`` is ``None`` and the GPT falls
    back to the per-clip references (the prompt already handles this).
    """
    client = get_client()
    index_id = _index_id()
    results = client.search.query(
        index_id=index_id,
        search_options=SEARCH_OPTIONS,
        query_text=query,
        group_by="clip",
        page_limit=10,
    )
    chunks = []
    for item in results:
        # Prefer the transcription when the index was built with it; otherwise
        # fall back to a human-readable locator so the chunk is never empty.
        text = item.transcription or (
            f"Clip from video {item.video_id} "
            f"({item.start:.0f}s-{item.end:.0f}s)"
        )
        chunks.append(
            {
                "text": text,
                "video": item.thumbnail_url,
                "videoId": item.video_id,
                "start": item.start,
                "end": item.end,
            }
        )
    return {"compilationVideo": None, "chunks": chunks}


def text_embedding(text):
    """Return a 512-dim Marengo embedding for ``text``.

    Exposed for callers that want to build their own vector index on top of
    Marengo rather than use the hosted search above.
    """
    client = get_client()
    res = client.embed.create(model_name=MARENGO_MODEL, text=text)
    return res.text_embedding.segments[0].float_
