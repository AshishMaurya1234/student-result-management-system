from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.utils.decorators import student_required
from app.models import Student, Result

student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.route("/dashboard")
@login_required
@student_required
def dashboard():
    student_profile = Student.query.filter_by(roll_no=current_user.username).first()
    results = Result.query.filter_by(roll_no=current_user.username).all() if student_profile else []
    return render_template("student/dashboard.html", student=student_profile, results=results)
