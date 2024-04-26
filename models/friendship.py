from flask_mongoengine import MongoEngine
from models.user import User

db = MongoEngine()

class Friendship(db.Document):
    user1 = db.ReferenceField(User, required=True)
    user2 = db.ReferenceField(User, required=True)
    status = db.StringField(choices=('pending', 'accepted'), default='pending')