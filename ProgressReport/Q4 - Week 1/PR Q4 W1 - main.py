"""
Documentation of Code Progress 
Hello, po. Here is the current code as of Quarter 4 PR #1

The following changes have been labeled based on the info written in the "Progress" section in the progress report

To navigate through the changes made in the code with ease, copypaste or download the code and open it in an IDE that has Ctrl + F functionality such as VS code.

Then, to view each change, copypaste either of the following blocks of text into the ctrl + f feature of the IDE. Note that multiple code blocks may have the same label.

Text blocks (Based on progress made):
"""

# 1 - Hashed countercheck answer for attendance creation
# 2 - Applied Section Header to group code blocks by purpose
# 3 - Made back menus in attendance and settings to go to parent frame instead of going to main menu
# main.py
# 4 - Added separate function for input validation and database storage access in main attendance feature functions.
# 5 - Moved sql queries to a new code file, db.py
# 6 - Added character limits to attendance name, length, and grace period
# 7 - Replace free text entry for grace period with spinbox (incremental arrowheads)
# 8 - Applied context managers for database-concerned functions

# main.py

# 2 - Applied Section Header to group code blocks by purpose
# ===================================
# Imports

#Standard Library
import sqlite3
from datetime import datetime, timedelta

#Third-party
import bcrypt

# Tkinter
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import db
# ===================================

date_format = "%m-%d-%Y"
time_format = "%H:%M"
display_format = "%m-%d-%Y %H:%M"

# ===================================
# SQLite Storage & Tables
db_name = "attendance.db"

def get_db():
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ===================================

# 2 - Applied Section Header to group code blocks by purpose
# ===================================
# Attendance Logic

# Create Attendance

# 4 - Added separate function for input validation and database storage access in main attendance feature functions.
def store_attendance(
        attendance_name, 
        start_datetime, 
        end_datetime, 
        minutes_late, 
        attendance_password, 
        user, 
        required_countercheck, 
        question, answer
    ):

    # 8 - Applied context managers for database-concerned functions
    with get_db() as conn:
        
        # 5 - Moved sql queries to a new code file, db.py
        has_duplicate_attendance = db.check_duplicate_attendance(conn, attendance_name)

        if has_duplicate_attendance:
            display_error_attendance(
                "Attendance Error", 
                "The attendance name entered is already used by another attendance."
                "\nPlease enter a different attendance name."
            )
            return
        
        hashed_attendance_password = hash_password(attendance_password).decode("utf-8")
        
        # 1 - Hashed countercheck answer for attendance creation
        hashed_answer = None
        if required_countercheck:
            hashed_answer = hash_password(answer).decode("utf-8")

        # 5 - Moved sql queries to a new code file, db.py
        db.insert_attendance(
            conn, 
            attendance_name, 
            start_datetime, 
            end_datetime, 
            minutes_late, 
            hashed_attendance_password, 
            user, 
            required_countercheck, 
            question, 
            hashed_answer
        )

        conn.commit()

# Countercheck Answer

# 4 - Added separate function for input validation and database storage access in main attendance feature functions.
def countercheck_question():
    question = ""
    answer = ""

    required_countercheck = messagebox.askyesno("Required Countercheck", "Require counterchecking for attendees?")
    if required_countercheck:
        question = simpledialog.askstring("Countercheck Question", "Enter the counterchecking question here: ", parent=win)
        if question is None:
            return None, None, None,
        while not question.strip():
            question = simpledialog.askstring("Invalid Input", "Empty input. Enter question: ", parent=win)
            if question is None:
                return None, None, None
        answer = ""
        answer = simpledialog.askstring("Countercheck Question", "Enter the answer here: ", parent=win)
        if answer is None:
            return None, None, None
        while not answer.strip():
            answer = simpledialog.askstring("Error", "Empty input. Enter answer: ", parent=win)
            if answer is None:
                return None, None, None
    
    return question, answer, required_countercheck

# 4 - Added separate function for input validation and database storage access in main attendance feature functions.
def validate_create_attendance_inputs(attendance_name, input_start_date, input_start_time, input_end_date, input_end_time, attendance_password, minutes_late):
    fields = {

        "Attendance Name cannot be empty."
        "\nPlease enter a name for attendance (3-30 characters)": 
        attendance_name,
        
        "Start Date can not be empty."
        "\nPlease enter start date in MM-DD-YYYY (10-01-2025 for October 1, 2025)": 
        input_start_date,
        
        "Start Time can not be empty."
        "\n Please entry start time 24 hour format (e.g, 14:50 for 2:50 PM)": 
        input_start_time,
        
        "End Date can not be empty."
        "\nPlease enter end date in MM-DD-YYYY (10-02-2025 for October 2, 2025)": 
        input_end_date,
        
        "End Time can not be empty."
        "\n Please enter end time 24 hour format (e.g, 15:40 for 3:40 PM)": 
        input_end_time,

        "Attendance Password can not be empty."
        "\nPlease enter an attendace password with 10-100 Characters": 
        attendance_password,
        
        "Grace Period can not be empty."
        "\nPlease enter a grace period between 1-30 minutes": 
        minutes_late
    }

    for key, value in fields.items():
        if not value.strip():
            return "Invalid Input", key
        
    # 6 - Added character limits to attendance name, length, and grace period
    if len(attendance_name) < 3 or len(attendance_name) > 30:
        return "Invalid Input", "Please make attendance name 3-30 characters long"

    # 6 - Added character limits to attendance name, length, and grace period
    if len(attendance_password) < 10 or len(attendance_password) > 100:
        return "Invalid Input", "Please make password between 10-100 characters long"

    if not minutes_late.isdigit():
        return "Invalid Input", "Please enter minutes as a whole number"

    # 6 - Added character limits to attendance name, length, and grace period
    if int(minutes_late) < 1 or int(minutes_late) > 30:
        return "Invalid Input", "Grace period must be between 1-30 minutes"

    return None, None

# 4 - Added separate function for input validation and database storage access in main attendance feature functions.
def check_attendance_dates(input_start_date, input_start_time, input_end_date, input_end_time, minutes_late):

    try:
        input_start_date = datetime.strptime(input_start_date, date_format).date()
    except ValueError:
        return "Invalid Date", "Start Date must be in MM-DD-YYYY format\n(e.g, 10-01-2025 for October 1, 2025)"
    
    try:
        input_start_time = datetime.strptime(input_start_time, time_format).time()
    except ValueError:
        return "Inavlid Date", "Start Time must be in HH:MM in 24-Hour Format\n(e.g, 14:50 for 2:50 PM)"
        
    
    try:
        input_end_date = datetime.strptime(input_end_date, date_format).date()
    except ValueError:
        return "Error in End Date", "End Date must be in MM-DD-YYYY"
    
    try:
        input_end_time = datetime.strptime(input_end_time, time_format).time()
    except ValueError:
        return "Error in Date Time", "Date Time must be in HH:MM in 24-Hour Format"

    try:
        minutes_late = int(minutes_late)
        if minutes_late < 0:
            return "Error in Grace Period", "Minutes till late cannot be negative"
    except ValueError:
        return "Error in Grace Period", "Grace period must be a number"

    return None, None

# 4 - Added separate function for input validation and database storage access in main attendance feature functions.
def parse_attendance_dates(input_start_date, input_start_time, input_end_date, input_end_time):
    start_date = datetime.strptime(input_start_date, date_format).date()
    start_time = datetime.strptime(input_start_time, time_format).time()
    end_date = datetime.strptime(input_end_date, date_format).date()
    end_time = datetime.strptime(input_end_time, time_format).time()
    
    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(end_date, end_time)

    return start_datetime, end_datetime

# 4 - Added separate function for input validation and database storage access in main attendance feature functions.
def validate_timeframe(start_datetime, end_datetime):
    if start_datetime > end_datetime:
        return "End datetime must be after start datetime"
    if start_datetime == end_datetime:
        return "Start Time should not be the same time as end time"
    if datetime.now() > end_datetime:
        return f"The current date, {datetime.now().strftime("%B %d, %Y")}, should not be past the end datetime of the attendance."
    return None

def read_create_attendance():
    attendance_name = create_frame_name_box.get().strip()
    input_start_date = create_frame_startdate_box.get().strip()
    input_start_time = create_frame_start_time_box.get().strip()
    input_end_date = create_frame_enddate_box.get().strip()
    input_end_time = create_frame_endtime_box.get().strip()
    attendance_password = create_frame_password_box.get()
    minutes_late = create_frame_minutes_box.get().strip()
    user = win.current_user
    create_attendance(attendance_name, input_start_date, input_start_time, input_end_date, input_end_time, attendance_password, minutes_late, user)

def create_attendance(attendance_name, input_start_date, input_start_time, input_end_date, input_end_time, attendance_password, minutes_late, user):
    
    if not user:
        display_error_attendance("Attendance Error", "Please be logged in to create attendance.")
        return

    create_attendance_error, create_attendnace_message = validate_create_attendance_inputs(attendance_name, input_start_date, input_start_time, input_end_date, input_end_time, attendance_password, minutes_late)
    if create_attendance_error:
        display_error_attendance(create_attendance_error, create_attendnace_message)
        return

    possible_date_error, possible_date_message = check_attendance_dates(input_start_date, input_start_time, input_end_date, input_end_time, minutes_late)
    if possible_date_error:
        display_error_attendance(possible_date_error, possible_date_message)
        return
    
    minutes_late = int(minutes_late)

    start_datetime, end_datetime = parse_attendance_dates(input_start_date, input_start_time, input_end_date, input_end_time)
    
    timeframe_attendance_error = validate_timeframe(start_datetime, end_datetime)

    if timeframe_attendance_error:
        display_error_attendance("Error", timeframe_attendance_error)
        return

    question, answer, required_countercheck = countercheck_question()
    
    if question is None or required_countercheck is None:
        return
    
    attendance_confirm = messagebox.askyesno(
        "Confirming Attendnace Creation", 
        "Create Attendance?\n\n"
        f"Name: {attendance_name}\n"
        f"Start: {start_datetime}\n"
        f"End: {end_datetime}\n"
        f"Grace Period: {minutes_late} minutes"
    )

    if not attendance_confirm:
        clear_create_attendance()
        return

    store_attendance(attendance_name, start_datetime, end_datetime, minutes_late, attendance_password, user, required_countercheck, question, answer)

    messagebox.showinfo("Success", "Attendance created successfully")
    clear_create_attendance()
    show_frame(attendance_frame)

def search_attendance(event=None):
    query = search_box.get().strip().lower()
    for row_id in creator_table.get_children():
        values = creator_table.item(row_id, "values")
        row_text = " ".join(str(v).lower() for v in values)
        if query not in row_text:
            creator_table.detach(row_id)
        else:
            creator_table.reattach(row_id, "", tk.END)
        
def show_attendance_view():
    show_frame(view_frame)
    creator_table_rows.clear()

    for table in (creator_table, participant_table):
        for row in table.get_children():
            table.delete(row)

    user = win.current_user

    # 8 - Applied context managers for database-concerned functions
    with get_db() as conn:
        
        # 4 - Added separate function for input validation and database storage access in main attendance feature functions.
        # 5 - Moved sql queries to a new code file, db.py
        creator_info = db.get_creator_info(conn, user)

        for row in creator_info:
            row_id = creator_table.insert("", tk.END, values=row)
            creator_table_rows.append(row_id)

        """Gets info from submissions table to use for Paricipant View"""
        
        # 4 - Added separate function for input validation and database storage access in main attendance feature functions.
        # 5 - Moved sql queries to a new code file, db.py
        participant_info = db.participant_info(conn, user)

        for row in participant_info:
            participant_table.insert("", tk.END, values=row)


# Fillout Attendance

# 4 - Added separate function for input validation and database storage access in main attendance feature functions.
def punctuality_check(start_dt, end_dt, minutes_late):
    now = datetime.now()
    start_dt = datetime.fromisoformat(start_dt)
    end_dt = datetime.fromisoformat(end_dt)

    if now > end_dt:
        status = "Absent"
        late_minutes = int((now - end_dt).total_seconds() // 60)
    else:
        late_cutoff = start_dt + timedelta(minutes=minutes_late)
        if now <= late_cutoff:
            status = "On Time"
            late_minutes = 0
        else:
            status = "Late"
            late_minutes = int((now - late_cutoff).total_seconds() // 60)
    return status, late_minutes, now


def read_fillout_attendance():
    attendance_name = fillout_frame_name_box.get().strip()
    attendance_password = fillout_frame_password_box.get()
    fillout_attendance(attendance_name, attendance_password)

def fillout_attendance(attendance_name, attendance_password):

    user = win.current_user

    if not user:
        messagebox.showerror("Error", "Please be logged in to create attendance.")
        return

    if not attendance_name or not attendance_password:
        messagebox.showwarning("Error", "Please enter attendance name and password")
        return

    # 8 - Applied context managers for database-concerned functions
    with get_db() as conn:
        
        # 5 - Moved sql queries to a new code file, db.py
        existing_attendance = db.check_attendance_existance(conn, attendance_name)
    
        if not existing_attendance:
            display_error_attendance("Error in Entered Attendance", "Attendance name or password is not found or matching")
            return

        stored_name, start_dt, end_dt, minutes_late, stored_hash, countercheck, question, hashed_answer = existing_attendance
    
        if not bcrypt.checkpw(attendance_password.encode(), stored_hash.encode()):
            display_error_attendance("Error in Entered Attendance", "Attendance name or password is not found or matching.")
            return

        # 5 - Moved sql queries to a new code file, db.py
        already_submitted =  db.check_already_submmited(conn, attendance_name, user)

        if already_submitted:
            display_error_attendance("Error", "You have already submitted this attendance")
            return
    
        status, late_minutes, now = punctuality_check(start_dt, end_dt, minutes_late)

        response = ""
        if countercheck:
            response = simpledialog.askstring("Countercheck", question)
            
            if response is None:
                return
            
            if not response.strip():
                messagebox.showwarning("Error", "Countercheck Answer Required")
                return
            
            if hashed_answer:
                if not bcrypt.checkpw(response.encode(), hashed_answer.encode()):
                    messagebox.showwarning("Error", "Incorrect countercheck response")
                    return
        
        # 4 - Added separate function for input validation and database storage access in main attendance feature functions.
        # 5 - Moved sql queries to a new code file, db.py
        db.record_submission(conn, stored_name, user, now.strftime(display_format), status, late_minutes, response)
        conn.commit()

    messagebox.showinfo("Success", f"Attendance recorded: {status}")
    clear_fillout_attendance()
# ===================================

# 2 - Applied Section Header to group code blocks by purpose
# ===================================
# Navigation / Frame Management

def clear_login_frame():
    login_frame_username_box.delete(0, tk.END)
    login_frame_password_box.delete(0, tk.END)

def show_appearance_frame():
    show_frame(appearance_frame)

def clear_fillout_attendance():
    fillout_frame_name_box.delete(0, tk.END)
    fillout_frame_password_box.delete(0, tk.END)

def attendance_fillout_menu():
    show_frame(fillout_frame)

def attendance_create_menu():
    show_frame(create_frame)

def settings_menu():
    show_frame(settings_frame)

def demo_msg():
    messagebox.showwarning("Error - Part not coded", "To Be Done")

def main_menu():
    clear_create_attendance()
    clear_fillout_attendance()
    show_frame(menu_frame)

def attendance_menu():
    show_frame(attendance_frame)

def show_frame(frame):
    for f in frames:
        f.pack_forget() 
    frame.pack(pady=10)

# 4 - Added separate function for input validation and database storage access in main attendance feature functions.
def display_error_attendance(error_message, error_info):
    messagebox.showwarning(error_message, error_info)
    return

def clear_create_attendance():
    create_frame_name_box.delete(0, tk.END)
    create_frame_startdate_box.delete(0, tk.END)
    create_frame_start_time_box.delete(0, tk.END)
    create_frame_enddate_box.delete(0, tk.END)
    create_frame_endtime_box.delete(0, tk.END)
    create_frame_password_box.delete(0, tk.END)
    create_frame_minutes_box.delete(0, tk.END)

# ===================================

# 2 - Applied Section Header to group code blocks by purpose
# ===================================
# Authentication (Login & Logout / Signup)

def login():
    username = login_frame_username_box.get()
    password = login_frame_password_box.get()

    if not username or not password:
        messagebox.showwarning("Error", "Please enter username and password.")
        return

    # 8 - Applied context managers for database-concerned functions
    with get_db() as conn:
        # 5 - Moved sql queries to a new code file, db.py
        row = db.find_user(conn, username)

        if not row:
            messagebox.showwarning("Error", "Invalid username or password.")
            clear_login_frame()
            return

        stored_username, stored_hash = row

        stored_hash = stored_hash.encode("utf-8")

        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            messagebox.showwarning("Error", "Invalid username or password.")
            clear_login_frame()
            return

        #Successful login
        win.current_user = stored_username
        now = datetime.now()
        menu_frame_msg_label.config(text=f"{username} logged IN at {now.strftime("%Y-%m-%d %H:%M:%S")}")
        fillout_frame_currentuser_label.config(text=f"Current User: {username}")
        show_frame(menu_frame)

        # Log login

        # 4 - Added separate function for input validation and database storage access in main attendance feature functions.
        # 5 - Moved sql queries to a new code file, db.py
        db.timestamp(conn, username, now.isoformat())
        conn.commit()

def logout():
    logout_decision = messagebox.askyesno("Logging Out", "Are you sure you want to log out?")
    if logout_decision:
        menu_frame_msg_label.config(text="")
        win.current_user = None
        clear_login_frame()
        show_frame(login_frame)

def signup():
    username = login_frame_username_box.get()
    password = login_frame_password_box.get()

    if not username.strip():
        messagebox.showwarning("Error", "Empty Username:\nPlease enter a username")
        return

    if not all(c.isalpha() or c.isspace() for c in username):
        messagebox.showwarning("Error", "Username must contain letters and spaces only.")
        return

    if len(password) < 10:
        messagebox.showwarning("Error", "Password must be at least 10 characters long.")
        return

    # 8 - Applied context managers for database-concerned functions
    with get_db() as conn:
        
        # 4 - Added separate function for input validation and database storage access in main attendance feature functions.
        # 5 - Moved sql queries to a new code file, db.py
        found_user = db.check_duplicate_user(conn, username)

        if found_user:
            messagebox.showwarning("Error in Username", "The entered username is not available\nPlease choose another")
            clear_login_frame()
            return

        hashed = hash_password(password).decode("utf-8")

        # 4 - Added separate function for input validation and database storage access in main attendance feature functions.
        # 5 - Moved sql queries to a new code file, db.py
        db.add_user(conn, username, hashed)

        conn.commit()
    
    messagebox.showinfo("Notice", "Sign Up Successful")
    clear_login_frame()
    return

def hash_password(password):
    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(pw_bytes, salt)
    return hashed_pw
    
# ===================================

# 2 - Applied Section Header to group code blocks by purpose
# ===================================
# Theme / Appearance
def light_screen():
    apply_theme(bg="#f0f0f0", fg="black", entry_bg="white")
    messagebox.showinfo("Background Change", "Light Mode Enabled")

def dark_screen():
    apply_theme(bg="#1c1c1c", fg="white", entry_bg="#2b2b2b")
    messagebox.showinfo("Background Change", "Dark Mode Enabled")

def apply_theme(bg, fg, entry_bg):
    win.configure(bg=bg)

    for frame in frames:
        frame.configure(bg=bg)

        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=bg, fg=fg)
            
            if isinstance(widget, tk.Button):
                widget.configure(bg=entry_bg, fg=fg, activebackground=bg)
            
            if isinstance(widget, tk.Entry):
                widget.configure(bg=entry_bg, fg=fg, insertbackground=fg)
# ===================================

# 2 - Applied Section Header to group code blocks by purpose
# ===================================
# UI Construction
def update_clock():
    """Updates the clock in the main menu every second"""
    current_time = datetime.now().strftime("%B %d, %Y - %H:%M:%S (%a)")
    menu_frame_time_label.config(text=f"Current time: {current_time}")
    win.after(1000, update_clock)

win = tk.Tk()

# 5 - Moved sql queries to a new code file, db.py
db.init_db()

style = ttk.Style()
style.theme_use("default")

style.configure(
    "Treeview",
    background="#2b2b2b",
    foreground="white",
    fieldbackground="#2b2b2b"
)

style.configure(
    "Treeview.Heading",
    background="#1c1c1c",
    foreground="white"
)

win.title("Attendance Checker")
win.current_user = None
win.geometry("1200x900")
win.resizable(False, False)

login_frame = tk.Frame(win)
menu_frame = tk.Frame(win)
attendance_frame = tk.Frame(win)
create_frame = tk.Frame(win)
settings_frame = tk.Frame(win)
fillout_frame = tk.Frame(win)
appearance_frame = tk.Frame(win)
view_frame = tk.Frame(win)

frames = [
    login_frame, 
    menu_frame, 
    attendance_frame, 
    create_frame, 
    view_frame,
    fillout_frame,
    settings_frame,
    appearance_frame
]

title = tk.Label(win, text="Attendance Checker", font=("Montserrat", 24))
title.pack(pady=(10,10))

menu_time = datetime.now().strftime("%B %d, %Y - %H:%M:%S (%a)")

#Login Frame
login_frame_username_label = tk.Label(login_frame, text="Enter Account Name (Letters and Spaces only):", font=("Arial", 12))
login_frame_username_box = tk.Entry(login_frame, width=30)
login_frame_password_label = tk.Label(login_frame, text="Enter Password (10+ Characters Required):", font=("Arial", 12))
login_frame_password_box = tk.Entry(login_frame, width=30, show="*")
login_frame_signup_btn = tk.Button(login_frame, text="Sign Up", width=15, font=("Montserrat", 12), command=signup)
login_frame_login_btn = tk.Button(login_frame, text="Log In", width=15, font=("Montserrat", 12), command=login)

login_frame_widgets = [
    login_frame_username_label, 
    login_frame_username_box, 
    login_frame_password_label,
    login_frame_password_box, 
    login_frame_signup_btn, 
    login_frame_login_btn
]
for login_widgets in login_frame_widgets:
    login_widgets.pack(pady=5)

#Main Menu Frame
menu_frame_msg_label = tk.Label(menu_frame, text="", fg="green", font=("Arial", 12))
menu_frame_time_label = tk.Label(menu_frame, text=f"Current time: {menu_time}", font=("Arial", 12))
menu_frame_menu_label = tk.Label(menu_frame, text="Main Menu", font=("Arial", 12))
menu_frame_attendance_btn = tk.Button(menu_frame, text="Attendance", width=15, font=("Montserrat", 12), command=attendance_menu)
menu_frame_settings_btn = tk.Button(menu_frame, text="Settings", width=15, font=("Montserrat", 12), command=settings_menu)
menu_frame_logout_btn = tk.Button(menu_frame, text="Log Out", width=15, font=("Montserrat", 12), command=logout)

menu_frame_widgets = [
    menu_frame_msg_label, 
    menu_frame_time_label, 
    menu_frame_menu_label, 
    menu_frame_attendance_btn, 
    menu_frame_settings_btn, 
    menu_frame_logout_btn
]

for menu_widgets in menu_frame_widgets:
    menu_widgets.pack(pady=5)

# Sub-menu Attendance Frame
attendance_frame_attendance_label = tk.Label(
    attendance_frame, 
    text="Attendance Options", 
    font=("Arial", 12)
)

attendance_frame_attendance_create_btn = tk.Button(attendance_frame, text="Create Attendance", width=15, font=("Montserrat", 12), command=attendance_create_menu)
attendance_frame_attendance_view_btn = tk.Button(attendance_frame, text="View Attendances", width=15, font=("Montserrat", 12), command=show_attendance_view)
attendance_frame_attendance_fillout_btn = tk.Button(attendance_frame, text="Fill out Attendance", width=15, font=("Montserrat", 12), command=attendance_fillout_menu)
attendance_frame_back_btn = tk.Button(attendance_frame, text="Back", width=15, font=("Montserrat", 12), command=main_menu)

attendance_frame_widgets = [
    attendance_frame_attendance_label, 
    attendance_frame_attendance_create_btn, 
    attendance_frame_attendance_view_btn, 
    attendance_frame_attendance_fillout_btn, 
    attendance_frame_back_btn
]

for attendance_widgets in attendance_frame_widgets:
    attendance_widgets.pack(pady=5)

# Attendance Frame: Create
today = datetime.now().strftime("%m-%d-%Y")

create_frame_label = tk.Label(create_frame, text="Create Attendance", font=("Arial", 15))

create_frame_name_label = tk.Label(create_frame, text="Attendance Name: ", font=("Arial", 12))
create_frame_name_box = tk.Entry(create_frame, width=30)

# Start datetime
# ----------
create_frame_startdate_label = tk.Label(create_frame, text="Start: Date checking attendance (MM-DD-YYYY): ", font=("Arial", 12))
create_frame_startdate_box = tk.Entry(create_frame, width=15)
create_frame_startdate_box.insert(0, today)

create_frame_start_time_label = tk.Label(create_frame, text="Start: Time checking attendance (HH:MM): ", font=("Arial", 12))
create_frame_start_time_box = tk.Entry(create_frame, width=15)

# ----------

# End datetime
# ----------
create_frame_enddate_label = tk.Label(create_frame, text="End: Date checking attendance (MM-DD-YYYY): ", font=("Arial", 12))
create_frame_enddate_box = tk.Entry(create_frame, width=15)

create_frame_endtime_label = tk.Label(create_frame, text="End: Time checking attendance (HH:MM): ", font=("Arial", 12))
create_frame_endtime_box = tk.Entry(create_frame, width=15)

create_frame_enddate_box.insert(0, today)

# ----------

create_frame_notice_label = tk.Label(create_frame, text="*Use 24-hour format", font=("Arial", 10))

create_frame_minutes_late = tk.Label(create_frame, text="Grace Period (Minutes)", font=("Arial", 12))

# 7 - Replace free text entry for grace period with spinbox (incremental arrowheads)
create_frame_minutes_box = tk.Spinbox(create_frame, from_=1, to=30, width=13)

create_frame_password_label = tk.Label(create_frame, text="Assign attendance a password: ", font=("Arial", 12))
create_frame_password_box = tk.Entry(create_frame, width=30, show="*")
create_attendance_btn = tk.Button(create_frame, text="Make attendance", width=15, font=("Montserrat", 12), command=read_create_attendance)

# 3 - Made back menus in attendance and settings to go to parent frame instead of going to main menu
create_menu_btn = tk.Button(create_frame, text="Back", width=15, font=("Montserrat", 12), command=attendance_menu)

create_widgets = [
    create_frame_label,
    create_frame_name_label,
    create_frame_name_box,

    create_frame_startdate_label,
    create_frame_startdate_box,
    create_frame_start_time_label,
    create_frame_start_time_box,

    create_frame_enddate_label,
    create_frame_enddate_box,
    create_frame_endtime_label, 
    create_frame_endtime_box,
    create_frame_notice_label, 

    create_frame_password_label, 
    create_frame_password_box,

    create_frame_minutes_late,
    create_frame_minutes_box,

    create_attendance_btn,
    create_menu_btn
]

for create_widget in create_widgets:
    create_widget.pack(pady=5)

# Attendance Frame: Fill out
fillout_frame_currentuser_label = tk.Label(fillout_frame, text=f"Current User: {win.current_user}", font=("Arial", 12))
fillout_frame_attendance_label = tk.Label(fillout_frame, text=f"Enter Attendance Name", font=("Arial", 12))
fillout_frame_name_box = tk.Entry(fillout_frame, width=30)
fillout_frame_password_label = tk.Label(fillout_frame, text="Enter Attendance Password", font=("Arial", 12))
fillout_frame_password_box = tk.Entry(fillout_frame, width=30, show="*")
fillout_frame_record_btn = tk.Button(fillout_frame, text="Record Attendance", width=15, font=("Montserrat", 12), command=read_fillout_attendance)

# 3 - Made back menus in attendance and settings to go to parent frame instead of going to main menu
fillout_menu_btn = tk.Button(fillout_frame, text="Back", width=15, font=("Montserrat", 12), command=attendance_menu)

fillout_frame_widgets = [
    fillout_frame_currentuser_label, 
    fillout_frame_attendance_label, 
    fillout_frame_name_box, 
    fillout_frame_password_label, 
    fillout_frame_password_box, 
    fillout_frame_record_btn,
    fillout_menu_btn
]

for fillout_widgets in fillout_frame_widgets:
    fillout_widgets.pack(pady=5)

# Settings Frame
settings_frame_label = tk.Label(settings_frame, text="Settings", font=("Arial", 12))
settings_frame_password_btn = tk.Button(settings_frame, text=f"Reset Password", width=15, font=("Montserrat", 12), command=demo_msg)
settings_attendance_btn = tk.Button(settings_frame, text ="Attendance", width=15, font=("Montserrat", 12), command=demo_msg)
settings_frame_appearance_btn = tk.Button(settings_frame, text="Personalization", width=15, font=("Montserrat", 12), command=show_appearance_frame)
settings_frame_accessibility_btn = tk.Button(settings_frame, text=f"Accessibility", width=15, font=("Montserrat", 12), command=demo_msg)

# 3 - Made back menus in attendance and settings to go to parent frame instead of going to main menu
setting_menu_btn = tk.Button(settings_frame, text="Back", width=15, font=("Montserrat", 12), command=main_menu)

settings_widgets = [
    settings_frame_label, 
    settings_frame_password_btn,
    settings_attendance_btn,
    settings_frame_appearance_btn,
    settings_frame_accessibility_btn,
    setting_menu_btn
]

for setting_widget in settings_widgets:
    setting_widget.pack(pady=5)

# Settings - Appearance Frame
appearance_frame_light_btn = tk.Button(appearance_frame, text=f"Light Mode", width=30, font=("Montserrat", 12), command=light_screen)
appearance_frame_dark_btn = tk.Button(appearance_frame, text=f"Dark Mode", width=30, font=("Montserrat", 12), command=dark_screen)

# 3 - Made back menus in attendance and settings to go to parent frame instead of going to main menu
accessibility_menu_btn = tk.Button(appearance_frame, text="Back", width=15, font=("Montserrat", 12), command=settings_menu)

appearance_widgets = [
    appearance_frame_light_btn, 
    appearance_frame_dark_btn, 
    accessibility_menu_btn
]

for appearance_widget in appearance_widgets:
    appearance_widget.pack(pady=5)

# View Attendance

# Title
view_title_label = tk.Label(view_frame, text="View Attendances", font=("Arial", 14))
view_title_label.pack(pady=10)

# Search box for creator table
search_label = tk.Label(view_frame, text="Search Attendance:")
search_label.pack()
search_box = tk.Entry(view_frame, width=30)
search_box.pack(pady=5)

search_box.bind("<KeyRelease>", search_attendance)

# Creator Table
creator_table_label = tk.Label(view_frame, text="Creator View: Attendances Made", font=("Arial", 12))
creator_table_label.pack(pady=5)

creator_table = ttk.Treeview(view_frame, columns=("Attendance", "User", "Time Recorded", "Status", "Minutes Late ", "Response"), show="headings", height=8)
for col in creator_table["columns"]:
    creator_table.heading(col, text=col)
creator_table.pack(pady=5)
creator_table_rows = []

# Participant Table
participant_table_label = tk.Label(view_frame, text="Participant View: Your Attendances", font=("Arial", 12))
participant_table_label.pack(pady=5)

participant_table = ttk.Treeview(
    view_frame,
    columns=("Attendance", "Status", "Time Recorded", "User", "Response"),
    show="headings",
    height=8
)
for col in participant_table["columns"]:
    participant_table.heading(col, text=col)
participant_table.pack(pady=5)

# 3 - Made back menus in attendance and settings to go to parent frame instead of going to main menu
view_frame_menu_btn = tk.Button(view_frame, text="Back", width=15, font=("Montserrat", 12), command=attendance_menu)
view_frame_menu_btn.pack(pady=10)


show_frame(login_frame)
update_clock()
win.mainloop()
# ===================================
