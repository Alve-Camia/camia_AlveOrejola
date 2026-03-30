# CHANGELOG 
This file lists all updates made to the Self-record Attendance System project, specifically the updates in the project's code.
---
## Version v0.4.0 - March 30, 2026

<b>List of changes for Version 0.4.0<b/>
<table>
  <tr>
    <th>Scope</th>
    <th>Description</th>
    <th>Reason/s</th>
  </tr>
  <tr>
    <td>Create Attendance</td>
    <td>Only hashed counterchck answer if enabled</td>
    <td>Hashing countercheck answers is unnecessary if the user does not intend to use it</td>
  </tr>
  <tr>
    <td>Settings</td>
    <td>Added a "Change Account Password" feature</td>
    <td>A preventive/reactive feature in case of database data breach/comprimise</td>
  </tr>
  <tr>
    <td>Project Code</td>
    <td>Partially implemented code modularization to project code (e.g, db, auth_service, attendance_service, validators, constants)</td>
    <td>To apply separation of concerns (SoC), a programming principle,make debugging easier to track, and make progress towards being able to implement automated testing </td>
  </tr>
  <tr>
    <td>Logic Refactoring</td>
    <td>Utilized Different Code Files for logic flow of attendance and user features</td>
    <td>To apply SoC and DRY (Don't Repeat Yourself), and to make logic resuable</td>
  </tr>
  </tr>
  <tr>
    <td>Create Attendance</td>
    <td>When countercheck is enabled, countercheck answer will now be hashed</td>
    <td>To mitigate effects of database comprimise, specifically for countercheck</td>
  </tr>
  </tr>
  <tr>
    <td>Settings</td>
    <td>Implemented Accessibility Features (First Pass), specifically high contrast mode and text resizing</td>
    <td>To implement an inclusive design choice and improve usability</td>
  </tr>
  </tr>
  <tr>
    <td>User Interface (UI)</td>
    <td>Switched to ttk, and applied ttk styles for UI appearance and settings</td>
    <td>To have a cleaner UI system, and to polish project code UI</td>
  </tr>
  <tr>
    <td>Create Attendance</td>
    <td>Replaced entry box for date entries with calendar picker (Date entries still accepts manual typing of dates)</td>
    <td>UX (User Experience) purposes, specifically to provide a visual calendar to select dates (for ease of date inputs)</td>
  </tr>
  <tr>
    <td>Create Attendance</td>
    <td>Added a spinbox (selection box) for grace period entry</td>
    <td>UX Purposes, users can now use it for grace period entry</td>
  </tr>
  <tr>
    <td>Create Attendance</td>
    <td>Before making attendance, the code program asks first to confirm their action.</td>
    <td>Acts as an option if user wants to make any changes first before making attendance. Additionally, it helps with preventing accidental, non-desired action</td>
  </tr>
  <tr>
    <td>User Experience</td>
    <td>Project Code asks user first a window close confirmation popup</td>
    <td>Prevents accidentally closing the app</td>
  </tr>
  <tr>
    <td>View Attendances</td>
    <td>Creator Table and Participant Table now have scrollbars.</td>
    <td>Acts as a UX addition for scrolling through tables in view attendances.</td>
  </tr>
  <tr>
    <td>Project Code</td>
    <td>Implemented helper functions (e.g, display_warning(), display_info(), yes_or_no())</td>
    <td>To remove repeated messageboxes in code, and to apply code reusability.</td>
  </tr>
  <tr>
    <td>Project Code</td>
    <td>Implemented a generic widget loader for widgets</td>
    <td>To apply DRY, specifically for avodiing repetitive .pack() loops</td>
  </tr>
  <tr>
    <td>Session Handling</td>
    <td>Replaced user session handling with python classes.</td>
    <td>To remove global dependency for current user.</td>
  </tr>
  <tr>
    <td>User Interface</td>
    <td>Reduced Window size from 1200x1200 to 1200X680</td>
    <td>To ensure that UI window does not take excessive space from the screen.</td>
  </tr>
</table>


---
## Version v0.3.0 - February 4, 2026
- 5th version of the code:
- Added SQLite Database, specifically attendance.db to replace the text file storage
- Added the Create, Fill Out, and View attendances in the Attendance Menu
- Added bcrypt hashing for attendance password
- Added "Light Mode and Dark Mode" in Settings
- Added a feature that tracks who is the current user in session
- Modified attendance creation such that it has Start/End Date & Time Validation
- Modified the password requirement on sign up (Password now requires 10 characters)
- Modified where bcrypt hashed for user authentication are now stored (SQlite is now used instead of .txt files)
- Modified Log Out wherein there is a confirmation prompt
- Modified Error handling messages
- Removed Demo Messages for attendance Buttons as it now has functionality
- Removed use of text files for storing data
---
## Version v0.2.0 - January 30, 2026
-  Version 4 of the program
- Changed how most of the widgets for each frame are called
- Added Hashing and Salting for passwords when saved in users.txt
- Changed the widget variable names in the code (FrameName_Description_WidgetType)
- Added a settings menu and a menu for create attendance (They currently have a demo message)
- Changed the use of comments in the code
---
## Version v0.1.1 - January 24, 2026
- 3rd Version of the program
- Modified how widgets are called in the code through using seperate frames for each part of the program
- Modified the clock in the menu so that it now updates every second
---
## Version v0.1.0 - January 22, 2026
- 2nd Version of the program
- Modified username restrictions, specifically usernames can now have spaces so long that there are at least letters in the username as well.
- Added a log out button
- Added a first version of the main menu of the program code. It currently has attendance button, log out button, and current time displayed (does not update yet)
- Added an attendance button that leads to the options for attendance. As of now, they only print out a label saying "still in development"
---
## Version v0.0.0 - January 20, 2026
- First Version of the program
- Currently the user can:
  - Sign up for an account for the program (Has restrictions such as 8 characters for minimum password, no empty entered user and/or password, only letters for account name)
  - Log in using the account name and password entered during sign up (Displays a message in green when the user logs in and specifies what time
