from datetime import datetime, timezone
from decimal import Decimal
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import CheckConstraint, UniqueConstraint, event
from app.extensions import db

class UserRole:
    ADMIN = "admin"
    FACULTY = "faculty"
    STUDENT = "student"
    CHOICES = [ADMIN, FACULTY, STUDENT]

class ResultStatus:
    PASS = "PASS"
    FAIL = "FAIL"
    RA = "RA"
    CHOICES = [PASS, FAIL, RA]

class User(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=UserRole.STUDENT)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        CheckConstraint("role IN ('admin', 'faculty', 'student')", name="check_user_role"),
    )

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def is_faculty(self) -> bool:
        return self.role == UserRole.FACULTY

    def is_student(self) -> bool:
        return self.role == UserRole.STUDENT

    def __repr__(self) -> str:
        return f"<User {self.username} [{self.role}]>"


class Student(db.Model):
    __tablename__ = "students"

    roll_no = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(30), nullable=False, default="BCA")
    semester = db.Column(db.Integer, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(15), nullable=True)

    __table_args__ = (
        CheckConstraint("semester >= 1 AND semester <= 6", name="check_student_semester_range"),
    )

    marks = db.relationship("Mark", back_populates="student", cascade="all, delete-orphan", lazy="dynamic")
    results = db.relationship("Result", back_populates="student", cascade="all, delete-orphan", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Student {self.roll_no} - {self.name}>"


class Subject(db.Model):
    __tablename__ = "subjects"

    sub_code = db.Column(db.String(15), primary_key=True)
    sub_name = db.Column(db.String(120), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(30), nullable=False, default="BCA")

    __table_args__ = (
        CheckConstraint("credits > 0", name="check_subject_positive_credits"),
        CheckConstraint("semester >= 1 AND semester <= 6", name="check_subject_semester_range"),
    )

    marks = db.relationship("Mark", back_populates="subject", cascade="all, delete-orphan", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Subject {self.sub_code}: {self.sub_name} (Credits: {self.credits})>"


class Mark(db.Model):
    __tablename__ = "marks"

    mark_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_no = db.Column(db.String(20), db.ForeignKey("students.roll_no", ondelete="CASCADE"), nullable=False)
    sub_code = db.Column(db.String(15), db.ForeignKey("subjects.sub_code", ondelete="CASCADE"), nullable=False)
    internal = db.Column(db.Integer, nullable=False)
    external = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(3), nullable=False)
    is_finalized = db.Column(db.Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("roll_no", "sub_code", name="uq_student_subject_mark"),
        CheckConstraint("internal >= 0 AND internal <= 30", name="check_internal_marks_range"),
        CheckConstraint("external >= 0 AND external <= 70", name="check_external_marks_range"),
        CheckConstraint("total >= 0 AND total <= 100", name="check_total_marks_range"),
        CheckConstraint(
            "grade IN ('A+', 'A', 'B+', 'B', 'C', 'D', 'F')", 
            name="check_valid_grade_letter"
        ),
    )

    student = db.relationship("Student", back_populates="marks")
    subject = db.relationship("Subject", back_populates="marks")

    @staticmethod
    def calculate_grade(total_score: int) -> str:
        if total_score >= 85:
            return "A+"
        elif total_score >= 75:
            return "A"
        elif total_score >= 65:
            return "B+"
        elif total_score >= 55:
            return "B"
        elif total_score >= 50:
            return "C"
        elif total_score >= 40:
            return "D"
        else:
            return "F"

    def compute_scores(self) -> None:
        self.total = int(self.internal) + int(self.external)
        self.grade = self.calculate_grade(self.total)

    def __repr__(self) -> str:
        return f"<Mark ID {self.mark_id}: {self.roll_no} - {self.sub_code} ({self.total}, Grade: {self.grade})>"


@event.listens_for(Mark, "before_insert")
@event.listens_for(Mark, "before_update")
def receive_before_mark_save(mapper, connection, target: Mark):
    target.compute_scores()


class Result(db.Model):
    __tablename__ = "results"

    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_no = db.Column(db.String(20), db.ForeignKey("students.roll_no", ondelete="CASCADE"), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    sgpa = db.Column(db.Numeric(4, 2), nullable=False)
    percentage = db.Column(db.Numeric(5, 2), nullable=False)
    status = db.Column(db.String(10), nullable=False, default=ResultStatus.PASS)
    generated_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        UniqueConstraint("roll_no", "semester", name="uq_student_semester_result"),
        CheckConstraint("semester >= 1 AND semester <= 6", name="check_result_semester_range"),
        CheckConstraint("status IN ('PASS', 'FAIL', 'RA')", name="check_result_status_valid"),
    )

    student = db.relationship("Student", back_populates="results")

    def __repr__(self) -> str:
        return f"<Result ID {self.result_id}: {self.roll_no} Sem {self.semester} (SGPA: {self.sgpa}, Status: {self.status})>"
