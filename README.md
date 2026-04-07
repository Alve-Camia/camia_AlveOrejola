# camia_AlveOrejola
# Project Title: APACE: Assistive Project Attendance Considering Efficiency
## Project Description
### Purpose

The purpose of APACE is to mainly be able to assist/help with the efficiency of the current attendance system methods observed in the campus. Specifically, the systems aims to reduce time ane effort of manual/traditional and QR-based systems.

> [!NOTE]
> The project's attendance system is neither intended to be a complete nor full replacement of the current attendance system of the campus. The attendance system is intented to be a supportive/assisstive tool in this said context.
---

### Problems/Issues with curent system/s:

• Manual attendance: Time-consuming for checking attendance. Slow, labor-intensive, prone to errors in records.

• QR-based Attendance: Can only handle one student per terminaal, resulting in possible scalability issues for hundreds of students.

### Proposed Solution

For teachers' point of view:

• For handling class attendance, provide a tool for the teacher to record attendance digitally (By providing the list of students of the class and only ask for updates on punctuality for exceptions to "Present" status.)

• Provide a summary report of the created attendance, including the subject and date, and how many were either present, tardy, cutting, or absent.

• Allow exporting of attendance data.

### Goals

• [To Be Reworked]

• Provide a transparent and assistive attendance tool that may help with the current limitations of traditional and semi-automated attendance systems.

---

## Features

• Sign up, Login, Logout feature (Account Authentication)

• Role-based system attendance (Teachers, Students, Admin)

• Attendance features: Create Attendance, Attendance Dashboard with summary report.

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
```

macOS / Linux (Terminal):

```
python3 --version
python3 -m tkinter
python3 -c "import bcrypt"
pip3 show tkcalendar
```

Required Installations:

• Python

Minimum: Python 3.7, Recommended: Python 3.9+.

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
``` 

macOS Terminal: 
```
brew install python-tk
pip3 install bcrypt
pip3 install tkcalendar
```

Linux Terminal:
[Instllation Instructions for Tkinter, bcrypt, and tkcalendar](https://docs.google.com/document/d/17NBHcRPlcBNnfrOUJptSqRkywimTyfhTTs4cq2rRGXs/edit?usp=sharing)

---

3. Download the zip file of this GitHub's repository. Ensure that you have extracted the file/s from the .zip (e.g, through WinRAR) 
<img width="930" height="418" alt="image" src="https://github.com/user-attachments/assets/68c0cb73-8f24-4e0e-acb9-f9e0095f4956" />

---

4. Move the attendance_app folder outside the camia_AlveOrejola and onto the desktop directory.
<img width="964" height="595" alt="image" src="https://github.com/user-attachments/assets/a9d65e22-2e12-4452-9afd-72ba892f0f37" />


5. Open a command or terminal and type the following command. Ensure that the current directory your currently on is the desktop:

`C:\Directory\Other Directory\Desktop>python -m attendance_app.main`

6. Follow the on-screen instructions to enter login authentication, options for attendance, etc.

## Example Output:
<img width="875" height="688" alt="image" src="https://github.com/user-attachments/assets/50f9e2f9-04d6-4da1-b1ac-58b26410d1d3" />

## Contributors
- Student 1: Gabriel Aaron L. Alve (Draft Proposal, Flowchart, Updates in Code and Documentation)
- Student 2: Claire L. Orejola (README, Initial Code of the Project)
