# CHANGELOG 
This file lists all updates made to the Self-record Attendance System project, specifically the updates in the project's code.
---
## Version v0.3.0 - February 4, 2026
- 5th version of the code:
- Added SQLite Database, specifically attendance.db to replace the text file storage
- Added an initialization of the tables used for the database
- Added the Create, Fill Out, and View attendances in the Attendance Menu
- Added a tracking logic with the attendance submissions (Minutes until considered late)
- Added bcrypt hashing for attendance password
- Added Countercheck feature, specifically the question and answer verification
- Added Attendance Status (On time, Late, Absent)
- Added ttk.Treeview to view creator and participant attendance views
- Added "Light Mode and Dark Mode" in Settings
- Added a "search query" for the View Attendance
- Added timestamps for login logging
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
