from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Student, Result
from app.forms import StudentProfileForm
from app.services.result_engine import ResultEngine
from app.utils.decorators import student_required

student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.route("/dashboard")
@login_required
@student_required
def dashboard():
    """Student portal dashboard."""
    student_profile = Student.query.filter_by(roll_no=current_user.username).first()
    results = Result.query.filter_by(roll_no=current_user.username).order_by(Result.semester.asc()).all() if student_profile else []
    return render_template("student/dashboard.html", student=student_profile, results=results)

@student_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
@student_required
def profile_edit():
    """Allows students to update their phone and email securely."""
    student = Student.query.filter_by(roll_no=current_user.username).first_or_404()
    form = StudentProfileForm(obj=student)

    if form.validate_on_submit():
        # Check email uniqueness against other students
        existing = Student.query.filter(Student.email == form.email.data.strip(), Student.roll_no != student.roll_no).first()
        if existing:
            flash("This email address is already in use by another record.", "danger")
            return render_template("student/profile_edit.html", form=form, student=student)

        student.email = form.email.data.strip()
        student.phone = form.phone.data.strip() if form.phone.data else None
        db.session.commit()
        flash("Your contact details have been updated successfully.", "success")
        return redirect(url_for("student.dashboard"))

    return render_template("student/profile_edit.html", form=form, student=student)

@student_bp.route("/marksheet/<int:semester>")
@login_required
@student_required
def view_marksheet(semester):
    """
    Renders official printable marksheet.
    Enforces server-side ownership verification: students can ONLY view their own marks.
    """
    roll_no = current_user.username
    student = Student.query.filter_by(roll_no=roll_no).first_or_404()
    result = Result.query.filter_by(roll_no=roll_no, semester=semester).first()

    if not result:
        flash(f"Semester {semester} result has not been published yet.", "warning")
        return redirect(url_for("student.dashboard"))

    try:
        breakdown = ResultEngine.calculate_student_semester_result(roll_no, semester)
    except Exception as e:
        flash(f"Unable to retrieve marksheet breakdown: {str(e)}", "danger")
        return redirect(url_for("student.dashboard"))

    return render_template(
        "student/marksheet.html",
        student=student,
        result=result,
        breakdown=breakdown,
        semester=semester
    )
