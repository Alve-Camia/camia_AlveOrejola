# camia_AlveOrejola
# Project Title: APACE: Assistive Project Attendance Considering Efficiency
## Project Description
### Purpose

The purpose of APACE is mainly to assist/help with the efficiency of the current attendance system methods observed on the campus. Specifically, the system aims to reduce the time and effort of manual/traditional and QR-based systems.

> [!NOTE]
The project's attendance system is neither intended to be a complete nor a full replacement for the campus's current attendance system. The attendance system is intended to be a supportive/assistive tool in this context.
---

### Problems/Issues with current system/s:

• Manual attendance: Time-consuming for checking attendance. Slow, labor-intensive, prone to errors in records.

• QR-based Attendance: Can only handle one student per terminal, resulting in possible scalability issues for hundreds of students.

### Proposed Solution

From the teachers' point of view:

• For handling class attendance, provide a tool for the teacher to record attendance digitally (By providing the list of students of the class and only asking for updates on punctuality for exceptions to "Present" status)

• Allow exporting of attendance data into a CSV (Comma Separated Values) file, allowing ease of attendance records compilation and data portability.

From the students' point of view:

• Provide the students with the list of their attendance records, which includes the date, subject, punctuality status, and cutting/tardy minutes (if applicable). This allows transparency of the students' attendance records.

### Goals

• Allow teachers to record attendance sessions through exception-based inputs for student punctuality.

• Provide a transparent and assistive attendance tool that may help with the current limitations of traditional and semi-automated attendance systems.

---

## Features

• Sign up, Login, Logout feature (Account Authentication)

• Role-based system attendance (Teachers, Students)

• Attendance features: Create Attendance, Attendance Dashboard.

• Data export of attendance records to CSV (Comma Separated Values)
 
• Pop-up messages for user actions in connection with event-driven GUI

---

## How to run the program
1. **Check installation**:

Windows (Command Prompt):
```
python --version 
python -m tkinter
pip show bcrypt
pip show tkcalendar
python -m pip install pandas
```

macOS / Linux (Terminal):

```
python3 --version
python3 -m tkinter
python3 -c "import bcrypt"
pip3 show tkcalendar
python -m pip install pandas
```

Required Installations:

• Python

Minimum: Python 3.9, Recommended: Python 3.11/3.12.

Download: [Python.org](https://www.python.org).

Additional Dependencies:

• tkinter

• bcrypt

• tkCalendar


---

2. Install missing libraries (Skip if there are no missing libraries)

> [!NOTE]
> In most cases, Tkinter is included in Python installation. However, many Linux distributions do not include Tkinter by default.

Command Prompt (Windows): 
```
pip install tkinter
pip install bcrypt
pip install tkcalendar
pip install pandas
``` 

macOS Terminal: 
```
brew install python-tk
pip3 install bcrypt
pip3 install tkcalendar 
pip3 install pandas
```
> [!NOTE]
> The last two lines can also work for the Linux Terminal.

Linux Terminal:
[Installation Instructions for Tkinter, bcrypt](https://docs.google.com/document/d/17NBHcRPlcBNnfrOUJptSqRkywimTyfhTTs4cq2rRGXs/edit?usp=sharing)

---

3. Download the zip file of this GitHub repository. Ensure that you have extracted the file/s from the .zip (e.g, through WinRAR) 
<img width="930" height="418" alt="image" src="https://github.com/user-attachments/assets/68c0cb73-8f24-4e0e-acb9-f9e0095f4956" />

---

4. Move the attendance_app folder outside the camia_AlveOrejola and onto the desktop directory.
<img width="964" height="595" alt="image" src="https://github.com/user-attachments/assets/a9d65e22-2e12-4452-9afd-72ba892f0f37" />


5. Open a command or terminal and type the following command. Ensure that the current directory you're in is the desktop:

`C:\Directory\Other Directory\Desktop>python -m attendance_app.main`

6. Follow the on-screen instructions to enter login authentication, options for attendance, etc.

## Example Output:
### Logged Out Menu:
<img width="796" height="624" alt="image" src="https://github.com/user-attachments/assets/8445048b-a9e3-4b63-a2a6-f03e5c78bdc2" />

### Login Page:
<img width="782" height="678" alt="image" src="https://github.com/user-attachments/assets/b17be453-9111-49a5-9fbb-7bc2691a5494" />

### Main Menu Page (Logged in):
<img width="781" height="661" alt="image" src="https://github.com/user-attachments/assets/0baf5a57-f676-4a63-b80a-2c75b9332989" />

### Attendance Dashboard:
<img width="786" height="683" alt="image" src="https://github.com/user-attachments/assets/af69f718-a485-4795-9b3d-6a746e77b2d2" />

### Attendance Marking Menu Example:
<img width="804" height="700" alt="image" src="https://github.com/user-attachments/assets/533734d1-5289-4482-a134-d422ff7436a2" />

### Attendance Export:
<img width="794" height="701" alt="image" src="https://github.com/user-attachments/assets/eef2d312-1db6-477f-8ecb-299ed03a2f24" />

### Logging Out:
<img width="806" height="687" alt="image" src="https://github.com/user-attachments/assets/a8e45109-a8f2-4341-97e7-f06954645f8a" />


## Contributors
- Student 1: Gabriel Aaron L. Alve (Draft Proposal, Flowchart, Updates in Code and Documentation)
- Student 2: Claire L. Orejola (README, Initial Code of the Project)
