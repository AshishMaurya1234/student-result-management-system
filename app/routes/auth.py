from urllib.parse import urlsplit
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User, UserRole
from app.forms import LoginForm, ChangePasswordForm

auth_bp = Blueprint("auth", __name__)

def get_role_redirect(role: str) -> str:
    if role == UserRole.ADMIN:
        return url_for("admin.dashboard")
    elif role == UserRole.FACULTY:
        return url_for("faculty.dashboard")
    elif role == UserRole.STUDENT:
        return url_for("student.dashboard")
    return url_for("auth.login")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(get_role_redirect(current_user.role))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=False)
            flash(f"Welcome, {user.username}! Signed in as {user.role.title()}.", "success")

            next_page = request.args.get("next")
            if next_page and not urlsplit(next_page).netloc and not urlsplit(next_page).scheme:
                return redirect(next_page)
            return redirect(get_role_redirect(user.role))

        flash("Invalid username or password. Please verify credentials.", "danger")

    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_pw = form.old_password.data.strip()
        new_pw = form.new_password.data.strip()

        # Verify old password
        if not current_user.check_password(old_pw):
            flash("The current password entered is incorrect.", "danger")
            return render_template("auth/change_password.html", form=form)

        # Set new password hash
        current_user.set_password(new_pw)
        db.session.add(current_user)
        db.session.commit()

        flash("Your password has been changed successfully. Please continue.", "success")
        return redirect(get_role_redirect(current_user.role))

    return render_template("auth/change_password.html", form=form)
