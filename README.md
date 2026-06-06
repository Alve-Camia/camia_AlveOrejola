# camia_AlveOrejola
# Project Title: APACE: Assistive Project Attendance Considering Efficiency
## Project Description
### Purpose

The purpose of APACE is mainly to improve the efficiency of the current attendance system methods observed on campus. Specifically, the system aims to reduce the time and effort of manual/traditional and QR-based systems.

> [!IMPORTANT]
The project's attendance system is neither intended to be a complete replacement for the campus's current attendance system. The attendance system is intended to be a supportive/assistive tool in this context.
---

### Problems/Issues with current system/s:

<ul>
    <li>Manual attendance: Time-consuming for checking attendance. Slow, labor-intensive, prone to errors in records.</li>
    <li>QR-based Attendance: Can only handle one student per terminal, resulting in possible scalability issues for hundreds of students.</li>
</ul>

### Proposed Solution

From the teachers' point of view:

<ul>
     <li>
      For handling class attendance, provide a tool for the teacher to record attendance digitally (By providing the list of students in the class and only asking for updates on punctuality for exceptions to "Present" status)
     </li>
     <li>
      Allow exporting of attendance data into a CSV (Comma Separated Values) file, allowing ease of attendance records compilation and data portability.
     </li>
</ul>

From the students' point of view:

<ul>
    <li>
     Provide the students with the list of their attendance records, which includes the date, subject, punctuality status, and cutting/tardy minutes (if applicable). This allows transparency of the students' attendance records.
    </li>
</ul>



### Goals

<ul>
     <li>Allow teachers to record attendance sessions through exception-based inputs for student punctuality.</li>
     <li>Provide a transparent and assistive attendance tool that may help with the current limitations of traditional and semi-automated attendance systems.</li>
</ul>

---

## Features

<ul>
    <li>Sign up, Login, Logout feature (Account Authentication)</li>
    <li>Role-based system attendance (Teachers, Students)</li>
    <li>Attendance features: Create Attendance, Attendance Dashboard.</li>
    <li>Data export of attendance records to CSV (Comma Separated Values)</li>
    <li>Pop-up messages for user actions in connection with event-driven GUI</li>
    <li>Settings Feature (Accessibility and Attendance Settings)</li>
</ul>

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

<ul>
    <li>Python</li> 
</ul>


Minimum: Python 3.9, Recommended: Python 3.11/3.12.

> [!NOTE]
> In most cases, Tkinter is included in Python installation. However, many Linux distributions do not include Tkinter by default.

Download: [Python.org](https://www.python.org).

Additional Dependencies:

<ul>
    <li>tkinter</li>
    <li>bcrypt</li>
    <li>tkCalendar</li>
    <li>pandas</li>
</ul>

> [!NOTE]
> For this context, "pandas" refers to the open-source library. This is not meant to be confused with the animal.

---

2. Install missing libraries (Skip if there are no missing libraries)

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
> [!TIP]
> The last two lines can also work for the Linux Terminal.

Linux Terminal:
[Installation Instructions for Tkinter, bcrypt](https://docs.google.com/document/d/17NBHcRPlcBNnfrOUJptSqRkywimTyfhTTs4cq2rRGXs/edit?usp=sharing)

---

3. Download the zip file of this GitHub repository. Ensure that you have extracted the file/s from the .zip (e.g, through WinRAR)

<img width="880" height="525" alt="image" src="https://github.com/user-attachments/assets/f14ac644-6547-4a7d-88fd-48b80887c4bc" />

---

4. Move the attendance_app folder outside the camia_AlveOrejola and onto the desktop directory.

<img width="987" height="505" alt="image" src="https://github.com/user-attachments/assets/7ba407a9-07ec-4393-8b0f-bedaad578b8f" />


5. Please run the program based on your device's operating system. Ensure the folder attendance_app is on the desktop or in the desktop directory.

### For Windows:

Open the Command Prompt and navigate to the **desktop directory**. 

<img width="1109" height="623" alt="image" src="https://github.com/user-attachments/assets/84a37910-88ed-405b-ab60-58dd05524362" />

Then type the following command:

`python -m attendance_app.main`

Example:

<img width="1194" height="623" alt="image" src="https://github.com/user-attachments/assets/b8b9de3e-d0a5-4778-8804-f1b382ad60af" />

6. Follow the on-screen instructions to enter login authentication, options for attendance, etc.


### For macOS:

Open a terminal and navigate to the **desktop directory**:

`cd ~/Desktop/[Parent Directory]/[Other Parent Directory]`

Then type the following command:

`python3 -m attendance_app.main`

### For Linux:

Run the following command from the parent directory containing the attendance_app folder:

<table>
     <tr>
          <th>Linux Distribution</th>
          <th>Command</th>
     </tr>
     <tr>
          <td>Debian, Ubuntu, Linux Mint, Fedora, RHEL, CentOS, Rocky Linux</td>
          <td>python3 -m attendance_app.main</td>
     </tr>
     <tr>
         <td>Arch Linux, Manjaro</td>
         <td>python -m attendance_app.main</td>
     </tr>
</table>


## Example Output:

### Logged Out Menu:

<img width="750" height="auto" alt="image" src="https://github.com/user-attachments/assets/ede59bad-b5c7-4b10-869b-14a0ad9a09f4" />

### Login Page:

<img width="750" height="auto" alt="image" src="https://github.com/user-attachments/assets/b4e0d65d-de52-409d-aff8-9fa7c19ab02b" />

### Teacher's Main Menu Page (Logged in):

<img width="750" height="auto" alt="image" src="https://github.com/user-attachments/assets/7fd57610-e79e-41da-8d35-adda07afa067" />

### Attendance Dashboard:

> [!NOTE]
> These are example attendance sessions. Please do not assume these were real classes happening.

<img width="797" height="707" alt="image" src="https://github.com/user-attachments/assets/4c23adf9-d2f8-47cb-919b-e7e13105a8a6" />

### Attendance Marking Menu Example:

> [!NOTE]
> The names are redacted for privacy reasons and to reduce digital footprint.

<img width="800" height="712" alt="image" src="https://github.com/user-attachments/assets/fcdab9e1-221b-4155-bb1a-47d3a1b09ed3" />

### Attendance Export:
<img width="806" height="713" alt="image" src="https://github.com/user-attachments/assets/10c13b26-d6e6-42ff-b65a-293f244ac68e" />

### Logging Out:
<img width="800" height="712" alt="image" src="https://github.com/user-attachments/assets/788677fa-7536-4f97-85e0-c4c6da502486" />

## Contributors
- Student 1: Gabriel Aaron L. Alve (Draft Proposal, Flowchart, Updates in Code and Documentation)
- Student 2: Claire L. Orejola (README, Initial Code of the Project)
