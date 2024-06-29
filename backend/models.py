# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from datetime import date

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    dinner = db.Column(db.Boolean, nullable=False)
    lunch = db.Column(db.Boolean, nullable=False)
    image_url = db.Column(db.String, nullable=False)

class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    diners = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time_of_day = db.Column(Enum('dinner', 'lunch', name='time_of_day'), nullable=False)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    reservations = db.Column(db.Integer, nullable=True, default=0)
    reservations_list = db.relationship('Reservation', backref='customer', lazy=True)

