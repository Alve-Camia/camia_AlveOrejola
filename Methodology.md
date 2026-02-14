# Detailed Methodology
## Methodology Contents
## 1. Implementation of Core Features
###   1.1 Log in and Log Out
###     1.1.1 Log In
###     1.1.2 Log Out
###     1.1.3 Account Creation (Sign Up)
##    1.2 Attendance Features and System Time Utilization for Attendance Punctuality
###      1.2.1 Create Attendance
###      1.2.2 View Attendance/s
###      1.2.3 Fill Out Attendance
## 2. Technologies Used (with justification)
###  2.1 Python
###  2.2 Tkinter
###  2.3 bcrypt
###  2.4 SQLite
## 3. Backend-frontend communication
###  3.1 Tkinter (Frontend)
###  3.2 Python (Backend)
###  3.3 SQLite (Storage)
## 4. Key Design Decisions or Trade-offs
###  4.1 Manual Date and Time Input
###  4.2 Single-file Architecture
###  4.3 Pop-up validation messages
###  4.4 Database Usage (SQLite)
## 5. References to Ethical Considerations in Programming Choices
###  5.1 User Privacy
###  5.2 Accessibility

## Methodology

## 1. Implementation of Core Features
The following content in Section 1 of the methodology describes how the features of the Self-Record Attendance System were implemented. Currently, there are three main features made: 
user authentication feature, attendance Feature, and system time feature.

Note for 1.1 and 1.2: 

Both their flow and utilize parameter placeholders (?) during the retrieval (SELECT) and insertion (INSERT) of data in SQLite connections. This is used to prevent SQL injection,
a type of injection code attack that results in the backend of applications running SQL queries or commands that can result in data breach effects, such as database compromise (Happens when a user enters 
the SQL commands in empty fields or input). Additionally, the system time utilization is part of the Attendance Feature, so 1.2 will be used to explain both of those
features.

### 1.1 Log in and Log Out

#### 1.1.1 Log in

The login system of the program was implemented using an account name and a hashed password system. A login system was used instead of directly showing the user the main menu to implement current user
session tracking. The current user tracking is implemented to prevent users from falsifying attendance records through impersonation of another user. When the user presses log in, the login system checks
whether there are empty login credentials. If there are empty credentials, the user would be notified about it with a pop-up message, and would be asked to enter the missing login credentials/s. Next, 
the program checks if the entered login credentials appear in the USERS table in the database. 

If the entered account name is not stored in the USERS table, the program notifies the user about it and asks the user to re-enter login credentials. The comparison of whether the account name is stored in the 
USERS table, which is case-insensitive. If the entered account name is found, the login system checks if the entered password corresponds to the stored, hashed password in the USERS table in the database. 
If the user did not enter their account password, the program would notify the user about it. Otherwise, the program proceeds and uses bcrypt.checkpw() to verify whether the entered account password matches the entered account name.

bcrypt.checkpw() is used because when the user signs up, their password is hashed and salted and stored in the USERS table.

bcrypt.checkpw() works by taking in the following arguments as follows:

bcrypt.checkpw(plain_string.encode(), hashed_string.encode())

The bcrypt.checkpw() hashes the plain string and uses the salt from the hashed string. If both of the salted and hashed strings match, then the user successfully logs in and is shown the main menu of the
program. The program additionally tracks who the current user is. Otherwise, the program informs the user that the password is incorrect.

#### 1.1.2 Log Out

In the main menu of the program, the user can click "log out" to log out of the program. When they do so, they are asked first to confirm that they intend to logout. This is to prevent accidental logout
and make the user enter their login credentials again. If the user clicks "Yes" in the log-out confirm prompt, then they will log out and be shown the login menu. Otherwise, if the user clicks "No", then 
they would be shown the attendance menu, and nothing happens.

#### 1.1.3 Account Creation (Sign Up)

A sign-up system and feature were implemented for the login and logout features because of three main reasons:

1. The user wouldn't have an account unless they manually make an account through a data storage
2. Manually adding users would take significant time, especially because you need to consider how the data will be input (e.g, hashed passwords will need to be entered).
3. Manually adding users would not scale well with tens or hundreds of users.

The sign-up feature works by taking in what the user has entered when they entered an account name and an account password. First, the sign-up system checks if the user has entered empty sign-up credentials, 
and informs the user about it if there are. Then, the program checks if the entered sign-up credentials match the requirements stated in the login menu.

Account Name: Only Letters and Spaces (Spaces by themself will not be accepted, as it can confuse users when a non-named user submits attendance, and the submission in View Attendances shows their name 
as whitespace)

Password: At least 10 characters

If the entered sign-up details do not match the specifications, then the user is informed about it and is asked to change their sign-up details. Otherwise, the sign-up system accepts the account name, hashes
and salts the entered account password through bcrypt, inserts the sign-up credentials in the USERS table, and prompts the user that they successfully signed up.

### 1.2 Attendance Features and System Time Utilization for Attendance Punctuality

#### 1.2.1 Create Attendance
The create attendance feature is implemented to make attendance in the program and add additional parts such as an attendance password and a counterchecking question to help with the data integrity of the program. 
First, the program asks the user to input the start/end date (MM-DD-YYYY), start/end time (24-hour format), attendance password, grace period (asks for a specific number of minutes until considered late), and an optional countercheck question with an answer (Via pop-up message). Then, the program takes in the created attendance info and checks if any of the conditions occur:
- Start or End Date is not in the MM-DD-YYYY format
- Start or End Time is not in 24-hour format
- End Time is earlier than Start Time
- Start Time is at the same time as End Time
- Either Start/End Date/Time is whitespace
- Attendance Password is less than 10 characters
- Grace period is either less than 0 minutes or is not a number
- Empty countercheck question or answer
If so, the program notifies the user about this through a pop-up. Otherwise, the program parses (converting raw text data into a usable format for the program) the dates via .striptime() and .combine(), hashes the attendance password, inserts the data into the ATTENDANCES table in the SQLite database, and gives the user a pop-up message saying that the attendance was made.
Data stored in the ATTENDANCE table:
- Attendance Name
- Start Datetime
- End Datetime
- Grace period (The actual code variable is minutes_lates)
- Hashed Attendance Password
- Account name of the user who created said attendance
- Int value of countercheck (Whether user clicked "Yes" or "No" when asked about adding countercheck question)
- Question (Empty String if user clicked "No")
- Answer (Empty String if user clicked "No")

#### 1.2.2 View Attendances
The purpose of the view attendances feature is for viewing the attendances made, who recorded their attendance, and the attendances that the user has filled out. First, the feature utilizes 2 tables by
using treeview, and using the following column names:
Creator View:
- Attendance Name
- The user who filled out the attendance
- Time of recording
- Attendance Status
- Minutes Late
- Response (If applicable)
Participant View:
- Attendance Name
- Attendance Status
- Time of recording
- Account Name
- Response (If applicable)
Additionally, the feature stores the current session account name and deletes all existing rows in both of the tables in order not to make old data stay there. Then, the creator table uses the ATTENDANCE
 table from the SQLite database to retrieve and populate the creator table (WHERE a.creator is used so that it only shows attendances made by the current user. Additionally, it uses LEFT JOIN
(during the database cur.execute) to give all submissions for an attendance. It gets all the fetched rows and iterates them in the table

On the other hand, the participant table is populated by getting the data entries from the SUBMISSIONS table in the database that the current user has filled out. Then, each submission made by the current user
is iterated in the participant table.

#### 1.2.3 Fill Out Attendance
The fill-out attendance is a feature of the 2nd Core feature of the program (Attendance Feature) that allows participants to record their attendance. The following describes how it was implemented
First, the fill-out feature uses texts (tk.Label) and fields (tk.Entry) to allow the user to enter the attendance name and attendance password (for recording their attendance). Then, the program takes in the 
user's input and checks if the inputted information is white space (Notifies the user about it). Then, the fill-out flow system retrieves the data from the ATTENDANCE table in the SQLite attendance.db to first
check if the entered attendance name is stored and exists. After that, the program uses bcrypt.checkpw() to compare the attendance password entered by the user with the hashed password corresponding to the
found attendance (By hashing the entered attendance password and using the hashed password's salt to determine if both of the hashed strings match). 

If they match, the program then checks if the user has already submitted their attendance using a cur.execute that fetches the data from the SUBMISSIONS table and uses "if cur.fetchone()" to check if the 
user's attendance submission to that attendance exists. Otherwise, the fillout logic flow gets the current time (of when the user has submitted their attendance) and compares it with the start datetime and 
end datetime. If the current time is past the end datetime, then the status of the user is recorded as absent, and how many minutes they were late is calculated. If they weren't late, but their time of submission
is past the grace period, then their attendance status of the user is marked late, and again, it calculates how many minutes late they were. Otherwise, they would be marked on time with 0 late minutes.

After that portion, the program checks if the filled-out attendance uses a countercheck question. If there is, the user is prompted with the question and must provide the correct answer for the countercheck
question before they can continue filling out the attendance. This section of the program additionally checks if the entered input has whitespace or not, and prompts the user to answer the question.

Finally, a connection and a cursor are used for inserting the recording of attendance in the SUBMISSION table in the attendance.db. Then, the user is prompted that their attendance was recorded, along with their
punctuality status.

## 2. Technologies Used (with justification)
### 2.1 Python
Python is an object-oriented programming language that is used in the project's code for the following reasons:

- Python's Self-documentation / Readability:

One of Python's main advantages is that it emphasizes and helps with the readability of code through simple syntax (syntaxes are self-descriptive and are English-like), minimalist design
  (does not use numerous parentheses or special characters), use of whitespace and mandatory indentation, and explicit, clear error messages (uses carets to pinpoint an issue with a line of code).
  Because of these reasons, it helps with the project code's maintainability and collaboration (In increased size and complexity of codes, reading code is done more than writing it. This helps with coders
  and developers when updates or snippets of code are given, as they have readability.

- Python's Comprehensive Standard Library:
 
    Python has numerous libraries used for specific tasks such as computations, datetime handling, UI, string handling, etc. This helps with the project's code through the multiple libraries' readable,
  and straightforward use and syntax that decreases the complexity of code in certain areas of the program.

Though Python has a slow execution speed compared to other object-oriented programming languages (e.g, C++, Java) and high memory usage, Python's library and syntax allow the program to be written with fewer
lines of code to achieve the same result (so long as the code is not messy and well-written).

### 2.2 Tkinter
Tkinter, additionally called "Tk interface," is a built-in library for creating a GUI (Graphical User Interface) for Python programs. The following is a list of reasons why Tkinter is used in the project code:

- No Separate installation required:

  Tkinter is additionally installed in most Python installations. This means that no separate or complex installation is required to use it when using it in code. This helps in the project code by not
   making the code too heavily focused on making the user interface itself

- Tkinter's Syntax and learning curve:
  The syntax of tkinter is straightforward (self-documenting and self-explanatory), resulting in a less steep learning curve and helping as a less complex and introductory-like GUI for beginners
  or those who aren't familiar with implementing GUI in coding. This helps in the project code because it functions as a less complex way to establish how the UI for the program is intended to appear.

### 2.3 bcrypt

bcrypt is a type of password-hashing function that uses the Blowfish cipher for its algorithm. It uses a one-way, irreversible, slow-running password hashing function used specifically for
secure password hashing and storage that can resist brute-force attacks (guessing all combinations, dictionary attacks) through its slow and memory-intensive hashing. It was used in this program to
encrypt the passwords used for accounts and attendance (If the user were to gain access to the database or info about the passwords, they would be hashed and salted, so they can't decipher or decode them 
to find the account passwords of other users).

### 2.4 SQLite

SQLite is used in the following program for the following reasons:
- SQLite organizes the data stored into a structured table with columns that support different data types. This structure of storing data requires less complexity for data parsing and interpretation when
  fetched.
- SQLite databases have scalability when handling hundereds ot thousands of data, and can use indexes for speeding up data retrieval in large amounts of data. Additionally, because of its use of SQL query
  language, it allows multiple types of operations for data access and manipulation, such as joining, filtering, sorting, etc.
- SQLite's Data storage can handle corruption errors by reporting an error code (SQLITE_CORRUPT) instead of crashing or writing a partial line of code

## Backend-frontend Communication

###  3.1 Tkinter (Frontend)
Note: UI means user interface, and UX means user experience

Tkinter, as the frontend and graphical user interface, contributes to the project code through its interactions with the backend, Python, and with its widgets and pop-up messages (that give info about the user's
actions, such as errors or info notices), which provide the user interactivity rather than using a text-based user interface. From a UI and UX point of view, it displays
widgets such as labels, buttons, entries, and tables in a vertical format that allows users to navigate the different parts of the program. For its interactions with the backend, when users interact with 
widgets, Tkinter takes this input and gives it to the backend of the program, and changes the current frame shown to the user accordingly (or gives the user pop-up messages). For example, when the user enters 
login credentials in the entry fields and presses the "Log In" button, Tkinter interacts with Python by going to the corresponding function. Then it gives Python the entered info and gets the 
computed results or info. After that, tkinter gives or changes the respective UI based on the computation given.

###  3.2 Python (Backend)

Python, as the backend and logic flow of the program, contributes to the project code by determining how the program works. In addition, it acts as the middle with its interaction with the frontend and storage
layer. It performs certain processes such as input validation, data integrity, computation, and more. Whenever the backend receives an input and/or an interaction from the frontend, the backend generally first 
does inputvalidation to check if the user input meets certain conditions. After that, the backend does computation for certain actions or calculations, such as hashing, time parsing, or time calculation. 
After that, it either results in the backend interacting with the frontend to do or display certain widgets, or it interacts with the storage to store certain data from its computation. To add on, the 
backend can communicate with the storage the retreive certain data from tables, compare it with the data given from the frontend. This results in either interaction with the frontend or the storage.

###  3.3 SQLite (Storage)

SQLite, as the storage of the program, contributes to the project code by being able to save certain data inputs that result from the backend processing it. Then, it stores that data in certain tables 
of the attendance database. In addition, the attendance database can retrieve data from its tables to give to the backend for computing. The storage layer does not directly interact with the frontend. Instead,
it uses the backend and SQL commands to communicate with the backend to process it and display or use it for the frontend. An example would be when the user goes to the view attendances, and
the storage gives the appropriate table data to the backend for processing. Then the backend gives the frontend the processed data to output it.

## 4. Key Design Decisions or Trade-offs

###  4.1 Manual Date and Time Input

For the time window section of the create attendance feature, a manual date and time input was used instead of a calendar widget. The main reason was that
if the user were to make multiple attendances, it would reduce interaction steps if the user manually input the start and end datetime instead of implementing a calendar widget 
(e.g, tkcalender) because of the time spent navigating through the calendar and picking the date. In contrast with calendar pickers, manual date and time inputs allow more accessibility by being more 
accessible for keyboard navigation. In addition, it reduces the number of clicks required to pick a date. Moreover, calendar pickers often feature a time picker that uses a clock that can be adjusted by 
dragging the clock's hands. This feature introduces increased user-interaction complexity for a time picker because you need to click and drag a clock instead of directly entering the time. 

Manual date and time input has trade-offs, such as the absence of day-of-week information and less visual guidance during date selection. However, these trade-offs were accepted in the design choice
because it simpliefies interaction and accessibility.
###  4.2 Single-file Architecture
All parts and components of the code, such as application logic, user interface, and database connections, were coded inside one file. This decision was made to help with testing the code
from start to finish by reducing the code's structural complexity. Additionally, it provides a traceable way to read the flow of the program. The single-file architecture additionally helps with
code sharing because the entire system is in a single file, and it does not require additional dependencies.

The single-file architecture limits readability and maintainability. However, they were accepted in the design choice because their effects can be mitigated through using consistent coding conventions
and by using the PEP (Python Enhancement Proposal) style guide to maintain readability.
###  4.3 Pop-up validation messages

For informing the user of info, warnings, and questions, a pop-up validation message was used. First, it provides the user with immediate user feedback on whether there is an error, the results of the input, and more.
Additionally, it reduces the confusion of why certain actions don't result in the expected outcome (error messages). Pop-up messages assist this by displaying the error to the user instead of appearing as a
console message. Moreover, pop-up messages assist in the user experience of the program as the flow of the application is an event-driven GUI.

Pop-up validation messages have trade-offs, such as their sudden disruption, reducing focus, and repetitiveness for certain actions in the program. However, these trade-offs were accepted in the
design choice because it provides user feedback on whether something went wrong, and it provides info in the case that their input results in an error, along with instructions on how to prevent it from constantly appearing.
     
###  4.4 Database Usage (SQLite)

The project code uses SQLite for storing data on what actions were done during a user session. This database was chosen mainly because SQLite does not require numerous steps for the server process or setup.
Moreover, SQLite uses a serverless architecture for its database engine. The serverless architecture contributes to the project code by having no server process for installation, configuration,
and starting. The approach of using SQLite allows the program to store and retrieve user accounts, attendance records, and submissions. To add, SQLite supports full ACID (Atomicity, Consistency,
Isolation, Durability) transactions, helping with the data integrity of the program by not inserting corrupt or malformed data entries in the database in the scenario of system crashes.

Using SQLite has tradeoffs such as limited concurrent access handling and scalability for large user environments, which other database systems (e.g., MySQL, PostgreSQL)
can provide. These tradeoffs were accepted in the design choice because it eliminates the requirements for networked or high-concurrency database access. To add, it is acceptable given that the
project scope and expected usage scale are expected to be in the hundreds or thousands range (if not tens or hundreds of thousands of users)

## 5. References to Ethical Considerations in Programming Choices

###  5.1 User Privacy
    
To address user privacy concerns, the program system implements hashing and salting of account and attendance password through using the bcrypt(utf-8) library instead of storing credentials in
plaintext. This design decision was chosen to reduce the effects of data breaches and credential exposure of accounts and attendance in the scenario of
unauthorized database access. The structure works by hashing and salting user and attendance credentials when inserted into the ATTENDANCES table of the attendance database. To add on, sensitive data
is only used in backend-storage interactions, ensuring that sensitive data will not reach the frontend. It is additionally noted that the storage layer uses parameter placeholders to prevent unauthorized
access to attendance.db through SQL injections. Though this overall approach for user privacy does not use network-level security measures, the current security measures are appropriate for a local and
non-networked application.

###  5.2 Accessibility

The project code implements user accessibility considerations in the program by implementing a user interface that supports keyboard-based interaction. First, the program uses labeled input fields, 
navigable layouts, and pop-up messages for feedback on the event-driven GUI, errors, and status. This approach helps with clear communication to the user of what is happening. Furthermore, the user 
interface for attendances have manual date and time input supports accessibility by avoiding interface elements that require a mouse or are drag-based. Lastly, the program allows the user to switch between
using light mode and dark mode of the program, which can be found in the appearance settings of the main menu. This feature reduces the amount of light emitted by the program, which assists users who have
light sensitivity. It also helps minimize eye strain and assist users with specific eye conditions (e.g., cataracts). Though the program does not fully meet formal accessibility standards,
this tradeoff was accepted because the rest of the design choices provide reasonable usability support, given the limitations of the Tkinter library and framework.
