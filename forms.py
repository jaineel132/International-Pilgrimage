from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange, Length, Regexp
from models import User
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=20, message="Username must be between 4 and 20 characters"),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', message="Username can only contain letters, numbers, dots or underscores")
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long"),
        Regexp('(?=.*\d)(?=.*[a-z])(?=.*[A-Z])', message="Password must include at least one uppercase letter, one lowercase letter, and one number")
    ])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(), 
        EqualTo('password', message="Passwords must match")
    ])
    full_name = StringField('Full Name', validators=[DataRequired()])
    country = SelectField('Country', choices=[
        ('', 'Select your country'),
        ('usa', 'United States'),
        ('uk', 'United Kingdom'),
        ('canada', 'Canada'),
        ('australia', 'Australia'),
        ('india', 'India'),
        ('france', 'France'),
        ('germany', 'Germany'),
        ('italy', 'Italy'),
        ('spain', 'Spain'),
        ('japan', 'Japan'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    profile_picture = FileField('Profile Picture (Optional)', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    terms_agree = BooleanField('I agree to the Terms and Conditions', validators=[
        DataRequired(message="You must agree to the terms and conditions")
    ])
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
    meal_preference = SelectField('Meal Preference', choices=[
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('non_vegetarian', 'Non-Vegetarian'),
        ('no_preference', 'No Preference')
    ])
    guide_required = BooleanField('Require a Guide')
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
    profile_picture = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
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

class ForumPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Post')


class ForumCommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Comment')


class TravelLogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Log Content', validators=[DataRequired()])
    location = StringField('Location', validators=[Length(max=100)])
    is_public = BooleanField('Make this travel log public')
    images = FileField('Upload Images', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only images are allowed')])
    submit = SubmitField('Submit')
