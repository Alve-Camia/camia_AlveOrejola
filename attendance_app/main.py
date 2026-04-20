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
import pandas as pd
from tkcalendar import DateEntry

# Tkinter
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, messagebox, simpledialog

# Code Files
from .db import db
from .utils import validators, constants
from .services import auth_service, attendance_service
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

window_width = 800
window_height = 680

# ===================================
# Attendance Logic
class attendance_session():
    def __init__(self):
        self.attendance_id = None
        self.attendance_grade = None
        self.attendance_section = None


# ===== Attendance Create =====
def read_attendance_input():
    entered_attendance_grade =  selected_attendance_grade.get()
    entered_attendance_section = selected_attendance_section.get()
    entered_attendance_subject = selected_attendance_subject.get()
    entered_attendance_date = attendance_date_picker.get()
    entered_attendance_period = attendance_start_period_spinbox.get()
    current_user_id = current_session.id

    attendance_creation_results = attendance_service.process_attendance_creation(
        entered_attendance_grade, entered_attendance_section,
        entered_attendance_subject, entered_attendance_date,
        entered_attendance_period, current_user_id
    )

    if attendance_creation_results["error_status"]:
        display_warning(
            attendance_creation_results["error_type"],
            attendance_creation_results["error_message"]
        )
        return
    
    clear_attendance_creation()
    display_info("Info", "Attendance has been successfully made.\n\nProceeding to attendance dashboard:")
    show_dashboard_frame()
    show_frame(dashboard_frame)
    return
# =====                  =====

# ===== Attendance Dashboard =====
def show_dashboard_frame():
    show_frame(dashboard_frame)
    attend_attendance_info.config(text="")
    selected_attendance_punctuality.set("")
    attendance_tardy_minutes_spinbox.set("")
    attendance_cutting_minutes_spinbox.set("")


    current_attendance.attendance_id = None
    current_attendance.attendance_grade = None
    current_attendance.attendance_section = None

    for row in dashboard_table.get_children():
        dashboard_table.delete(row)
    
    creator_id = current_session.id
    
    with get_db() as conn:
        attendance_dashboard_info = db.get_dashboard_table_info(conn, creator_id)
    
    for info in attendance_dashboard_info:
        row_id = dashboard_table.insert("", tk.END, values=info)

def export_dashboard_csv():
    teacher_id = current_session.id

    try:
        with get_db() as conn:
            data = db.export_attendance_data(conn, teacher_id)
    except sqlite3.IntegrityError as error_message:
        display_error("Database Error", f"Integrity Error: {str(error_message)}\nPlease try again later.")
    except sqlite3.OperationalError as error_message:
        display_error("Databse Error", f"Operational Error: {str(error_message)}\nPlease try again later.")
    
    if not data:
        display_warning("Export Error", "No data available.")
        return

    columns = [
        "Session ID",
        "Date",
        "First Name",
        "Surname",
        "Grade",
        "Section",
        "Subject",
        "Period",
        "Status",
        "Minutes Cut",
        "Minutes Late"
    ]

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(f"attendance_export - {datetime.now().strftime("%Y-%m-%d, %H-%M=%S")}.csv", index=False)

    display_info("Info", "Your attendance data has been successfully exported as CSV.\nTry checking on your device for the file.")


# =====                      =====

# ===== Marking Attendnace =====
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
# =====                    =====


def filter_view_attendance(event):
    view_attendance_filter = view_attendance_query_entry.get().strip().lower()

    for row in view_attendance_table.get_children():
        view_attendance_table.delete(row)


    for row in view_attendance_rows:
        row_info =  " ".join(map(str, row)).lower()

        if view_attendance_filter in row_info:
            view_attendance_table.insert("", tk.END, values=row)

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

def delete_all_attendance_made():
    if current_session.role != "Teacher":
        display_error("Access Denied", "You're currently using a student account.\nOnly teachers can delete attendance.")
        return
    
    if yes_or_no("Confirm Action", "Are you sure you want to delete all the attendances you have made?\nPlease ensure that you have at least exported your attendance data."):
        teacher_id = current_session.id
        with get_db() as conn:
            db.delete_all_attendances_madde(conn, teacher_id)
        display_info("Info", "All attendance you have made are now deleted.")

# Student Attendance Feature
def show_student_attendance():
    show_frame(student_attendance_frame)

    for row in view_attendance_table.get_children():
        view_attendance_table.delete(row)

    view_attendance_rows.clear()
    student_id = current_session.id
    with get_db() as conn:
        view_attendance_info  = db.search_student_attendance_info(conn, student_id)

    for info in view_attendance_info:
        row_id = view_attendance_table.insert("", tk.END, values=info)
        view_attendance_rows.append(info)


# ===================================

# ===================================
# Authentication (Login & Logout / Signup)


class account_session:
    def __init__(self):
        self.given_name = None
        self.surname = None
        self.role = None
        self.id = None


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
    account_id = account_data["id"]

    current_session.given_name = account_given_name
    current_session.surname = account_surname
    current_session.role = account_role
    current_session.id = account_id

    clear_login_page()

    if current_session.role == "Teacher":
        show_frame(teacher_frame)
        settings_frame_attendance_deletion.config(state="NORMAL")
    if current_session.role == "Student":
        show_frame(student_frame)
        settings_frame_attendance_deletion.config(state="DISABLED")
    return
    


# 0.4.0 Code
class current_user:
    def __init__(self):
        self.username = None

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

def show_respective_menu():
    if current_session.role == "Teacher":
        show_frame(teacher_frame)
    else:
        show_frame(student_frame)

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

def show_accessibility_frame():
    show_frame(accessibility_frame)

def show_text_adjust():
    show_frame(adjustment_frame)    

def not_logged_message():
    display_error(constants.AUTH_ERROR,"There was not account detected in your current login session.\nPlease ensure you're logged in, and try again.")

def settings_menu():
    show_frame(settings_frame)

def demo_msg():
    display_info("Info", "The following feature is not yet implemented.\nPlease wait for later updates. ")


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

    style.configure("TButton",
        background="#FFFFFF",
        foreground="#000000"
    )

    style.map("TButton",
        background=[("active", "#eeebe7")],
        foreground=[("active", "#000000")]
    )

    display_info("Info", "Default Mode Enabled")

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
        attendance_tardy_minutes_spinbox.set(1)

        attendance_cutting_minutes_spinbox.config(state="disabled")
        attendance_cutting_minutes_spinbox.set(0)

    elif selected_student_punctuality == "Cutting":
        attendance_cutting_minutes_spinbox.config(state="normal")
        attendance_cutting_minutes_spinbox.set(1)

        attendance_tardy_minutes_spinbox.config(state="disabled")
        attendance_tardy_minutes_spinbox.set(0)

    else:
        attendance_tardy_minutes_spinbox.config(state="disabled")

        attendance_cutting_minutes_spinbox.config(state="disabled")

        attendance_tardy_minutes_spinbox.set(0)
        attendance_cutting_minutes_spinbox.set(0)


def frame_row_configure(frame: ttk.Frame, counter_limit: int) -> None:
    for counter in range(counter_limit):
        frame.rowconfigure(counter, weight=1)



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
            (grade_year_label, 6, 0, (275, 10), 5, "w"),
            (grade_level_selector, 6, 1, (10, 275), 5, "")
        ])
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
            (grade_section_label, 7, 0, (275, 10), 5, "w"),
            (grade_section_selector, 7, 1, (10, 275), 5, "")
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

screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

win.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
win.resizable(False, False)

# v0.5.0 Frames
start_menu = ttk.Frame(win, style="TFrame")
signup_page = ttk.Frame(win, style="TFrame")
login_page = ttk.Frame(win, style="TFrame")

teacher_frame = ttk.Frame(win, style="TFrame")
dashboard_frame = ttk.Frame(win, style="TFrame")
attendance_marking_frame = ttk.Frame(win, style="TFrame")
attendance_create = ttk.Frame(win, style="TFrame")

student_frame = ttk.Frame(win, style="TFrame")
student_attendance_frame = ttk.Frame(win, style="TFrame")



# Salvaged - v0.4.0 Frames
settings_frame = ttk.Frame(win, style="TFrame")
accessibility_frame = ttk.Frame(win, style="TFrame")
adjustment_frame = ttk.Frame(win, style="TFrame")


frames = [
    start_menu,
    signup_page,
    login_page,
    teacher_frame,
    student_frame,
    student_attendance_frame,
    attendance_create,
    dashboard_frame,
    attendance_marking_frame,

    settings_frame,
    accessibility_frame,
    adjustment_frame
]

title = ttk.Label(win, text="Attendance Checker", style="Title.TLabel")
title.grid(row=0, column=0, padx=10, pady=20, sticky="n")

menu_time = datetime.now().strftime("%B %d, %Y - %H:%M:%S (%a)")

user_session = current_user()

current_session = account_session()
current_attendance = attendance_session()


# ========== Logged Out ==========
signup_button = button_constructor(start_menu, "Sign Up", "NORMAL", "TButton", lambda: show_frame(signup_page))
login_button = button_constructor(start_menu, "Login", "NORMAL", "TButton", lambda: show_frame(login_page))

start_menu_widgets = [
    (signup_button, 1, 0, 275, 5, "e"),
    (login_button, 2, 0, 275, 5, "e"),
]
for counter in range(4):
    start_menu.rowconfigure(counter, minsize=20)
    start_menu.columnconfigure(counter, weight=1)
grid_layout_manager(start_menu_widgets)

# ================================

# ========== Sign Up ==========

# Account Name
signup_page_title = label_constructor(signup_page, "Account Creation")
given_name_label = label_constructor(signup_page, "Given Name: ")
given_name_entry = entry_constructor(signup_page, 15)
surname_label = label_constructor(signup_page, "Surname: ")
surname_entry = entry_constructor(signup_page, 15)

# Account Identifier
identifier_signup_label = label_constructor(signup_page, "Account Username: ")
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
    (signup_page_title, 1, 0, (250, 10), 5, ""),
    
    (given_name_label, 2, 0, (250, 10), 5, "w"),
    (given_name_entry, 2, 1, (10, 250), 5, ""),
    (surname_label, 3, 0, (250, 10), 5, "w"),
    (surname_entry, 3, 1, (10, 250), 5, ""),
    (identifier_signup_label, 4, 0, (250, 10), 5, "w"),
    (identifier_signup_entry, 4, 1, (10, 250), 5, ""),

    (account_role_label, 5, 0, (250, 10), 5, "w"),
    (account_role_selector, 5, 1, (10, 250), 5, ""),
    (account_password_label, 8, 0, (250, 10), 5, "w"),
    (account_password_entry, 8, 1, (10, 250), 5, ""),
    
    (signup_back_button, 9, 0, (250, 15), 5, ""),
    (create_account_button, 9, 1, (15, 250) , 5, "")
]

for counter in range(10):
    signup_page.rowconfigure(counter, weight=1)



grade_section_label = label_constructor(signup_page, "Section: ")
grade_section_selector = ttk.Combobox(signup_page, textvariable=selected_grade_section, values=[], state='readonly', width=15)

grid_layout_manager(signup_page_widgets)
# =============================

# ========== Login Page ==========
login_page_title = label_constructor(login_page, "Login")
login_identifier_label = label_constructor(login_page, "Account Username: ")
login_identifier_entry = entry_constructor(login_page, 15)
login_password_label = label_constructor(login_page, "Password: ")
login_password_entry = entry_constructor(login_page, 15)
login_password_entry.config(show="*")

login_account_button = button_constructor(login_page, "Login", "NORMAL", "TButton", read_login_entries)

login_back_button = button_constructor(login_page, "Back", "NORMAL", "TButton", lambda: show_frame(start_menu))

login_page_widgets = [
    (login_page_title, 1, 0, (275, 10), 5, ""),
    (login_identifier_label, 2, 0, (275, 10), 5, "w"),
    (login_identifier_entry, 2, 1, (10, 275), 5, ""),
    (login_password_label, 3, 0, (275, 10), 5, "w"),
    (login_password_entry, 3, 1, (10, 275), 5, ""),
    (login_account_button, 4, 1, (15, 250), 5, ""),
    (login_back_button, 4, 0, (250, 15), 5, "")
]

grid_layout_manager(login_page_widgets)


frame_row_configure(login_page, 10)


# ========== Teacher Menu ==========
# v0.5.0 Main Menu Frame
menu_frame_menu_label = label_constructor(teacher_frame, text="Main Menu")
menu_frame_attendance_button = button_constructor(teacher_frame, "Dashboard", "NORMAL", "TButton", show_dashboard_frame)
menu_frame_settings_button = button_constructor(teacher_frame, "Settings", "NORMAL", "TButton", lambda: show_frame(settings_frame))
menu_frame_logout_button = button_constructor(teacher_frame, "Log Out", "TButton", command=menu_logout)

teacher_menu_widgets = [
    (menu_frame_menu_label, 1, 0, 250, 5, "w"),
    (menu_frame_attendance_button, 3, 0, 250, 5, "w"),
    (menu_frame_settings_button, 5, 0, 250, 5, "w"),
    (menu_frame_logout_button, 6, 0, 250, 5, "w")
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
    (create_attendance_label, 1, 0, (275, 10), 5, ""),

    (attendance_grade_label, 2, 0, (275, 10), 5, "w"),
    (attendance_grade_selector, 2, 1, (10, 275), 5, ""),

    (attendance_section_label, 3, 0, (275, 10), 5, "w"),
    (attendance_section_selector, 3, 1, (10, 275), 5, ""),

    (attendance_subject_label, 4, 0, (275, 10), 5, "w"),
    (attendance_subject_selector, 4, 1, (10, 275), 5, ""),

    (attendance_date_label, 5, 0, (275, 10), 5, "w"),
    (attendance_date_picker, 5, 1, (10, 275), 5, ""),
    
    (attendance_period_label, 6, 0, (275, 10), 5, "w"),
    (attendance_start_period_spinbox, 6, 1, (10, 275), 5, ""),

    (attendance_create_back, 7, 0, (250, 20), 5, ""),
    (attendance_create_button, 7, 1, (20, 250), 5, "")

]

grid_layout_manager(attendance_create_widgets)

# ========== Student Menu ==========

student_menu_label = label_constructor(student_frame, text="Main Menu")
student_view_attendance_button = button_constructor(student_frame, "View Attendance", "NORMAL", "TButton", show_student_attendance)
menu_frame_settings_button = button_constructor(student_frame, "Settings", "NORMAL", "TButton", lambda: show_frame(settings_frame))
menu_frame_logout_button = button_constructor(student_frame, "Log Out", "TButton", command=menu_logout)


student_menu_widgets = [
    (student_menu_label, 1, 0, 5, 10, ""),
    (student_view_attendance_button, 2, 0, 5, 10, ""),
    (menu_frame_settings_button, 3, 0, 5, 10, ""),
    (menu_frame_logout_button, 4, 0, 5, 10, "")
]

grid_layout_manager(student_menu_widgets)


student_frame.columnconfigure(0, weight=1)
student_frame.columnconfigure(1, weight=0)
student_frame.columnconfigure(2, weight=0)

# Settings Frame
settings_frame_label = ttk.Label(settings_frame, text="Settings", style="TLabel")
settings_frame_accessibility_btn = ttk.Button(settings_frame, text="Accessibility", style="TButton", command=show_accessibility_frame)
settings_frame_attendance_deletion = button_constructor(settings_frame, "Delete All Attendances", "NORMAL", "TButton", delete_all_attendance_made)

setting_menu_btn = ttk.Button(settings_frame, text="Back", width=15, style="TButton", command=show_respective_menu)

settings_widgets = [
    (settings_frame_label, 1, 0, 275, 10, ""), 
    (settings_frame_accessibility_btn, 2, 0, 275, 10, ""),
    (settings_frame_attendance_deletion, 3, 0, 275, 10, ""),
    (setting_menu_btn, 4, 0, 275, 10, "")
]

grid_layout_manager(settings_widgets)

# Settings - Accessibility Frame
accessibility_frame_label = ttk.Label(accessibility_frame, text="Accessibility", style="TLabel")
accessibility_frame_default_mode = button_constructor(accessibility_frame, "Default", "NORMAL", "TButton", light_screen)
accessibility_frame_high_contrast_btn = ttk.Button(accessibility_frame, text="High Contrast Mode",  style="TButton", command=high_contrast_mode)
accessibility_frame_text_adjustment_btn = ttk.Button(accessibility_frame, text="Display Adjustment",  style="TButton", command=show_text_adjust)
accessibility_frame_back_btn = ttk.Button(accessibility_frame, text="Back",  style="TButton", command=settings_menu)

accessibility_widgets = [
    (accessibility_frame_label, 1, 0, 275, 10, ""),
    (accessibility_frame_default_mode, 2, 0, 275, 10, ""),
    (accessibility_frame_high_contrast_btn, 3, 0, 275, 10, ""),
    (accessibility_frame_text_adjustment_btn, 4, 0, 275, 10, ""),
    (accessibility_frame_back_btn, 5, 0, 275, 10, "")
]

grid_layout_manager(accessibility_widgets)

# Accessibility -  Text Adjustment Frame

adjustment_frame_label = ttk.Label(adjustment_frame, text="Text and Display Size Adjustment", style="TLabel")

adjust_text_size_label = ttk.Label(adjustment_frame, text="Adjust Text Size", style="TLabel")
small_text_size_button = ttk.Button(adjustment_frame, text="Small Text", style="TButton", command=adjust_text_size_small)
default_text_size_button = ttk.Button(adjustment_frame, text="Default Text", style="TButton", command=adjust_text_size_default)
large_text_size_button = ttk.Button(adjustment_frame, text="Large Text", style="TButton", command=adjust_text_size_large)

adjustment_frame_menu_btn = ttk.Button(adjustment_frame, text="Back",  style="TButton", command=show_accessibility_frame)

adjustment_frame_widgets = [
    (adjustment_frame_label, 1, 0, 275, 10, ""),
    (adjust_text_size_label, 2, 0, 275, 10, ""),

    (small_text_size_button, 3, 0, 275, 10, ""),
    (default_text_size_button, 4, 0, 275, 10, ""),
    (large_text_size_button, 5, 0, 275, 10, ""),

    (adjustment_frame_menu_btn, 6, 0, 275, 10, ""),
]

grid_layout_manager(adjustment_frame_widgets)


# v0.5.0 Attendance dashboard
dashboard_label = ttk.Label(dashboard_frame, text="Attendance dashboard", style="TLabel")
dashboard_label.grid(row=1, column=0, padx=5, pady=10)

dashboard_create_attendance = button_constructor(dashboard_frame, "Create Attendance", "NORMAL", "TButton", show_attendance_creation)
dashboard_refersh = button_constructor(dashboard_frame, "Refresh", "NORMAL", "TButton",  show_dashboard_frame)
dashboard_export = button_constructor(dashboard_frame, "Export CSV", "NORMAL", "TButton", export_dashboard_csv)

dashboard_attendance_sessions_label= label_constructor(dashboard_frame, "Attendance Sessions")

dashboard_back_button = button_constructor(dashboard_frame, "Back", "NORMAL", "TButton", lambda: show_frame(teacher_frame))

dashboard_widgets = [
    (dashboard_label, 1, 0, 5, 10, ""),
    (dashboard_create_attendance, 2, 0, 5, 10, ""),
    (dashboard_refersh, 2, 1, 5, 10, ""),
    (dashboard_export , 2, 2, 5, 10, ""),
    (dashboard_attendance_sessions_label, 3, 0, 5, 10, ""),
    (dashboard_back_button, 5, 1, 5, 10, "")
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
dashboard_table.column("Subject", width=150)
dashboard_table.column("Period", width=50)



dashboard_table.configure(yscrollcommand=dashboard_scrollbar.set)
dashboard_scrollbar.config(command=dashboard_table.yview)

dashboard_table.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")


dashboard_table.bind("<<TreeviewSelect>>", read_selected_attendance)


for col in dashboard_table["columns"]:
    dashboard_table.heading(col, text=col)

# Student -  View Attendance Feature
view_attendance_label = label_constructor(student_attendance_frame, "Student Attendance Records")

view_attendance_query_label = label_constructor(student_attendance_frame, "Attendance Query: ")
view_attendance_query_entry = entry_constructor(student_attendance_frame, 15)
view_attendance_back_button = button_constructor(student_attendance_frame, "Back", "NORMAL", "TButton", lambda: show_frame(student_frame))

student_view_attendance_widgets = [
    (view_attendance_label, 1, 0, 5, 10, ""),
    (view_attendance_query_label, 2, 0, 5, 10, "w"),
    (view_attendance_query_entry, 2, 1, 5, 10, ""),
    (view_attendance_back_button, 4, 0, 5, 10, "")
]

grid_layout_manager(student_view_attendance_widgets)

view_attendance_query_entry.bind("<KeyRelease>", filter_view_attendance)

view_table_frame = ttk.Frame(student_attendance_frame)

view_table_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")

view_attendance_scrollbar = ttk.Scrollbar(view_table_frame, orient="vertical")
view_attendance_scrollbar.grid(row=0, column=1, pady=5, sticky="ns")

view_attendance_table = ttk.Treeview(
    view_table_frame,
    columns=(
        "Attendance ID",
        "Date",
        "Subject",
        "Period",
        "Status"
    ),
    show="headings",
    height=8
)

view_attendance_table.column("Attendance ID", width=100)
view_attendance_table.column("Date", width=100)
view_attendance_table.column("Subject", width=100)
view_attendance_table.column("Period", width=100)
view_attendance_table.column("Status", width=100)

view_attendance_rows = []

for col in view_attendance_table["columns"]:
    view_attendance_table.heading(col, text=col)

view_attendance_table.configure(yscrollcommand=view_attendance_scrollbar.set)
view_attendance_scrollbar.config(command=view_attendance_table.yview)

view_attendance_table.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

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
    (attendance_marking_query, 3, 1, 5, 10, "w")
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
    height=8
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

attendance_apply_changes = button_constructor(attendance_marking_frame, "Apply Changes", "NORMAL", "TButton", record_attendance_marking)


attendance_back_button = button_constructor(
    attendance_marking_frame, "Back", 
    "NORMAL", "TButton", 
    show_dashboard_frame)

attendance_marking_widgets = [
    (attendance_student_id_label, 5, 0, 5, 10, "e"),
    (attendance_student_id_spinbox, 5, 1, 5, 10, "e"),
    (attendance_punctuality_label, 6, 0, 5, 10, "e"),
    (attendance_punctuality_selector, 6, 1, 5, 10, "e"),
    (attendance_tardy_minutes_label, 7, 0, 5, 10, "e"),
    (attendance_tardy_minutes_spinbox, 7, 1, 5, 10, "e"),
    (attendance_cutting_minutes_label, 8, 0 , 5, 10, "e"),
    (attendance_cutting_minutes_spinbox, 8, 1, 5, 10, "e"),
    (attendance_back_button, 9, 0, 5, 10, ""),
    (attendance_apply_changes, 9, 1, 5, 10, "")
]


grid_layout_manager(attendance_marking_widgets)

attendance_marking_table_rows = []

win.protocol("WM_DELETE_WINDOW", on_closing)

show_frame(start_menu)
win.mainloop()
# ===================================