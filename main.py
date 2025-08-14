import streamlit as st
import subprocess
import os
import pickle
import numpy as np
import pandas as pd
import cv2
import time
import csv
import auth  # new import
from datetime import datetime
from twilio.rest import Client
from PIL import Image
from streamlit_autorefresh import st_autorefresh
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet



# If not logged in, show login UI
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    auth.auth_ui()
    st.stop()  # Stop running the rest until logged in
# ------------------ FUNCTIONS ------------------


def send_sms(to_number, message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=message, from_=twilio_number, to=to_number)
    return message.sid

def get_absent_students(total_students, present_students):
    return [student for student in total_students if student not in present_students]

def load_attendance():
    if not os.path.exists("Attendance"):
        os.makedirs("Attendance")
    attendance_files = [f for f in os.listdir("Attendance") if f.endswith('.csv')]
    all_data = []
    for file in attendance_files:
        df = pd.read_csv(f"Attendance/{file}")
        # Ensure necessary columns
        expected_cols = {'NAME', 'TIME', 'Method'}
        missing = expected_cols - set(df.columns)
        for col in missing:
            df[col] = None
        df['Date'] = file.split('_')[1].replace('.csv', '')
        all_data.append(df)
    return pd.concat(all_data, ignore_index=True) if all_data else None


def load_faces_data():
    if (
        os.path.exists('data/faces_data.pkl') and
        os.path.exists('data/names.pkl') and
        os.path.exists('data/phones.pkl')
    ):
        with open('data/faces_data.pkl', 'rb') as f:
            faces_data = pickle.load(f)
        with open('data/names.pkl', 'rb') as f:
            names = pickle.load(f)
        with open('data/phones.pkl', 'rb') as f:
            phones = pickle.load(f)
        return faces_data, names, phones
    return None, None, None

def remove_face(name):
    faces_data, names, phones = load_faces_data()
    if faces_data is not None and names is not None:
        if name in names:
            indices = [i for i, n in enumerate(names) if n == name]
            faces_data = np.delete(faces_data, indices, axis=0)
            names = [n for i, n in enumerate(names) if n != name]
            phones = [p for i, p in enumerate(phones) if names[i] != name]
            with open('data/faces_data.pkl', 'wb') as f:
                pickle.dump(faces_data, f)
            with open('data/names.pkl', 'wb') as f:
                pickle.dump(names, f)
            with open('data/phones.pkl', 'wb') as f:
                pickle.dump(phones, f)
            st.success(f"Removed all entries for {name}")
        else:
            st.error(f"Name {name} not found.")
    else:
        st.error("Faces data not found.")

def mark_present(name):
    ts = time.time()
    timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
    date = datetime.fromtimestamp(ts).strftime("%d-%m-%y")
    attendance = [name, timestamp, "Button"]
    if os.path.exists(f"Attendance/Attendance_{date}.csv"):
        with open(f"Attendance/Attendance_{date}.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(attendance)
    else:
        with open(f"Attendance/Attendance_{date}.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(['NAME', 'TIME', 'Method'])
            writer.writerow(attendance)
    st.success(f"Marked {name} as present.")

def add_face_page():
    st.title("Add New Face")

    # Input fields
    name = st.text_input("Enter Name")
    phone = st.text_input("Enter Phone Number")

    # Take picture from camera
    img_file = st.camera_input("Take a Picture")

    if img_file is not None:
        # Convert image to numpy
        image = Image.open(img_file)
        image_np = np.array(image)

        # Detect and encode faces
        face_encodings = face_recognition.face_encodings(image_np)
        if len(face_encodings) > 0:
            st.success("Face detected successfully!")

            if st.button("Save Face Data"):
                encoding = face_encodings[0]

                # Save encodings and names to pickle
                if os.path.exists("faces.pkl"):
                    with open("faces.pkl", "rb") as f:
                        known_faces = pickle.load(f)
                else:
                    known_faces = {"encodings": [], "names": [], "phones": []}

                known_faces["encodings"].append(encoding)
                known_faces["names"].append(name)
                known_faces["phones"].append(phone)

                with open("faces.pkl", "wb") as f:
                    pickle.dump(known_faces, f)

                st.success(f"Face for {name} saved successfully!")
        else:
            st.error("No face detected. Please try again.")

def save_face_data(name, phone, faces_data):
    """Helper to save face, name, and phone data to pickle files."""
    # Save names
    if 'names.pkl' not in os.listdir('data/'):
        names = [name] * faces_data.shape[0]
    else:
        with open('data/names.pkl', 'rb') as f:
            names = pickle.load(f)
        names += [name] * faces_data.shape[0]
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)

    # Save phones
    if 'phones.pkl' not in os.listdir('data/'):
        phones = [phone] * faces_data.shape[0]
    else:
        with open('data/phones.pkl', 'rb') as f:
            phones = pickle.load(f)
        phones += [phone] * faces_data.shape[0]
    with open('data/phones.pkl', 'wb') as f:
        pickle.dump(phones, f)

    # Save face data
    if 'faces_data.pkl' not in os.listdir('data/'):
        with open('data/faces_data.pkl', 'wb') as f:
            pickle.dump(faces_data, f)
    else:
        with open('data/faces_data.pkl', 'rb') as f:
            existing_faces = pickle.load(f)
        updated_faces = np.append(existing_faces, faces_data, axis=0)
        with open('data/faces_data.pkl', 'wb') as f:
            pickle.dump(updated_faces, f)


def attendance_page():
    df_all_attendance = load_attendance()
    if st.button("🔄 Refresh Data"):
        st.rerun()


    faces_data, names, phones = load_faces_data()

    st.title("Attendance Dashboard")
    st.subheader("(SMS to parents may not work,because i have not used paid Twilio account and now for hosting i have removed the private details for security)")

    st.sidebar.header("Total Classes")
    total_classes = st.sidebar.number_input("Enter Total Number of Classes", min_value=1, value=10)

    # Build student data from names & phones
    student_data = {}
    if names and phones:
        for n, p in zip(names, phones):
            student_data[n] = {"parent_phone": p}

    total_students = list(set(student_data.keys()))  # Unique names

    # Case 1: No attendance data but have faces
    if df_all_attendance is None:
        if total_students:
            st.warning("No attendance records found. You can start taking attendance.")
            df_all_attendance = pd.DataFrame(columns=['NAME', 'TIME', 'Date', 'Method'])
        else:
            st.error("No face data and no attendance data found.")
            return

    # Ensure 'Method' column exists
    if 'Method' not in df_all_attendance.columns:
        df_all_attendance['Method'] = np.nan  

    st.subheader("Attendance Records")
    st.dataframe(df_all_attendance[['NAME', 'TIME', 'Date', 'Method']])

    # Find absent students for today
    present_students = df_all_attendance[
        df_all_attendance['Date'] == datetime.now().strftime("%d-%m-%y")
    ]["NAME"].unique().tolist()
    absent_students = get_absent_students(total_students, present_students)

    st.subheader("Individual Attendance Percentage")
    attendance_summary = []
    for name in total_students:
        attendance_count = df_all_attendance[df_all_attendance["NAME"] == name].shape[0]
        attendance_percentage = (attendance_count / total_classes) * 100
        attendance_summary.append({
            "Name": name,
            "Attendance Count": attendance_count,
            "Attendance Percentage": attendance_percentage
        })
    attendance_df = pd.DataFrame(attendance_summary)

    if not attendance_df.empty and all(col in attendance_df.columns for col in ['Name', 'Attendance Count', 'Attendance Percentage']):
        st.table(attendance_df[['Name', 'Attendance Count', 'Attendance Percentage']])
    else:
        st.warning("No attendance summary available yet.")
        st.table(pd.DataFrame(columns=['Name', 'Attendance Count', 'Attendance Percentage']))

# CSV download
    csv = attendance_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Attendance Summary (CSV)",
        data=csv,
        file_name="attendance_summary.csv",
        mime="text/csv"
    )
    # Excel download
    excel_buffer = BytesIO()
    attendance_df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    st.download_button(
        label="📥 Download Attendance Summary (Excel)",
        data=excel_buffer,
        file_name="attendance_summary.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # PDF download (simple table)


    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Add a title
    elements.append(Paragraph("Attendance Summary", styles['Title']))

    # Convert DataFrame to list for Table
    # Convert DataFrame to list for Table (always include header row)
    data_for_pdf = [["Name", "Attendance Count", "Attendance Percentage"]]

    if not attendance_df.empty:
        for index, row in attendance_df.iterrows():
            data_for_pdf.append([
                row['Name'],
                row['Attendance Count'],
                row['Attendance Percentage']
            ])

    table = Table(data_for_pdf)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)

    doc.build(elements)
    pdf_buffer.seek(0)

    st.download_button(
        label="📄 Download Attendance Summary (PDF)",
        data=pdf_buffer,
        file_name="attendance_summary.pdf",
        mime="application/pdf"
    )

    st.sidebar.header("Admin Actions")
    remove_name = st.sidebar.text_input("Enter name to remove")
    if st.sidebar.button("Remove Face"):
        if remove_name:
            remove_face(remove_name)
        else:
            st.sidebar.error("Please enter a name.")

    st.subheader("Absent Students")
    for student in absent_students:
        col1, col2 = st.columns([2, 1])
        col1.write(student)
        if col2.button(f"Mark {student} Present"):
            mark_present(student)
            st.rerun()  # instantly refresh the page to update table


    if st.sidebar.button("Send SMS to Parents"):
        if absent_students:
            for student in absent_students:
                parent_phone = student_data.get(student, {}).get("parent_phone")
                if parent_phone:
                    sms_message = f"Dear Parent, your child {student} was absent today."
                    try:
                        sms_sid = send_sms(parent_phone, sms_message)
                        st.success(f"SMS sent to parent of {student} (SID: {sms_sid})")
                    except Exception as e:
                        st.error(f"Failed to send SMS to parent of {student}: {e}")
                else:
                    st.error(f"No phone number found for {student}")
        else:
            st.info("No absent students to notify.")

    st.sidebar.header("Take Attendance")
    if st.sidebar.button("Take Attendance (Face Recognition)"):
        try:
            subprocess.Popen(['python', 'test.py'])
            st.sidebar.success("Attendance is being taken via face recognition...")
        except Exception as e:
            st.sidebar.error(f"Failed to take attendance: {e}")


# ------------------ MAIN ------------------
page = st.sidebar.selectbox("Navigation", ["Add Face", "Attendance"])
if page == "Add Face":
    add_face_page()
elif page == "Attendance":
    attendance_page()
if st.sidebar.button("Logout"):
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.rerun() 
