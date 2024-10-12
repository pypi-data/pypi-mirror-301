class User:
    def __init__(self, name, url, image, country, age, gender, subscriber, playcount, playlists, bootstrap, registered, type):
        self.name = name
        self.url = url
        self.image = image
        self.country = country
        self.age = age
        self.gender = gender
        self.subscriber = subscriber
        self.playcount = playcount
        self.playlists = playlists
        self.bootstrap = bootstrap
        self.registered = registered
        self.type = type

    def __repr__(self):
        return f"User(name={self.name}, url={self.url})"
