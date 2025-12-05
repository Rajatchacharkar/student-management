from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Student
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "students.db")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "dev-secret"  # development only

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    students = Student.query.order_by(Student.id.desc()).all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        d = request.form
        try:
            dob = datetime.strptime(d.get('date_of_birth'), "%Y-%m-%d").date() if d.get('date_of_birth') else None
        except ValueError:
            flash("Date format invalid. Use YYYY-MM-DD.")
            return redirect(url_for('add_student'))

        s = Student(
            first_name=d.get('first_name'),
            last_name=d.get('last_name'),
            gender=d.get('gender'),
            date_of_birth=dob,
            blood_group=d.get('blood_group'),
            email=d.get('email'),
            mobile_number=d.get('mobile_number'),
            address=d.get('address'),
            guardian_name=d.get('guardian_name'),
            guardian_contact=d.get('guardian_contact'),
            admission_year=int(d.get('admission_year')) if d.get('admission_year') else None,
            previous_qualification=d.get('previous_qualification'),
            current_course=d.get('current_course'),
            current_year=int(d.get('current_year')) if d.get('current_year') else None,
            roll_number=d.get('roll_number')
        )
        try:
            db.session.add(s)
            db.session.commit()
            flash("Student added successfully.")
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash("Error adding student: " + str(e))
            return redirect(url_for('add_student'))
    return render_template('add_student.html')

@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    s = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        d = request.form
        try:
            s.first_name = d.get('first_name')
            s.last_name = d.get('last_name')
            s.gender = d.get('gender')
            s.date_of_birth = datetime.strptime(d.get('date_of_birth'), "%Y-%m-%d").date() if d.get('date_of_birth') else None
            s.blood_group = d.get('blood_group')
            s.email = d.get('email')
            s.mobile_number = d.get('mobile_number')
            s.address = d.get('address')
            s.guardian_name = d.get('guardian_name')
            s.guardian_contact = d.get('guardian_contact')
            s.admission_year = int(d.get('admission_year')) if d.get('admission_year') else None
            s.previous_qualification = d.get('previous_qualification')
            s.current_course = d.get('current_course')
            s.current_year = int(d.get('current_year')) if d.get('current_year') else None
            s.roll_number = d.get('roll_number')
            db.session.commit()
            flash("Student updated.")
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash("Error updating: " + str(e))
            return redirect(url_for('edit_student', student_id=student_id))
    return render_template('edit_student.html', student=s)

@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    s = Student.query.get_or_404(student_id)
    try:
        db.session.delete(s)
        db.session.commit()
        flash("Student deleted.")
    except Exception as e:
        db.session.rollback()
        flash("Error deleting: " + str(e))
    return redirect(url_for('index'))

# optional simple JSON API
@app.route('/api/students', methods=['GET'])
def api_list():
    return jsonify([s.to_dict() for s in Student.query.all()])

if __name__ == '__main__':
    app.run(debug=True)
