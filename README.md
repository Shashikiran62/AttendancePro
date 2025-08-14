Attendance Pro
Attendance Pro is a facial recognition-based attendance management system built with Python, Streamlit, and OpenCV. It allows users to register faces, take attendance using facial recognition, track attendance records, and generate reports in CSV, Excel, and PDF formats. The system also includes user authentication and optional SMS notifications for absent students (Twilio integration is included but requires a paid account for full functionality). This project is ideal for educational institutions or organizations looking to automate attendance tracking with a modern, user-friendly interface.
Features

Face Registration: Capture and store face data for attendance purposes.
Facial Recognition Attendance: Automatically detect and mark attendance using a webcam and KNN-based classification.
Attendance Dashboard: View real-time attendance records, including attendance percentages and absent students.
Report Generation: Download attendance summaries in CSV, Excel, and PDF formats.
User Authentication: Secure login and signup system with password hashing using bcrypt.
Admin Actions: Remove registered faces and manually mark students as present.
SMS Notifications: Send absence alerts to parents (requires a paid Twilio account; currently disabled for security in the demo).
Responsive UI: Built with Streamlit for an intuitive and interactive web interface.

Prerequisites
Before running the project, ensure you have the following installed:

Python 3.8 or higher
A webcam for face capture and recognition
Required Python packages (listed in requirements.txt)

Installation

Clone the Repository:
git clone https://github.com/your-username/attendance-pro.git
cd attendance-pro


Install Dependencies:Install the required Python packages using:
pip install -r requirements.txt


Directory Setup:Ensure the following directories exist in the project root:

data/: Stores face data (faces_data.pkl), names (names.pkl), and phone numbers (phones.pkl).
Attendance/: Stores attendance records in CSV format (e.g., Attendance_DD-MM-YY.csv).Create these directories if they don't exist:

mkdir data Attendance


Download Haar Cascade:Ensure the haarcascade_frontalface_default.xml file is present in the data/ directory. You can download it from the OpenCV GitHub repository.


Usage

Run the Application:Start the Streamlit app to access the main interface:
streamlit run main.py


Navigation:

Add Face: Register a new user by providing a name and phone number, then capture face data using a webcam.
Attendance: View attendance records, download reports, mark students present manually, or take attendance via facial recognition.
Authentication: Sign up or log in to access the system. Login logs are stored in login_logs.csv.


Take Attendance via Face Recognition:

From the sidebar, click "Take Attendance (Face Recognition)" to launch the facial recognition script (test.py).
Press o to save attendance to a CSV file.
Press q to exit the face recognition window.


Download Reports:

On the Attendance page, download attendance summaries in CSV, Excel, or PDF formats.



Project Structure
attendance-pro/
├── data/
│   ├── haarcascade_frontalface_default.xml  # Haar cascade for face detection
│   ├── faces_data.pkl                      # Stored face data
│   ├── names.pkl                           # Stored names
│   └── phones.pkl                          # Stored phone numbers
├── Attendance/
│   └── Attendance_DD-MM-YY.csv             # Attendance records
├── add_faces_streamlit.py                  # Script for face registration
├── test.py                                 # Script for facial recognition attendance
├── main.py                                 # Main Streamlit app
├── auth.py                                 # Authentication module
├── login_logs.csv                          # Login history
├── requirements.txt                        # Python dependencies
├── background.png                          # Background image for face recognition
└── README.md                               # Project documentation

Dependencies
The project uses the following Python packages (see requirements.txt):

streamlit: Web app framework
opencv-python: Computer vision for face detection and recognition
numpy: Numerical computations
pandas: Data manipulation and report generation
twilio: SMS notifications (optional, requires a paid account)
streamlit-autorefresh: Auto-refresh for real-time updates
reportlab: PDF report generation
openpyxl: Excel report generation
bcrypt: Password hashing for authentication
pywin32: Text-to-speech for attendance confirmation (Windows only)

Install them using:
pip install -r requirements.txt

Notes

Twilio SMS: The SMS feature is included but disabled in the demo for security reasons (private credentials removed). To enable it, configure your Twilio account SID, auth token, and phone number in main.py.
Windows Dependency: The test.py script uses pywin32 for text-to-speech, which is Windows-specific. For non-Windows systems, remove or replace the Speak function.
Face Data Storage: Each registered face generates 100 samples stored in faces_data.pkl, names.pkl, and phones.pkl.
Performance: Ensure sufficient lighting and clear webcam input for accurate face detection.

Limitations

The facial recognition system uses a simple KNN classifier, which may not be highly accurate in complex scenarios. Consider upgrading to a deep learning-based model for better performance.
The SMS feature requires a paid Twilio account and is disabled in the demo.
The text-to-speech feature in test.py is Windows-specific.

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

OpenCV for face detection and image processing.
Streamlit for the web interface.
Twilio for SMS integration.
ReportLab for PDF generation.


For issues or feature requests, please open an issue on the GitHub repository.
