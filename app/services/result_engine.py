from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any, List
from app.extensions import db
from app.models import Student, Subject, Mark, Result, ResultStatus
from config import Config

class ResultEngine:
    """
    Centralized academic computation engine for SGPA, percentage,
    and semester evaluation status.
    """

    GRADE_POINT_MAP = Config.GRADE_POINT_MAP

    @classmethod
    def calculate_student_semester_result(cls, roll_no: str, semester: int) -> Dict[str, Any]:
        """
        Calculates SGPA, percentage, and PASS/FAIL/RA status for a student in a specific semester.
        Formula:
            SGPA = Sum(Grade Point * Credits) / Sum(Credits)
            Percentage = (Total Marks Obtained / Total Maximum Marks) * 100
        """
        student = Student.query.get(roll_no)
        if not student:
            raise ValueError(f"Student with roll number '{roll_no}' not found.")

        # Fetch subjects configured for this semester and course
        subjects = Subject.query.filter_by(semester=semester, course=student.course).all()
        if not subjects:
            raise ValueError(f"No subjects found for {student.course} Semester {semester}.")

        # Fetch student marks for these subjects
        sub_codes = [s.sub_code for s in subjects]
        marks = Mark.query.filter(
            Mark.roll_no == roll_no,
            Mark.sub_code.in_(sub_codes)
        ).all()

        marks_dict = {m.sub_code: m for m in marks}

        # Check if all subjects have finalized or entered marks
        if len(marks) < len(subjects):
            missing = set(sub_codes) - set(marks_dict.keys())
            raise ValueError(f"Marks missing for subject(s): {', '.join(missing)}")

        total_credits = 0
        total_weighted_gp = 0
        total_obtained_marks = 0
        total_max_marks = len(subjects) * 100
        has_f_grade = False

        subject_breakdown = []

        for sub in subjects:
            mark_entry = marks_dict[sub.sub_code]
            gp = cls.GRADE_POINT_MAP.get(mark_entry.grade, 0)
            weighted_gp = gp * sub.credits

            total_credits += sub.credits
            total_weighted_gp += weighted_gp
            total_obtained_marks += mark_entry.total

            if mark_entry.grade == "F":
                has_f_grade = True

            subject_breakdown.append({
                "sub_code": sub.sub_code,
                "sub_name": sub.sub_name,
                "credits": sub.credits,
                "internal": mark_entry.internal,
                "external": mark_entry.external,
                "total": mark_entry.total,
                "grade": mark_entry.grade,
                "grade_point": gp,
                "weighted_gp": weighted_gp
            })

        if total_credits == 0:
            raise ValueError("Total credits cannot be zero.")

        # Compute SGPA rounded to 2 decimal places
        sgpa_raw = Decimal(total_weighted_gp) / Decimal(total_credits)
        sgpa = sgpa_raw.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Compute percentage
        percentage_raw = (Decimal(total_obtained_marks) / Decimal(total_max_marks)) * Decimal(100)
        percentage = percentage_raw.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        status = ResultStatus.FAIL if has_f_grade else ResultStatus.PASS

        return {
            "roll_no": roll_no,
            "semester": semester,
            "total_credits": total_credits,
            "total_weighted_gp": total_weighted_gp,
            "total_obtained_marks": total_obtained_marks,
            "total_max_marks": total_max_marks,
            "sgpa": sgpa,
            "percentage": percentage,
            "status": status,
            "subject_breakdown": subject_breakdown
        }

    @classmethod
    def generate_and_save_result(cls, roll_no: str, semester: int) -> Result:
        """Computes and upserts the result record into the RESULTS table."""
        res_data = cls.calculate_student_semester_result(roll_no, semester)

        result = Result.query.filter_by(roll_no=roll_no, semester=semester).first()
        if not result:
            result = Result(
                roll_no=roll_no,
                semester=semester,
                sgpa=res_data["sgpa"],
                percentage=res_data["percentage"],
                status=res_data["status"]
            )
            db.session.add(result)
        else:
            result.sgpa = res_data["sgpa"]
            result.percentage = res_data["percentage"]
            result.status = res_data["status"]

        db.session.commit()
        return result
