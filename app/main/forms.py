from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, ValidationError, URL
from app.models import Track, Location

class TrackForm(FlaskForm):
    """Form to create a new track"""
    name = StringField(u'Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField(u'Description', validators=[DataRequired(), Length(min=2, max=1000)])
    image_url = StringField(u'Track Photo', validators=[URL()])
    location = QuerySelectField(u'Location', query_factory=lambda: Location.query, allow_blank=False)
    submit = SubmitField('Submit')

    def validate_track(self, name):
        track = Track.query.filter_by(name=name.data).first()
        if track:
            raise ValidationError('Looks like that track has already been added.')


class LocationForm(FlaskForm):
    """Form to create a new location."""
    name = StringField(u'Name', validators=[DataRequired(), Length(min=3, max=80)])
    address = StringField(u'Address', validators=[DataRequired(), Length(min=3, max=80)])
    description = TextAreaField(u'Description', validators=[DataRequired(), Length(min=2, max=1000)])
    image_url = StringField(u'Location Photo', validators=[URL()])
    submit = SubmitField('Submit')

    def validate_location(self, name):
        location = Location.query.filter_by(name=name.data).first()
        if location:
            raise ValidationError('Looks like that location has already been added')


class ReviewForm(FlaskForm):
    """Form to create a new review."""
    title = StringField(u'Title', validators=[DataRequired(), Length(min=3, max=80)])
    rating = SelectField(u'Rating', choices=["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"],
        validators=[DataRequired()])
    difficulty = SelectField(u'Difficulty', choices=["Easy", "Medium", "Hard", "Impossible"],
        validators=[DataRequired()])
    description = TextAreaField(u'Description', validators=[DataRequired(), Length(min=2, max=1000)])
    submit = SubmitField('Submit')


class UpdateUserForm(FlaskForm):
    riding_experience = SelectField(u'Riding Level', choices=["Beginner", "Amateur", "Intermediate", "Semi-Pro", "Pro"],
        validators=[DataRequired()])
    bike = StringField(u'Current Bike', validators=[DataRequired(), Length(min=3, max=50)])
    submit = SubmitField('Submit')