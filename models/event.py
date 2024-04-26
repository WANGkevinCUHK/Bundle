from flask_mongoengine import MongoEngine
from models.user import User

db = MongoEngine()

class Event(db.Document):
    title = db.StringField(required=True)
    location = db.StringField()
    time = db.DateTimeField()
    description = db.StringField()
    creator = db.ReferenceField(User)
    participants = db.ListField(db.ReferenceField(User))

    def to_json(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "location": self.location,
            "time": self.time.isoformat() if self.time else None,
            "description": self.description,
            "creator": self.creator.to_json(),
            "participants": [participant.to_json() for participant in self.participants]
        }