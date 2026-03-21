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


## How to run the program
1. **Check installation**:

Windows (Command Prompt):
```
python --version
python -m tkinter
pip show bcrypt
```

macOS / Linux (Terminal):

```
python3 --version
python3 -m tkinter
python3 -c "import bcrypt"
```

Minimum: Python 3.7, 
Recommended: Python 3.9+.

Download: [Python.org](https://www.python.org).

2. Install missing libraries (Skip if there are no missing libraries)
> [!NOTE]
> In most cases, Tkinter is included in Python installation. However, many Linux distributions do not include Tkinter by default.

Command Prompt (Windows): 
```
pip install tkinter
pip install bcrypt
``` 

macOS Terminal: 
```
brew install python-tk
pip3 install bcrypt
```

Linux Terminal:
[Instllation Instructions for Tkinter and bcrypt](https://docs.google.com/document/d/17NBHcRPlcBNnfrOUJptSqRkywimTyfhTTs4cq2rRGXs/edit?usp=sharing)

3. Download the file `Self-record Attendance.py`, or copy-paste the code from it and paste it into a Python file.

4. Open a terminal or command prompt.

5. Run the program by pressing F5 or clicking 'Run.' 

6. Follow the on-screen instructions to enter login authentication, options for attendance, etc.

## Example Output:
<img width="700" height="471" alt="image" src="https://github.com/user-attachments/assets/b179f4db-8ee1-44ac-8012-ed3cf390275f" />

## Contributors
- Student 1: Gabriel Aaron L. Alve (Draft Proposal, Flowchart, Updates in Code and Documentation)
- Student 2: Claire L. Orejola (README, Initial Code of the Project)
