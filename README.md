# 📸 Attendance Pro

**Attendance Pro** is a **facial recognition-based attendance management system** built with **Python**, **Streamlit**, and **OpenCV**.  
It allows users to **register faces**, take **attendance using facial recognition**, track attendance records, and generate reports in **CSV**, **Excel**, and **PDF** formats.  
The system also includes **user authentication** and optional **SMS notifications** for absent students *(Twilio integration — requires a paid account)*.  

> Ideal for educational institutions or organizations looking to **automate attendance tracking** with a modern, user-friendly interface.

---

## ✨ Features

- 🖼 **Face Registration** – Capture and store face data for attendance.
- 🎯 **Facial Recognition Attendance** – Automatically detect and mark attendance using a webcam and **KNN-based classification**.
- 📊 **Attendance Dashboard** – View real-time attendance, percentages, and absent student lists.
- 📥 **Report Generation** – Download attendance summaries in **CSV**, **Excel**, or **PDF** formats.
- 🔒 **User Authentication** – Secure login & signup system with **bcrypt password hashing**.
- 🛠 **Admin Actions** – Remove registered faces, manually mark students present.
- 📲 **SMS Notifications** – Send absence alerts to parents *(Twilio API — paid account)*.
- 💻 **Responsive UI** – Built with **Streamlit** for an intuitive experience.

---

## 📋 Prerequisites

- **Python** ≥ 3.8
- **Webcam** for face capture & recognition
- **Required Python packages** (see `requirements.txt`)

---

## ⚙️ Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/attendance-pro.git
   cd attendance-pro
2. **Install Dependencies**
   ```bash
    pip install -r requirements.txt

3.**Directory Setup**
      Make sure these folders exist in the root.
      
4.**Download Haar Cascade from OpenCV GitHub**
    ```haarcascade_frontalface_default.xml```


---

##Start the App🚀
```streamlit run main.py```

---

##⚠️ Notes
1.Twilio SMS – Disabled by default for security (requires paid account).
2.Windows-only TTS – test.py uses pywin32 for speech; remove or replace for other OS.
3.Face Data – Each registered face creates 100 samples saved in .pkl files.
4.Lighting & Camera Quality – Directly affect recognition accuracy.

---

##🚫 Limitations
1.Uses a simple KNN classifier — accuracy may be limited; consider upgrading to deep learning for production.
2.SMS notifications require paid Twilio account.
3.TTS feature is Windows-specific.

---

##🙏 Acknowledgments
1.OpenCV – Face detection & image processing
2.Streamlit – Web interface
3.Twilio – SMS integration
4.ReportLab – PDF generation
