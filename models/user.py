from flask_mongoengine import MongoEngine

db = MongoEngine()

class User(db.Document):
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    name = db.StringField()
    friends = db.ListField(db.ReferenceField('User'))

    def to_json(self):
        return {
            "email": self.email,
            "name": self.name,
            "friends": [friend.email for friend in self.friends]
        }