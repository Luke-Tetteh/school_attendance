from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from fabfile import db

class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

student_courses = db.Table('student_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
)

class Student(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    attendances = db.relationship('Attendance', backref='students_attendance', lazy='dynamic')
    courses = db.relationship('Course', secondary='student_courses', backref='students')

    def __repr__(self):
        return f'<Student {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Attendance(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    is_present = db.Column(db.Boolean, default=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    attendance_record = db.Column(JSON)

    student = db.relationship('Student', backref=db.backref('attendance_student', lazy=True))
    course = db.relationship('Course', backref='attendance_records', lazy=True)

class Course(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True, nullable=False)
    marks = db.relationship('Mark', backref='course', lazy=True)
    total_sessions = db.Column(db.Integer, nullable=False, default=0)
    # Define the relationship with the Attendance model
    attendances = db.relationship('Attendance', backref='related_course', lazy=True)

    def __repr__(self):
        return f"Course(id={self.id}, name='{self.name}', total_sessions={self.total_sessions})"



class Mark(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'marks'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    mark = db.Column(db.Integer, nullable=False)


class StudentCourse(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'student_course'
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    # Define relationships
    student = db.relationship('Student', backref=db.backref('enrollments', lazy=True))
    course = db.relationship('Course', backref=db.backref('enrollments', lazy=True))

    __table_args__ = {'extend_existing': True}  # Add this line

    def __init__(self, student_id, course_id):
        self.student_id = student_id
        self.course_id = course_id


