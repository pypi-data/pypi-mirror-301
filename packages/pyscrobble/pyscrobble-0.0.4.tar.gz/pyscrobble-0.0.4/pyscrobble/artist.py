class Artist:
    def __init__(self, name, mbid, url, image, streamable, ontour, stats, **kwargs):
        self.name = name
        self.mbid = mbid
        self.url = url
        self.image = image
        self.streamable = streamable
        self.ontour = ontour
        self.stats = stats
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"Artist(name={self.name}, url={self.url})"
