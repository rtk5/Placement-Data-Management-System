# utils.py - helper functions used by app pages
from db_connection import run_query, run_commit

def get_student_by_login(student_id, first_name, phone):
    rows = run_query(
        "SELECT * FROM STUDENT WHERE Student_ID=%s AND First_Name=%s AND Phone=%s",
        (student_id, first_name, phone),
    )
    return rows[0] if rows else None

def get_officer_by_login(email, password):
    rows = run_query(
        "SELECT * FROM PLACEMENT_OFFICER WHERE Email=%s AND Password=%s",
        (email, password),
    )
    return rows[0] if rows else None

def student_is_eligible_for_job(student_cgpa, job_row):
    # job_row expected to have 'Minimum_CGPA' key
    try:
        return float(student_cgpa) >= float(job_row.get("Minimum_CGPA", 0))
    except Exception:
        return False
