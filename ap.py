
import json
from werkzeug.security import generate_password_hash
#from flask_bcrypt import check_password_hash
from logging import DEBUG
from flask import jsonify, render_template, redirect, request, session, url_for, flash
from flask_migrate import Migrate
from forms import StudentForm, CourseForm, AttendanceForm, MarkForm
from forms import AttendanceForm, LoginForm, SignupForm
from model import Enrollment, Student, Attendance, Course, Mark, User
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from fabfile import db, app
import datetime




migrate = Migrate(app, db)

# with app.app_context():
#     # Run the Alembic upgrade command
#     from alembic.config import Config
#     from alembic import command

#     alembic_cfg = Config("alembic.ini")
#     command.upgrade(alembic_cfg, "head")


def validate_credentials(username, password_hash):
    # Assuming you have a User model or a database table named 'users'
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password_hash):
        # Credentials are valid
        return True
    else:
        # Credentials are invalid
        return False
    

def calculate_attendance_re(student, attendances):
    attendances = Attendance.query.filter_by(student=student).all()

    total_classes = len(attendances)
    present_count = sum(attendance.is_present == True for attendance in attendances)
    attendance_percentage = (present_count / total_classes) * 100

    attendance_record = {
        'student_id': student.id,
        'attendance_percentage': attendance_percentage
    }

    return attendance_record

def filtered_records(name):
    # Retrieve attendance records
    attendance_records = Attendance.query.all()

    # Filter attendance records based on a condition
    filtered_records = []
    for record in attendance_records:
        if record.student.username == name:
            filtered_records.append({
                'student_name': record.student.name,
                'course_name': record.course.name,
                'is_present': record.is_present,
                'date': str(record.date),
                'attendance_record': record.attendance_record
            })

    return filtered_records


def calculate_attendance_record(student):
    total_classes = student.attendances.count()
    present_count = student.attendances.filter_by(is_present=True).count()
    absent_count = total_classes - present_count

    if total_classes != 0:
         attendance_percentage = (present_count / total_classes) * 100

    # Format the attendance record string
         attendance_record = f"Present: {present_count} | Absent: {absent_count} | Percentage: {attendance_percentage:.2f}%"
    else:
        attendance_record = 0

    return attendance_record




def calculate_attendance_record(student, attendances):
    total_attendance = len(attendances)
    present_count = sum(attendance.is_present for attendance in attendances)
    absent_count = total_attendance - present_count

    attendance_record = {
        'total_attendance': total_attendance,
        'present_count': present_count,
        'absent_count': absent_count
    }

    return attendance_record



login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/users/info')
def users_info():
    # Retrieve user data from the database
    users = User.query.all()

    return render_template('users_info.html', users=users)


@app.route('/addstudent', methods=['GET', 'POST'])
def create_student():

    
    if request.method == 'POST':
            

            username = request.form.get('username')
            password = request.form.get('password')
            # Validate that the username and password are provided
            password_hash = generate_password_hash(password)

            student = Student(username=username, password_hash=password_hash)
            db.session.add(student)
            db.session.commit()
            # Store the username and password hash in the database or perform other operations

            student_data = {
            'username': username,
            'password_hash': password_hash
            }

            return jsonify(student=student_data)

            
            
    return render_template('create_student.html')




@app.route('/features')
def features():
    # Redirect to the home page
    return redirect(url_for('home', _anchor='features'))



@app.route('/contact')
def contact():
    # Redirect to the home page
    return redirect(url_for('home', _anchor='contact'))

@app.route('/about')
def about():
    # Redirect to the home page
    return redirect(url_for('home', _anchor='about'))

@app.route('/feature')
def feature():
    return render_template('features.html')


@app.route('/student_detail3')
@login_required


def student_detail3():
    # Retrieve student data from the database or any other source
    students = Student.query.all() 

    # Create a list to store the student details
    student_details = []

    # Retrieve attendance data for each student
    for student in students:
        attendances = Attendance.query.filter_by(student_id=student.id).all()
        student_detail = {
            'student': student,
            'attendances': attendances
            
        }
        student_details.append(student_detail)

    return render_template('stude_detail.html', student_details=student_details)






@app.route('/student_detail3/<int:student_id>')

def student_detail33(student_id):
    # Retrieve student data from the database or any other source
    student = Student.query.get(student_id)
    student_details = []

    if student:
        # Retrieve attendance data for the specific student
        attendances = Attendance.query.filter_by(student_id=student.id).all()
        attendance_record = []
        for attendance in attendances:
            attendance_percentage = calculate_attendance_re(student, attendance)
            record = {
                'course_id': attendance.course.id,
                'attendance_percentage': attendance_percentage
            }
            attendance_record.append(record)
        student_detail = {
            'student': student,
            'attendances': attendances,
            'attendance_record': attendance_record
        }
        student_details.append(student_detail)
        return render_template('st_det.html', student_details=student_details)
    else:
        flash('Student not found.', 'error')
        return redirect(url_for('students'))



@app.route('/attendance_confirmation', methods=['GET', 'POST'])
def attendance_confirmation():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        is_present = request.form.get('is_present')

        # Perform any necessary actions or database updates based on the attendance data
        # For example, you can update the attendance record in the database

        # Check if the attendance record exists
        attendance = Attendance.query.filter_by(student_id=student_id).first()
        if attendance is None:
            return render_template('confirmation_error.html', error_message='Attendance record not found.')

        # Update the attendance record for the student
        attendance.is_present = is_present
        db.session.commit()

        return render_template('confirmation_success.html', student_id=student_id, is_present=is_present)
    else:
        return render_template('attendance_confirmation.html')


    
    


@app.route('/login', methods=['GET', 'POST'])

def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        users = User.query.all()

        found_user = next((user for user in users if user.username == username), None)
        
        if found_user:
            # User found, perform the login logic
            # Example login logic using Flask-Login:
            if found_user.check_password(form.password.data):
                # Login successful
                login_user(found_user)  # Login the user using Flask-Login
                flash("Login successful.", "success")
                return redirect(url_for('dashboard'))
            else:
                # Incorrect password
                flash("Invalid password.", "danger")

    # Render the login page with the login form
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))





@app.route('/success')
def success():
    return render_template('success.html')




@app.route('/students', methods=['GET'])
@login_required
def get_student():
    # Retrieve all students from the database
    students = Student.query.all()

    # Create a list to store student records
    student_records = []

    # Iterate over each student to calculate their attendance record
    for student in students:
        attendances = Attendance.query.filter_by(student_id=student.id).all()
        
        # Calculate attendance record for the student
        attendance_record = calculate_attendance_record(student, attendances)
        
        # Create a student record dictionary with student details and attendance record
        student_record = {
            'student': student,
            'attendance_record': attendance_record
        }
        
        # Append the student record to the student_records list
        student_records.append(student_record)

    return render_template('student.html', student_records=student_records)



@app.route('/create_user', methods=['POST' , 'GET'])
@login_required

def create_user():
    # Handle user creation form submission
    username = request.form.get('username')
    password = request.form.get('password')

    # Validate that the username and password are provided
    if not username or not password:
        flash('Username and password are required.')
        return render_template('/create_user.html')

    # Perform necessary actions to create a new user
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    flash('User created successfully.')
    return redirect('login')


@app.route('/dashboard', methods=['GET', 'POST'])

def dashboard():
    # Retrieve the list of students and courses from the database
    students = Student.query.all()
    courses = Course.query.all()
    


    if request.method == 'POST':
        entity_type = request.form.get('entity_type')
        
        if entity_type == 'student':
            # Handle student creation form submission
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Validate that the username and password are provided
            if not username or not password:
                flash('Username and password are required.')
            else:
                password_hash = generate_password_hash(password)
                
                # Perform necessary actions to create a new student
                student = Student(username=username, password_hash=password_hash)
                db.session.add(student)
                db.session.commit()
                
                flash('Student created successfully.')
        
        elif entity_type == 'course':
            # Handle course creation form submission
            course_name = request.form.get('course_name')
            
            # Validate that the course name is provided
            if not course_name:
                flash('Course name is required.')
            else:
                # Perform necessary actions to create a new course
                course = Course(name=course_name)
                db.session.add(course)
                db.session.commit()
                
                flash('Course created successfully.')

        elif entity_type == 'attendance':
            # Handle attendance mark submission
            student_id = request.form.get('student_id')
            student = Student.query.get(student_id)

            if student is None:
                flash('Student not found.')
                return redirect('/dashboard')
            
            course_id = request.form.get('course_id')
            is_present = request.form.get('is_present')
            attendance_date = request.form.get('attendance_date')
            attendance_record = request.form.get('attendance_record')

            # Perform necessary actions to add an attendance mark
            if not student_id or not course_id or is_present is None:
                flash('Student, course selection, and attendance status are required.')
            else:
                # Convert the string value to a boolean
                is_present = bool(is_present)

                attendance = Attendance(student_id=student_id, course_id=course_id, is_present=is_present, date=attendance_date, attendance_record=attendance_record)
                db.session.add(attendance)
                db.session.commit()

                # Calculate attendance counts after committing the new attendance record
                student = Student.query.get(student_id)
                attendances = Attendance.query.filter_by(student_id=student.id).all()

                attendance_record = calculate_attendance_record(student, attendances)
                total_attendance = Attendance.query.filter_by(student_id=student_id).count()
                present_count = Attendance.query.filter_by(student_id=student_id, is_present=True).count()
                absent_count = total_attendance - present_count

                flash('Attendance mark added successfully.')

                # Render the dashboard template with the updated attendance counts
                return render_template('dashboard.html', students=students, courses=courses, total_attendance=total_attendance, present_count=present_count, absent_count=absent_count)

    # Render the dashboard template
    return render_template('dashboard.html', students=students, courses=courses)
@app.route('/users', methods=['GET', 'POST'])
def users():

    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please login.')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/signup', methods=['POST', 'GET'])

def signup():
    if request.method == "POST":
        form = SignupForm()
        if form.validate_on_submit():
            # Create a new user instance
            user = User(username=form.username.data, password=form.password.data)

            # Add the new user to the database
            db.session.add(user)
            db.session.commit()

            flash("Registration successful. Please login.", "success")
            return redirect(url_for('login'))

    # Handle the GET method (displaying the signup form)
    form = SignupForm()
    return render_template('signup.html', form=form)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = []

    if query:
        # Perform search in the database using SQLAlchemy
        results = Course.query.filter(Course.name.ilike(f'%{query}%')).all()

    return render_template('search.html', query=query, results=results)

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    form = AttendanceForm()

    students = Student.query.all()
    courses = Course.query.all()

    if request.method == 'GET':
        selected_student_id = request.args.get('student_id')
        selected_student = None

        if selected_student_id:
            selected_student = Student.query.get(selected_student_id)

        attendance_records = Attendance.query.filter_by(student_id=selected_student_id).all()

        student_records = []

        for student in students:
            student_attendance = [record for record in attendance_records if record.student_id == student.id]
            attendance_record = calculate_attendance_record(student, student_attendance)

            student_record = {
                'student': student,
                'attendance_record': attendance_record
            }

            student_records.append(student_record)

        return render_template('attendance.html', form=form, students=students, courses=courses,
                               student_records=student_records, selected_student=selected_student)
    
    elif request.method == 'POST':
    # Handle attendance mark submission
    
    
        student_id = request.form.get('student_id')
        student = Student.query.get(student_id)

        if student is None:
            flash('Student not found.')
            return redirect('/dashboard')

        course_id = request.form.get('course_id')
        is_present = request.form.get('is_present')
        attendance_date = request.form.get('attendance_date')
        attendance_record = request.form.get('attendance_record')

        # Assign default values to total_attendance, present_count, and absent_count
        total_attendance = 0
        present_count = 0
        absent_count = 0

        # Perform necessary actions to add an attendance mark
        if not student_id or not course_id or is_present is None:
            flash('Student, course selection, and attendance status are required.')
        else:
            # Convert the string value to a boolean
            is_present = bool(is_present)

            student_id = request.form['student_id']
            course_id = request.form['course_id']
            is_present = request.form['is_present']

            if is_present == 'true':
                is_present = True
            else:
                is_present = False
    

            

            # Assign current date
            attendance_date = datetime.date.today().isoformat()

            # Create attendance record
            attendance_record = Attendance(student_id=student_id, is_present=is_present, course_id=course_id, date=attendance_date)

            # Add record to the database
            db.session.add(attendance_record)
            db.session.commit()

            # Flash success message
            flash('Attendance recorded successfully.')

            # Redirect to the attendance page
            return redirect(url_for('dashboard'))

        # Render the attendance template with the updated attendance counts
        return render_template('attendance.html', students=students, courses=courses, total_attendance=total_attendance, present_count=present_count, absent_count=absent_count,form=form)



@app.route('/courses', methods=['GET', 'POST'])
def courses():
    if request.method == 'POST':
        # Handle the form submission to enroll in a course
        course_id = request.form.get('course_id')

        # Perform any necessary actions with the course enrollment data
        # ...

        # After performing the necessary actions, you can redirect or render a template
        # based on your application's requirements
        return redirect(url_for('success'))

    # Handle the GET request for displaying the course page
    # Retrieve the courses from the database or any other source
    courses = Course.query.all()

    # Render the template for the course page and pass the courses data to the template
    return render_template('courses.html', courses=courses)




@app.route('/students', methods=['GET', 'POST'])
def students():
    form = StudentForm()

    if form.validate_on_submit():  # Process the form data only if it's a POST request
        # Retrieve the form data
        username = form.username.data

        # Create a new student record with the form data
        student = Student(username=username)

        # Process attendance records for each course
        for course in courses:
            attendance_field_name = f"attendance_{course.id}"
            attendance = form[attendance_field_name].data
            # Process the attendance data as needed and update the student record

        # Save the student record to the database
        db.session.add(student)
        db.session.commit()

        flash('Student added successfully!', 'success')
        return redirect(url_for('students'))

    # Render the students template with the form and the list of students
    students = Student.query.all()
    return render_template('students.html', form=form, students=students)

@app.route('/add_mark', methods=['GET', 'POST'])
def add_mark():
    form = MarkForm()

    if request.method == 'POST':
        # Retrieve the selected student and course from the form
        student_id = form.student_id.data
        course_id = form.course_id.data

        # Retrieve the student and course objects from the database
        student = Student.query.get(student_id)
        course = Course.query.get(course_id)

        if student and course:
            # Create a new mark record
            mark = Mark(
                student_id=student_id,
                course_id=course_id,
                mark=form.mark.data,
                score=form.score.data
            )

            # Add the mark record to the database session
            db.session.add(mark)
            db.session.commit()

            flash('Mark added successfully!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid student or course selected.', 'danger')

    # Render the add_mark template with the form and the list of students and courses
    students = Student.query.all()
    courses = Course.query.all()
    return render_template('add_mark.html', form=form, students=students, courses=courses)



@app.route('/enroll_student', methods=['GET', 'POST'])
def enroll_student():
    if request.method == 'POST':
        # Perform the necessary actions to enroll the student
        # You can access form data using request.form
        student_id = request.form.get('student_id')
        course_id = request.form.get('course_id')

        # Find the student and course objects from the database
        student = Student.query.get(student_id)
        course = Course.query.get(course_id)

        if student and course:
            # Create a new enrollment record
            record = Enrollment(student_id=student_id, course_id=course_id)

            # Add the record to the database session
            db.session.add(record)

            # Commit the changes to the database
            db.session.commit()

            # Redirect to a success page or render a template
            return render_template('enrollment_success.html')

        # If student or course is not found, return an error response
        return render_template('enrollment_error.html')

    # Handle GET requests or other HTTP methods
    # You can render a form template or redirect to a different page
    return render_template('enrollment_form.html')



if __name__ == '__main__':
    with app.app_context():

            db.create_all()
    app.run(debug=DEBUG, host='localhost', port='5000')
