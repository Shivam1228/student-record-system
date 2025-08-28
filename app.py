import streamlit as st
import pandas as pd
import re

# -------------------------
# Global variable
# -------------------------
students = []

# -------------------------
# Validation functions
# -------------------------
def validate_id(student_id):
    return re.fullmatch(r"\d{3}", student_id) is not None

def validate_age(age):
    return re.fullmatch(r"\d{2}", age) is not None

def validate_gender(gender):
    return gender in ["Male", "Female", "Other"]

def validate_grade(grade):
    return re.fullmatch(r"[A-Z]", grade) is not None

# -------------------------
# Functions
# -------------------------
def add_student(student_id, name, age, gender, course, grade):
    global students
    if not validate_id(student_id):
        st.error("❌ ID must be 3 digits (e.g., 101).")
        return
    if not validate_age(age):
        st.error("❌ Age must be 2 digits (e.g., 20).")
        return
    if not validate_gender(gender):
        st.error("❌ Gender must be Male, Female, or Other.")
        return
    if not validate_grade(grade):
        st.error("❌ Grade must be a single capital letter (A–Z).")
        return
    
    students.append([student_id, name, age, gender, course, grade])
    st.success("✅ Student record added successfully!")

def view_students(filter_by=None, value=None):
    global students
    if not students:
        st.warning("⚠️ No student records available.")
        return pd.DataFrame()
    
    df = pd.DataFrame(students, columns=["ID", "Name", "Age", "Gender", "Course", "Grade"])
    
    if filter_by and value:
        df = df[df[filter_by].astype(str).str.contains(value, case=False, na=False)]
    
    return df

def download_data(df, file_type="csv"):
    if file_type == "csv":
        return df.to_csv(index=False).encode("utf-8")
    elif file_type == "excel":
        return df.to_excel("students.xlsx", index=False)

# -------------------------
# Streamlit App
# -------------------------
st.title("🎓 Student Record System")

menu = ["Add Student", "View Records", "Download Records"]
choice = st.sidebar.selectbox("📌 Menu", menu)

if choice == "Add Student":
    st.subheader("➕ Add Student Record")
    student_id = st.text_input("Student ID (3 digits)")
    name = st.text_input("Full Name")
    age = st.text_input("Age (2 digits)")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    course = st.text_input("Course")
    grade = st.text_input("Grade (Capital Letter)")
    
    if st.button("Add Record"):
        add_student(student_id, name, age, gender, course, grade)

elif choice == "View Records":
    st.subheader("📖 View Student Records")
    
    filter_option = st.selectbox("Filter By", ["None", "ID", "Name", "Course", "Grade"])
    filter_value = ""
    if filter_option != "None":
        filter_value = st.text_input(f"Enter {filter_option}")
    
    df = view_students(None if filter_option == "None" else filter_option, filter_value)
    
    if not df.empty:
        st.dataframe(df)

elif choice == "Download Records":
    st.subheader("💾 Download Student Records")
    df = view_students()
    if not df.empty:
        file_type = st.radio("Select File Type", ["CSV", "Excel"])
        
        if file_type == "CSV":
            st.download_button("Download CSV", download_data(df, "csv"), "students.csv", "text/csv")
        elif file_type == "Excel":
            st.download_button("Download Excel", df.to_excel(index=False), "students.xlsx")
    else:
        st.warning("⚠️ No records to download.")
