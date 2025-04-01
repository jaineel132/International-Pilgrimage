from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import datetime
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.String(100))
    country = db.Column(db.String(50))
    profile_picture = db.Column(db.String(200))
    bio = db.Column(db.Text)
    preferences = db.Column(db.String(50), default='all')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy='dynamic')
    trip_plans = db.relationship('TripPlan', backref='user', lazy='dynamic')
    reviews = db.relationship('Review', backref='author', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_unread_notifications_count(self):
        return Notification.query.filter_by(user_id=self.id, read=False).count()

class Pilgrimage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50))
    best_time = db.Column(db.String(100))
    image_url = db.Column(db.String(200))
    gallery = db.Column(db.Text)  # JSON string of image URLs
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    price = db.Column(db.Float, default=0.0)
    difficulty_level = db.Column(db.String(20), default='moderate')
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='pilgrimage', lazy='dynamic')
    trip_plans = db.relationship('TripPlan', backref='pilgrimage', lazy='dynamic')
    reviews = db.relationship('Review', backref='pilgrimage', lazy='dynamic')
    
    @property
    def average_rating(self):
        reviews = Review.query.filter_by(pilgrimage_id=self.id).all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)
    
    @property
    def gallery_images(self):
        if not self.gallery:
            return []
        try:
            return json.loads(self.gallery)
        except:
            return []

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pilgrimage_id = db.Column(db.Integer, db.ForeignKey('pilgrimage.id'), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    special_requirements = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TripPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pilgrimage_id = db.Column(db.Integer, db.ForeignKey('pilgrimage.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    num_travelers = db.Column(db.Integer, nullable=False)
    accommodation_type = db.Column(db.String(20), nullable=False)
    transportation = db.Column(db.String(20), nullable=False)
    meal_preference = db.Column(db.String(20), default='no_preference')
    guide_required = db.Column(db.Boolean, default=False)
    additional_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmation_code = db.Column(db.String(20), unique=True)
    total_price = db.Column(db.Float)
    payment_status = db.Column(db.String(20), default='pending')
    payment_id = db.Column(db.String(100))
    status = db.Column(db.String(20), default='planned')  # planned, ongoing, completed, cancelled
    itinerary = db.Column(db.Text)  # JSON string of daily activities
    
    # Add these new fields
    payment_method = db.Column(db.String(50))
    payment_date = db.Column(db.DateTime)
    refund_reason = db.Column(db.String(100))
    refund_details = db.Column(db.Text)
    refund_requested_at = db.Column(db.DateTime)
    
    # Add price breakdown fields
    base_price = db.Column(db.Float)
    accommodation_fee = db.Column(db.Float)
    transportation_fee = db.Column(db.Float)
    guide_fee = db.Column(db.Float)
    tax_amount = db.Column(db.Float)
    discount_amount = db.Column(db.Float)
    
    @property
    def itinerary_days(self):
        if not self.itinerary:
            return []
        try:
            return json.loads(self.itinerary)
        except:
            return []

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pilgrimage_id = db.Column(db.Integer, db.ForeignKey('pilgrimage.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    images = db.Column(db.Text)  # JSON string of image URLs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    helpful_votes = db.Column(db.Integer, default=0)
    
    @property
    def review_images(self):
        if not self.images:
            return []
        try:
            return json.loads(self.images)
        except:
            return []

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(200))
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

print("Enhanced models have been defined!")

