from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange, Length
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class BookingForm(FlaskForm):
    travel_date = DateField('Travel Date', validators=[DataRequired()])
    special_requirements = TextAreaField('Special Requirements')
    submit = SubmitField('Book Pilgrimage')

class TripPlanningForm(FlaskForm):
    pilgrimage = SelectField('Select Pilgrimage', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    num_travelers = IntegerField('Number of Travelers', validators=[DataRequired(), NumberRange(min=1, max=20)])
    accommodation_type = SelectField('Accommodation Type', choices=[
        ('budget', 'Budget'),
        ('standard', 'Standard'),
        ('luxury', 'Luxury')
    ], validators=[DataRequired()])
    transportation = SelectField('Transportation', choices=[
        ('public', 'Public Transport'),
        ('private', 'Private Vehicle'),
        ('guided_tour', 'Guided Tour')
    ], validators=[DataRequired()])
    additional_notes = TextAreaField('Additional Notes')
    submit = SubmitField('Plan My Trip')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('About Me', validators=[Length(max=500)])
    preferences = SelectField('Travel Preferences', choices=[
        ('religious', 'Religious Pilgrimages'),
        ('historical', 'Historical Sites'),
        ('cultural', 'Cultural Experiences'),
        ('all', 'All Types')
    ])
    submit = SubmitField('Update Profile')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[(str(i), str(i)) for i in range(1, 6)], validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Submit Review')

