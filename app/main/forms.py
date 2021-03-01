from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError, URL
from app.models import Track, Location, Review, User

class TrackForm(FlaskForm):
    """Form to create a new track"""
    name = StringField(u'Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField(u'Description', validators=[DataRequired(), Length(min=2, max=1000)])
    image_url = StringField('Track Photo', validators=[URL()])
    location = QuerySelectField('Location', query_factory=lambda: Location.query, allow_blank=False)
    submit = SubmitField('Submit')


class LocationForm(FlaskForm):
    """Form to create a new location."""
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=80)])
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=80)])
    description = TextAreaField(u'Description', validators=[DataRequired(), Length(min=2, max=1000)])
    image_url = StringField('Location Photo', validators=[URL()])
    submit = SubmitField('Submit')


class ReviewForm(FlaskForm):
    """Form to create a new review."""
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=80)])
    rating = SelectField(u'Rating', choices=["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"],
        validators=[DataRequired()])
    difficulty = SelectField(u'Difficulty', choices=["Easy", "Medium", "Hard", "Impossible"],
        validators=[DataRequired()])
    description = TextAreaField(u'Description', validators=[DataRequired(), Length(min=2, max=1000)])
    submit = SubmitField('Submit')