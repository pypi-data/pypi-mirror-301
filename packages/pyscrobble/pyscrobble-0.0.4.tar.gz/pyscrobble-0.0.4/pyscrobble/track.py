class Track:
    def __init__(self, name, mbid, url, image, streamable, artist, album, **kwargs):
        self.name = name
        self.mbid = mbid
        self.url = url
        self.image = image
        self.streamable = streamable
        self.artist = artist
        self.album = album
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"Track(name={self.name}, artist={self.artist.name}, album={self.album.title})"
