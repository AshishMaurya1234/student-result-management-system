from datetime import date
from decimal import Decimal
from app import create_app
from app.extensions import db
from app.models import User, Student, Subject, Mark, Result, UserRole, ResultStatus

def seed_database():
    app = create_app("development")
    
    with app.app_context():
        print("[1/5] Creating database tables...")
        db.create_all()

        print("[2/5] Seeding user accounts...")
        users_data = [
            {"username": "admin", "password": "AdminPassword@123", "role": UserRole.ADMIN},
            {"username": "faculty", "password": "FacultyPassword@123", "role": UserRole.FACULTY},
            {"username": "2350382985", "password": "StudentPassword@123", "role": UserRole.STUDENT},
            {"username": "2350382986", "password": "StudentPassword@123", "role": UserRole.STUDENT},
        ]
        
        for u in users_data:
            existing_user = User.query.filter_by(username=u["username"]).first()
            if not existing_user:
                new_user = User(username=u["username"], role=u["role"])
                new_user.set_password(u["password"])
                db.session.add(new_user)
        db.session.commit()

        print("[3/5] Seeding BCA Semester 5 subjects...")
        subjects_data = [
            {"sub_code": "BCS-051", "sub_name": "Introduction to Software Engineering", "credits": 4, "semester": 5, "course": "BCA"},
            {"sub_code": "BCS-052", "sub_name": "Network Programming and Administration", "credits": 4, "semester": 5, "course": "BCA"},
            {"sub_code": "BCS-053", "sub_name": "Web Programming", "credits": 4, "semester": 5, "course": "BCA"},
            {"sub_code": "BCS-054", "sub_name": "Numerical and Statistical Computing", "credits": 4, "semester": 5, "course": "BCA"},
            {"sub_code": "BCSL-056", "sub_name": "Network Programming and Web Programming Lab", "credits": 2, "semester": 5, "course": "BCA"},
        ]

        for s in subjects_data:
            if not Subject.query.filter_by(sub_code=s["sub_code"]).first():
                sub = Subject(**s)
                db.session.add(sub)
        db.session.commit()

        print("[4/5] Seeding student profiles...")
        students_data = [
            {
                "roll_no": "2350382985",
                "name": "Prince Kumar",
                "course": "BCA",
                "semester": 5,
                "dob": date(2002, 8, 15),
                "email": "prince.kumar@example.com",
                "phone": "9876543210"
            },
            {
                "roll_no": "2350382986",
                "name": "Amit Sharma",
                "course": "BCA",
                "semester": 5,
                "dob": date(2003, 3, 22),
                "email": "amit.sharma@example.com",
                "phone": "9876543211"
            }
        ]

        for st in students_data:
            if not Student.query.filter_by(roll_no=st["roll_no"]).first():
                student_obj = Student(**st)
                db.session.add(student_obj)
        db.session.commit()

        print("[5/5] Seeding academic evaluation marks and results...")
        prince_marks = [
            {"roll_no": "2350382985", "sub_code": "BCS-051", "internal": 24, "external": 55, "is_finalized": True},
            {"roll_no": "2350382985", "sub_code": "BCS-052", "internal": 22, "external": 48, "is_finalized": True},
            {"roll_no": "2350382985", "sub_code": "BCS-053", "internal": 20, "external": 40, "is_finalized": True},
            {"roll_no": "2350382985", "sub_code": "BCS-054", "internal": 26, "external": 60, "is_finalized": True},
            {"roll_no": "2350382985", "sub_code": "BCSL-056", "internal": 25, "external": 60, "is_finalized": True},
        ]

        for m in prince_marks:
            existing_mark = Mark.query.filter_by(roll_no=m["roll_no"], sub_code=m["sub_code"]).first()
            if not existing_mark:
                mark_obj = Mark(
                    roll_no=m["roll_no"],
                    sub_code=m["sub_code"],
                    internal=m["internal"],
                    external=m["external"],
                    total=m["internal"] + m["external"],
                    grade=Mark.calculate_grade(m["internal"] + m["external"]),
                    is_finalized=m["is_finalized"]
                )
                db.session.add(mark_obj)

        if not Result.query.filter_by(roll_no="2350382985", semester=5).first():
            result_obj = Result(
                roll_no="2350382985",
                semester=5,
                sgpa=Decimal("8.67"),
                percentage=Decimal("76.00"),
                status=ResultStatus.PASS
            )
            db.session.add(result_obj)

        db.session.commit()
        print("\n==================================================")
        print(" Database successfully initialized and seeded! ")
        print(" Default Accounts:")
        print("   - Admin:   username='admin'      | password='AdminPassword@123'")
        print("   - Faculty: username='faculty'    | password='FacultyPassword@123'")
        print("   - Student: username='2350382985' | password='StudentPassword@123'")
        print("==================================================")

if __name__ == "__main__":
    seed_database()
