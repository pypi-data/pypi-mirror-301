class Album:
    def __init__(self, title, mbid, url, image, artist):
        self.title = title
        self.mbid = mbid
        self.url = url
        self.image = image
        self.artist = artist

    def __repr__(self):
        return f"Album(title={self.title}, artist={self.artist.name})"
