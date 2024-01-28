from pytube import Playlist
from videodb import connect

from dotenv import load_dotenv

load_dotenv()


def get_youtube_playlist_video_urls(playlist_url):
    # TODO: Error and exception handling
    playlist = Playlist(playlist_url)
    urls = [url for url in playlist]
    return urls


def bulk_upload(urls):
    # Read VideoDB API key from env and create a connection
    conn = connect()
    # Get a collection
    coll = conn.get_collection()
    for url in urls:
        # Upload Videos to a collection checkout https://docs.videodb.io for more upload functions
        print(f"Uploading {url}")
        video = coll.upload(url=url)
        print(f"Uploaded {video.name}")
        print(f"Indexing {video.name}")
        video.index_spoken_words()
        print(f"Indexed {video.name}")
        print("-----")

# run bulk upload fn on list of videos
"""
urls = [
    "https://www.youtube.com/watch?v=lsODSDmY4CY",
    "https://www.youtube.com/watch?v=vZ4kOr38JhY",
    "https://www.youtube.com/watch?v=uak_dXHh6s4",
]
bulk_upload(urls)
"""

# run bulk upload fn on YouTube playlist
"""
playlist_url = "https://www.youtube.com/watch?v=jSMZoLjB9JE&list=PLoaVOjvkzQtwcMfopT02bXWzjmnnF5olS"
urls = get_youtube_playlist_video_urls(playlist_url)
bulk_upload(urls)
"""