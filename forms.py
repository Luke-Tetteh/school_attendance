from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired
from wtforms import FloatField
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from model import Course

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    roll_number = StringField('Roll Number', validators=[DataRequired()])
    submit = SubmitField('Add Student')

    def __init__(self, courses, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for course in courses:
            field_name = f"attendance_{course.id}"
            label = f"Attendance for {course.name}"
            setattr(self, field_name, BooleanField(label))

class CourseForm(FlaskForm):
    name = StringField('Course Name', validators=[DataRequired()])
    submit = SubmitField('Add Course')


class AttendanceForm(FlaskForm):
    attendance = SelectField('Attendance', choices=[('1', 'Present'), ('0', 'Absent')], validators=[DataRequired()])
    course_id = SelectField('Course', choices=[], validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    attendance_record = StringField('Attendance Record')

    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.course_id.choices = [(str(course.id), course.name) for course in Course.query.all()]

class MarkForm(FlaskForm):
    student_id = IntegerField('Student ID', validators=[InputRequired()])
    course_id = IntegerField('Course ID', validators=[InputRequired()])
    score = FloatField('Score', validators=[InputRequired()])
    mark = StringField('Mark', validators=[DataRequired()])



