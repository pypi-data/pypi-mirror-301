class Artist:
    def __init__(self, name, mbid, url, image, streamable, ontour, stats):
        self.name = name
        self.mbid = mbid
        self.url = url
        self.image = image
        self.streamable = streamable
        self.ontour = ontour
        self.stats = stats

    def __repr__(self):
        return f"Artist(name={self.name}, url={self.url})"
