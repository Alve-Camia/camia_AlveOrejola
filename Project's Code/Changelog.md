# CHANGELOG

> [!NOTE]
> This file lists all updates made to the APACE (formerly the Self-record Attendance System), specifically updates in the project's code.

---
## Version v0.5.1 - June 3, 2026

### List of changes for Version 0.5.1

> [!NOTE]
> The following update details may be incomplete because of the large number of modifications and additions to the project code.


### Added

<table>  
  <tr>
    <th>Scope</th>
    <th>Description</th>
    <th>Reason/s</th>
  </tr>
  
  <tr>
    <td>Functions depending on current session and attendance info</td>
    <td>Added Dependency injection</td>
    <td>To identify more efficiently whether a certain function requires/utilizes the current session or current attendance</td>
  </tr>
  
  <tr>
    <td>Unit Tests (Found in the test_validators.py)</td>
    <td>
      <ul>
        <li>Added Edge Cases and Sad Paths for the attendance creation validator</li>
        <li>Added Tests for the auth service and attendance service function validators</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>Reduces Technical Debt</li>
        <li>Tests can check if modifcation/s to the tested code block will result in bugs/errors.</li>
        <li>In case of failed tests, they can often pinpoint errors without needing to open the program</li>
      </ul>
    </td>


  </tr>
  <tr>
    <td>Services Layer, Database layer, main.py, validators.py</td>
    <td>Added type hints to functions</td>
    <td>Documents what the expected function paramter/s' data types is/are</td>
  </tr>

  <tr>
    <td>main.py</td>
    <td>Added keyboard shortcuts to UI frames that have forms (i.e., Press enter when the selected entry, spinbox, or dropdown has focus, which is visually shown with a blue highlight).</td>
    <td>
      <ul>
        <li>Keyboard Support Purposes (Accessibility)</li>
        <li>Reduces the amount of dependency needed for using the mouse (UX)</li>
      </ul>
    </td>
  </tr>

  <tr>
    <td>main.py</td>
    <td>Added a combobox constructor (helper function). Comboboxes are now created through this.</td>
    <td>SoC (If the type of GUI changes, updating the helper function can give more progress for updating the comboboxes)</td>
  </tr>

  <tr>
    <td>main.py</td>
    <td>Added an `if __name__ == "__main__"`</td>
    <td>Added so that the program cannot be run from a different code file outside of main.py.</td>
  </tr>

  <tr>
    <td>main.py</td>
    <td>Added a helper function that loads table data</td>
    <td>Removing code duplication of inserting ttk.treeview rows based on fetched results from the storage</td>
  </tr>
  
</table>

#### Modified
<table>
  
  <tr>
    <th>Scope</th>
    <th>Description</th>
    <th>Reason/s</th>
  </tr>
  
  <tr>
    <td>main.py, auth_service, attendance_service</td>
    <td>Switched the data type for storing error statuses from dictionary to dataclass instances</td>
    <td>
      <ul>
        <li>When accessing the values from the error_response dictionary, you had to use strings, which can be prone to mistyping. </li>
        <li>IDE Extension Autocompletion Support (IDEs or IDE Extensions can provide autocompletion for accessing an instance's attributes.)</li>
      </ul>
    </td>
  </tr>
  
  <tr>
    <td>validators.py, attendance_service.py, auth_service.py, constants.py</td>
    <td>Assigned error messages to variables, which were then moved to constants.py</td>
    <td>
      <ul>
        <li>Prevents "Magic Strings"/"Hardcoding Strings"</li>
      </ul>
    </td>
  </tr>

  <tr>
    <td>main.py, constants.py</td>
    <td>Turned the variable, possible_grade_sections, into its own constant in constants.py</td>
    <td>Removes variable definition duplication, and the variable will rarely change.</td>
  </tr>

  <tr>
    <td>UI Pages</td>
    <td>Further Centered UI Pages</td>
    <td>
      <ul>
        <li>Makes the page have a focal point, and adds comfortable eye tracking of the UI pages</li>
      </ul>
    </td>
  </tr>

  <tr>
    <td>main.py, attendance_service</td>
    <td>Moved the attendance data export logic to the service layer.</td>
    <td>SoC (If the export file type changes, only the service layer will be affected).</td>
  </tr>

  <tr>
    <td>main.py (Helper Function)</td>
    <td>Renamed the popup helper functions to include 'popup' in their name</td>
    <td>It is now more explicit that it is a pop-up creator function.</td>
  </tr>

  <tr>
    <td>main.py, constants.py</td>
    <td>Moved window width and height values (of the program) into constants.py</td>
    <td>Program UI width and height values are constants, so they were moved to constants.py</td>
  </tr>

  <tr>
    <td>main.py, service layer</td>
    <td>Moved the remaining business logic (for the attendance marking) in main.py to the service layer
</td>
    <td>SoC (Business logic should stay in service layer, in this case it was attendance_service, for organizing code)</td>
  </tr>

  <tr>
    <td>main.py, constants.py</td>
    <td>Assigned the "NORMAL" (the one that is used for button state) into its own constant and moved it to constants.py</td>
    <td>Removes 'magic strings'</td>
  </tr>

  <tr>
    <td>main.py (Attendance Marking)</td>
    <td>Turned the process_punctuality_input function into two different functions</td>
    <td>The original process_punctuality_input had a large if-else code block, so it was split into smaller portions</td>
  </tr>

  <tr>
    <td>main.py</td>
    <td>Turned the three text size adjustment functions into one generic text size function</td>
    <td>Passing the font size multiplier directly to the font size adjuster would be more direct than using a function that will pass it themself (which was an extra step).</td>
  </tr>
</table>

#### Deleted

<table>
  <tr>
    <th>Scope</th>
    <th>Description</th>
    <th>Reason/s</th>
  </tr>
  
  <tr>
    <td>main.py</td>
    <td>Removed the get_db() function</td>
    <td>
      <ul>
        <li>get_db() ss already defined in db.py</li>
        <li>Removing it improves SoC in case the DB will need to change (e.g., type, how its called)</li>
      </ul>
    </td>
  </tr>
  
  <tr>
    <td>main.py</td>
    <td>Removed the remaining v0.4.0 code</td>
    <td>It is no longer being utilized (dead code).</td>
  </tr>

  <tr>
    <td>main.py (Theme / Appearance)</td>
    <td>Removed the accent_bg parameter in def apply_theme</td>
    <td>accent_bg is no longer being used, for now (dead code)</td>
  </tr>

  <tr>
    <td>main.py</td>
    <td>Removed direct DB calls in main.py</td>
    <td>SoC (If the 'how' of calling the db changes, the storage layer is affected, not the main.py)</td>
  </tr>
</table>


---
## Version v0.5.0 - April 23, 2026

### List of changes for Version 0.5.0

#### Added
<table>
  
  <tr>
    <th>Scope</th>
    <th>Description</th>
    <th>Reason/s</th>
  </tr>
  
  <tr>
    <td>User Authentication</td>
    <td>Added account roles that will determine allowed, accessible app features</td>
    <td>Prevent unauthorized access to certain app features. (e.g, Students should not be allowed to make an attendance)</td>
  </tr>
  
  <tr>
    <td>Unit Tests</td>
    <td>Added unit tests to the attendance app, specifically for the validator's code file.</td>
    <td>Helps check if any changes to code would result in bugs or errors, reducing the inefficiency of manual testing</td>
  </tr>
  
  <tr>
    <td>Attendance Data Export</td>
    <td>Added a feature for exporting attendance data</td>
    <td>To allow attendance data portability, and not make the data saved through the app limited to the database.</td>
  </tr>
  
</table>

#### Modified
<table>
  
  <tr>
    <th>Scope</th>
    <th>Description</th>
    <th>Reason/s</th>
  </tr>
  
  <tr>
    <td>Database Schema</td>
    <td>Modified the SQLite database schema to the following: student accounts, teacher accounts, attendance sessions, attendance records, login timestamps</td>
    <td>Student and Teacher accounts were used to adapt to the account role features, and to make account querying more efficient, as combining both account types would result in some accounts having N/A data stored</td>
  </tr>
  
  <tr>
    <td>Attendance System</td>
    <td>Modified the attendance such that it mainly utilizes exception-based teacher inputs</td>
    <td><a href="https://github.com/Alve-Camia/camia_AlveOrejola/issues/16">Refer to the problem statement</a></td>
  </tr>

  <tr>
    <td>Signup Page</td>
    <td>Signup Page now requires name (first and surname), account role (Student, Teacher), and grade level and section (if the selected account role is teacher)</td>
    <td>To help organize student account info, and help with attendance recording (so that names can be used instead of relying on usernames that can be potentially misleading)</td>
  </tr>

  
</table>

#### Deleted
<table>
  <tr>
    <th>Scope</th>
    <th>Description</th>
    <th>Reason/s</th>
  </tr>
  
  <tr>
    <td>Settings</td>
    <td>Removed Personalization and Password Reset</td>
    <td>
      <li>Due to time constraints.</li>
      <li>Personalization adds little value to the app, given that the project has an academic and/or professional context.</li>
    </td>
  </tr>
  
  <tr>
    <td>Attendance</td>
    <td>Deleted Password-based attendance system</td>
    <td><a href="https://github.com/Alve-Camia/camia_AlveOrejola/issues/16">Refer to the problem statement</a></td>
  </tr>

</table>

---

## Version v0.4.0 - March 30, 2026

### List of changes for Version 0.4.0


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
    <td>A preventive/reactive feature in case of database data breach/compromise </td>
  </tr>
  <tr>
    <td>Project Code</td>
    <td>Partially implemented code modularization to project code (e.g, db, auth_service, attendance_service, validators, constants)</td>
    <td>To apply separation of concerns (SoC), a programming principle, make debugging easier to track, and make progress towards being able to implement automated testing </td>
  </tr>
  <tr>
    <td>Logic Refactoring</td>
    <td>Utilized Different Code Files for logic flow of attendance and user features</td>
    <td>To apply SoC and DRY (Don't Repeat Yourself), and to make logic reusable </td>
  </tr>
  </tr>
  <tr>
    <td>Create Attendance</td>
    <td>When countercheck is enabled, countercheck answer will now be hashed</td>
    <td>To mitigate effects of database compromise, specifically for countercheck</td>
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
    <td>Acts as an option if the user wants to make any changes first before making attendance. Additionally, it helps with preventing accidental, non-desired action</td>
  </tr>
  <tr>
    <td>User Experience</td>
    <td>Project Code asks the user first for a window close confirmation popup</td>
    <td>Prevents accidentally closing the app</td>
  </tr>
  <tr>
    <td>View Attendances</td>
    <td>Creator Table and Participant Table now have scrollbars.</td>
    <td>Acts as a UX addition for scrolling through tables in the view attendance.</td>
  </tr>
  <tr>
    <td>Project Code</td>
    <td>Implemented helper functions (e.g, display_warning(), display_info(), yes_or_no())</td>
    <td>To remove repeated message boxes in code, and to apply code reusability.</td>
  </tr>
  <tr>
    <td>Project Code</td>
    <td>Implemented a generic widget loader for widgets</td>
    <td>To apply DRY, specifically for avodiing repetitive .pack() loops</td>
  </tr>
  <tr>
    <td>Session Handling</td>
    <td>Replaced user session handling with Python classes.</td>
    <td>To remove global dependency for the current user.</td>
  </tr>
  <tr>
    <td>User Interface</td>
    <td>Reduced Window size from 1200x1200 to 1200X680</td>
    <td>To ensure that the UI window does not take excessive space from the screen.</td>
  </tr>
</table>

---
## Version v0.3.0 - February 4, 2026 
- 5th version of the code:
- Added SQLite Database, specifically attendance.db, to replace the text file storage
- Added the Create, Fill Out, and View attendances in the Attendance Menu
- Added bcrypt hashing for attendance password
- Added "Light Mode and Dark Mode" in Settings
- Added a feature that tracks who the current user is in the session
- Modified attendance creation such that it has Start/End Date & Time Validation
- Modified the password requirement on sign up (Password now requires 10 characters)
- Modified where bcrypt hashed for user authentication are now stored (SQLite is now used instead of .txt files)
- Modified Log Out wherein there is a confirmation prompt
- Modified error-handling messages
- Removed Demo Messages for attendance Buttons as it now has functionality
- Removed use of text files for storing data
---
## Version v0.2.0 - January 30, 2026 
-  Version 4 of the program
- Changed how most of the widgets for each frame are called
- Added Hashing and Salting for passwords when saved in users.txt
- Changed the widget variable names in the code (FrameName_Description_WidgetType)
- Added a settings menu and a menu for creating attendance (They currently have a demo message)
- Changed the use of comments in the code
---
## Version v0.1.1 - January 24, 2026
- 3rd Version of the program
- Modified how widgets are called in the code by using separate frames for each part of the program
- Modified the clock in the menu so that it now updates every second
---
## Version v0.1.0 - January 22, 2026 
- 2nd Version of the program
- Modified username restrictions, specifically, usernames can now have spaces so long that there are at least letters in the username as well.
- Added a log-out button
- Added a first version of the main menu of the program code. It currently has an attendance button, a log out button, and the current time displayed (does not update yet)
- Added an attendance button that leads to the options for attendance. As of now, they only print out a label saying "still in development."
---
## Version v0.0.0 - January 20, 2026
- First Version of the program
- Currently, the user can:
  - Sign up for an account for the program (Has restrictions such as 8 characters for minimum password, no empty entered user and/or password, only letters for account name)
  - Log in using the account name and password entered during sign up (Displays a message in green when the user logs in and specifies what time
