from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify, send_file
from flask_login import login_required, current_user
from models import TripPlan, User, Notification, Booking
from extensions import db, mail, csrf
from flask_mail import Message
import uuid
from datetime import datetime
import os
import json

payment_bp = Blueprint('payment', __name__)

# Dummy account for testing payments
DUMMY_ACCOUNTS = {
  "test@example.com": {
      "card_number": "4111111111111111",
      "expiry": "12/25",
      "cvv": "123",
      "name": "Test User",
      "balance": 50000.00
  },
  "demo@example.com": {
      "card_number": "5555555555554444",
      "expiry": "10/26",
      "cvv": "321",
      "name": "Demo User",
      "balance": 100000.00
  }
}

@payment_bp.route('/checkout/<int:trip_id>', methods=['GET'])
@login_required
def checkout(trip_id):
  trip = TripPlan.query.get_or_404(trip_id)
  
  # Ensure the trip belongs to the current user
  if trip.user_id != current_user.id:
      flash('You do not have permission to access this trip.', 'danger')
      return redirect(url_for('main.dashboard'))
  
  # If already paid, redirect to receipt
  if trip.payment_status == 'paid':
      flash('This trip has already been paid for.', 'info')
      return redirect(url_for('payment.receipt', trip_id=trip.id))
  
  # Calculate price breakdown if not already stored
  if not trip.base_price:
      pilgrimage = trip.pilgrimage
      price_breakdown = calculate_trip_price(
          pilgrimage,
          trip.num_travelers,
          trip.accommodation_type,
          trip.transportation,
          trip.guide_required
      )
      trip.base_price = price_breakdown['base_price']
      trip.accommodation_fee = price_breakdown['accommodation_fee']
      trip.transportation_fee = price_breakdown['transportation_fee']
      trip.guide_fee = price_breakdown['guide_fee']
      trip.tax_amount = price_breakdown['tax_amount']
      trip.discount_amount = price_breakdown['discount_amount']
      trip.total_price = price_breakdown['total']
      db.session.commit()
  
  # Get dummy accounts for testing
  dummy_accounts = list(DUMMY_ACCOUNTS.keys())
  
  return render_template('payment/checkout.html', 
                        trip=trip,
                        dummy_accounts=dummy_accounts,
                        stripe_public_key=current_app.config.get('STRIPE_PUBLIC_KEY', 'pk_test_sample'))

@csrf.exempt
@payment_bp.route('/process-payment/<int:trip_id>', methods=['POST'])
@login_required
def process_payment(trip_id):
    trip = TripPlan.query.get_or_404(trip_id)

    # Ensure the trip belongs to the current user
    if trip.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    # Simplified payment processing - always succeed
    try:
        # Update trip payment status
        trip.payment_status = 'paid'
        trip.payment_id = f"PAYMENT-{uuid.uuid4().hex[:10].upper()}"
        trip.payment_method = 'card'  # Default to card
        trip.payment_date = datetime.utcnow()
        
        # Generate confirmation code if not already set
        if not trip.confirmation_code:
            trip.confirmation_code = f"SJ-{uuid.uuid4().hex[:8].upper()}"
        
        # Create a booking record for this paid trip
        booking = Booking(
            user_id=current_user.id,
            pilgrimage_id=trip.pilgrimage_id,
            travel_date=trip.start_date,
            special_requirements=trip.additional_notes
        )
        db.session.add(booking)
        
        # Create notification
        notification = Notification(
            user_id=current_user.id,
            title='Payment Successful',
            message=f'Your payment for the trip to {trip.pilgrimage.name} was successful.',
            link=url_for('payment.receipt', trip_id=trip.id)
        )
        db.session.add(notification)
        
        db.session.commit()
        
        # Send receipt email to user
        send_receipt_email(trip)
        
        return jsonify({
            'success': True,
            'redirect': url_for('payment.receipt', trip_id=trip.id)
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Payment error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/receipt/<int:trip_id>')
@login_required
def receipt(trip_id):
  trip = TripPlan.query.get_or_404(trip_id)
  
  # Ensure the trip belongs to the current user
  if trip.user_id != current_user.id:
      flash('You do not have permission to access this receipt.', 'danger')
      return redirect(url_for('main.dashboard'))
  
  return render_template('payment/receipt.html', trip=trip)

def send_simple_confirmation(trip):
  """Dummy function that would send an email in production"""
  print(f"Would send email to {current_user.email} for trip {trip.id}")
  return True

@payment_bp.route('/dashboard/payment/<int:trip_id>')
@login_required
def dashboard_payment(trip_id):
  """Redirect to the payment checkout page from dashboard"""
  return redirect(url_for('payment.checkout', trip_id=trip_id))

def calculate_trip_price(pilgrimage, num_travelers, accommodation_type, transportation, guide_required):
  """Calculate the total price of a trip based on various factors and return price breakdown"""
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
  
  # Calculate individual components
  base_total = base_price * num_travelers
  accommodation_fee = base_total * (accommodation_multipliers.get(accommodation_type, 1.0) - 1.0)
  transportation_fee = base_total * (transportation_multipliers.get(transportation, 1.0) - 1.0)
  guide_fee = 50.0 if guide_required else 0.0
  
  # Calculate tax (8.5%)
  subtotal = base_total + accommodation_fee + transportation_fee + guide_fee
  tax_amount = round(subtotal * 0.085, 2)
  
  # Apply discount (if any) - for example, 5% for trips with more than 3 travelers
  discount_amount = 0
  if num_travelers > 3:
      discount_amount = round(subtotal * 0.05, 2)
  
  # Calculate total
  total = subtotal + tax_amount - discount_amount
  
  # Return price breakdown
  price_breakdown = {
      'base_price': base_price,
      'base_total': base_total,
      'accommodation_fee': accommodation_fee,
      'transportation_fee': transportation_fee,
      'guide_fee': guide_fee,
      'subtotal': subtotal,
      'tax_amount': tax_amount,
      'discount_amount': discount_amount,
      'total': round(total, 2)
  }
  
  return price_breakdown

def send_receipt_email(trip):
    """Send receipt email to the user"""
    try:
        user = User.query.get(trip.user_id)
        if not user or not user.email:
            print("Cannot send email: User not found or no email address")
            return False
        
        # Create the email
        subject = f"Sacred Journeys - Payment Receipt #{trip.confirmation_code}"
        
        # Render the receipt template for email
        html_body = render_template(
            'payment/email_receipt.html',
            trip=trip,
            user=user
        )
        
        msg = Message(
            subject=subject,
            recipients=[user.email],
            html=html_body,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@sacredjourneys.com')
        )
        
        # Send the email
        mail.send(msg)
        print(f"Receipt email sent to {user.email}")
        return True
    except Exception as e:
        print(f"Error sending receipt email: {str(e)}")
        return False

