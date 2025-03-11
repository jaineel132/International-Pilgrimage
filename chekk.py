from models import Booking, TripPlan
from extensions import db

# Check all bookings
bookings = Booking.query.all()
print("Bookings:", bookings)

# Check all trip plans
trip_plans = TripPlan.query.all()
print("Trip Plans:", trip_plans)