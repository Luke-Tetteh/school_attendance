import unittest
import pymysql 
pymysql.install_as_MySQLdb()
from flask import Flask
from ap import app, db
import json
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash



from model import Student, Course, User

class YourAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Create a temporary database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:janvier22@localhost/hmsys'
        with app.app_context():
            db.create_all()

    
          


    def test_home_page(self):
        response = self.app.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Attendance Student Management', response.data)

    def test_create_student(self):
        # Send a POST request to create a student
        password = 'password'

        response = self.app.post('/addstudent', data=dict(username='test1user510011', password=password))
        self.assertEqual(response.status_code, 200)

        # Parse the response data as JSON
        data = json.loads(response.data)

        # Assert that the 'student' key is present in the response data
        self.assertIn('student', data)

        # Extract the 'student' dictionary from the response data
        student = data['student']

        # Assert that the 'username' key in the 'student' dictionary matches the expected value
        self.assertEqual(student['username'], 'test1user510011')

        # Generate the password hash using the same algorithm and compare it with the actual value
        self.assertTrue(check_password_hash(student['password_hash'], password))


class CheckUserClass(unittest.TestCase):
    def test_user_creation(self):
        # Create a User instance
        username = 'testuser'
        password = 'password'
        user = User(username, password)

        # Assert that the username and password of the User instance match the expected values
        self.assertEqual(user.username, username)
        self.assertEqual(user.password, password)

    def test_password_hashing(self):
        # Create a User instance
        username = 'testuser'
        password = 'password'
        user = User(username, password)

        # Assert that the password hash is not empty
        self.assertNotEqual(user.password_hash, '')

        # Verify that the password matches the password hash using the check_password method
        self.assertTrue(user.check_password(password))




    def test_courses_page(self):
        with self.app as client:
            response = client.get('/courses')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1 class="courses-heading">Courses</h1>', response.data)


    def test_attendance_page(self):
    # Create a test client
        with self.app as client:
            # Make a GET request to the attendance page
            response = client.get('/attendance')

            # Assert that the response status code is 200
            self.assertEqual(response.status_code, 200)

            # Assert that the attendance page contains the expected content
            self.assertIn(b'Attendance', response.data)
            
            self.assertIn(b'Student', response.data)

            self.assertIn(b'Student ID:', response.data)
            self.assertIn(b'Present', response.data)
            self.assertIn(b'Course ID', response.data)
            self.assertIn(b'Date', response.data)

    # Add more test cases for different functionalities

if __name__ == '__main__':
    unittest.main()