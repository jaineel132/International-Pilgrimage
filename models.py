from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    bookings = db.relationship('Booking', backref='user', lazy='dynamic')
    trip_plans = db.relationship('TripPlan', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Pilgrimage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50))
    best_time = db.Column(db.String(100))
    image_url = db.Column(db.String(200))
    # Relationships
    bookings = db.relationship('Booking', back_populates='pilgrimage')
    trip_plans = db.relationship('TripPlan', back_populates='pilgrimage')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pilgrimage_id = db.Column(db.Integer, db.ForeignKey('pilgrimage.id'), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    special_requirements = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to Pilgrimage
    pilgrimage = db.relationship('Pilgrimage', back_populates='bookings')

class TripPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pilgrimage_id = db.Column(db.Integer, db.ForeignKey('pilgrimage.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    num_travelers = db.Column(db.Integer, nullable=False)
    accommodation_type = db.Column(db.String(20), nullable=False)
    transportation = db.Column(db.String(20), nullable=False)
    additional_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to Pilgrimage
    pilgrimage = db.relationship('Pilgrimage', back_populates='trip_plans')
print("Models have been defined")
