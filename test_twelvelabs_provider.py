"""Tests for the opt-in TwelveLabs backend (twelvelabs_provider).

The unit tests mock the TwelveLabs SDK and need no network or API key.
The live test exercises real Marengo search + Pegasus analyze and is skipped
unless both TWELVELABS_API_KEY and TWELVELABS_INDEX_ID are set.

Run with: python -m unittest test_twelvelabs_provider
"""

import os
import unittest
from types import SimpleNamespace
from unittest import mock

import twelvelabs_provider as provider


class SearchShapeTest(unittest.TestCase):
    def test_search_returns_videodb_compatible_shape(self):
        items = [
            SimpleNamespace(
                transcription="a goal is scored",
                thumbnail_url="https://t/1.jpg",
                video_id="v1",
                start=0.0,
                end=8.0,
            ),
            SimpleNamespace(
                transcription=None,
                thumbnail_url=None,
                video_id="v2",
                start=4.0,
                end=12.0,
            ),
        ]
        fake = mock.Mock()
        fake.search.query.return_value = items

        with mock.patch.dict(os.environ, {"TWELVELABS_INDEX_ID": "idx"}), \
                mock.patch.object(provider, "get_client", return_value=fake):
            result = provider.search("goal")

        self.assertEqual(result["compilationVideo"], None)
        self.assertEqual(len(result["chunks"]), 2)
        # First chunk uses the transcription; second falls back to a locator.
        self.assertEqual(result["chunks"][0]["text"], "a goal is scored")
        self.assertIn("v2", result["chunks"][1]["text"])
        # Search wiring uses the configured index and multimodal options.
        _, kwargs = fake.search.query.call_args
        self.assertEqual(kwargs["index_id"], "idx")
        self.assertEqual(kwargs["search_options"], provider.SEARCH_OPTIONS)
        self.assertEqual(kwargs["query_text"], "goal")

    def test_get_video_uses_pegasus_summary(self):
        fake = mock.Mock()
        fake.analyze.return_value = SimpleNamespace(data="A soccer highlight.")
        with mock.patch.object(provider, "get_client", return_value=fake):
            result = provider.get_video("v1")

        self.assertEqual(result["video"]["id"], "v1")
        self.assertEqual(result["video"]["transcript"], "A soccer highlight.")
        _, kwargs = fake.analyze.call_args
        self.assertEqual(kwargs["model_name"], provider.PEGASUS_MODEL)
        self.assertEqual(kwargs["video_id"], "v1")

    def test_missing_index_id_raises(self):
        with mock.patch.dict(os.environ, {}, clear=True), \
                mock.patch.object(provider, "get_client", return_value=mock.Mock()):
            with self.assertRaises(provider.TwelveLabsError):
                provider.search("anything")


@unittest.skipUnless(
    os.getenv("TWELVELABS_API_KEY") and os.getenv("TWELVELABS_INDEX_ID"),
    "set TWELVELABS_API_KEY and TWELVELABS_INDEX_ID for the live test",
)
class LiveTest(unittest.TestCase):
    def test_marengo_text_embedding(self):
        vec = provider.text_embedding("a cat playing piano")
        self.assertEqual(len(vec), 512)

    def test_marengo_search_and_pegasus_answer(self):
        result = provider.search("goal")
        self.assertIn("chunks", result)
        self.assertTrue(result["chunks"])
        video_id = result["chunks"][0]["videoId"]
        answer = provider.get_video(video_id)
        self.assertTrue(answer["video"]["transcript"])


if __name__ == "__main__":
    unittest.main()
