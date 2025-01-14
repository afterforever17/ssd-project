from datetime import datetime
from f1shop import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    bank = db.Column(db.Integer, nullable=False, default=10)
    role = db.Column(db.String(10), nullable=False, default='customer')
    team = db.Column(db.String(30), nullable=False, default='noteam')
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
    image_file = db.Column(db.String(20), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class PilotRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(10), nullable=False)
    pilot_id = db.Column(db.Integer, nullable=True)
    pilot_name = db.Column(db.String(40), nullable=False)
    pilot_email = db.Column(db.String(120), nullable=False)
    pilot_password = db.Column(db.String(60), nullable=False)
    pilot_image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    pilot_bank = db.Column(db.Integer, nullable=False, default=1000)
    pilot_team = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='pending')
    type = db.Column(db.Integer, nullable=False, default='pilot')


    def __repr__(self):
        return f"Request('{self.action}', '{self.pilot_name}', '{self.pilot_team}')"

class ItemRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(10), nullable=False)
    item_id = db.Column(db.Integer, nullable=True)
    item_name = db.Column(db.String(40), nullable=False)
    item_image_file = db.Column(db.String(20), nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(10), nullable=False, default='pending')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.Integer, nullable=False, default='item')

