import streamlit as st
import pandas as pd
import io

# Global list to store student records
students = []

# --- Input Validation Functions ---
def validate_student_id(student_id):
    return student_id.isdigit() and len(student_id) == 3

def validate_age(age):
    return age.isdigit() and len(age) <= 2

def validate_gender(gender):
    return gender.lower() in ["male", "female", "others"]

def validate_grade(grade):
    return grade.isalpha() and grade.isupper() and len(grade) == 1


# --- Add Student Function ---
def add_student():
    st.subheader("➕ Add New Student")

    student_id = st.text_input("Enter Student ID (3 digits)")
    name = st.text_input("Enter Student Name")
    age = st.text_input("Enter Age (2 digits)")
    gender = st.selectbox("Select Gender", ["Male", "Female", "Others"])
    course = st.text_input("Enter Course Name")
    grade = st.text_input("Enter Grade (A/B/C etc., CAPITAL only)", max_chars=1)

    if st.button("Add Student"):
        if not validate_student_id(student_id):
            st.error("❌ Student ID must be 3 digits only")
        elif not validate_age(age):
            st.error("❌ Age must be 1 or 2 digit number")
        elif not validate_gender(gender):
            st.error("❌ Gender must be Male, Female, or Others")
        elif not validate_grade(grade):
            st.error("❌ Grade must be a single uppercase letter")
        elif any(s["ID"] == student_id for s in students):
            st.error("❌ Student ID already exists!")
        else:
            student = {
                "ID": student_id,
                "Name": name,
                "Age": age,
                "Gender": gender,
                "Course": course,
                "Grade": grade,
            }
            students.append(student)
            st.success(f"✅ Student {name} added successfully!")


# --- View Students Function ---
def view_students():
    st.subheader("📋 View Student Records")

    if not students:
        st.warning("No records found.")
        return

    df = pd.DataFrame(students)

    filter_option = st.selectbox("Filter by:", ["All", "ID", "Course", "Name"])

    if filter_option == "ID":
        sid = st.text_input("Enter Student ID to search")
        if sid:
            df = df[df["ID"] == sid]

    elif filter_option == "Course":
        course = st.text_input("Enter Course Name to search")
        if course:
            df = df[df["Course"].str.lower() == course.lower()]

    elif filter_option == "Name":
        name = st.text_input("Enter Student Name to search")
        if name:
            df = df[df["Name"].str.lower() == name.lower()]

    st.dataframe(df)

    # --- Download Options ---
    if not df.empty:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="students.csv",
            mime="text/csv",
        )

        output = io.BytesIO()
        df.to_excel(output, index=False, engine="openpyxl")
        st.download_button(
            label="⬇️ Download Excel",
            data=output.getvalue(),
            file_name="students.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


# --- Update Student Function ---
def update_student():
    st.subheader("✏️ Update Student Record")

    if not students:
        st.warning("No records to update.")
        return

    ids = [s["ID"] for s in students]
    selected_id = st.selectbox("Select Student ID", ids)

    student = next(s for s in students if s["ID"] == selected_id)

    new_name = st.text_input("Update Name", student["Name"])
    new_age = st.text_input("Update Age", student["Age"])
    new_gender = st.selectbox("Update Gender", ["Male", "Female", "Others"], index=["Male", "Female", "Others"].index(student["Gender"]))
    new_course = st.text_input("Update Course", student["Course"])
    new_grade = st.text_input("Update Grade (A/B/C etc.)", student["Grade"], max_chars=1)

    if st.button("Update"):
        if not validate_age(new_age):
            st.error("❌ Age must be 1 or 2 digit number")
        elif not validate_grade(new_grade):
            st.error("❌ Grade must be a single uppercase letter")
        else:
            student["Name"] = new_name
            student["Age"] = new_age
            student["Gender"] = new_gender
            student["Course"] = new_course
            student["Grade"] = new_grade
            st.success(f"✅ Student {selected_id} updated successfully!")


# --- Delete Student Function ---
def delete_student():
    st.subheader("🗑️ Delete Student Record")

    if not students:
        st.warning("No records to delete.")
        return

    ids = [s["ID"] for s in students]
    selected_id = st.selectbox("Select Student ID to Delete", ids)

    if st.button("Delete"):
        global students
        students = [s for s in students if s["ID"] != selected_id]
        st.success(f"✅ Student {selected_id} deleted successfully!")


# --- Main App ---
def main():
    st.title("🎓 Student Record Management System")

    menu = ["Add Student", "View Records", "Update Record", "Delete Record"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Student":
        add_student()
    elif choice == "View Records":
        view_students()
    elif choice == "Update Record":
        update_student()
    elif choice == "Delete Record":
        delete_student()


if __name__ == "__main__":
    main()
