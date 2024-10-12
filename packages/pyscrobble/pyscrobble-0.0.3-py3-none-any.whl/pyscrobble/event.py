class Event:
    def __init__(self, id, title, artists, venue, location, date, image, url, attendees, description):
        self.id = id
        self.title = title
        self.artists = artists
        self.venue = venue
        self.location = location
        self.date = date
        self.image = image
        self.url = url
        self.attendees = attendees
        self.description = description

    def __repr__(self):
        return f"Event(title={self.title}, artists={self.artists}, venue={self.venue})"
