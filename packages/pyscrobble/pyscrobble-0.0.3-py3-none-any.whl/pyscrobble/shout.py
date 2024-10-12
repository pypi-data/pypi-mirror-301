class Shout:
    def __init__(self, body, author, date):
        self.body = body
        self.author = author
        self.date = date

    def __repr__(self):
        return f"Shout(body={self.body}, author={self.author})"
