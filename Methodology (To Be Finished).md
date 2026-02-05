# TO BE FINISHED
## For now, please ignore this file because it is currently not final and will be updated.

# Detailed Methodology
## Methodology Contents
## 1. Implementation of Core Features
###   1.1 Log in and Log Out
###     1.1.1 Log In
###     1.1.2 Log Out
###     1.1.3 Account Creation (Sign Up)
##    1.2 Attendance Features
###      1.2.1 Create Attendance
###      1.2.2 View Attendance/s
###      1.2.3 Fill Out Attendance
## 2. Technologies Used (with justification)
###  2.1 Python
###  2.2 Tkinter
###  2.3 bcrypt (Additionally known as Blowfish crypt)
###  2.4 SQLite
## 3. Backend-frontend communication
###  3.1 Tkinter (Frontend)
###  3.2 Python (Backend)
###  3.3 SQLite (Storage)
## 4. Key Design decisions or Trade-offs
###  4.1 Manual Date and Time Input
###  4.2 Single-file Architecture
###  4.3 Pop-up validation messages
###  4.4 Database Usage (SQLite)
## 5. References to Ethical Considerations in Programming Choices
###  5.1 User Privacy
###  5.2 Data Minimization
###  5.3 Accessibility

## Methodology

## 1. Implementation of Core Features
The following content in Section 1 of the methodology contains how were the features of the Self-Record Attendance System were implementated. 
Currently, there are three main features made: user authentication feature, atendance Feature, and system time feature.

Note for 1.1 and 1.2: Both their flow and system during the connection of SQLite use parameter placeholders (?) during retrieval (SELECT) and inserting (INSERT) of data. This is used to prevent SQL injection,
a type of injection code attack that results in the backend of applications to run SQL queries or commands that can result in data breach effects such as database comprimisation (Happens when user enters the
commands in empty fields or input).
### 1.1 Log in and Log Out

#### 1.1.1 Log in

The login system of the program was implemented using an account name and hashed password system. A login system was used instead of directly showing the user the main menu in order to implement current user
session tracking. The current user tracking is implemented to prevent users from falsifying attendance record through impersonation of another user.

When the user presses log in, the login system checks whether there are empty inputted login credentials. If there empty credentials, the user would be notified about it with a pop-up message, and will be asked
to enter the missing login credentials/s. Next, the program checks if the entered login credentials appear in the USERS table in the database. 

If the entered account name is not stored in the USERS table, the program notifies the user about it and asks user to reenter login credentials. The comparison of whether the account name is stored in the USERS
table is case-insensitive.

If the entered account name is found, the login system checks if the entered password corresponds to the stored, hashed password in the USERS table in the database. If the user did not enter their account
password, the program would notify the user about it. Otherwise, the program proceeds, and uses bcrypt.checkpw() to check verify whether the entered account password matches with the entered account name.

bcrypt.checkpw() is used because when the user signs up, their password is hashed and salted and stored in the USERS table 

bcrypt.checkpw() works by taking in the following arguments as follows:

bcrypt.checkpw(plain_string.encode(), hashed_string.encode())

The bcrypt.checkpw() hashes the plain string and uses the salt from the hashed string. If both of the salted and hashed strings match, then the user successfully logs in, and is shown the main menu of the program. The program additionally tracks who is the current user. Otherwise, the program informs the user that the password is incorrect.

#### 1.1.2 Log Out

In the main menu of the program, the user can click "log out" to log out of the program. When they do so, they are asked first, to confirm that they intend to logout. This is to prevent accidental log out, 
and make the user enter their login credentials again. If the user clicks "Yes" in the log out confirm prompt, then they would log out and be shown the login menu. Otherwise, if the user clicks "No", then they
would be shown the attendance menu, and nothing happens.

#### 1.1.3 Account Creation (Sign Up)

A sign up system and sub-feature was implemented for the login and log out feature because of three main reasons:

1. The user wouldn't have an account unless they would manually make an account through a data storage
2. Manually adding users would take significant time, especially because you need to consider how the data will be inputted (e.g, hashed passwords will need to be entered).
3. Manually adding users would not scale well with tens or hundreds of users.

The sign up feature works by taking in what the user has entered when they entered an account name and an account password. First, the sign up system checks if the user has entered empty sign up credentials, 
and informs the user about it if there are. Then, the program checks if the entered sign up credentials match the requirements stated in the log in menu.

Account Name: Only Letters and Spaces (Spaces by themself will not be accepted, as it can confuse users when the an non-named user submits attendance, and the submission in View Attendances shows their name 
as whitspace)

Password: At least 10 characters

If the entered sign up details do not match the specifications, then the user is informed about it and is asked to change their sign up details. Otherwise, the sign up system accepts the account name, hashes
and salts the entered account password through bcrypt, inserts the sign up credentials in the USERS table, and prompts the user that they successfully signed up.

### 1.2 Attendance Feature

#### 1.2.1 Create Attendance
The create attendance feature is implemented to make attendances in the program and add additional parts such as attendance password and counterchecking question to help with the data integrity of the program. 
First, the program asks the user to input the start/end date (MM-DD-YYYY), start/end time (24-hour format), attendance password, grace period (asks a number for minutes until considered late), and optional 
countercheck question with answer (Via pop-up message). Then, the program takes in the create attendance info and checks if any of the conditions occur:
- Start or End Date is not in the MM-DD-YYYY format
- Start or End Time is not in 24-hour format
- End Time is earlier than Start Time
- Start Time is at the same time as End time
- Either Start/End Date/Time is whitespace
- Attendance Password is less than 10 characters
- Grace period is either less than 0 minutes or is not a number
- Empty countercheck question or answer
If so, the program notifies the user about this through a pop-up. Otherwise the program parses (converting raw text data into a useable format for the program) the dates via .striptime() and .combine(), hashes
the attendance password, inserts the data into the ATTENDANCES table in the SQLite database, and give the user a pop-up message saying that the attendance was made.
Data stored in the ATTENDANCE table:
- Attendance Name
- Start Datetime
- End Datetime
- Grace period (The acutal code variable is minutes_lates)
- Hashed Attendance Password
- Account name of the user who created said attendance
- Int value of countercheck (Whether user clicked "Yes" or "No" when asked about adding countercheck quesion)
- Question (Empty String if user clicked "No")
- Answer (Empty String if user clicked "No")

#### 1.2.2 View Attendances
The purpose of the view attendances feature is for viewing the attendances made, who recorded their attendance, and the attendances that the user has filled out. First, the feature utilizes 2 tables by
using treeview, and using the following column names:
Creator View:
- Attendance Name
- User who filled out attendance
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
Additionally, the feature stores the current session account name and deletes all existing rows in both of the tables in order to not make old data stay there. Then, for, the creator table uses the ATTENDANCE
 table from the SQLite database to retrieve and populate the creator table (WHERE a.creator is used so that it only shows attendances made by the current user. Additionally, it uses LEFT JOIN
(during the database cur.execute) to give all submissions for an attendance. It get all fetched rows and iterates them in the table

On the other hand, the participant table is populated by getting the data entries form the SUBMISSIONS table in the database that the current user has filled out. Then, each submission made by the current user
is iterated in the participant table.

#### 1.2.3 Fill Out Attendance
The fill out attendance is a sub-feature of the 2nd Core feature of the program (Attendance Feature) that allows participants to record their attendance. The following describes how it was implemented
First, the fill out feature uses texts (tk.Label) and fields (tk.Entry) to allow the user to enter the attendance name and attendance password (for recording their attendance). Then, the program takes in the 
user's input and checks if the inputted fill out info is white space (Notifies user about it). Then, the fill out flow system retrieves the data from the ATTENDANCE table in the SQLite attendance.db to first
check if the entered attendance name is stored and exists. After that, the program uses bcrypt.checkpw() to compare the attendance password entered by the user with the hashed password corresponding to the
found attendance (By hashing the enetered attendance password and using the hashed password's salt to deterimene if both of the hashed strings match). 

If they match, the program then checks if the user has already submitted there attendance using a cur.execute that fetches the data from the SUBMISSIONS table and uses "if cur.fetchone()" to check if the 
user's attendance submission to that attendance exists. Otherwise, the fillout logic flow gets the current time (of when the user has submiited their attendance) and compares it with the start datetime and 
end datetime. If the current time is past the end datetime, then the status of the user is recorded as absent, and calculate how many minutes late they were. If they weren't late, but their time of submission
is past the grace period, then their attendance status of the user is marked late, and, again, calculates how many minutes late they were. Otherwise, they would be marked On time with 0 late minutes.

After that portion, the program checks if the filled out attendance uses a countercheck question. If there is, the user is prompted the question and must provide the correct answer for the countercheck
question before they can be done filling out the attendance. This section of the program addtionally checks if the entered input has whitescpace or not, and prompts te user to answer the question.

Finally, a connection and cursor is used for inserting the recording of attendnce in the SUBMISSION table in the attendance.db. Then, the user is prompted that their attendance was recordrd, along with their
punctuality status.
