from flask import Blueprint, jsonify, request, current_app
from flask_login import current_user, login_required
from models import Pilgrimage, Review, TravelTip, User, SavedPilgrimage, TripPlan
from extensions import db, cache
import requests
from datetime import datetime
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/pilgrimages')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_pilgrimages():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pilgrimages = Pilgrimage.query.paginate(page=page, per_page=per_page)
    
    result = {
        'items': [{
            'id': p.id,
            'name': p.name,
            'location': p.location,
            'image_url': p.image_url,
            'price': p.price,
            'average_rating': p.average_rating,
            'reviews_count': p.reviews.count()
        } for p in pilgrimages.items],
        'total': pilgrimages.total,
        'pages': pilgrimages.pages,
        'current_page': pilgrimages.page
    }
    
    return jsonify(result)

@api_bp.route('/pilgrimages/<int:id>')
def get_pilgrimage(id):
    pilgrimage = Pilgrimage.query.get_or_404(id)
    
    # Get weather data if coordinates are available
    weather_data = None
    if pilgrimage.latitude and pilgrimage.longitude:
        weather_data = get_weather(pilgrimage.latitude, pilgrimage.longitude)
    
    # Check if the user has saved this pilgrimage
    is_saved = False
    if current_user.is_authenticated:
        saved = SavedPilgrimage.query.filter_by(
            user_id=current_user.id, 
            pilgrimage_id=pilgrimage.id
        ).first()
        is_saved = saved is not None
    
    result = {
        'id': pilgrimage.id,
        'name': pilgrimage.name,
        'location': pilgrimage.location,
        'description': pilgrimage.description,
        'duration': pilgrimage.duration,
        'best_time': pilgrimage.best_time,
        'image_url': pilgrimage.image_url,
        'gallery': pilgrimage.gallery_images,
        'latitude': pilgrimage.latitude,
        'longitude': pilgrimage.longitude,
        'price': pilgrimage.price,
        'difficulty_level': pilgrimage.difficulty_level,
        'virtual_tour_url': pilgrimage.virtual_tour_url,
        'average_rating': pilgrimage.average_rating,
        'reviews_count': pilgrimage.reviews.count(),
        'weather': weather_data,
        'is_saved': is_saved
    }
    
    return jsonify(result)

@api_bp.route('/pilgrimages/<int:id>/reviews')
def get_pilgrimage_reviews(id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    reviews = Review.query.filter_by(pilgrimage_id=id).order_by(Review.created_at.desc())
    pagination = reviews.paginate(page, per_page, error_out=False)
    
    reviews = Review.query.filter_by(pilgrimage_id=id).order_by(
        Review.created_at.desc()
    ).paginate(page=page, per_page=per_page)
    
    result = {
        'items': [{
            'id': r.id,
            'rating': r.rating,
            'comment': r.comment,
            'images': r.review_images,
            'created_at': r.created_at.isoformat(),
            'author': {
                'id': r.author.id,
                'username': r.author.username,
                'profile_picture': r.author.profile_picture
            },
            'helpful_votes': r.helpful_votes
        } for r in reviews.items],
        'total': reviews.total,
        'pages': reviews.pages,
        'current_page': reviews.page
    }
    
    return jsonify(result)

@api_bp.route('/pilgrimages/<int:id>/tips')
def get_pilgrimage_tips(id):
    tips = TravelTip.query.filter_by(pilgrimage_id=id).all()
    
    result = [{
        'id': tip.id,
        'title': tip.title,
        'content': tip.content,
        'category': tip.category,
        'created_at': tip.created_at.isoformat()
    } for tip in tips]
    
    return jsonify(result)

@api_bp.route('/pilgrimages/search')
def search_pilgrimages():
    query = request.args.get('q', '')
    location = request.args.get('location', '')
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 100000, type=float)
    difficulty = request.args.get('difficulty', '')
    
    # Start with base query
    pilgrimages_query = Pilgrimage.query
    
    # Apply filters
    if query:
        pilgrimages_query = pilgrimages_query.filter(
            Pilgrimage.name.ilike(f'%{query}%') | 
            Pilgrimage.description.ilike(f'%{query}%')
        )
    
    if location:
        pilgrimages_query = pilgrimages_query.filter(
            Pilgrimage.location.ilike(f'%{location}%')
        )
    
    pilgrimages_query = pilgrimages_query.filter(
        Pilgrimage.price >= min_price,
        Pilgrimage.price <= max_price
    )
    
    if difficulty:
        pilgrimages_query = pilgrimages_query.filter(
            Pilgrimage.difficulty_level == difficulty
        )
    
    # Execute query
    pilgrimages = pilgrimages_query.all()
    
    result = [{
        'id': p.id,
        'name': p.name,
        'location': p.location,
        'image_url': p.image_url,
        'price': p.price,
        'average_rating': p.average_rating,
        'reviews_count': p.reviews.count()
    } for p in pilgrimages]
    
    return jsonify(result)

@api_bp.route('/save-pilgrimage/<int:id>', methods=['POST'])
@login_required
def save_pilgrimage(id):
    pilgrimage = Pilgrimage.query.get_or_404(id)
    
    # Check if already saved
    existing = SavedPilgrimage.query.filter_by(
        user_id=current_user.id,
        pilgrimage_id=id
    ).first()
    
    if existing:
        return jsonify({'message': 'Already saved', 'saved': True})
    
    # Save the pilgrimage
    saved = SavedPilgrimage(user_id=current_user.id, pilgrimage_id=id)
    db.session.add(saved)
    db.session.commit()
    
    return jsonify({'message': 'Pilgrimage saved', 'saved': True})

@api_bp.route('/unsave-pilgrimage/<int:id>', methods=['POST'])
@login_required
def unsave_pilgrimage(id):
    # Find and delete the saved pilgrimage
    saved = SavedPilgrimage.query.filter_by(
        user_id=current_user.id,
        pilgrimage_id=id
    ).first()
    
    if not saved:
        return jsonify({'message': 'Not saved', 'saved': False})
    
    db.session.delete(saved)
    db.session.commit()
    
    return jsonify({'message': 'Pilgrimage unsaved', 'saved': False})

@api_bp.route('/user/saved-pilgrimages')
@login_required
def get_saved_pilgrimages():
    saved = SavedPilgrimage.query.filter_by(user_id=current_user.id).all()
    
    result = [{
        'id': s.pilgrimage.id,
        'name': s.pilgrimage.name,
        'location': s.pilgrimage.location,
        'image_url': s.pilgrimage.image_url,
        'price': s.pilgrimage.price,
        'saved_at': s.created_at.isoformat()
    } for s in saved]
    
    return jsonify(result)

@api_bp.route('/user/upcoming-trips')
@login_required
def get_upcoming_trips():
    today = datetime.now().date()
    trips = TripPlan.query.filter(
        TripPlan.user_id == current_user.id,
        TripPlan.start_date >= today
    ).order_by(TripPlan.start_date).all()
    
    result = [{
        'id': t.id,
        'pilgrimage_name': t.pilgrimage.name,
        'location': t.pilgrimage.location,
        'start_date': t.start_date.isoformat(),
        'end_date': t.end_date.isoformat(),
        'days_until': (t.start_date - today).days,
        'payment_status': t.payment_status
    } for t in trips]
    
    return jsonify(result)

def get_weather(lat, lon):
    """Get current weather data for a location"""
    api_key = current_app.config['OPENWEATHER_API_KEY']
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
    except Exception as e:
        print(f"Error fetching weather data: {e}")
    
    return None

