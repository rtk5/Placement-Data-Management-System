# 🎓 College Placement Management System

A modern, interactive **Placement Management System** built with **Streamlit** and **MySQL**.  
This project helps colleges manage placement activities efficiently — allowing **students** to apply for jobs, and **placement officers** to manage companies, job postings, interviews, and final placement results.

---

## 🚀 Features

### 🧑‍🎓 Student Portal
- Secure login using **Student ID**, Name, and Phone.
- Edit personal details (name, email, phone, CGPA).
- View all available job postings with **eligibility status** based on CGPA.
- Apply for jobs directly from the dashboard.
- Track application status and interview progress.
- View final **placement status** (Placed / Not Placed / Pending).

### 🧑‍💼 Placement Officer Portal
- Officer login using Email and Password.
- Manage **Companies**: add new companies with contact info.
- Manage **Job Postings**: post new openings, update vacancies, and eligibility criteria.
- Manage **Applications**: view and update student application statuses.
- Manage **Interviews**: schedule and update interview results.
- **Update Placement Results**: mark a student as *Placed* or *Not Placed* manually.
- View all **students and their placement status**.

---

## 🏗️ Project Structure

```
placement_app/
│
├── app.py                  # Entry point, handles login and routing
├── db_connection.py        # MySQL connection and helper functions
├── utils.py                # Utility functions (e.g. eligibility checks)
├── requirements.txt        # Required dependencies
├── README.md               # Documentation
│
└── pages/
    ├── student_portal.py   # Student dashboard
    └── officer_portal.py   # Placement officer dashboard
```

---

## 🧩 Database Schema (MySQL)

**Database Name:** `collegeplacementdb`

**Tables:**

| Table | Description |
|-------|-------------|
| `STUDENT` | Stores student personal info and placement status |
| `COMPANY` | Stores registered companies and details |
| `JOB_POSTING` | Job postings linked to companies |
| `APPLICATION` | Job applications submitted by students |
| `INTERVIEW` | Interview schedules and results |
| `PLACEMENT_OFFICER` | Login details of placement officers |

### Example SQL snippet

```sql
CREATE TABLE STUDENT (
    Student_ID INT PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Email VARCHAR(100),
    Phone VARCHAR(15),
    CGPA FLOAT,
    Placement_Status VARCHAR(50) DEFAULT 'Pending'
);
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/placement_app.git
cd placement_app
```

### 2️⃣ Set up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate    # On macOS/Linux
venv\Scripts\activate       # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Database Connection
Edit your `db_connection.py` file to match your local MySQL setup:

```python
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="collegeplacementdb"
    )
```

### 5️⃣ Run the App
```bash
streamlit run app.py
```

---

## 🔑 Default Login Credentials

### Placement Officer
| Field | Value |
|-------|-------|
| Email | admin@college.com |
| Password | admin123 |

### Student
Students log in using their **Student ID**, **Name**, and **Phone number** from the database.

---

## 💡 Key Functional Highlights
- Role-based access (Student vs. Officer)
- Dynamic SQL queries for CRUD operations
- Real-time updates with Streamlit
- Placement tracking for each student
- Clean, modular structure for easy maintenance
- Error handling for missing data or null values

---

## 🧠 Future Improvements
- Upload and download resume PDFs
- Export placement statistics (CSV/PDF)
- Add email notifications for shortlists
- Integrate data visualization for placement analytics
- Implement authentication security (hashed passwords)

---

## 🖼️ Screenshots (optional)
is in the folder
---

## 🧑‍💻 Tech Stack
- **Frontend/UI:** Streamlit
- **Backend:** Python (Streamlit Server)
- **Database:** MySQL
- **Libraries:** mysql.connector, streamlit, pandas, bcrypt (optional for hashing)

---

## 📜 License
This project is open-source under the MIT License.  
Feel free to use and modify for educational or institutional purposes.

