# pages/officer_portal.py
import streamlit as st
from db_connection import run_query, run_commit

def show_officer_portal(officer):
    st.header("🧑‍💼 Placement Officer Dashboard")
    st.markdown(f"**Welcome, {officer.get('Officer_Name', officer.get('Email','Officer'))}**")

    tabs = st.tabs(["Companies", "Job Postings", "Applications", "Interviews", "Students"])

    # ---------------- COMPANIES TAB ---------------- #
    with tabs[0]:
        st.subheader("🏢 Companies")
        companies = run_query("SELECT * FROM COMPANY ORDER BY Company_ID")
        st.dataframe(companies, use_container_width=True)

        with st.expander("➕ Add New Company"):
            name = st.text_input("Company Name", key="comp_name")
            ctype = st.text_input("Company Type", key="comp_type")
            phone = st.text_input("Phone", key="comp_phone")
            industry = st.text_input("Industry Type", key="comp_ind")
            email = st.text_input("Email", key="comp_email")
            website = st.text_input("Website", key="comp_web")
            address = st.text_area("Address", key="comp_addr")
            if st.button("Add Company"):
                run_commit("""
                    INSERT INTO COMPANY (Company_Name, Company_Type, Phone, Industry_Type, Email, Website, Address)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, (name, ctype, phone, industry, email, website, address))
                st.success("✅ Company added successfully.")

    # ---------------- JOB POSTINGS TAB ---------------- #
    with tabs[1]:
        st.subheader("💼 Job Postings")
        jobs = run_query("""
            SELECT j.Job_ID, j.Job_Title, c.Company_Name, j.Salary_Package, j.Location,
                   j.Minimum_CGPA, j.Application_Deadline
            FROM JOB_POSTING j
            JOIN COMPANY c ON j.Company_ID = c.Company_ID
            ORDER BY j.Job_ID DESC
        """)
        st.dataframe(jobs, use_container_width=True)

        with st.expander("➕ Post New Job"):
            company_id = st.number_input("Company ID", min_value=1, key="new_job_company")
            title = st.text_input("Job Title", key="new_job_title")
            desc = st.text_area("Description", key="new_job_desc")
            salary = st.number_input("Salary Package", min_value=0.0, key="new_job_salary")
            loc = st.text_input("Location", key="new_job_loc")
            min_cgpa = st.number_input("Minimum CGPA", min_value=0.0, max_value=10.0, step=0.1, key="new_job_min_cgpa")
            deadline = st.date_input("Application Deadline", key="new_job_deadline")
            vacancies = st.number_input("Number of Positions", min_value=1, key="new_job_vacancies")
            if st.button("Post Job"):
                run_commit("""
                    INSERT INTO JOB_POSTING (Company_ID, Job_Title, Job_Description, Salary_Package,
                                             Location, Minimum_CGPA, Application_Deadline, Number_of_Positions)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (company_id, title, desc, salary, loc, min_cgpa, deadline, vacancies))
                st.success("✅ Job posted successfully.")

    # ---------------- APPLICATIONS TAB ---------------- #
    with tabs[2]:
        st.subheader("📋 Applications")
        apps = run_query("""
            SELECT a.Application_ID, s.Student_ID, s.First_Name, s.Last_Name, j.Job_Title, 
                   c.Company_Name, a.Application_Date, a.Application_Status
            FROM APPLICATION a
            JOIN STUDENT s ON a.Student_ID = s.Student_ID
            JOIN JOB_POSTING j ON a.Job_ID = j.Job_ID
            JOIN COMPANY c ON j.Company_ID = c.Company_ID
            ORDER BY a.Application_Date DESC
        """)
        st.dataframe(apps, use_container_width=True)

        st.markdown("### ✏️ Update Application Status")
        app_id = st.number_input("Application ID", min_value=1, key="update_app_id")
        new_status = st.selectbox("New Status", 
                                  ["Under Review", "Shortlisted", "Interview Scheduled", "Selected", "Rejected"],
                                  key="update_app_status")
        if st.button("Update Status"):
            run_commit("UPDATE APPLICATION SET Application_Status=%s WHERE Application_ID=%s", 
                       (new_status, app_id))
            st.success("✅ Application status updated successfully.")

    # ---------------- INTERVIEWS TAB ---------------- #
    with tabs[3]:
        st.subheader("🗓 Interviews")

        interviews = run_query("""
            SELECT i.Interview_ID, a.Application_ID, s.Student_ID, s.First_Name, s.Last_Name,
                   j.Job_Title, c.Company_Name, i.Interview_Date, i.Interview_Round, i.Result
            FROM INTERVIEW i
            JOIN APPLICATION a ON i.Application_ID = a.Application_ID
            JOIN STUDENT s ON a.Student_ID = s.Student_ID
            JOIN JOB_POSTING j ON a.Job_ID = j.Job_ID
            JOIN COMPANY c ON j.Company_ID = c.Company_ID
            ORDER BY i.Interview_Date DESC
        """)
        st.dataframe(interviews, use_container_width=True)

        with st.expander("➕ Schedule New Interview"):
            app_id = st.number_input("Application ID", min_value=1, key="sch_app_id")
            date = st.date_input("Interview Date", key="sch_date")
            round_name = st.text_input("Round (e.g. HR, Tech)", key="sch_round")
            result = st.selectbox("Initial Result", ["Pending", "Shortlisted", "Selected", "Rejected"], key="sch_result")
            if st.button("Schedule Interview"):
                run_commit("""
                    INSERT INTO INTERVIEW (Application_ID, Interview_Date, Interview_Round, Result)
                    VALUES (%s,%s,%s,%s)
                """, (app_id, date, round_name, result))
                run_commit("UPDATE APPLICATION SET Application_Status=%s WHERE Application_ID=%s", 
                           ("Interview Scheduled", app_id))
                st.success("✅ Interview scheduled successfully.")

        st.markdown("---")
        st.subheader("🔄 Update Interview Result")
        int_id = st.number_input("Interview ID", min_value=1, key="upd_int_id")
        new_result = st.selectbox("Set Result", ["Pending", "Shortlisted", "Selected", "Rejected"], key="upd_result")
        if st.button("Update Interview Result"):
            run_commit("UPDATE INTERVIEW SET Result=%s WHERE Interview_ID=%s", (new_result, int_id))
            run_commit("""
                UPDATE APPLICATION
                SET Application_Status = %s
                WHERE Application_ID = (SELECT Application_ID FROM INTERVIEW WHERE Interview_ID=%s)
            """, (new_result, int_id))
            st.success(f"✅ Interview #{int_id} updated to '{new_result}'.")

        # ---------------- MANUAL STUDENT PLACEMENT RESULT ---------------- #
        st.markdown("---")
        st.subheader("🎯 Update Student Placement Result")

        student_id = st.number_input("Enter Student ID", min_value=1, key="place_student_id")
        if st.button("Fetch Student Interviews"):
            interviews = run_query("""
                SELECT i.Interview_ID, j.Job_Title, c.Company_Name, i.Interview_Date, i.Result
                FROM INTERVIEW i
                JOIN APPLICATION a ON i.Application_ID = a.Application_ID
                JOIN JOB_POSTING j ON a.Job_ID = j.Job_ID
                JOIN COMPANY c ON j.Company_ID = c.Company_ID
                WHERE a.Student_ID = %s
                ORDER BY i.Interview_Date DESC
            """, (student_id,))

            if interviews:
                st.write("### Student’s Interview History")
                st.dataframe(interviews, use_container_width=True)

                interview_ids = [str(i["Interview_ID"]) for i in interviews]
                chosen_interview = st.selectbox("Select Interview ID to mark placement result", interview_ids)
                final_result = st.selectbox("Set Final Result", ["Placed", "Not Placed", "Pending"])

                if st.button("Update Placement Result"):
                    # Update interview result
                    run_commit("UPDATE INTERVIEW SET Result=%s WHERE Interview_ID=%s", (final_result, chosen_interview))

                    # Update related application
                    app_id_row = run_query("SELECT Application_ID FROM INTERVIEW WHERE Interview_ID=%s", (chosen_interview,))
                    if app_id_row:
                        app_id = app_id_row[0]["Application_ID"]
                        status = "Placed" if final_result == "Placed" else "Not Selected" if final_result == "Not Placed" else "Under Review"
                        run_commit("UPDATE APPLICATION SET Application_Status=%s WHERE Application_ID=%s", (status, app_id))
                        # Update student's placement status
                        try:
                            run_commit("ALTER TABLE STUDENT ADD COLUMN IF NOT EXISTS Placement_Status VARCHAR(50)")
                        except Exception:
                            pass
                        run_commit("UPDATE STUDENT SET Placement_Status=%s WHERE Student_ID=%s", (final_result, student_id))
                        st.success(f"✅ Student #{student_id} marked as '{final_result}' for Interview #{chosen_interview}.")
                    else:
                        st.warning("⚠️ Could not find application linked to this interview.")
            else:
                st.info("No interviews found for that student.")

    # ---------------- STUDENTS TAB ---------------- #
    with tabs[4]:
        st.subheader("🎓 Students")
        students = run_query("""
            SELECT Student_ID, First_Name, Last_Name, Email, Phone, CGPA, Placement_Status
            FROM STUDENT ORDER BY Student_ID
        """)
        st.dataframe(students, use_container_width=True)

        st.markdown("### 🔍 View Detailed Student Profile")
        student_id = st.number_input("Enter Student ID", min_value=1, key="view_student_id")
        if st.button("Get Student Details"):
            rows = run_query("SELECT * FROM STUDENT WHERE Student_ID=%s", (student_id,))
            if rows:
                st.json(rows[0])
            else:
                st.warning("⚠️ Student not found.")
