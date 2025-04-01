from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import ForumCategory, ForumPost, ForumComment, TravelLog, User, Notification
from forms import ForumPostForm, ForumCommentForm, TravelLogForm
from extensions import db
from datetime import datetime
import json

community_bp = Blueprint('community', __name__)

# Forum routes
@community_bp.route('/forum')
def forum():
    categories = ForumCategory.query.all()
    recent_posts = ForumPost.query.order_by(ForumPost.created_at.desc()).limit(5).all()
    
    return render_template('community/forum.html', 
                          categories=categories, 
                          recent_posts=recent_posts)

@community_bp.route('/forum/category/<int:id>')
def forum_category(id):
    category = ForumCategory.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    
    posts = ForumPost.query.filter_by(category_id=id).order_by(
        ForumPost.created_at.desc()
    ).paginate(page=page, per_page=10)
    
    return render_template('community/category.html', 
                          category=category, 
                          posts=posts)

@community_bp.route('/forum/post/<int:id>', methods=['GET', 'POST'])
def forum_post(id):
    post = ForumPost.query.get_or_404(id)
    form = ForumCommentForm()
    
    # Increment view count
    post.views += 1
    db.session.commit()
    
    if form.validate_on_submit() and current_user.is_authenticated:
        comment = ForumComment(
            content=form.content.data,
            user_id=current_user.id,
            post_id=post.id
        )
        db.session.add(comment)
        
        # Create notification for post author
        if post.user_id != current_user.id:
            notification = Notification(
                user_id=post.user_id,
                title='New Comment on Your Post',
                message=f'{current_user.username} commented on your post "{post.title}"',
                link=url_for('community.forum_post', id=post.id)
            )
            db.session.add(notification)
        
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('community.forum_post', id=post.id))
    
    # Get comments
    comments = ForumComment.query.filter_by(post_id=id).order_by(
        ForumComment.created_at.asc()
    ).all()
    
    return render_template('community/post.html', 
                          post=post, 
                          comments=comments, 
                          form=form)

@community_bp.route('/forum/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = ForumPostForm()
    form.category.choices = [(c.id, c.name) for c in ForumCategory.query.all()]
    
    if form.validate_on_submit():
        post = ForumPost(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id,
            category_id=form.category.data
        )
        db.session.add(post)
        db.session.commit()
        
        flash('Your post has been created!', 'success')
        return redirect(url_for('community.forum_post', id=post.id))
    
    return render_template('community/new_post.html', form=form)

# Travel Logs routes
@community_bp.route('/travel-logs')
def travel_logs():
    page = request.args.get('page', 1, type=int)
    
    # Get public travel logs
    logs = TravelLog.query.filter_by(is_public=True).order_by(
        TravelLog.created_at.desc()
    ).paginate(page=page, per_page=6)
    
    return render_template('community/travel_logs.html', logs=logs)

@community_bp.route('/travel-logs/<int:id>')
def travel_log(id):
    log = TravelLog.query.get_or_404(id)
    
    # Check if log is private and not owned by current user
    if not log.is_public and (not current_user.is_authenticated or log.user_id != current_user.id):
        abort(403)
    
    return render_template('community/travel_log.html', log=log)

@community_bp.route('/travel-logs/new', methods=['GET', 'POST'])
@login_required
def new_travel_log():
    form = TravelLogForm()
    
    if form.validate_on_submit():
        # Process uploaded images
        images = []
        if form.images.data:
            for image in form.images.data:
                # Save image and get URL
                # This would be implemented to save the image to a storage location
                # and return the URL
                image_url = '/static/uploads/placeholder.jpg'  # Placeholder
                images.append(image_url)
        
        log = TravelLog(
            user_id=current_user.id,
            title=form.title.data,
            content=form.content.data,
            location=form.location.data,
            is_public=form.is_public.data
        )
        
        if images:
            log.log_images = images
        
        db.session.add(log)
        db.session.commit()
        
        flash('Your travel log has been created!', 'success')
        return redirect(url_for('community.travel_log', id=log.id))
    
    return render_template('community/new_travel_log.html', form=form)

@community_bp.route('/travel-logs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_travel_log(id):
    log = TravelLog.query.get_or_404(id)
    
    # Ensure the log belongs to the current user
    if log.user_id != current_user.id:
        abort(403)
    
    form = TravelLogForm()
    
    if form.validate_on_submit():
        # Update log
        log.title = form.title.data
        log.content = form.content.data
        log.location = form.location.data
        log.is_public = form.is_public.data
        
        # Process new images
        if form.images.data and any(form.images.data):
            # Get existing images
            existing_images = log.log_images
            
            # Process new uploads
            for image in form.images.data:
                if image:
                    # Save image and get URL
                    image_url = '/static/uploads/placeholder.jpg'  # Placeholder
                    existing_images.append(image_url)
            
            log.log_images = existing_images
        
        db.session.commit()
        
        flash('Your travel log has been updated!', 'success')
        return redirect(url_for('community.travel_log', id=log.id))
    elif request.method == 'GET':
        form.title.data = log.title
        form.content.data = log.content
        form.location.data = log.location
        form.is_public.data = log.is_public
    
    return render_template('community/edit_travel_log.html', form=form, log=log)

