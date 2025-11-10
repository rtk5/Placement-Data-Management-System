# db_connection.py
import mysql.connector
import streamlit as st

# Update these credentials if needed
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "kali",
    "database": "collegeplacementdb",
    "port": 3306,
    "autocommit": False,
}

def get_connection():
    """
    Create and return a new MySQL connection object.
    We open a fresh connection for each operation to avoid stale connections
    when Streamlit hot-reloads.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        # show friendly error in Streamlit UI and stop execution
        st.error(f"Database connection failed: {e}")
        return None

def run_query(query, params=None):
    """
    Executes SELECT queries and returns list of dicts.
    """
    conn = get_connection()
    if not conn:
        st.stop()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        results = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return results

def run_commit(query, params=None):
    """
    Executes INSERT/UPDATE/DELETE and commits.
    """
    conn = get_connection()
    if not conn:
        st.stop()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        conn.commit()
    finally:
        cursor.close()
        conn.close()
