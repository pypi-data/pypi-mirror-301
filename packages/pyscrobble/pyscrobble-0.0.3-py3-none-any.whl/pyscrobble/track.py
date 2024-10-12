class Track:
    def __init__(self, name, mbid, url, image, streamable, artist, album):
        self.name = name
        self.mbid = mbid
        self.url = url
        self.image = image
        self.streamable = streamable
        self.artist = artist
        self.album = album

    def __repr__(self):
        return f"Track(name={self.name}, artist={self.artist.name}, album={self.album.title})"
