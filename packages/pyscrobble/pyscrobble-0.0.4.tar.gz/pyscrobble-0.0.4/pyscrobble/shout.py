class Shout:
    def __init__(self, body, author, date, **kwargs):
        self.body = body
        self.author = author
        self.date = date
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"Shout(body={self.body}, author={self.author})"
