# add_faces_streamlit.py
import streamlit as st
import cv2
import pickle
import numpy as np
import os

st.title("Face Registration")

# Input fields for name and number
name = st.text_input("Enter your Name:")
phone = st.text_input("Enter your Phone Number:")

# Button to start face capture
if st.button("Add Face"):
    if not name.strip() or not phone.strip():
        st.error("Please enter both Name and Phone Number.")
    else:
        st.info("Starting camera... Press 'q' in the camera window to stop.")
        
        video = cv2.VideoCapture(0)
        facesdetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

        faces_data = []
        i = 0

        while True:
            ret, frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facesdetect.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                crop_img = frame[y:y+h, x:x+w, :]
                resized_img = cv2.resize(crop_img, (50, 50))
                
                if len(faces_data) <= 100 and i % 10 == 0:
                    faces_data.append(resized_img)
                i += 1
                
                cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
            
            cv2.imshow("Face Capture", frame)
            k = cv2.waitKey(1)
            if k == ord('q') or len(faces_data) == 100:
                break

        video.release()
        cv2.destroyAllWindows()

        faces_data = np.asarray(faces_data)
        faces_data = faces_data.reshape(100, -1)

        # Save names
        if 'names.pkl' not in os.listdir('data/'):
            names = [name] * 100
            with open('data/names.pkl', 'wb') as f:
                pickle.dump(names, f)
        else:
            with open('data/names.pkl', 'rb') as f:
                names = pickle.load(f)
            names = names + [name] * 100
            with open('data/names.pkl', 'wb') as f:
                pickle.dump(names, f)

        # Save phone numbers
        if 'phones.pkl' not in os.listdir('data/'):
            phones = [phone] * 100
            with open('data/phones.pkl', 'wb') as f:
                pickle.dump(phones, f)
        else:
            with open('data/phones.pkl', 'rb') as f:
                phones = pickle.load(f)
            phones = phones + [phone] * 100
            with open('data/phones.pkl', 'wb') as f:
                pickle.dump(phones, f)

        # Save faces data
        if 'faces_data.pkl' not in os.listdir('data/'):
            with open('data/faces_data.pkl', 'wb') as f:
                pickle.dump(faces_data, f)
        else:
            with open('data/faces_data.pkl', 'rb') as f:
                faces = pickle.load(f)
            faces = np.append(faces, faces_data, axis=0)
            with open('data/faces_data.pkl', 'wb') as f:
                pickle.dump(faces, f)

        st.success(f"Face data for {name} added successfully!")
