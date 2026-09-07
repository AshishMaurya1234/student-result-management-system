from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange, Optional

class LoginForm(FlaskForm):
    username = StringField(
        "Username / Roll Number", 
        validators=[
            DataRequired(message="Username or Roll Number is required."),
            Length(min=3, max=80, message="Username must be between 3 and 80 characters.")
        ],
        render_kw={"placeholder": "e.g. admin or 2350382985", "autocomplete": "username"}
    )
    password = PasswordField(
        "Password", 
        validators=[DataRequired(message="Password is required.")],
        render_kw={"placeholder": "Enter your password", "autocomplete": "current-password"}
    )
    submit = SubmitField("Sign In")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        "Current Password", 
        validators=[DataRequired(message="Current password is required.")],
        render_kw={"placeholder": "Enter current password"}
    )
    new_password = PasswordField(
        "New Password", 
        validators=[
            DataRequired(message="New password is required."),
            Length(min=8, message="Password must be at least 8 characters long.")
        ],
        render_kw={"placeholder": "Enter new password (min 8 characters)"}
    )
    confirm_password = PasswordField(
        "Confirm New Password", 
        validators=[
            DataRequired(message="Please confirm your new password."),
            EqualTo("new_password", message="Passwords must match.")
        ],
        render_kw={"placeholder": "Repeat new password"}
    )
    submit = SubmitField("Update Password")

class StudentForm(FlaskForm):
    roll_no = StringField(
        "Roll Number / Enrolment No.",
        validators=[DataRequired(), Length(min=5, max=20)],
        render_kw={"placeholder": "e.g. 2350382987"}
    )
    name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={"placeholder": "e.g. Rahul Sharma"}
    )
    course = SelectField(
        "Course",
        choices=[("BCA", "Bachelor of Computer Applications (BCA)")],
        default="BCA",
        validators=[DataRequired()]
    )
    semester = SelectField(
        "Semester",
        choices=[(str(i), f"Semester {i}") for i in range(1, 7)],
        validators=[DataRequired()]
    )
    dob = DateField(
        "Date of Birth",
        validators=[DataRequired()],
        render_kw={"type": "date"}
    )
    email = StringField(
        "Email Address",
        validators=[DataRequired(), Email(), Length(max=120)],
        render_kw={"placeholder": "e.g. student@example.com"}
    )
    phone = StringField(
        "Contact Number",
        validators=[Optional(), Length(min=10, max=15)],
        render_kw={"placeholder": "e.g. 9876543210"}
    )
    submit = SubmitField("Save Student")

class StudentProfileForm(FlaskForm):
    """Allows students to update their own contact information."""
    email = StringField(
        "Email Address",
        validators=[DataRequired(), Email(), Length(max=120)],
        render_kw={"placeholder": "e.g. student@example.com"}
    )
    phone = StringField(
        "Phone Number",
        validators=[Optional(), Length(min=10, max=15)],
        render_kw={"placeholder": "e.g. 9876543210"}
    )
    submit = SubmitField("Update Profile")

class SubjectForm(FlaskForm):
    sub_code = StringField(
        "Subject Code",
        validators=[DataRequired(), Length(min=3, max=15)],
        render_kw={"placeholder": "e.g. BCS-055"}
    )
    sub_name = StringField(
        "Subject Title",
        validators=[DataRequired(), Length(min=3, max=120)],
        render_kw={"placeholder": "e.g. Java Programming"}
    )
    credits = IntegerField(
        "Credit Hours",
        validators=[DataRequired(), NumberRange(min=1, max=8, message="Credits must be between 1 and 8.")],
        render_kw={"placeholder": "e.g. 4"}
    )
    semester = SelectField(
        "Semester",
        choices=[(str(i), f"Semester {i}") for i in range(1, 7)],
        validators=[DataRequired()]
    )
    course = SelectField(
        "Course",
        choices=[("BCA", "Bachelor of Computer Applications (BCA)")],
        default="BCA",
        validators=[DataRequired()]
    )
    submit = SubmitField("Save Subject")

class MarkEntryForm(FlaskForm):
    internal = IntegerField(
        "Internal Marks (Max 30)",
        validators=[DataRequired(), NumberRange(min=0, max=30, message="Internal marks must be 0 to 30.")],
        render_kw={"min": "0", "max": "30", "id": "input_internal"}
    )
    external = IntegerField(
        "External Marks (Max 70)",
        validators=[DataRequired(), NumberRange(min=0, max=70, message="External marks must be 0 to 70.")],
        render_kw={"min": "0", "max": "70", "id": "input_external"}
    )
    submit = SubmitField("Save Draft")
    finalize = SubmitField("Finalize & Lock Marks")

class CSVUploadForm(FlaskForm):
    file = FileField(
        "Select CSV File",
        validators=[
            FileRequired(message="Please select a CSV file to upload."),
            FileAllowed(["csv"], "Only standard CSV files are accepted.")
        ]
    )
    submit = SubmitField("Upload & Process Students")
