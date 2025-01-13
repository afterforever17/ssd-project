from datetime import datetime
from f1shop import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=True, nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    bank = db.Column(db.Integer, nullable=False, default=10)
    role = db.Column(db.String(10), nullable=False, default='customer')
    items = db.relationship('Item', backref='owner', lazy=True)

    @property
    def has_items(self):
        return self.role == 'pilot'
    
    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.bank}', '{self.role}')"

    


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

