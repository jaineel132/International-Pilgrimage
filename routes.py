from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app, abort
from flask_login import login_required, current_user
from models import Pilgrimage, Booking, TripPlan, Review, User
from forms import BookingForm, TripPlanningForm, ProfileForm, ReviewForm
from extensions import db, mail
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename
from flask_mail import Message
import random
import string

main = Blueprint('main', __name__)

def generate_confirmation_code():
    """Generate a random confirmation code for trip plans"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def calculate_trip_price(pilgrimage, num_travelers, accommodation_type, transportation, guide_required):
    """Calculate the total price of a trip based on various factors"""
    # Base price from pilgrimage
    base_price = pilgrimage.price or 100.0  # Default to 100 if no price set
    
    # Accommodation multiplier
    accommodation_multipliers = {
        'budget': 1.0,
        'standard': 1.5,
        'luxury': 2.5
    }
    
    # Transportation multiplier
    transportation_multipliers = {
        'public': 1.0,
        'private': 1.8,
        'guided_tour': 2.2
    }
    
    # Guide fee
    guide_fee = 50.0 if guide_required else 0.0
    
    # Calculate total
    total = (base_price * num_travelers * 
             accommodation_multipliers.get(accommodation_type, 1.0) * 
             transportation_multipliers.get(transportation, 1.0) + 
             guide_fee)
    
    return round(total, 2)

def send_trip_confirmation_email(user, trip_plan, pilgrimage):
    """Send a confirmation email with trip details"""
    msg = Message(
        subject="Your Sacred Journey Trip Confirmation",
        recipients=[user.email]
    )
    
    # Format dates
    start_date = trip_plan.start_date.strftime('%B %d, %Y')
    end_date = trip_plan.end_date.strftime('%B %d, %Y')
    
    # Create email body
    msg.html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #1a233e; color: white; padding: 10px 20px; text-align: center; }}
            .content {{ padding: 20px; border: 1px solid #ddd; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #777; }}
            .details {{ margin: 20px 0; }}
            .details table {{ width: 100%; border-collapse: collapse; }}
            .details table td, .details table th {{ padding: 8px; border-bottom: 1px solid #ddd; }}
            .price {{ font-size: 24px; font-weight: bold; color: #1a233e; text-align: right; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Sacred Journeys</h1>
            </div>
            <div class="content">
                <h2>Trip Confirmation</h2>
                <p>Dear {user.full_name or user.username},</p>
                <p>Thank you for planning your pilgrimage with Sacred Journeys. Your trip has been confirmed!</p>
                
                <div class="details">
                    <h3>Trip Details</h3>
                    <table>
                        <tr>
                            <th align="left">Confirmation Code:</th>
                            <td>{trip_plan.confirmation_code}</td>
                        </tr>
                        <tr>
                            <th align="left">Pilgrimage:</th>
                            <td>{pilgrimage.name}</td>
                        </tr>
                        <tr>
                            <th align="left">Location:</th>
                            <td>{pilgrimage.location}</td>
                        </tr>
                        <tr>
                            <th align="left">Dates:</th>
                            <td>{start_date} to {end_date}</td>
                        </tr>
                        <tr>
                            <th align="left">Travelers:</th>
                            <td>{trip_plan.num_travelers}</td>
                        </tr>
                        <tr>
                            <th align="left">Accommodation:</th>
                            <td>{trip_plan.accommodation_type.capitalize()}</td>
                        </tr>
                        <tr>
                            <th align="left">Transportation:</th>
                            <td>{trip_plan.transportation.replace('_', ' ').capitalize()}</td>
                        </tr>
                        <tr>
                            <th align="left">Meal Preference:</th>
                            <td>{trip_plan.meal_preference.replace('_', ' ').capitalize()}</td>
                        </tr>
                        <tr>
                            <th align="left">Guide:</th>
                            <td>{'Yes' if trip_plan.guide_required else 'No'}</td>
                        </tr>
                    </table>
                </div>
                
                <div class="price">
                    Total: ${trip_plan.total_price}
                </div>
                
                <p>Please keep this confirmation for your records. You can also view your trip details in your dashboard.</p>
                
                <p>We look forward to helping you on your sacred journey!</p>
                
                <p>Best regards,<br>The Sacred Journeys Team</p>
            </div>
            <div class="footer">
                <p>© 2024 Sacred Journeys Explorer. All rights reserved.</p>
                <p>If you have any questions, please contact us at support@sacredjourneys.com</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@main.route('/')
def index():
    featured_pilgrimages = Pilgrimage.query.limit(3).all()
    return render_template('index.html', featured_pilgrimages=featured_pilgrimages)

@main.route('/pilgrimages')
def pilgrimages():
    page = request.args.get('page', 1, type=int)
    pilgrimages = Pilgrimage.query.paginate(page=page, per_page=9)
    return render_template('pilgrimages.html', pilgrimages=pilgrimages)

@main.route('/pilgrimage/<int:id>')
def pilgrimage(id):
    pilgrimage = Pilgrimage.query.get_or_404(id)
    booking_form = BookingForm()
    review_form = ReviewForm()
    reviews = Review.query.filter_by(pilgrimage_id=id).order_by(Review.created_at.desc()).all()
    return render_template('pilgrimage.html', pilgrimage=pilgrimage, form=booking_form, review_form=review_form, reviews=reviews)

@main.route('/book/<int:pilgrimage_id>', methods=['POST'])
@login_required
def book_pilgrimage(pilgrimage_id):
    pilgrimage = Pilgrimage.query.get_or_404(pilgrimage_id)
    # Redirect to trip planning with the pilgrimage pre-selected
    return redirect(url_for('main.plan_trip', pilgrimage_id=pilgrimage_id))

@main.route('/api/search')
def search():
    query = request.args.get('q', '').lower()
    pilgrimages = Pilgrimage.query.filter(
        (Pilgrimage.name.ilike(f'%{query}%')) | (Pilgrimage.location.ilike(f'%{query}%'))
    ).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'location': p.location,
        'image_url': p.image_url,
        'average_rating': p.average_rating,
        'reviews_count': p.reviews.count()
    } for p in pilgrimages])

@main.route('/dashboard')
@login_required
def dashboard():
    user_bookings = current_user.bookings.order_by(Booking.travel_date.desc()).all()
    user_trip_plans = TripPlan.query.filter_by(user_id=current_user.id).order_by(TripPlan.start_date.desc()).all()
    now = datetime.now().date()
    return render_template('dashboard.html', bookings=user_bookings, trip_plans=user_trip_plans, now=now)

@main.route('/trip_details/<int:trip_id>')
@login_required
def trip_details(trip_id):
    trip = TripPlan.query.get_or_404(trip_id)
    # Ensure the trip belongs to the current user
    if trip.user_id != current_user.id:
        abort(403)
    return render_template('trip_details.html', trip=trip)

@main.route('/plan_trip', methods=['GET', 'POST'])
@login_required
def plan_trip():
    form = TripPlanningForm()
    
    # Get all pilgrimages for the dropdown
    pilgrimages = Pilgrimage.query.all()
    form.pilgrimage.choices = [(str(p.id), p.name) for p in pilgrimages]
    
    # Pre-select pilgrimage if provided in URL
    pilgrimage_id = request.args.get('pilgrimage_id')
    if pilgrimage_id and request.method == 'GET':
        form.pilgrimage.data = pilgrimage_id
    
    if form.validate_on_submit():
        # Get the selected pilgrimage
        pilgrimage = Pilgrimage.query.get(int(form.pilgrimage.data))
        
        # Generate confirmation code
        confirmation_code = generate_confirmation_code()
        
        # Calculate total price
        total_price = calculate_trip_price(
            pilgrimage,
            form.num_travelers.data,
            form.accommodation_type.data,
            form.transportation.data,
            form.guide_required.data
        )
        
        # Create trip plan
        trip_plan = TripPlan(
            user_id=current_user.id,
            pilgrimage_id=int(form.pilgrimage.data),
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            num_travelers=form.num_travelers.data,
            accommodation_type=form.accommodation_type.data,
            transportation=form.transportation.data,
            meal_preference=form.meal_preference.data,
            guide_required=form.guide_required.data,
            additional_notes=form.additional_notes.data,
            confirmation_code=confirmation_code,
            total_price=total_price,
            payment_status='confirmed'  # For simplicity, we'll mark it as confirmed
        )
        
        db.session.add(trip_plan)
        db.session.commit()
        
        # Send confirmation email
        send_trip_confirmation_email(current_user, trip_plan, pilgrimage)
        
        flash('Your trip has been planned successfully! A confirmation has been sent to your email.', 'success')
        return redirect(url_for('main.trip_details', trip_id=trip_plan.id))
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text}: {error}", "danger")
    
    return render_template('plan_trip.html', form=form)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(original_username=current_user.username, original_email=current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.preferences = form.preferences.data
        
        # Handle profile picture upload
        if form.profile_picture.data:
            filename = secure_filename(form.profile_picture.data.filename)
            # Create a unique filename
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            # Save the file
            file_path = os.path.join(current_app.root_path, 'static', 'uploads', unique_filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            form.profile_picture.data.save(file_path)
            # Update the user's profile picture
            current_user.profile_picture = f"/static/uploads/{unique_filename}"
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.preferences.data = current_user.preferences
    
    user_reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).all()
    return render_template('profile.html', form=form, reviews=user_reviews)

@main.route('/review/<int:pilgrimage_id>', methods=['POST'])
@login_required
def review_pilgrimage(pilgrimage_id):
    pilgrimage = Pilgrimage.query.get_or_404(pilgrimage_id)
    form = ReviewForm()
    if form.validate_on_submit():
        # Check if user has already reviewed this pilgrimage
        existing_review = Review.query.filter_by(
            user_id=current_user.id, 
            pilgrimage_id=pilgrimage.id
        ).first()
        
        if existing_review:
            existing_review.rating = int(form.rating.data)
            existing_review.comment = form.comment.data
            flash('Your review has been updated!', 'success')
        else:
            review = Review(
                user_id=current_user.id,
                pilgrimage_id=pilgrimage.id,
                rating=int(form.rating.data),
                comment=form.comment.data
            )
            db.session.add(review)
            flash('Your review has been submitted!', 'success')
        
        db.session.commit()
        return redirect(url_for('main.pilgrimage', id=pilgrimage.id))
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text}: {error}", "danger")
    
    return redirect(url_for('main.pilgrimage', id=pilgrimage.id))

print("Routes have been defined!")

