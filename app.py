# app.py - main entry file
import streamlit as st
from utils import get_student_by_login, get_officer_by_login

st.set_page_config(page_title="Placement Portal", layout="wide")

if "role" not in st.session_state:
    st.session_state.role = None
if "user" not in st.session_state:
    st.session_state.user = None

st.title("🎓 College Placement Management System")

def logout():
    st.session_state.role = None
    st.session_state.user = None
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


if st.session_state.role is None:
    st.sidebar.info("Login to continue")
    role = st.sidebar.selectbox("Login as", ["Student", "Placement Officer"])
    if role == "Student":
        st.header("🔐 Student Login")
        student_id = st.text_input("Student ID")
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        if st.button("Login as Student"):
            if not (student_id and name and phone):
                st.error("Please provide Student ID, Name and Phone.")
            else:
                user = get_student_by_login(student_id, name, phone)
                if user:
                    st.session_state.role = "Student"
                    st.session_state.user = user
                    st.success("Logged in as student.")
                    if hasattr(st, "rerun"):
                        st.rerun()
                    else:
                        st.experimental_rerun()

                else:
                    st.error("Invalid student credentials.")
    else:
        st.header("🧑‍💼 Placement Officer Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login as Officer"):
            if not (email and password):
                st.error("Enter email and password.")
            else:
                user = get_officer_by_login(email, password)
                if user:
                    st.session_state.role = "Officer"
                    st.session_state.user = user
                    st.success("Logged in as officer.")
                    if hasattr(st, "rerun"):
                        st.rerun()
                    else:
                        st.experimental_rerun()

                else:
                    st.error("Invalid officer credentials.")
else:
    user = st.session_state.user
    role = st.session_state.role
    st.sidebar.success(f"{role} logged in")
    if st.sidebar.button("Logout"):
        logout()

    # route to pages
    if role == "Student":
        from pages.student_portal import show_student_portal
        show_student_portal(user)
    else:
        from pages.officer_portal import show_officer_portal
        show_officer_portal(user)
