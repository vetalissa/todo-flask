from apps.app import db
from apps.todoapps.users.models import User


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    description = db.Column(db.String)
    important = db.Column(db.Boolean, default=False)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __repr__(self):
        return f'{self.user_id}: {self.title} - {self.description}'
