# pages/student_portal.py
import streamlit as st
from db_connection import run_query, run_commit
from utils import student_is_eligible_for_job


def show_student_portal(student):
    st.header("🎓 Student Dashboard")
    st.markdown(f"**Hello, {student.get('First_Name', 'Student')} (ID: {student.get('Student_ID')})**")

    # ---------------- PERSONAL INFO ---------------- #
    with st.expander("👤 View / Edit Personal Info", expanded=True):
        fname = st.text_input("First Name", student.get("First_Name", ""))
        lname = st.text_input("Last Name", student.get("Last_Name", ""))
        email = st.text_input("Email", student.get("Email", ""))
        phone = st.text_input("Phone", student.get("Phone", ""))
        cgpa = st.number_input(
            "CGPA", 
            value=float(student.get("CGPA") or 0.0), 
            min_value=0.0, max_value=10.0, step=0.1
        )

        if st.button("Update Profile"):
            run_commit("""
                UPDATE STUDENT
                SET First_Name=%s, Last_Name=%s, Email=%s, Phone=%s, CGPA=%s
                WHERE Student_ID=%s
            """, (fname, lname, email, phone, cgpa, student["Student_ID"]))
            st.success("✅ Profile updated successfully! Please refresh or re-login to see the latest data.")

    st.divider()

    # ---------------- JOB POSTINGS ---------------- #
    st.subheader("💼 Job Postings (eligible first)")

    jobs = run_query("""
        SELECT j.Job_ID, j.Job_Title, j.Salary_Package, j.Minimum_CGPA, j.Location, c.Company_Name
        FROM JOB_POSTING j
        JOIN COMPANY c ON j.Company_ID = c.Company_ID
        ORDER BY j.Salary_Package DESC
    """)

    rows = []
    for j in jobs:
        eligible = student_is_eligible_for_job(student.get("CGPA", 0), j)
        rows.append({
            "Job_ID": j["Job_ID"],
            "Job_Title": j["Job_Title"],
            "Company": j["Company_Name"],
            "Salary": j.get("Salary_Package"),
            "Min_CGPA": j.get("Minimum_CGPA"),
            "Location": j.get("Location"),
            "Eligible": "✅ Yes" if eligible else "❌ No"
        })
    st.dataframe(rows, use_container_width=True)

    st.divider()

    # ---------------- APPLY FOR JOB ---------------- #
    st.subheader("📩 Apply for a Job")
    job_id = st.number_input("Job ID to apply", min_value=1)
    cover = st.text_area("Cover Letter (optional)")
    if st.button("Submit Application"):
        job = run_query("SELECT * FROM JOB_POSTING WHERE Job_ID=%s", (job_id,))
        if not job:
            st.error("❌ Job ID not found.")
        else:
            job = job[0]
            if not student_is_eligible_for_job(student.get("CGPA", 0), job):
                st.warning("⚠️ You do not meet the minimum CGPA. Officer may still review your application.")
            run_commit("""
                INSERT INTO APPLICATION (Student_ID, Job_ID, Application_Date, Application_Status, Cover_Letter)
                VALUES (%s, %s, CURDATE(), %s, %s)
            """, (student["Student_ID"], job_id, "Under Review", cover))
            st.success("✅ Application submitted successfully!")

    st.divider()

    # ---------------- APPLICATIONS ---------------- #
    st.subheader("🧾 My Applications & Interview Info")

    apps = run_query("""
        SELECT a.Application_ID, j.Job_Title, c.Company_Name, 
               a.Application_Date, a.Application_Status
        FROM APPLICATION a
        JOIN JOB_POSTING j ON a.Job_ID = j.Job_ID
        JOIN COMPANY c ON j.Company_ID = c.Company_ID
        WHERE a.Student_ID = %s
        ORDER BY a.Application_Date DESC
    """, (student["Student_ID"],))
    st.dataframe(apps, use_container_width=True)

    st.divider()

    # ---------------- INTERVIEWS ---------------- #
    st.subheader("🗓️ My Interview Rounds")

    interviews = run_query("""
        SELECT i.Interview_ID, j.Job_Title, c.Company_Name,
               i.Interview_Date, i.Interview_Round, i.Result
        FROM INTERVIEW i
        JOIN APPLICATION a ON i.Application_ID = a.Application_ID
        JOIN JOB_POSTING j ON a.Job_ID = j.Job_ID
        JOIN COMPANY c ON j.Company_ID = c.Company_ID
        WHERE a.Student_ID = %s
        ORDER BY i.Interview_Date DESC
    """, (student["Student_ID"],))

    if interviews:
        st.dataframe(interviews, use_container_width=True)

        # determine latest interview result safely
        latest_result = (interviews[0].get("Result") or "").strip().lower()
        st.markdown("---")
        st.markdown("### 📋 Final Status")

        if latest_result in ("selected", "passed", "shortlisted", "placed"):
            st.success("🎉 You have been **shortlisted or placed**! Congratulations!")
        elif latest_result in ("not placed", "rejected", "failed"):
            st.error("❌ You were **not selected** in the latest interview round.")
        elif latest_result in ("pending", "", None):
            st.info("⏳ Your interview result is still **pending**.")
        else:
            st.write(f"🟡 Current status: {interviews[0].get('Result')}")
    else:
        st.info("No interview records found yet.")
