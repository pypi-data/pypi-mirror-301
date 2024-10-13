class Album:
    def __init__(self, title, mbid, url, image, artist, **kwargs):
        self.title = title
        self.mbid = mbid
        self.url = url
        self.image = image
        self.artist = artist
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"Album(title={self.title}, artist={self.artist.name})"
