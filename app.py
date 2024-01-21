import os

from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from videodb import connect, SearchError

load_dotenv()

# Flask config
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.url_map.strict_slashes = False
CORS(app)


def get_connection():
    conn = connect()
    return conn


@app.route("/")
def hello():
    return "StreamRAG: Your Go-To Video Search Agent"


@app.route("/videos", methods=["GET"])
def list_videos():
    """
    Get a list of all videos in the database of your default collection.
    """
    conn = get_connection()
    all_videos = conn.get_collection().get_videos()
    all_videos = [
        {
            "id": vid.id,
            "title": vid.name,
            "url": vid.stream_url,
            "length": round(float(vid.length)),
        }
        for vid in all_videos
    ]
    response = {"videos": all_videos}
    return response


@app.route("/video/<id>", methods=["GET"])
def get_video(id):
    """
    Get a single video by id from default collection
    """
    conn = get_connection()
    all_videos = conn.get_collection().get_videos()

    vid = next(vid for vid in all_videos if vid.id == id)

    print("vid", vid)
    vid.get_transcript()
    transcript_text = vid.transcript_text

    response = {
        "video": {
            "id": vid.id,
            "title": vid.name,
            "url": vid.stream_url,
            "length": round(float(vid.length)),
            "transcript": transcript_text,
        }
    }
    return response


@app.route("/search", methods=["POST"])
def search_videos():
    """
    Search across videos in the database in default collection
    """
    data = request.get_json()
    query = data.get("query")
    conn = get_connection()
    try:
        coll = conn.get_collection()
        search_results = coll.search(query)
        search_results.compile()
        compilation_vid = search_results.player_url
    except SearchError:
        return "No Search Results found", 404

    shots = [
        {"text": shot.text, "video": shot.stream_url}
        for shot in search_results.get_shots()
    ]
    response = {"compilationVideo": compilation_vid, "chunks": shots}
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
