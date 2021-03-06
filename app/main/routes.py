"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from app.models import Track, Location, Review, User
from app.main.forms import TrackForm, LocationForm, ReviewForm, UpdateUserForm
from app import bcrypt

# Import app and db from app package so that we can run app
from app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


@main.route('/')
def homepage():
    all_tracks = Track.query.all()
    return render_template('home.html', all_tracks=all_tracks)


@main.route('/create_track', methods=['GET', 'POST'])
@login_required
def create_track():
    form = TrackForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        new_track = Track(
            name=form.name.data,
            image_url=form.image_url.data,
            location=form.location.data,
            description=form.description.data,
            author=current_user
        )
        db.session.add(new_track)
        db.session.commit()

        flash('New track was added successfully.')
        return redirect(url_for('main.track_detail', track_id=new_track.id))
    return render_template('create_track.html', form=form)


@main.route('/create_location', methods=['GET', 'POST'])
@login_required
def create_location():
    form = LocationForm()
    if form.validate_on_submit():
        new_location = Location(
            name=form.name.data,
            image_url=form.image_url.data,
            address=form.address.data,
            description=form.description.data,
            author=current_user
        )
        db.session.add(new_location)
        db.session.commit()

        flash('New location added successfully.')
        return redirect(url_for('main.homepage'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_location.html', form=form)


@main.route('/track/<track_id>', methods=['GET', 'POST'])
def track_detail(track_id):
    already_reviewed = False
    track = Track.query.get(track_id)
    form = ReviewForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        for track_review in track.reviews:
            if track_review.author == current_user:
                already_reviewed = True

        if already_reviewed == False:
            new_review = Review(
                title=form.title.data,
                rating=form.rating.data,
                difficulty=form.difficulty.data,
                description=form.description.data,
                author=current_user,
                track=track
            )
        
            db.session.add(new_review)
            db.session.commit()

            flash('Review was added successfully.')
        else:
            flash('You have already reviewed this track')

        return redirect(url_for('main.track_detail', track_id=track_id))

    return render_template('track_detail.html', track=track, form=form)


@main.route('/location/<location_id>', methods=['GET', 'POST'])
def location_detail(location_id):
    location = Location.query.get(location_id)

    return render_template('location_detail.html', location=location)


@main.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    user = User.query.filter_by(username=username).one()
    form = UpdateUserForm(obj=user)

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        print("test")
        user.riding_experience = form.riding_experience.data
        user.bike = form.bike.data

        db.session.commit()

        flash('Profile was updated successfully.')
        return redirect(url_for('main.profile', username=username))

    return render_template('profile.html', user=user, form=form)
