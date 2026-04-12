"""
IMPORTANT 
Note: Please run the following program by inputting the following lines in terminal:

1. cd "C:/[Parent Directory]/[Other Parent Directory]/Desktop"
As long as the attendance_app folder is at desktop directory


2. python -m attendance_app.main
This is because the code program uses relative importing, so things may not run properly if you use other ways to run the code.
"""

# ===================================
# Imports

#Standard Library
import sqlite3
from typing import Callable, Optional
from datetime import datetime, timedelta

#Third-party
import bcrypt
from tkcalendar import DateEntry

# Tkinter
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, messagebox, simpledialog

# Code Files
from .db import db
from attendance_app.utils import validators, constants
from attendance_app.services import auth_service, attendance_service
# ===================================

# ===================================
# SQLite Storage & Tables
db_name = "attendance.db"

def get_db():
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
# ===================================

# main.py

# ===================================
# Attendance Logic
class attendance_session():
    def __init__(self):
        self.attendance_id = None
        self.attendance_grade = None
        self.attendance_section = None


def read_attendance_input():
    entered_attendance_grade =  selected_attendance_grade.get()
    entered_attendance_section = selected_attendance_section.get()
    entered_attendance_subject = selected_attendance_subject.get()
    entered_attendance_date = attendance_date_picker.get()
    entered_attendance_period = attendance_start_period_spinbox.get()

    attendance_creation_results = attendance_service.process_attendance_creation(
        entered_attendance_grade, entered_attendance_section,
        entered_attendance_subject, entered_attendance_date,
        entered_attendance_period, current_session.given_name,
        current_session.surname
    )

    if attendance_creation_results["error_status"]:
        display_warning(
            attendance_creation_results["error_type"],
            attendance_creation_results["error_message"]
        )
        return
    
    display_info("Info", "Attendance has been successfully made.\n\nProceeding to attendance dashboard:")
    show_dashboard_frame()
    show_frame(dashboard_frame)
    return

def show_dashboard_frame():
    show_frame(dashboard_frame)
    attend_attendance_info.config(text="")

    current_attendance.attendance_id = None
    current_attendance.attendance_grade = None
    current_attendance.attendance_section = None

    for row in dashboard_table.get_children():
        dashboard_table.delete(row)
    
    
    creator_given_name = current_session.given_name
    creator_surname =  current_session.surname
    creator_full_name =  " ".join((creator_given_name, creator_surname))
    
    with get_db() as conn:
        attendance_dashboard_info = db.get_dashboard_table_info(conn, creator_full_name)
    
    for info in attendance_dashboard_info:
        row_id = dashboard_table.insert("", tk.END, values=info)


def read_selected_attendance(event):
    selected_row = dashboard_table.focus()
        
    if not selected_row:
        return

    attendance_marking_table_rows.clear()
    show_frame(attendance_marking_frame)
    attendance_marking_query.focus()

    dashborad_row_values = dashboard_table.item(selected_row, 'values')
    attendance_id = dashborad_row_values[0]
    attendance_date = datetime.strptime(dashborad_row_values[1], "%Y-%m-%d")
    attendance_grade = dashborad_row_values[2]
    attendance_section = dashborad_row_values[3]
    attendance_subject =  dashborad_row_values[4]
    attendance_period = dashborad_row_values[5]

    current_attendance.attendance_id = attendance_id
    current_attendance.attendance_grade = attendance_grade
    current_attendance.attendance_section = attendance_section

    attend_attendance_info.config(text=f"Grade {attendance_grade} - {attendance_section} | {attendance_subject} | Period {attendance_period} | {attendance_date}")


    with get_db() as conn:
        populate_attendance_marking_table(conn, attendance_id, attendance_grade, attendance_section)
    
def populate_attendance_marking_table(conn, attendance_id, attendance_grade, attendance_section):
    
    for row in attendance_table.get_children():
        attendance_table.delete(row)
    
    attendance_marking_info = db.get_attendance_marking_info(
        conn, attendance_id, 
        attendance_grade, attendance_section)
        
    for attendance_info in attendance_marking_info:
        row_id = attendance_table.insert("", tk.END, values=attendance_info)
        attendance_marking_table_rows.append(attendance_info)

def filter_marking_table(event):
    attendance_filter = attendance_marking_query.get().strip().lower()

    for row in attendance_table.get_children():
        attendance_table.delete(row)

    for row in attendance_marking_table_rows:
        student_first_name = row[1]
        student_surname = row[2]

        student_full_name = " ".join([student_first_name, student_surname]).lower()

        if attendance_filter in student_full_name:
            attendance_table.insert("", tk.END, values=row)


def record_attendance_marking():
    selected_student_id = attendance_student_id_spinbox.get().strip()
    attendance_punctuality = selected_attendance_punctuality.get()
    tardy_minutes = attendance_tardy_minutes_spinbox.get()
    cutting_minutes = attendance_cutting_minutes_spinbox.get()
    attendance_id = current_attendance.attendance_id
    
    if attendance_punctuality == "Present" or attendance_punctuality == "Absent":
        tardy_minutes = 0
        cutting_minutes = 0

    validator_error, validator_message = validators.validate_attendance_marking(
        selected_student_id, attendance_punctuality, tardy_minutes,
        cutting_minutes
    )

    if validator_error:
        display_warning(validator_error, validator_message)
        return
    
    with get_db() as conn:
        found_attendance_record = db.check_attendance_record(conn, selected_student_id, attendance_id)
        
        if not found_attendance_record:
            display_warning("Input Error","The entered student ID is not part of the following attendance.\nPlease enter a student ID that is part of the attendance.")
            return
        
        db.update_attendance_record(
            conn, attendance_punctuality,
            tardy_minutes, cutting_minutes,
            attendance_id, selected_student_id)
        
        populate_attendance_marking_table(
        conn,
        current_attendance.attendance_id, 
        current_attendance.attendance_grade, current_attendance.attendance_section)


# ===== v0.4.0 =====
# Create Attendance
def store_attendance(
        attendance_name, start_datetime, 
         end_datetime, minutes_late, 
         attendance_password, user, 
         required_countercheck, question, 
         answer):
    
    with get_db() as conn:
        
        if db.check_duplicate_attendance(conn, attendance_name):
            display_warning("Attendance Error", "The attendance name entered is already used by another attendance.\nPlease enter a different attendance name.")
            return
        
        hashed_attendance_password = hash_password(attendance_password).decode("utf-8")
        
        
        hashed_answer = None
        if required_countercheck:
            hashed_answer = hash_password(answer).decode("utf-8")

        
        db.insert_attendance(
            conn, attendance_name, 
            start_datetime, end_datetime, 
            minutes_late, hashed_attendance_password, 
            user, required_countercheck, 
            question, hashed_answer)

        conn.commit()

def countercheck_question():
    question = ""
    answer = ""

    required_countercheck = yes_or_no("Required Countercheck", "Require counterchecking for attendees?")
    if required_countercheck:
        question = simpledialog.askstring(
            "Countercheck Question", 
            "Enter the question here: ", 
            parent=win
            )
        
        if question is None:
            return None, None, None
        
        while not question.strip():
            question = simpledialog.askstring("Invalid Input", "Countercheck question cannot be empty. Enter question: ", parent=win)
            
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

def parse_attendance_dates(input_start_date, input_start_time, input_end_date, input_end_time):
    start_date = datetime.strptime(input_start_date, "%m-%d-%Y").date()
    start_time = datetime.strptime(input_start_time, "%H:%M").time()
    end_date = datetime.strptime(input_end_date, "%m-%d-%Y").date()
    end_time = datetime.strptime(input_end_time, "%H:%M").time()
    
    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(end_date, end_time)

    return start_datetime, end_datetime

def read_create_attendance():
    # Read UI input
    attendance_name = create_frame_name_box.get().strip()
    input_start_date = create_frame_startdate_calendar.get()
    input_start_time = create_frame_start_time_box.get()
    input_end_date = create_frame_enddate_calendar.get().strip()
    input_end_time = create_frame_endtime_box.get().strip()
    attendance_password = create_frame_password_box.get()
    minutes_late = create_frame_minutes_box.get().strip()
    user = user_session.username

    create_attendance(
        attendance_name, input_start_date, 
         input_start_time, input_end_date, 
         input_end_time, attendance_password, 
         minutes_late, user)

def create_attendance(
        attendance_name, input_start_date, 
         input_start_time, input_end_date, 
          input_end_time, attendance_password, 
          minutes_late, user):

    error_status, error_title, error_message, attendance_info = attendance_service.validate_create_input(
        attendance_name, input_start_date, 
         input_start_time, input_end_date, 
         input_end_time, attendance_password, 
         minutes_late, user
    )
    
    if error_status:
        display_warning(error_title, error_message)
        return
    
    start_datetime = attendance_info["start_datetime"]
    end_datetime = attendance_info["end_datetime"]
    minutes_late = attendance_info["minutes_late"]

    question, answer, required_countercheck = countercheck_question()
    
    if question is None or answer is None or required_countercheck is None:
        display_info("Cancelled", "Action cancelled.")
        return
    
    attendance_confirm = yes_or_no(
        "Confirming Attendance Creation", 
        "Create Attendance?\n\n"
        f"Name: {attendance_name}\n"
        f"Start: {start_datetime}\n"
        f"End: {end_datetime}\n"
        f"Grace Period: {minutes_late} minutes"
    )

    if not attendance_confirm:
        return

    store_attendance(attendance_name, start_datetime, end_datetime, minutes_late, attendance_password, user, required_countercheck, question, answer)

    display_info("Info", "Attendance created successfully.\nTry Checking 'View Attendances' to check updates/records on it.")
    clear_create_attendance()
    show_frame(attendance_frame)

def search_attendance(event=None):
    query = search_box.get().strip().lower()

    # Clear table
    for row in creator_table.get_children():
        creator_table.delete(row)

    # Reinsert filtered rows
    for row in creator_table_rows:
        row_text = " ".join(str(v).lower() for v in row)
        
        if query in row_text:
            creator_table.insert("", tk.END, values=row)

        
def show_attendance_view():
    show_frame(view_frame)
    search_box.focus()
    creator_table_rows.clear()

    for table in (creator_table, participant_table):
        for row in table.get_children():
            table.delete(row)

    user = user_session.username

    
    with get_db() as conn:
        
        creator_info = db.get_creator_info(conn, user)

        for row in creator_info:
            row_id = creator_table.insert("", tk.END, values=row)
            creator_table_rows.append(row)

        # Gets info from submissions table to use for Paricipant View
        
        participant_info = db.participant_info(conn, user)

        for row in participant_info:
            participant_table.insert("", tk.END, values=row)

# Fillout Attendance

def punctuality_check(start_dt, end_dt, minutes_late):
    now = datetime.now()
    start_dt = datetime.fromisoformat(start_dt)
    end_dt = datetime.fromisoformat(end_dt)

    late_cutoff = start_dt + timedelta(minutes=minutes_late)
    if now <= late_cutoff:
        status = "On Time"
        late_minutes = 0
    else:
        status = "Late"
        late_minutes = int((now - late_cutoff).total_seconds() // 60)
    return status, late_minutes, now

def handle_countercheck(question):
    response = simpledialog.askstring("Countercheck Question", question)
    return response

# ====================================

def read_fillout_attendance():
    attendance_name = fillout_frame_name_box.get().strip()
    attendance_password = fillout_frame_password_box.get()
    user = user_session.username
    fillout_attendance(user, attendance_name, attendance_password)

def fillout_attendance(user, attendance_name, attendance_password):
    
    with get_db() as conn:
        process_fillout_results = attendance_service.validate_fillout_input(user, attendance_name, attendance_password)
        if process_fillout_results["error_status"]:
            display_warning(
                process_fillout_results["error_type"],
                process_fillout_results["error_message"]
            )    
            return
    
        attendance_data = process_fillout_results["data"]
        
        stored_name = attendance_data["stored_name"]
        start_datetime = attendance_data["start_datetime"]
        end_datetime = attendance_data["end_datetime"]
        minutes_late = attendance_data["minutes_late"]
        countercheck = attendance_data["countercheck"]
        question = attendance_data["question"]
        hashed_answer = attendance_data["hashed_answer"]

        status, late_minutes, now = punctuality_check(start_datetime, end_datetime, minutes_late)

        response = ""

        if countercheck:
            response = handle_countercheck(question)
            process_countercheck_results = attendance_service.validate_countercheck_input(response, hashed_answer)
            
            if process_countercheck_results["error_status"]:
                display_warning(
                    process_countercheck_results["error_type"],
                    process_countercheck_results["error_message"]
                )
                return
        
        db.record_submission(conn, stored_name, user, now, status, late_minutes, response)
        conn.commit()

    display_info(
        "Info",
        f"Attendance has been successfully recorded."
        f"\nPunctuality Status: {status}"
        f"\nMinutes Late: {late_minutes}"
        )
    clear_fillout_attendance()
    return
# ===================================

# ===================================
# Authentication (Login & Logout / Signup)


class account_session:
    def __init__(self):
        self.given_name = None
        self.surname = None
        self.role = None


def clean_text(text):
    return " ".join(text.split()) if text else ""

def process_account_creation():
    entered_given_name = clean_text(given_name_entry.get())
    entered_surname = clean_text(surname_entry.get())
    entered_identifier =  clean_text(identifier_signup_entry.get())
    grade_level = selected_grade_level.get()
    grade_section = selected_grade_section.get()
    role = selected_account_role.get()
    
    entered_password = account_password_entry.get()
    
    process_account_results = auth_service.process_account(
        entered_given_name, entered_surname,
        entered_password, role,
        grade_level, grade_section, entered_identifier
    )

    if process_account_results["error_status"]:
        display_warning(
            process_account_results["error_type"],
            process_account_results["error_message"]
        )
        return
    
    display_info(
        process_account_results["error_type"],
        process_account_results["error_message"]
    )
    clear_signup_page()
    return

def read_login_entries():
    entered_password = login_password_entry.get()
    entered_identifier = login_identifier_entry.get()
    process_login(entered_password, entered_identifier)

def process_login(entered_password, entered_identifier):
    login_results = auth_service.process_account_login(
        entered_password, entered_identifier
    )
    if login_results["error_status"]:
        display_warning(
            login_results["error_type"],
            login_results["error_message"],
        )

        clear_login_page()
        return
    

    account_data = login_results["data"]
    account_given_name = account_data["given_name"]
    account_surname = account_data["surname"]
    account_role = account_data["role"]

    current_session.given_name = account_given_name
    current_session.surname = account_surname
    current_session.role = account_role

    clear_login_page()

    if current_session.role == "Teacher":
        show_frame(teacher_frame)
    if current_session.role == "Student":
        display_info("Info", "Main Menu for Students: \nTo Be Added")
    return
    


# 0.4.0 Code
class current_user:
    def __init__(self):
        self.username = None

def login():
    username = login_frame_username_box.get()
    password = login_frame_password_box.get()

    error_status, login_error, login_message, stored_username = auth_service.process_login(username, password)
    if error_status:
        display_warning(login_error, login_message)
        clear_login_frame()
        return

    # Successful login
    user_session.username = stored_username
    now = datetime.now()
    menu_frame_login_label.config(text=f"Login Time: {now.strftime('%B %d, %Y - %H:%M:%S')}")
    fillout_frame_current_user_label.config(text=f"Current User: {user_session.username}")
    show_frame(menu_frame)

def logout():
    logout_decision = yes_or_no("Info", "Logging out:\nAre you sure you want to log out?")
    
    if logout_decision:
        login_frame_username_box.focus()
        menu_frame_login_label.config(text="")
        user_session.username = None
        clear_login_frame()
        show_frame(login_frame)

def signup():
    username = login_frame_username_box.get().strip().lower()
    password = login_frame_password_box.get().strip()

    error_status, popup_title, popup_message = auth_service.check_and_add_user(username, password)
    if error_status:
        display_warning(popup_title, popup_message)
        return
    
    display_info(popup_title, popup_message)
    clear_login_frame()
    return



def confirm_password_changes(user, old_password, new_password):
    change_password_decision = yes_or_no(
        "Confirming Password Change",
        "Are you sure you want to change your password?"
        f"\nAccount Name: {user}"
        "\n\nPlease make sure to remember it."
    )

    if change_password_decision:
        change_password(user, old_password, new_password)

def change_password(user, old_password, new_password):
    
    password_change_error, password_change_message = validators.validate_password_change_entry(user, old_password, new_password)
    
    if password_change_error:
        display_warning(password_change_error, password_change_message)
        return
    
    with get_db() as conn:
        stored_account_info = db.find_current_account_password(conn, user)
        
        if not stored_account_info:
            display_error("Error", "Account not found.\nPlease ensure that you are logged in.")
            return

        stored_account_name, stored_account_password = stored_account_info
        stored_account_password = stored_account_password.encode("utf-8")
    
        if not bcrypt.checkpw(old_password.encode("utf-8"), stored_account_password):
                display_warning("Input Error", "The entered current password doesn't match.\nPlease try again.")
                return
        
        hashed_new_password = hash_password(new_password).decode("utf-8")
        db.change_account_password(conn, user, hashed_new_password)
        
        conn.commit()

        display_info("Success", "Account password has been successfully changed.")
        return
def hash_password(password):
    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(pw_bytes, salt)
    return hashed_pw
    
# ===================================

# ===================================
# Navigation / Frame Management
#v0.5.0
def menu_logout():
    log_out_decision = yes_or_no("Info", "Logging out:\nAre you sure you want to log out?")
    if log_out_decision:
        
        current_session.given_name = None
        current_session.surname = None
        current_session.role = None
        
        show_frame(login_page)

def show_signup_page():
    show_frame(signup_page)


def clear_attendance_creation():
    selected_attendance_grade.set('')
    selected_attendance_section.set('')
    selected_attendance_subject.set('')
    attendance_date_picker.set_date(datetime.today())
    attendance_start_period_spinbox.delete(0, tk.END)

def entry_reseter(entries):
    for entry in entries:
        entry.delete(0, tk.END)

def clear_login_page():
    entry_reseter([
         login_password_entry, login_identifier_entry
    ])


def on_closing():
    if yes_or_no("Quit", "Exiting the program:\nAre you sure you want to quit the program?"):
        win.destroy()

def clear_signup_page():
    selected_account_role.set("")
    selected_grade_level.set("")
    selected_grade_section.set("")
    entry_reseter(
        [given_name_entry, surname_entry,
         account_password_entry, identifier_signup_entry]
    )

# 0.4.0

def clear_login_frame():
    login_frame_username_box.delete(0, tk.END)
    login_frame_password_box.delete(0, tk.END)

def show_accessibility_frame():
    show_frame(accessibility_frame)
 
def clear_fillout_attendance():
    fillout_frame_name_box.delete(0, tk.END)
    fillout_frame_password_box.delete(0, tk.END)

def attendance_fillout_menu():
    show_frame(fillout_frame)
    fillout_frame_name_box.focus()

def attendance_create_menu():
    show_frame(create_frame)
    create_frame_name_box.focus()

def show_text_adjust():
    show_frame(adjustment_frame)    

def not_logged_message():
    display_error(constants.AUTH_ERROR,"There was not account detected in your current login session.\nPlease ensure you're logged in, and try again.")

def settings_menu():
    show_frame(settings_frame)

def demo_msg():
    display_info("Info", "The following feature is not yet implemented.\nPlease wait for later updates. ")

def main_menu():
    clear_create_attendance()
    clear_fillout_attendance()
    show_frame(menu_frame)

def attendance_menu():
    show_frame(attendance_frame)

def show_frame(frame):
    for f in frames:
        f.grid_forget() 
    frame.grid(row=1, column=0, sticky="nsew")

def display_warning(warning_title, warning_message):
    messagebox.showwarning(warning_title, warning_message)
    return

def display_error(error_title, error_message):
    messagebox.showerror(error_title, error_message)
    return

def display_info(info_title, info_message):
    messagebox.showinfo(info_title, info_message)
    return

def yes_or_no(popup_title, popup_question):
    response = messagebox.askyesno(popup_title, popup_question)
    return response

def clear_create_attendance():
    create_frame_name_box.delete(0, tk.END)
    create_frame_start_time_box.delete(0, tk.END)
    create_frame_endtime_box.delete(0, tk.END)
    create_frame_password_box.delete(0, tk.END)
    create_frame_minutes_box.delete(0, tk.END)

# ===================================

# ===================================
# Theme / Appearance
def adjust_text_size_small():
    set_text_size(0.75)
    display_info("Info", "Small text size has been enabled.")

def adjust_text_size_default():
    set_text_size(1)
    display_info("Info", "Default text size has been enabled.")

def adjust_text_size_large():
    set_text_size(1.25)
    display_info("Info", "Large text size has been enabled.")

def set_text_size(text_size_multiplier):
    label_font.configure(size=int(12*text_size_multiplier))

def light_screen():
    apply_theme(
         bg="#f0f0f0", fg="#1c1c1c", 
         accent_bg="#f0f0f051")
    
    display_info("Info", "Light Mode Enabled")

def dark_screen():
    apply_theme(
        bg="#1c1c1c", fg="#f0f0f0",
         accent_bg="#2b2b2b")
    
    display_info("Info", "Dark Mode Enabled")

def high_contrast_mode():
    apply_theme(
        bg="#000000", fg="#FFFFFF", 
         accent_bg="#FFFF00",)
    
    style = ttk.Style()

    style.configure("TButton",
        background="#FFFFFF",
        foreground="#000000"
    )

    style.map("TButton",
        background=[("active", "#FFFF00")],
        foreground=[("active", "#000000")]
    )

    display_info("Info", "High contrast mode enabled")

def show_attendance_creation():
    attendance_grade_selector.focus()
    show_frame(attendance_create)

def apply_theme(bg, fg, accent_bg):
    style = ttk.Style()

    # General backgrounds
    win.configure(bg=bg)
    style.configure("TFrame", background=bg)

    # ttk widgets
    style.configure("TLabel", background=bg, foreground=fg)
    style.configure("TButton", background=bg, foreground=fg)
    style.configure("TEntry", fieldbackground=bg, foreground=fg)
    style.configure("TSpinbox", fieldbackground=bg, foreground=fg)

    style.configure(
        "Treeview",
        background=bg,
        foreground=fg,
        fieldbackground=bg
    )

    style.configure(
        "Treeview.Heading",
        background=bg,
        foreground=fg
    )
        

# ===================================

# ===================================
# UI
def process_punctuality_input(event):
    selected_student_punctuality = selected_attendance_punctuality.get()
    if selected_student_punctuality == "Tardy":
        attendance_tardy_minutes_spinbox.config(state="normal")
        attendance_cutting_minutes_spinbox.config(state="disabled")

    elif selected_student_punctuality == "Cutting":
        attendance_cutting_minutes_spinbox.config(state="normal")
        attendance_tardy_minutes_spinbox.config(state="disabled")

    else:
        attendance_tardy_minutes_spinbox.config(state="disabled")
        attendance_cutting_minutes_spinbox.config(state="disabled")

        attendance_tardy_minutes_spinbox.set(0)
        attendance_cutting_minutes_spinbox.set(0)

def calendar_focus(event):
    event.widget._top_cal.focus_set()

def widget_remover(widget_list):
    for widget in widget_list:
        widget.grid_forget()

def grid_layout_manager(widget_tuples):
    for widget_name, widget_row, widget_column, x_spacing, y_spacing, sticky in widget_tuples:
        widget_name.grid(row=widget_row, column=widget_column, padx=x_spacing, pady=y_spacing, sticky=sticky)

def pack_widget_loader(parent, widgets):
    for widget in widgets:
        widget.pack(in_=parent, pady=5)

def label_constructor(frame, text, style="TLabel"):
    return ttk.Label(frame, text=text, style=style)

def button_constructor(
    frame: tk.Frame, 
    text: str, 
    state: str, 
    style: str = "TButton", 
    command: Optional[Callable] = None) -> ttk.Button:
    return ttk.Button(frame, text=text, state=state, style=style, command=command)

def entry_constructor(frame, width, style="TEntry"):
    return ttk.Entry(frame, width=width, style=style)

def has_role_student(event):
    current_account_role = selected_account_role.get()
    grade_level_selector.set("")
    grade_section_selector.set("")
    if current_account_role == "Student":
        grid_layout_manager([
            (grade_year_label, 6, 0, 10, 5, "w"),
            (grade_level_selector, 6, 1, 10, 5, "")
        ])
        selected_grade_section
    else:
        widget_remover([
            grade_level_selector, grade_section_selector,
            grade_year_label, grade_section_label
        ])

def show_section_selector(event):
    grade_section_selector.set("")
    selected_grade = int(selected_grade_level.get())
    
    # Define sections based on grade
    sections = {
        7: ("Emerald", "Diamond", "Ruby"),
        8: ("Camia", "Jasmine", "Sampaguita"),
        9: ("Potassium", "Rubidium", "Sodium"),
        10: ("Electron", "Neutron", "Proton"),
        11: ("A", "B", "C"),
        12: ("A", "B", "C")
    }
    
    if selected_grade in sections:
        grade_section_selector.config(values=sections[selected_grade])
        grid_layout_manager([
            (grade_section_label, 7, 0, 10, 5, "w"),
            (grade_section_selector, 7, 1, 10, 5, "")
        ])

def show_possible_sections(event):
    selected_grade_level = int(selected_attendance_grade.get())
    selected_attendance_section.set('')
    sections = {
        7: ("Emerald", "Diamond", "Ruby"),
        8: ("Camia", "Jasmine", "Sampaguita"),
        9: ("Potassium", "Rubidium", "Sodium"),
        10: ("Electron", "Neutron", "Proton"),
        11: ("A", "B", "C"),
        12: ("A", "B", "C")
    }

    attendance_section_selector.config(values=sections[selected_grade_level])


def show_possible_subjects(event):
    entered_attendance_grade = int(selected_attendance_grade.get())
    selected_attendance_subject.set('')
    sections = {
        7: constants.GRADE_7_SUBJECTS,
        8: constants.GRADE_8_SUBJECTS,
        9: constants.GRADE_9_SUBJECTS,
        10: constants.GRADE_10_SUBJECTS,
        11: constants.GRADE_11_SUBJECTS,
        12: constants.GRADE_12_SUBJECTS,
    }

    attendance_subject_selector.config(values=sections[entered_attendance_grade])

def on_grade_selected(event):
    show_possible_sections(event)
    show_possible_subjects(event)

def update_clock():
    """Updates the clock in the main menu every second"""
    current_time = datetime.now().strftime("%B %d, %Y - %H:%M:%S (%a)")
    menu_frame_time_label.config(text=f"Current time: {current_time}")
    win.after(1000, update_clock)

win = tk.Tk()

db.init_db()

style = ttk.Style()
style.theme_use("clam")

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

style.configure(
    "TButton",
    font=constants.BUTTON_FONT_SIZE,
    foreground=constants.DEFAULT_STYLE["foreground"],
    background=constants.DEFAULT_STYLE["background"],
    width=15,
)

label_font = tkFont.Font(family="Arial", size=12)
style.configure(
    "TLabel",
    font=label_font,
    foreground=constants.DEFAULT_STYLE["foreground"],
    background=constants.DEFAULT_STYLE["background"]
)

style.configure(
    "TEntry",
    font=constants.BUTTON_FONT_SIZE,
    foreground=constants.DEFAULT_STYLE["foreground"],
    fieldbackground=constants.DEFAULT_STYLE["background"],
    state="NORMAL"
)

style.configure(
    "TSpinbox",
    foreground=constants.DEFAULT_STYLE["foreground"],
    fieldbackground=constants.DEFAULT_STYLE["background"],
    font=constants.SPINBOX_FONT_SIZE,
    width=15
)

style.configure(
    "TFrame",
    background=constants.DEFAULT_STYLE["background"]
)

style.configure(
    "Title.TLabel",
    font=("Montserrat", 24, "bold")
)

win.title("APACE - v0.5.0")
win.geometry("800x680")
win.resizable(False, False)

# v0.5.0 Frames
logged_out = ttk.Frame(win, style="TFrame")
start_menu = ttk.Frame(win, style="TFrame")
signup_page = ttk.Frame(win, style="TFrame")
login_page = ttk.Frame(win, style="TFrame")
teacher_frame = ttk.Frame(win, style="TFrame")
dashboard_frame = ttk.Frame(win, style="TFrame")
attendance_marking_frame = ttk.Frame(win, style="TFrame")
settings = ttk.Frame(win, style="TFrame")

# v0.4.0 Frames
login_frame = ttk.Frame(win, style="TFrame")
menu_frame = ttk.Frame(win, style="TFrame")
attendance_frame = ttk.Frame(win, style="TFrame")
create_frame = ttk.Frame(win, style="TFrame")
view_frame = ttk.Frame(win, style="TFrame")
fillout_frame = ttk.Frame(win, style="TFrame")
settings_frame = ttk.Frame(win, style="TFrame")
accessibility_frame = ttk.Frame(win, style="TFrame")
adjustment_frame = ttk.Frame(win, style="TFrame")
attendance_create = ttk.Frame(win, style="TFrame")

frames = [
    logged_out,
    start_menu,
    signup_page,
    login_page,
    teacher_frame,
    attendance_create,
    dashboard_frame,
    attendance_marking_frame,
    settings,

    login_frame, 
    menu_frame, 
    attendance_frame, 
    create_frame, 
    view_frame,
    fillout_frame,
    settings_frame,
    accessibility_frame,
    adjustment_frame
]



title = ttk.Label(win, text="Attendance Checker", style="Title.TLabel")
title.grid(row=0, column=0, padx=10, pady=15, sticky="n")

menu_time = datetime.now().strftime("%B %d, %Y - %H:%M:%S (%a)")

user_session = current_user()

current_session = account_session()
current_attendance = attendance_session()

#Logged Out Frame
# NOTE to self: so because deleting old code from scratch and doing the major rewrite after is apparently a terrible idea, just make the reworked version as a separate thing from the old version.

legacy_version_button = button_constructor(logged_out, "v0.4.0 Code", "NORMAL", "TButton", lambda: show_frame(login_frame))
reworked_version_button = button_constructor(logged_out, "v0.5.0 Code", "NORMAL", "TButton", lambda: show_frame(start_menu))
close_program_button = button_constructor(logged_out, "Close Program", "NORMAL", "TButton", on_closing)

logged_out_widgets = [
    (legacy_version_button, 1, 1, 10, 5, ""),
    (reworked_version_button, 2, 1, 10, 5, ""),
    (close_program_button, 3, 1, 10, 5, "")
]

for logged_out_column_counter in range(3):
    logged_out.columnconfigure(logged_out_column_counter, weight=1)


grid_layout_manager(logged_out_widgets)


#v0.5.0 Logged Out - Main Menu Frame
signup_button = button_constructor(start_menu, "Sign Up", "NORMAL", "TButton", lambda: show_frame(signup_page))
login_button = button_constructor(start_menu, "Login", "NORMAL", "TButton", lambda: show_frame(login_page))

start_menu_widgets = [
    (signup_button, 1, 0, 10, 5, "e"),
    (login_button, 2, 0, 10, 5, "e"),
]
for counter in range(4):
    start_menu.rowconfigure(counter, minsize=20)
    start_menu.columnconfigure(counter, weight=1)
grid_layout_manager(start_menu_widgets)

#0.5.0 Signup Page

# Account Name
signup_page_title = label_constructor(signup_page, "Account Creation")
given_name_label = label_constructor(signup_page, "Given Name: ")
given_name_entry = entry_constructor(signup_page, 15)
surname_label = label_constructor(signup_page, "Surname: ")
surname_entry = entry_constructor(signup_page, 15)

# Account Identifier
identifier_signup_label = label_constructor(signup_page, "Account Identifier: ")
identifier_signup_entry = entry_constructor(signup_page, 15)

# Account Role Selection
selected_account_role = tk.StringVar()
account_role_label = label_constructor(signup_page, "Account Role: ")
possible_account_roles = ("Student", "Teacher")
account_role_selector = ttk.Combobox(signup_page, textvariable=selected_account_role, values=possible_account_roles, state='readonly', width=15)
account_role_selector.bind("<<ComboboxSelected>>", has_role_student)

# Grade Yr. and Section (If applicable)
grade_year_label = label_constructor(signup_page, "Grade Level: ")
selected_grade_level = tk.StringVar()
possible_grade_levels = (7, 8, 9, 10, 11, 12)
grade_level_selector = ttk.Combobox(signup_page, textvariable=selected_grade_level, values=possible_grade_levels, state='readonly', width=15)
grade_level_selector.bind("<<ComboboxSelected>>", show_section_selector)


# Account Password
selected_grade_section = tk.StringVar()
account_password_label = label_constructor(signup_page, "Account Password: ")
account_password_entry = entry_constructor(signup_page, 15)
account_password_entry.config(show="*")

create_account_button = button_constructor(signup_page, "Create Account", "NORMAL", "TButton", process_account_creation)
signup_back_button = button_constructor(signup_page, "Back", "NORMAL", "TButton", lambda: show_frame(start_menu))

signup_page_widgets = [
    (signup_page_title, 1, 0, 10, 5, ""),
    
    (given_name_label, 2, 0, 10, 5, "w"),
    (given_name_entry, 2, 1, 10, 5, ""),
    (surname_label, 3, 0, 10, 5, "w"),
    (surname_entry, 3, 1, 10, 5, ""),
    (identifier_signup_label, 4, 0, 10, 5, "w"),
    (identifier_signup_entry, 4, 1, 10, 5, ""),

    (account_role_label, 5, 0, 10, 5, "w"),
    (account_role_selector, 5, 1, 10, 5, ""),
    (account_password_label, 8, 0, 10, 5, "w"),
    (account_password_entry, 8, 1, 10, 5, ""),
    
    (signup_back_button, 9, 0, 15, 5, ""),
    (create_account_button, 9, 1, 15 , 5, "")
]

for counter in range(10):
    signup_page.rowconfigure(counter, weight=1)


grade_section_label = label_constructor(signup_page, "Section: ")
grade_section_selector = ttk.Combobox(signup_page, textvariable=selected_grade_section, values=[], state='readonly', width=15)

grid_layout_manager(signup_page_widgets)

# v0.5.0 Login Page
login_page_title = label_constructor(login_page, "Login")
login_identifier_label = label_constructor(login_page, "Account Identifier: ")
login_identifier_entry = entry_constructor(login_page, 15)
login_password_label = label_constructor(login_page, "Password: ")
login_password_entry = entry_constructor(login_page, 15)
login_password_entry.config(show="*")

login_account_button = button_constructor(login_page, "Login", "NORMAL", "TButton", read_login_entries)

login_back_button = button_constructor(login_page, "Back", "NORMAL", "TButton", lambda: show_frame(start_menu))

login_page_widgets = [
    (login_page_title, 1, 0, 10, 5, ""),
    (login_identifier_label, 2, 0, 10, 5, "w"),
    (login_identifier_entry, 2, 1, 10, 5, ""),
    (login_password_label, 3, 0, 10, 5, "w"),
    (login_password_entry, 3, 1, 10, 5, ""),
    (login_account_button, 4, 1, 10, 5, ""),
    (login_back_button, 4, 0, 10, 5, "")
]

grid_layout_manager(login_page_widgets)

# v0.5.0 Main Menu Frame
menu_frame_menu_label = label_constructor(teacher_frame, text="Main Menu")
menu_frame_create_attendance_buttonn = button_constructor(teacher_frame, "Create Attendance", "NORMAL", "TButton", show_attendance_creation)
menu_frame_attendance_button = button_constructor(teacher_frame, "Dashboard", "NORMAL", "TButton", show_dashboard_frame)
menu_frame_settings_button = button_constructor(teacher_frame, "Settings", "NORMAL", "TButton", demo_msg)
menu_frame_logout_button = button_constructor(teacher_frame, "Log Out", "TButton", command=menu_logout)

teacher_menu_widgets = [
    (menu_frame_menu_label, 1, 0, 10, 5, ""),
    (menu_frame_create_attendance_buttonn, 2, 0, 10, 5, ""),
    (menu_frame_attendance_button, 3, 0, 10, 5, ""),
    (menu_frame_settings_button, 5, 0, 10, 5, ""),
    (menu_frame_logout_button, 6, 0, 10, 5, "")
]

grid_layout_manager(teacher_menu_widgets)

# v0.5.0 Attendance Create
create_attendance_label = label_constructor(attendance_create, "Create Attendance")

# Grade Level
attendance_grade_label = label_constructor(attendance_create, "Grade Level:")
selected_attendance_grade = tk.StringVar()
possible_attendance_grade = (7, 8, 9, 10, 11, 12)
attendance_grade_selector = ttk.Combobox(
    attendance_create, textvariable=selected_attendance_grade, 
     values=possible_attendance_grade, state='readonly', 
     width=15
)

# Grade Section
attendance_section_label = label_constructor(attendance_create, "Grade Section: ")
selected_attendance_section = tk.StringVar()
attendance_section_selector = ttk.Combobox(
    attendance_create, textvariable=selected_attendance_section, 
    values=[], state='readonly', 
    width=15
)
attendance_grade_selector.current(0)

# Subject
attendance_subject_label = label_constructor(attendance_create, "Subject: ")
selected_attendance_subject = tk.StringVar()
attendance_subject_selector = ttk.Combobox(
    attendance_create, textvariable=selected_attendance_subject, 
    values=[], state='readonly', 
    width=15
)

attendance_grade_selector.bind("<<ComboboxSelected>>", on_grade_selected)

# Attendance Date
today = datetime.now().strftime(constants.DATE_FORMAT)
attendance_date_label = label_constructor(attendance_create, "Date: ")

attendance_date_picker = DateEntry(
    attendance_create, width=15, 
    background='#003566', foreground='#f0f0f0', 
    borderwidth=2, date_pattern='mm-dd-yyyy',
    maxdate=datetime.today())

attendance_date_picker.bind("<<DateEntryPopup>>", calendar_focus)

# Start Class schedule
attendance_period_label = label_constructor(attendance_create, "Period: ")
attendance_start_period_spinbox = ttk.Spinbox(
    attendance_create, from_=1, 
    to=10, style="TSpinbox")


# Attendance Submission and back button
attendance_create_back = button_constructor(attendance_create, "Back", "NORMAL", "TButton", lambda: show_frame(teacher_frame))
attendance_create_button = button_constructor(attendance_create, "Create Attendance", "NORMAL", "TButton", read_attendance_input)


attendance_create_widgets = [
    (create_attendance_label, 1, 0, 10, 5, ""),

    (attendance_grade_label, 2, 0, 10, 5, "w"),
    (attendance_grade_selector, 2, 1, 10, 5, ""),

    (attendance_section_label, 3, 0, 10, 5, "w"),
    (attendance_section_selector, 3, 1, 10, 5, ""),

    (attendance_subject_label, 4, 0, 10, 5, "w"),
    (attendance_subject_selector, 4, 1, 10, 5, ""),

    (attendance_date_label, 5, 0, 10, 5, "w"),
    (attendance_date_picker, 5, 1, 10, 5, ""),
    
    (attendance_period_label, 6, 0, 10, 5, "w"),
    (attendance_start_period_spinbox, 6, 1, 10, 5, ""),

    (attendance_create_back, 7, 0, 20, 5, ""),
    (attendance_create_button, 7, 1, 20, 5, "")

]

grid_layout_manager(attendance_create_widgets)
# v0.5.0 Settings
settings_title =  label_constructor(settings, "Settings")


"""
Thanks for being flawed but useful for me, v0.4.0
"""

# 0.4.0 Code - To be deprecated and/or salvaged

#Login Frame
login_frame_username_label = ttk.Label(login_frame, text="Account Name:", style="TLabel")
login_frame_username_box = ttk.Entry(login_frame, width=15, style="TEntry")
login_frame_username_box.focus()

login_frame_password_label = ttk.Label(login_frame, text="Account Password:", style="TLabel")
login_frame_password_box = ttk.Entry(login_frame, width=15, style="TEntry", show="*")

login_frame_signup_btn = ttk.Button(login_frame, text="Sign Up", style="TButton", command=signup)
login_frame_login_btn = ttk.Button(login_frame, text="Log In", style="TButton", command=login)

login_frame_back_btn = ttk.Button(login_frame, text="Back", style="TButton", command=lambda: show_frame(logged_out))

login_frame_widgets = [
    (login_frame_username_label, 1, 0, 10, 5, "e"), 
    (login_frame_username_box, 1, 2, 10, 5, "w"), 
    (login_frame_password_label, 2, 0, 10, 5, "e"),
    (login_frame_password_box, 2, 2, 10, 5, "w"),
    (login_frame_signup_btn, 4, 0, 10, 10, "e"), 
    (login_frame_login_btn, 4, 2, 10, 10, "w"),
    (login_frame_back_btn, 5, 0, 10, 5, "")
]

for login_frame_counter in range(5):
    login_frame.columnconfigure(login_frame_counter, weight=1)

grid_layout_manager(login_frame_widgets)




#Main Menu Frame
menu_frame_login_label= ttk.Label(menu_frame, text="", style="TLabel")
menu_frame_time_label = ttk.Label(menu_frame, text=f"Current time: {menu_time}", style="TLabel")
menu_frame_menu_label = ttk.Label(menu_frame, text="Main Menu", style="TLabel")
menu_frame_attendance_btn = ttk.Button(menu_frame, text="Attendance", style="TButton", command=attendance_menu)
menu_frame_settings_btn = ttk.Button(menu_frame, text="Settings", style="TButton", command=settings_menu)
menu_frame_logout_btn = ttk.Button(menu_frame, text="Log Out", style="TButton", command=logout)

menu_frame_widgets = [
    (menu_frame_login_label, 1, 0, 10, 5, ""), 
    (menu_frame_time_label, 2, 0, 10, 5, ""), 
    (menu_frame_menu_label, 3, 0, 10, 5, ""), 
    (menu_frame_attendance_btn, 4, 0, 10, 5, ""), 
    (menu_frame_settings_btn, 5, 0, 10, 5, ""), 
    (menu_frame_logout_btn, 6, 0, 10, 5, "")
]

for menu_frame_counter in range(8):
    menu_frame.columnconfigure(menu_frame_counter, weight=1)

grid_layout_manager(menu_frame_widgets)

# Sub-menu Attendance Frame
attendance_frame_attendance_label = ttk.Label(attendance_frame, text="Attendance Options", style="TLabel")

attendance_frame_attendance_create_btn = ttk.Button(attendance_frame, text="Create Attendance", style="TButton", command=attendance_create_menu)
attendance_frame_attendance_view_btn = ttk.Button(attendance_frame, text="View Attendances", style="TButton", command=show_attendance_view)
attendance_frame_attendance_fillout_btn = ttk.Button(attendance_frame, text="Fill out Attendance", style="TButton", command=attendance_fillout_menu)
attendance_frame_back_btn = ttk.Button(attendance_frame, text="Back", style="TButton", command=main_menu)

attendance_frame_widgets = [
    attendance_frame_attendance_label, 
    attendance_frame_attendance_create_btn, 
    attendance_frame_attendance_view_btn, 
    attendance_frame_attendance_fillout_btn, 
    attendance_frame_back_btn
]

pack_widget_loader(attendance_frame, attendance_frame_widgets)

# TODO: To be deprecated or majorly reworked
# Attendance Frame: Create


create_frame_label = ttk.Label(create_frame, text="Create Attendance", state="TLabel")

create_frame_name_label = ttk.Label(create_frame, text="Attendance Name: ", style="TLabel")
create_frame_name_box = ttk.Entry(create_frame, width=30, style="TEntry")

# Start datetime
# ----------
create_frame_startdate_label = ttk.Label(create_frame, text="Start Date (MM-DD-YYYY): ", style="TLabel")
create_frame_startdate_calendar = DateEntry(create_frame, width=15, background='#003566', foreground='#f0f0f0', borderwidth=2, date_pattern='mm-dd-yyyy')

create_frame_start_time_label = ttk.Label(create_frame, text="Start Time (HH:MM): ", style="TLabel")
create_frame_start_time_box = ttk.Entry(create_frame, width=15, style="TEntry")
# ----------

# End datetime
# ----------
create_frame_enddate_label = ttk.Label(create_frame, text="End Date (MM-DD-YYYY): ", style="TLabel")
create_frame_enddate_calendar = DateEntry(create_frame, width=15, background="#003566", foreground= "#f0f0f0", borderwidth=2, date_pattern='mm-dd-yyyy')

create_frame_endtime_label = ttk.Label(create_frame, text="End Time (HH:MM): ", style="TLabel")
create_frame_endtime_box = ttk.Entry(create_frame, width=15, style="TEntry")
# ----------

create_frame_notice_label = ttk.Label(create_frame, text="*Use 24-hour format", style="TLabel")

create_frame_minutes_late = ttk.Label(create_frame, text="Grace Period (Minutes):", style="TLabel")

create_frame_minutes_box = ttk.Spinbox(
    create_frame, from_=1, 
    to=30, style="TSpinbox")

create_frame_password_label = ttk.Label(create_frame, text="Attendance Password: ", style="TLabel")
create_frame_password_box = ttk.Entry(create_frame, width=30, show="*", style="TEntry")
create_attendance_btn = ttk.Button(create_frame, text="Make Attendance", style="TButton", command=read_create_attendance)

create_menu_btn = ttk.Button(create_frame, text="Back", style="TButton", command=attendance_menu)

create_widgets = [
    create_frame_label,

    create_frame_name_label,
    create_frame_name_box,
    
    create_frame_startdate_label,
    create_frame_startdate_calendar,
    create_frame_start_time_label,
    create_frame_start_time_box,
    
    create_frame_enddate_label,
    create_frame_enddate_calendar,
    
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

pack_widget_loader(create_frame, create_widgets)

# TODO: To be deprecated or majorly reworked
# Attendance Frame: Fill out
fillout_frame_current_user_label = ttk.Label(fillout_frame, text=f"Current User: {user_session.username}", style="TLabel")
fillout_frame_attendance_label = ttk.Label(fillout_frame, text=f"Enter Attendance Name", style="TLabel")
fillout_frame_name_box = ttk.Entry(fillout_frame, width=30, style="TEntry")

fillout_frame_password_label = ttk.Label(fillout_frame, text="Enter Attendance Password", style="TLabel")
fillout_frame_password_box = ttk.Entry(fillout_frame, width=30, show="*", style="TEntry")
fillout_frame_record_btn = ttk.Button(fillout_frame, text="Record Attendance", style="TButton", command=read_fillout_attendance)


fillout_menu_btn = ttk.Button(fillout_frame, text="Back", style="TButton", command=attendance_menu)

fillout_frame_widgets = [
    fillout_frame_current_user_label, 
    fillout_frame_attendance_label, 
    fillout_frame_name_box, 
    fillout_frame_password_label, 
    fillout_frame_password_box, 
    fillout_frame_record_btn,
    fillout_menu_btn
]

pack_widget_loader(fillout_frame, fillout_frame_widgets)

# Settings Frame
settings_frame_label = ttk.Label(settings_frame, text="Settings", style="TLabel")
settings_frame_password_btn = ttk.Button(settings_frame, text="Change Password", style="TButton", command=demo_msg)
settings_frame_accessibility_btn = ttk.Button(settings_frame, text="Accessibility", style="TButton", command=show_accessibility_frame)

setting_menu_btn = ttk.Button(settings_frame, text="Back", width=15, style="TButton", command=main_menu)

settings_widgets = [
    settings_frame_label, 
    settings_frame_password_btn,
    settings_frame_accessibility_btn,
    setting_menu_btn
]

pack_widget_loader(settings_frame, settings_widgets)


# Settings - Accessibility Frame
accessibility_frame_label = ttk.Label(accessibility_frame, text="Accessibility", style="TLabel")
accessibility_frame_high_contrast_btn = ttk.Button(accessibility_frame, text="High Contrast Mode",  style="TButton", command=high_contrast_mode)
accessibility_frame_text_adjustment_btn = ttk.Button(accessibility_frame, text="Display Adjustment",  style="TButton", command=show_text_adjust)
accessibility_frame_back_btn = ttk.Button(accessibility_frame, text="Back",  style="TButton", command=settings_menu)

accessibility_widgets = [
    accessibility_frame_label,
    accessibility_frame_high_contrast_btn,
    accessibility_frame_text_adjustment_btn,
    accessibility_frame_back_btn
]

pack_widget_loader(accessibility_frame, accessibility_widgets)

# Accessibility -  Text Adjustment Frame

adjustment_frame_label = ttk.Label(adjustment_frame, text="Text and Display Size Adjustment", style="TLabel")

adjust_text_size_label = ttk.Label(adjustment_frame, text="Adjust Text Size", style="TLabel")
small_text_size_button = ttk.Button(adjustment_frame, text="Small Text", style="TButton", command=adjust_text_size_small)
default_text_size_button = ttk.Button(adjustment_frame, text="Default Text", style="TButton", command=adjust_text_size_default)
large_text_size_button = ttk.Button(adjustment_frame, text="Large Text", style="TButton", command=adjust_text_size_large)

adjustment_frame_menu_btn = ttk.Button(adjustment_frame, text="Back",  style="TButton", command=show_accessibility_frame)

adjustment_frame_widgets = [
    adjustment_frame_label,
    adjust_text_size_label,

    small_text_size_button,
    default_text_size_button,
    large_text_size_button,

    adjustment_frame_menu_btn,
]

pack_widget_loader(adjustment_frame, adjustment_frame_widgets)


# v0.5.0 Attendance dashboard
dashboard_label = ttk.Label(dashboard_frame, text="Attendance dashboard", style="TLabel")
dashboard_label.grid(row=1, column=0, padx=5, pady=10)

dashboard_create_attendance = button_constructor(dashboard_frame, "Create Attendance", "NORMAL", "TButton", show_attendance_creation)
dashboard_refersh = button_constructor(dashboard_frame, "Refresh", "NORMAL", "TButton", demo_msg)
dashboard_export = button_constructor(dashboard_frame, "Export CSV", "NORMAL", "TButton", demo_msg)

dashboard_attendance_sessions_label= label_constructor(dashboard_frame, "Attendance Sessions")

dashboard_back_button = button_constructor(dashboard_frame, "Back", "NORMAL", "TButton", lambda: show_frame(teacher_frame))

dashboard_widgets = [
    (dashboard_label, 1, 0, 5, 10, "w"),
    (dashboard_create_attendance, 2, 0, 5, 10, "ew"),
    (dashboard_refersh, 2, 1, 5, 10, "ew"),
    (dashboard_export , 2, 2, 5, 10, "ew"),
    (dashboard_attendance_sessions_label, 3, 0, 5, 10, "w"),
    (dashboard_back_button, 5, 0, 5, 10, "w")
]


for column in range(3):
    dashboard_frame.columnconfigure(column, weight=1)

dashboard_frame.rowconfigure(4, weight=1)
dashboard_frame.columnconfigure(0, weight=1)

grid_layout_manager(dashboard_widgets)


dashboard_table_frame = ttk.Frame(dashboard_frame)
dashboard_table_frame.grid(row=4, column=0, columnspan=3, sticky="nsew")

dashboard_table_frame.rowconfigure(0, weight=1)
dashboard_table_frame.columnconfigure(0, weight=1)

dashboard_scrollbar = ttk.Scrollbar(dashboard_table_frame, orient="vertical")
dashboard_scrollbar.grid(row=0, column=1, pady=5, sticky="ns")

dashboard_table = ttk.Treeview(
    dashboard_table_frame,
    columns=(
        "Session ID",
        "Date", 
        "Grade", 
        "Section", 
        "Subject", 
        "Period"
    ),
    show="headings",
    height=8
)

dashboard_table.column("Session ID", width=100)
dashboard_table.column("Date", width=100)
dashboard_table.column("Grade", width=100)
dashboard_table.column("Section", width=100)
dashboard_table.column("Subject", width=100)
dashboard_table.column("Period", width=100)



dashboard_table.configure(yscrollcommand=dashboard_scrollbar.set)
dashboard_scrollbar.config(command=dashboard_table.yview)

dashboard_table.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")


dashboard_table.bind("<<TreeviewSelect>>", read_selected_attendance)


for col in dashboard_table["columns"]:
    dashboard_table.heading(col, text=col)

# v0.5.0 Attendance Marking
attend_marking_label = label_constructor(attendance_marking_frame, "Session Info: ")
attend_attendance_info = label_constructor(attendance_marking_frame, "")
attendance_query_label = label_constructor(attendance_marking_frame, "Search Student: ")
attendance_marking_query = entry_constructor(attendance_marking_frame, 15, "TEntry")

attendance_marking_query.bind("<KeyRelease>", filter_marking_table)

attendance_widgets = [
    (attend_marking_label, 1, 0, 5, 10, "w"),
    (attend_attendance_info, 2, 0, 5, 10, ""),
    (attendance_query_label, 3, 0, 5, 10, "w"),
    (attendance_marking_query, 3, 1, 5, 10, "")
]

grid_layout_manager(attendance_widgets)
attendance_table_frame = ttk.Frame(attendance_marking_frame)

attendance_marking_frame.rowconfigure(0, weight=0)
attendance_marking_frame.rowconfigure(4, weight=1)


attendance_marking_frame.columnconfigure(0, weight=1)
attendance_marking_frame.columnconfigure(1, weight=1)


attendance_table_frame.grid(row=4, column=0, columnspan=2, sticky="nsew")

attendance_scrollbar = ttk.Scrollbar(attendance_table_frame, orient="vertical")
attendance_scrollbar.grid(row=0, column=1, pady=5, sticky="ns")

attendance_table = ttk.Treeview(
    attendance_table_frame,
    columns=(
        "ID",
        "First Name", 
        "Surname", 
        "Status", 
        "Tardy Minutes", 
        "Cutting Minutes"
    ),
    show="headings",
    height=5
)

attendance_table.column("ID", width=100)
attendance_table.column("First Name", width=100)
attendance_table.column("Surname", width=100)
attendance_table.column("Status", width=100)
attendance_table.column("Tardy Minutes", width=100)
attendance_table.column("Cutting Minutes", width=100)

for col in attendance_table["columns"]:
    attendance_table.heading(col, text=col)

attendance_table.configure(yscrollcommand=attendance_scrollbar.set)
attendance_scrollbar.config(command=attendance_table.yview)

attendance_table.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

attendance_student_id_label = label_constructor(attendance_marking_frame, "Student ID: ")
attendance_student_id_spinbox = ttk.Spinbox(attendance_marking_frame, from_=1, style="TSpinbox")

selected_attendance_punctuality = tk.StringVar()
possible_attendance_punctuality = ("Present", "Absent", "Cutting", "Tardy")
attendance_punctuality_label = label_constructor(attendance_marking_frame, "Select Punctuality:")
attendance_punctuality_selector = ttk.Combobox(
    attendance_marking_frame, textvariable=selected_attendance_punctuality,
    values=possible_attendance_punctuality, state='readonly',
    width=15)

attendance_punctuality_selector.bind("<<ComboboxSelected>>", process_punctuality_input)

attendance_tardy_minutes_label = label_constructor(attendance_marking_frame, "Tardy Minutes: ")
attendance_tardy_minutes_spinbox = ttk.Spinbox(
    attendance_marking_frame, from_=0, 
    state='disabled', style="TSpinbox")

attendance_cutting_minutes_label = label_constructor(attendance_marking_frame, "Cutting Minutes: ")
attendance_cutting_minutes_spinbox = ttk.Spinbox(
    attendance_marking_frame, from_=0, 
    state='disabled', style="TSpinbox")

attendance_apply_changes = button_constructor(attendance_marking_frame, "Record Attendance", "NORMAL", "TButton", record_attendance_marking)


attendance_back_button = button_constructor(
    attendance_marking_frame, "Back", 
    "NORMAL", "TButton", 
    show_dashboard_frame)



attendance_marking_widgets = [
    (attendance_student_id_label, 5, 0, 5, 10, ""),
    (attendance_student_id_spinbox, 5, 1, 5, 10, ""),
    (attendance_punctuality_label, 6, 0, 5, 10, ""),
    (attendance_punctuality_selector, 6, 1, 5, 10, ""),
    (attendance_tardy_minutes_label, 7, 0, 5, 10, ""),
    (attendance_tardy_minutes_spinbox, 7, 1, 5, 10, ""),
    (attendance_cutting_minutes_label, 8, 0 , 5, 10, ""),
    (attendance_cutting_minutes_spinbox, 8, 1, 5, 10, ""),
    (attendance_back_button, 9, 0, 5, 10, ""),
    (attendance_apply_changes, 9, 1, 5, 10, "")
]


grid_layout_manager(attendance_marking_widgets)

attendance_marking_table_rows = []

# TODO: To be deprecated or majorly reworked
# View Attendance

# Title
view_title_label = ttk.Label(view_frame, text="View Attendances", style="TLabel")
view_title_label.pack(pady=10)

# Search box for creator table
search_label = ttk.Label(view_frame, text="Search Attendance:")
search_label.pack()
search_box = ttk.Entry(view_frame, width=15, style="TEntry")
search_box.pack()

search_box.bind("<KeyRelease>", search_attendance)

# Creator Table
creator_table_label = ttk.Label(view_frame, text="Creator View: Attendances Made", style="TLabel")
creator_table_label.pack()

creator_frame = ttk.Frame(view_frame)
creator_frame.pack()

creator_scrollbar = ttk.Scrollbar(creator_frame, orient="vertical")
creator_scrollbar.pack(side="right", fill="y")


creator_table = ttk.Treeview(
    creator_frame,
    columns=(
        "Attendance", 
        "User", 
        "Time Recorded", 
        "Status", 
        "Minutes Late", 
        "Response"
    ),
    show="headings",
    height=8
)

creator_table.configure(yscrollcommand=creator_scrollbar.set)
creator_scrollbar.config(command=creator_table.yview)

creator_table.pack(side="left", fill="both", expand=True)

for col in creator_table["columns"]:
    creator_table.heading(col, text=col)

creator_table_rows = []

# Participant Table
participant_table_label = ttk.Label(view_frame, text="Participant View: Your Attendances", style="TLabel")
participant_table_label.pack()

participant_frame = ttk.Frame(view_frame)
participant_frame.pack()

participant_scrollbar = ttk.Scrollbar(participant_frame, orient="vertical")
participant_scrollbar.pack(side="right", fill="y")

participant_table = ttk.Treeview(
    participant_frame,
    columns=("Attendance", "Status", "Time Recorded", "User", "Response"),
    show="headings",
    height=8
)
participant_table.configure(yscrollcommand=participant_scrollbar.set)
participant_scrollbar.config(command=participant_table.yview)

for col in participant_table["columns"]:
    participant_table.heading(col, text=col)
    participant_table.column(col, width=200, anchor="center")  # Set width

participant_table.pack(side="left", fill="both", expand=True)

view_frame_menu_btn = ttk.Button(view_frame, text="Back",  style="TButton", command=attendance_menu)
view_frame_menu_btn.pack(pady=10)

win.protocol("WM_DELETE_WINDOW", on_closing)

show_frame(start_menu)
update_clock()
win.mainloop()
# ===================================