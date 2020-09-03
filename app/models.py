from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    phone = db.Column(db.String(14), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=1)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(64), nullable=False, default='sales')
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f"<Role {self.role}>"


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(64), nullable=False, unique=True)
    stock = db.Column(db.Integer)
    price = db.Column(db.Float)

    def __repr__(self):
        return f"<Product {self.name}>"

    
class Discount(db.Model):
    __tablename__ = 'discounts'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), nullable=False, unique=True)
    rate = db.Column(db.Float)
    amount = db.Column(db.Float)
    expiry_date = db.Column(db.Date)

    def __repr__(self):
        return f"<Dicount {self.code}>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


