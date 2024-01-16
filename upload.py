from videodb import connect


def bulk_upload():
    #Read VideoDB API key from env and create a connection
    conn = connect()
    # Get a collection
    coll = conn.get_collection()
    # Upload Videos to a collection
    coll.upload(url="https://www.youtube.com/watch?v=lsODSDmY4CY")
    coll.upload(url="https://www.youtube.com/watch?v=vZ4kOr38JhY")
    coll.upload(url="https://www.youtube.com/watch?v=uak_dXHh6s4")
    #ADD more to index for StreamRAG agent

    for video in coll.get_videos():
        video.index_spoken_words()
        print(f"Indexed {video.name}")

#run bulk upload.