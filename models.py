from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Basic Info
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    blood_group = db.Column(db.String(10))

    # Contact Info
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text)

    guardian_name = db.Column(db.String(120))
    guardian_contact = db.Column(db.String(20))

    # Academic Info
    admission_year = db.Column(db.Integer)
    previous_qualification = db.Column(db.String(200))

    current_course = db.Column(db.String(120), nullable=False)
    current_year = db.Column(db.Integer)  # 1,2,3...
    roll_number = db.Column(db.String(50), unique=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
