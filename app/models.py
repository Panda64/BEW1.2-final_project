from app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin


class Track(db.Model):
    """Track model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.Sring(250))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', back_populates='added_tracks')
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    location = db.relationship('Location', backref=backref("location", uselist=False))
    
    def __str__(self):
        return f'<Track: {self.name}>'

    def __repr__(self):
        return f'<Track: {self.name}>'

class Location(db.Model):
    """Location model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    address = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.Sring(250))

    def __str__(self):
        return f'<Location Name: {self.name}>'

    def __repr__(self):
        return f'<Location Name: {self.name}>'

class Review(db.Model):
    """Review model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.String(10), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', back_populates='reviews')

    def __str__(self):
        return f'<Review Title: {self.title}>'

    def __repr__(self):
        return f'<Review Title: {self.title}>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    riding_experience = db.Column(db.String(20), nullable=False)
    bike = db.Column(db.String(50), nullable=False)
    reviews = db.relationship('Review', back_populates='author')
    added_tracks = db.relationship('Track', back_populates='author') 

    def __repr__(self):
        return f'<User: {self.username}>'
