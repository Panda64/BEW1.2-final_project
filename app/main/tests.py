import os
import unittest
 
from app import app, db, bcrypt
from app.models import Track, Location, Review, User

"""
Run these tests with the command:
python -m unittest app.main.tests
"""

#################################################
# Setup
#################################################

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_track(user):

    l1 = Location(
        name='Riverdale Raceway',
        image_url='https://i2.wp.com/ridepnw.com/wp-content/uploads/2017/11/Riverdale-Main-Track.jpg?fit=1920%2C1080&ssl=1',
        address='250 Rodale Dr. Toutle, WA',
        description="test location description",
        author=user
        )
    t1 = Track(
        name='Riverdale Vintage Track',
        image_url='https://i.ytimg.com/vi/hUXSNCtMf2M/maxresdefault.jpg',
        location=l1,
        description='test track description',
        author=user
    )
    db.session.add(t1)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(
        username='user1', 
        password=password_hash,
        riding_experience='Pro',
        bike='CRF250R')
    db.session.add(user)
    db.session.commit()
    return user

#################################################
# Tests
#################################################

class MainTests(unittest.TestCase):
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    def test_homepage_logged_out(self):
        """Test that the tracks show up on the homepage."""
        # Set up
        user = create_user()
        login(self.app, 'user1', 'password')
        create_track(user)
        logout(self.app)

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Riverdale Vintage Track', response_text)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        self.assertNotIn('Add a Track', response_text)
        self.assertNotIn('Add a Location', response_text)
        self.assertNotIn('My Profile', response_text)
        self.assertNotIn('My Log Out', response_text)
 
    def test_homepage_logged_in(self):
        """Test that the tracks show up on the homepage."""
        # Set up
        user = create_user()
        login(self.app, 'user1', 'password')
        create_track(user)

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Riverdale Vintage Track', response_text)
        self.assertIn('My Profile', response_text)
        self.assertIn('user1', response_text)
        self.assertIn('Add a Track', response_text)
        self.assertIn('Add a Location', response_text)
        self.assertIn('Log Out', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged out users)
        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    def test_track_detail_logged_out(self):
        """Test that the track appears on its detail page."""
        # Set up
        user = create_user()
        login(self.app, 'user1', 'password')
        create_track(user)
        logout(self.app)

        # Make a GET request
        response = self.app.get('/track/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Riverdale Vintage Track', response_text)
        self.assertIn('250 Rodale Dr.', response_text)
        self.assertIn('test track description', response_text)

       # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        self.assertNotIn('Review this track', response_text)

    def test_track_detail_logged_in(self):
        """Test that the track appears on its detail page."""
        # Set up
        user = create_user()
        login(self.app, 'user1', 'password')
        create_track(user)

       # Make a GET request
        response = self.app.get('/track/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Riverdale Vintage Track', response_text)
        self.assertIn('250 Rodale Dr.', response_text)
        self.assertIn('test track description', response_text)
        self.assertIn('Review this track', response_text)

    def test_review_track(self):
        """Test updating a book."""
        # Set up
        user = create_user()
        login(self.app, 'user1', 'password')
        create_track(user)

        # Make POST request with data
        post_data = {
            'title': 'test review title',
            'rating': '5 Stars',
            'difficulty': 'Easy',
            'description': 'Easy going track'
        }
        self.app.post('/track/1', data=post_data)
        
        # Make sure the book was updated as we'd expect
        review = Review.query.get(1)
        self.assertEqual(review.title, 'test review title')
        self.assertEqual(review.rating, '5 Stars')
        self.assertEqual(review.difficulty, 'Easy')

    def test_location_detail(self):
        """Test that the track appears on its detail page."""
        # Set up
        user = create_user()
        login(self.app, 'user1', 'password')
        create_track(user)

       # Make a GET request
        response = self.app.get('/location/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Riverdale Raceway', response_text)
        self.assertIn('250 Rodale Dr.', response_text)
        self.assertIn('test location description', response_text)
        self.assertIn('user1', response_text)


    def test_profile_page(self):
        """Test that the profile page returns all of the appropriate user info."""
        # Set up
        create_user()
        login(self.app, 'user1', 'password')


        # Make a GET request
        response = self.app.get('/profile/user1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('user1', response_text)
        self.assertIn('Pro', response_text)
        self.assertIn('CRF250R', response_text)
