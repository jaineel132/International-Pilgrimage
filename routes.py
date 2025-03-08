from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Pilgrimage, Booking, TripPlan
from forms import BookingForm, TripPlanningForm
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
    form = BookingForm()
    return render_template('pilgrimage.html', pilgrimage=pilgrimage, form=form)

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
        return redirect(url_for('main.pilgrimage', id=pilgrimage.id))
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
    return render_template('dashboard.html', bookings=user_bookings, trip_plans=user_trip_plans)

@main.route('/plan_trip', methods=['GET', 'POST'])
@login_required
def plan_trip():
    form = TripPlanningForm()
    form.pilgrimage.choices = [(p.id, p.name) for p in Pilgrimage.query.all()]
    
    if form.validate_on_submit():
        trip_plan = TripPlan(
            user_id=current_user.id,
            pilgrimage_id=form.pilgrimage.data,
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
    
    return render_template('plan_trip.html', form=form)

print("Routes have been defined!")

