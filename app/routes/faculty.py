from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models import Student, Subject, Mark
from app.forms import MarkEntryForm
from app.utils.decorators import faculty_required

faculty_bp = Blueprint("faculty", __name__, url_prefix="/faculty")

@faculty_bp.route("/dashboard")
@login_required
@faculty_required
def dashboard():
    subjects = Subject.query.order_by(Subject.semester.asc(), Subject.sub_code.asc()).all()
    selected_sub = request.args.get("subject", "").strip()

    students_marks = []
    current_subject = None

    if selected_sub:
        current_subject = Subject.query.get(selected_sub)
        if current_subject:
            # Query students eligible for the subject's semester
            students = Student.query.filter_by(semester=current_subject.semester).order_by(Student.roll_no.asc()).all()
            for s in students:
                mark_rec = Mark.query.filter_by(roll_no=s.roll_no, sub_code=current_subject.sub_code).first()
                students_marks.append({
                    "student": s,
                    "mark": mark_rec
                })

    return render_template(
        "faculty/dashboard.html",
        subjects=subjects,
        selected_sub=selected_sub,
        current_subject=current_subject,
        students_marks=students_marks
    )

@faculty_bp.route("/marks/<string:roll_no>/<string:sub_code>/edit", methods=["GET", "POST"])
@login_required
@faculty_required
def mark_entry(roll_no, sub_code):
    student = Student.query.get_or_404(roll_no)
    subject = Subject.query.get_or_404(sub_code)
    mark = Mark.query.filter_by(roll_no=roll_no, sub_code=sub_code).first()

    # Prevent modification if already finalized
    if mark and mark.is_finalized:
        flash(f"Marks for {student.roll_no} in {subject.sub_code} are FINALIZED and locked against changes.", "warning")
        return redirect(url_for("faculty.dashboard", subject=sub_code))

    form = MarkEntryForm(obj=mark)

    if form.validate_on_submit():
        internal = form.internal.data
        external = form.external.data
        is_finalize_action = "finalize" in request.form

        if not mark:
            mark = Mark(
                roll_no=roll_no,
                sub_code=sub_code,
                internal=internal,
                external=external,
                total=internal + external,
                grade=Mark.calculate_grade(internal + external),
                is_finalized=is_finalize_action
            )
            db.session.add(mark)
        else:
            mark.internal = internal
            mark.external = external
            mark.compute_scores()
            mark.is_finalized = is_finalize_action

        db.session.commit()
        status_msg = "finalized and locked" if is_finalize_action else "saved as draft"
        flash(f"Marks for {student.name} ({student.roll_no}) {status_msg}.", "success")
        return redirect(url_for("faculty.dashboard", subject=sub_code))

    return render_template("faculty/mark_entry.html", student=student, subject=subject, mark=mark, form=form)
