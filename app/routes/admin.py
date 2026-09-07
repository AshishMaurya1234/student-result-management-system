import csv
import io
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models import Student, Subject, Mark, Result, User, UserRole
from app.forms import StudentForm, SubjectForm, CSVUploadForm
from app.services.result_engine import ResultEngine
from app.utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    stats = {
        "students_count": Student.query.count(),
        "subjects_count": Subject.query.count(),
        "marks_count": Mark.query.count(),
        "results_count": Result.query.count()
    }
    return render_template("admin/dashboard.html", stats=stats)

# ==================== RESULT MANAGEMENT ====================

@admin_bp.route("/results")
@login_required
@admin_required
def results_manager():
    semester = request.args.get("semester", "5").strip()
    sem_val = int(semester) if semester.isdigit() else 5

    students = Student.query.filter_by(semester=sem_val).order_by(Student.roll_no.asc()).all()
    results_map = {r.roll_no: r for r in Result.query.filter_by(semester=sem_val).all()}

    student_data = []
    for s in students:
        student_data.append({
            "student": s,
            "result": results_map.get(s.roll_no)
        })

    return render_template("admin/results_manager.html", sem_val=sem_val, student_data=student_data)

@admin_bp.route("/results/generate/<string:roll_no>/<int:semester>", methods=["POST"])
@login_required
@admin_required
def generate_single_result(roll_no, semester):
    try:
        res = ResultEngine.generate_and_save_result(roll_no, semester)
        flash(f"Result generated for {roll_no}: SGPA = {res.sgpa}, Status = {res.status}.", "success")
    except Exception as e:
        flash(f"Could not generate result for {roll_no}: {str(e)}", "danger")
    return redirect(url_for("admin.results_manager", semester=semester))

@admin_bp.route("/results/generate-batch/<int:semester>", methods=["POST"])
@login_required
@admin_required
def generate_batch_results(semester):
    students = Student.query.filter_by(semester=semester).all()
    success_count = 0
    errors = []

    for s in students:
        try:
            ResultEngine.generate_and_save_result(s.roll_no, semester)
            success_count += 1
        except Exception as e:
            errors.append(f"{s.roll_no}: {str(e)}")

    if success_count > 0:
        flash(f"Batch generation completed: {success_count} student results generated.", "success")
    if errors:
        flash(f"Errors occurred in {len(errors)} student(s). First error: {errors[0]}", "warning")

    return redirect(url_for("admin.results_manager", semester=semester))

# ==================== STUDENT CRUD ====================

@admin_bp.route("/students")
@login_required
@admin_required
def students_list():
    search = request.args.get("search", "").strip()
    sem_filter = request.args.get("semester", "").strip()

    query = Student.query
    if search:
        query = query.filter((Student.roll_no.ilike(f"%{search}%")) | (Student.name.ilike(f"%{search}%")))
    if sem_filter and sem_filter.isdigit():
        query = query.filter(Student.semester == int(sem_filter))

    students = query.order_by(Student.roll_no.asc()).all()
    return render_template("admin/students_list.html", students=students, search=search, sem_filter=sem_filter)

@admin_bp.route("/students/new", methods=["GET", "POST"])
@login_required
@admin_required
def student_create():
    form = StudentForm()
    if form.validate_on_submit():
        if Student.query.filter_by(roll_no=form.roll_no.data.strip()).first():
            flash(f"Student with Roll No '{form.roll_no.data.strip()}' already exists.", "danger")
            return render_template("admin/student_form.html", form=form, title="Add New Student")

        if Student.query.filter_by(email=form.email.data.strip()).first():
            flash(f"Email '{form.email.data.strip()}' is already registered.", "danger")
            return render_template("admin/student_form.html", form=form, title="Add New Student")

        student = Student(
            roll_no=form.roll_no.data.strip(),
            name=form.name.data.strip(),
            course=form.course.data,
            semester=int(form.semester.data),
            dob=form.dob.data,
            email=form.email.data.strip(),
            phone=form.phone.data.strip() if form.phone.data else None
        )
        db.session.add(student)

        if not User.query.filter_by(username=student.roll_no).first():
            student_user = User(username=student.roll_no, role=UserRole.STUDENT)
            student_user.set_password(f"Student@{student.roll_no[-4:] if len(student.roll_no) >= 4 else '123'}")
            db.session.add(student_user)

        db.session.commit()
        flash(f"Student {student.name} ({student.roll_no}) added successfully.", "success")
        return redirect(url_for("admin.students_list"))

    return render_template("admin/student_form.html", form=form, title="Add New Student")

@admin_bp.route("/students/<string:roll_no>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def student_edit(roll_no):
    student = Student.query.get_or_404(roll_no)
    form = StudentForm(obj=student)
    form.roll_no.render_kw = {"readonly": True}

    if form.validate_on_submit():
        email_check = Student.query.filter(Student.email == form.email.data.strip(), Student.roll_no != roll_no).first()
        if email_check:
            flash(f"Email '{form.email.data.strip()}' is in use by another student.", "danger")
            return render_template("admin/student_form.html", form=form, title="Edit Student")

        student.name = form.name.data.strip()
        student.course = form.course.data
        student.semester = int(form.semester.data)
        student.dob = form.dob.data
        student.email = form.email.data.strip()
        student.phone = form.phone.data.strip() if form.phone.data else None

        db.session.commit()
        flash(f"Student {student.roll_no} updated successfully.", "success")
        return redirect(url_for("admin.students_list"))

    form.semester.data = str(student.semester)
    return render_template("admin/student_form.html", form=form, title="Edit Student")

@admin_bp.route("/students/<string:roll_no>/delete", methods=["POST"])
@login_required
@admin_required
def student_delete(roll_no):
    student = Student.query.get_or_404(roll_no)
    user = User.query.filter_by(username=roll_no).first()

    db.session.delete(student)
    if user:
        db.session.delete(user)
    db.session.commit()

    flash(f"Student {roll_no} and associated marks have been deleted.", "info")
    return redirect(url_for("admin.students_list"))

# ==================== SUBJECT CRUD ====================

@admin_bp.route("/subjects")
@login_required
@admin_required
def subjects_list():
    subjects = Subject.query.order_by(Subject.semester.asc(), Subject.sub_code.asc()).all()
    return render_template("admin/subjects_list.html", subjects=subjects)

@admin_bp.route("/subjects/new", methods=["GET", "POST"])
@login_required
@admin_required
def subject_create():
    form = SubjectForm()
    if form.validate_on_submit():
        code = form.sub_code.data.strip().upper()
        if Subject.query.filter_by(sub_code=code).first():
            flash(f"Subject code '{code}' already exists.", "danger")
            return render_template("admin/subject_form.html", form=form, title="Add Subject")

        subject = Subject(
            sub_code=code,
            sub_name=form.sub_name.data.strip(),
            credits=form.credits.data,
            semester=int(form.semester.data),
            course=form.course.data
        )
        db.session.add(subject)
        db.session.commit()
        flash(f"Subject {subject.sub_code} added successfully.", "success")
        return redirect(url_for("admin.subjects_list"))

    return render_template("admin/subject_form.html", form=form, title="Add Subject")

@admin_bp.route("/subjects/<string:sub_code>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def subject_edit(sub_code):
    subject = Subject.query.get_or_404(sub_code)
    form = SubjectForm(obj=subject)
    form.sub_code.render_kw = {"readonly": True}

    if form.validate_on_submit():
        subject.sub_name = form.sub_name.data.strip()
        subject.credits = form.credits.data
        subject.semester = int(form.semester.data)
        subject.course = form.course.data

        db.session.commit()
        flash(f"Subject {subject.sub_code} updated successfully.", "success")
        return redirect(url_for("admin.subjects_list"))

    form.semester.data = str(subject.semester)
    return render_template("admin/subject_form.html", form=form, title="Edit Subject")

@admin_bp.route("/subjects/<string:sub_code>/delete", methods=["POST"])
@login_required
@admin_required
def subject_delete(sub_code):
    subject = Subject.query.get_or_404(sub_code)
    db.session.delete(subject)
    db.session.commit()
    flash(f"Subject {sub_code} removed successfully.", "info")
    return redirect(url_for("admin.subjects_list"))

# ==================== CSV BULK IMPORT ====================

@admin_bp.route("/students/import", methods=["GET", "POST"])
@login_required
@admin_required
def import_students():
    form = CSVUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)

        expected_headers = {"roll_no", "name", "course", "semester", "dob", "email", "phone"}
        if not expected_headers.issubset(set([h.strip() for h in (reader.fieldnames or [])])):
            flash(f"Invalid CSV headers. Required: {', '.join(expected_headers)}", "danger")
            return render_template("admin/import_csv.html", form=form)

        success_count = 0
        skipped_count = 0

        try:
            for row in reader:
                roll_no = row["roll_no"].strip()
                email = row["email"].strip()

                if not roll_no or not email:
                    skipped_count += 1
                    continue

                if Student.query.filter((Student.roll_no == roll_no) | (Student.email == email)).first():
                    skipped_count += 1
                    continue

                dob_val = datetime.strptime(row["dob"].strip(), "%Y-%m-%d").date()
                student = Student(
                    roll_no=roll_no,
                    name=row["name"].strip(),
                    course=row["course"].strip(),
                    semester=int(row["semester"].strip()),
                    dob=dob_val,
                    email=email,
                    phone=row["phone"].strip() if row.get("phone") else None
                )
                db.session.add(student)

                if not User.query.filter_by(username=roll_no).first():
                    user = User(username=roll_no, role=UserRole.STUDENT)
                    user.set_password(f"Student@{roll_no[-4:] if len(roll_no)>=4 else '123'}")
                    db.session.add(user)

                success_count += 1

            db.session.commit()
            flash(f"CSV processed: {success_count} student(s) imported, {skipped_count} skipped.", "success")
            return redirect(url_for("admin.students_list"))
        except Exception as e:
            db.session.rollback()
            flash(f"CSV import failed: {str(e)}", "danger")

    return render_template("admin/import_csv.html", form=form)
