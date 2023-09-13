from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime
from model import Student, Course , StudentCourse, Attendance, Mark
from forms import StudentForm, CourseForm, AttendanceForm, MarkForm
from fabfile import db, app


migrate = Migrate(app, db)




# Routes
@app.route('/')
def home():
    return 'Welcome to the student management system!'

@app.route('/students', methods=['GET', 'POST'])
def students():
    form = StudentForm()
    if form.validate_on_submit():
        # Add a new student to the database
        new_student = Student(name=form.name.data, roll_number=form.roll_number.data)
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully!')
        return redirect('/students')

    students = Student.query.all()
    return render_template('student.html', form=form, students=students)

@app.route('/courses', methods=['GET', 'POST'])
def courses():
    form = CourseForm()
    if form.validate_on_submit():
        # Add a new course to the database
        new_course = Course(name=form.name.data)
        db.session.add(new_course)
        db.session.commit()
        flash('Course added successfully!')
        return redirect('/courses')

    courses = Course.query.all()
    return render_template('courses.html', form=form, courses=courses)

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    form = AttendanceForm()
    form.student.choices = [(student.id, student.name) for student in Student.query.all()]

    if form.validate_on_submit():
        # Add attendance for a student
        student_id = form.student.data
        present = form.present.data == '1'

        new_attendance = Attendance(student_id=student_id, present=present)
        db.session.add(new_attendance)
        db.session.commit()

        flash('Attendance added successfully!')
        return redirect('/attendance')

    attendance_records = Attendance.query.all()
    return render_template('attendance.html', form=form, attendance_records=attendance_records)

@app.route('/marks', methods=['GET', 'POST'])
def marks():
    form = MarkForm()
    form.student.choices = [(student.id, student.name) for student in Student.query.all()]
    form.course.choices = [(course.id, course.name) for course in Course.query.all()]

    if form.validate_on_submit():
        # Add marks for a student and course
        student_id = form.student.data
        course_id = form.course.data
        marks = form.marks.data

        new_mark = Mark(student_id=student_id, course_id=course_id, marks=marks)
        db.session.add(new_mark)
        db.session.commit()

        flash('Marks added successfully!')
        return redirect('/marks')

    marks = Mark.query.all()
    return render_template('marks.html', form=form, marks=marks)

if __name__ == '__main__':
    app.run(debug=True)

