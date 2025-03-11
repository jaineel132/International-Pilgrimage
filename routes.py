from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Pilgrimage, Booking, TripPlan, Review, User
from forms import BookingForm, TripPlanningForm, ProfileForm, ReviewForm
from extensions import db
from datetime import datetime

main = Blueprint('main', __name__)

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
    form = BookingForm()
    if form.validate_on_submit():
        booking = Booking(
            user_id=current_user.id,
            pilgrimage_id=pilgrimage.id,
            travel_date=form.travel_date.data,
            special_requirements=form.special_requirements.data
        )
        db.session.add(booking)
        db.session.commit()
        flash('Your pilgrimage has been booked successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text}: {error}", "danger")
    
    return render_template('pilgrimage.html', pilgrimage=pilgrimage, form=form)

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
        'image_url': p.image_url
    } for p in pilgrimages])

@main.route('/dashboard')
@login_required
def dashboard():
    user_bookings = current_user.bookings.order_by(Booking.travel_date.desc()).all()
    user_trip_plans = TripPlan.query.filter_by(user_id=current_user.id).order_by(TripPlan.start_date.desc()).all()
    now = datetime.now().date()
    return render_template('dashboard.html', bookings=user_bookings, trip_plans=user_trip_plans, now=now)

@main.route('/plan_trip', methods=['GET', 'POST'])
@login_required
def plan_trip():
    form = TripPlanningForm()
    form.pilgrimage.choices = [(str(p.id), p.name) for p in Pilgrimage.query.all()]
    
    if form.validate_on_submit():
        trip_plan = TripPlan(
            user_id=current_user.id,
            pilgrimage_id=int(form.pilgrimage.data),
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            num_travelers=form.num_travelers.data,
            accommodation_type=form.accommodation_type.data,
            transportation=form.transportation.data,
            additional_notes=form.additional_notes.data
        )
        db.session.add(trip_plan)
        db.session.commit()
        flash('Your trip has been planned successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
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

