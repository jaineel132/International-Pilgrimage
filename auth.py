from flask import Blueprint, render_template, redirect, url_for, flash, request
from urllib.parse import urlparse, urljoin
from flask_login import login_user, logout_user, current_user
from extensions import db
from models import User
from forms import LoginForm, RegistrationForm
from werkzeug.utils import secure_filename
import os
import uuid
from flask import current_app

auth = Blueprint('auth', __name__)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or not is_safe_url(next_page):
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data,
            full_name=form.full_name.data,
            country=form.country.data
        )
        user.set_password(form.password.data)
        
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
            user.profile_picture = f"/static/uploads/{unique_filename}"
        
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

print("Authentication routes have been defined!")

