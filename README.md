# camia_AlveOrejola
# Project Title: Self-record Attendance System

## Project Description
### Purpose

The Self-record Attendance System allow students to record their own attendance. The systems aims to reduce time ane effort of manual/traditional and QR-based systems.

### Problems/Issues with curent systems/methods:

• Manual attendance: Time-consuming for checking attendance. Slow, labor-intensive, prone to errors in recording

• QR-based systems: Terminals can handle one student at a time, making scaling difficult for hundreds of students.

### Proposed Solution

• Students log attendance through code program

• Attendance login requires attendance name, password, and possible countercheck questions.

• Attendance is logged/timestamped to discourage falsification

### Goals

• Allow students to record their own attendance, mainly in classes.

• To ensure that the system verifies the inputs and outputs properly, so there’s no dishonest recording.

• Provide a transparent and efficient attendance system to address the current limitations of traditional and semi-automated attendance systems.

## Features
• User Authentication (Login, Logout, Signup)

• Create, view, and fill attendance records

• System time utilization for attendance punctuality 

• Settings configurations

• Notifications and user feedback for event-driven GUI

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
