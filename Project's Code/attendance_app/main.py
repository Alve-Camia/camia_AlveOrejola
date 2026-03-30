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

def read_change_password_entries():
    user = user_session.username
    old_password = password_frame_old_password_box.get()
    new_password = password_frame_new_password_box.get()
    confirm_password_changes(user, old_password, new_password)

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
        clear_password_change()
        return
def hash_password(password):
    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(pw_bytes, salt)
    return hashed_pw
    
# ===================================

# ===================================
# Navigation / Frame Management

def on_closing():
    if yes_or_no("Quit", "Exiting the program:\nAre you sure you want to quit the program?"):
        win.destroy()

def clear_login_frame():
    login_frame_username_box.delete(0, tk.END)
    login_frame_password_box.delete(0, tk.END)

def show_appearance_frame():
    show_frame(appearance_frame)

def show_password_frame():
    show_frame(password_frame)
    password_frame_old_password_box.focus()

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
    clear_password_change()
    show_frame(settings_frame)

def clear_password_change():
    password_frame_old_password_box.delete(0, tk.END)
    password_frame_new_password_box.delete(0, tk.END)

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
        f.pack_forget() 
    frame.pack(fill="both", expand=True)

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
# UI Construction
def widget_loader(parent, widgets):
    for widget in widgets:
        widget.pack(in_=parent, pady=5)

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
    font=constants.SPINBOX_FONT_SIZE
)

style.configure(
    "TFrame",
    background=constants.DEFAULT_STYLE["background"]
)

win.title("Attendance Checker: v0.4.0")
win.geometry("1200x680")
win.resizable(False, False)

login_frame = ttk.Frame(win, style="TFrame")
menu_frame = ttk.Frame(win, style="TFrame")
attendance_frame = ttk.Frame(win, style="TFrame")
create_frame = ttk.Frame(win, style="TFrame")
settings_frame = ttk.Frame(win, style="TFrame")
fillout_frame = ttk.Frame(win, style="TFrame")
appearance_frame = ttk.Frame(win, style="TFrame")
view_frame = ttk.Frame(win, style="TFrame")
password_frame = ttk.Frame(win, style="TFrame")
accessibility_frame = ttk.Frame(win, style="TFrame")
adjustment_frame = ttk.Frame(win, style="TFrame")
frames = [
    login_frame, 
    menu_frame, 
    attendance_frame, 
    create_frame, 
    view_frame,
    fillout_frame,
    settings_frame,
    appearance_frame,
    password_frame,
    accessibility_frame,
    adjustment_frame
]

title = ttk.Label(win, text="Attendance Checker", font=("Montserrat", 24))
title.pack(pady=(10,10))

menu_time = datetime.now().strftime("%B %d, %Y - %H:%M:%S (%a)")

user_session = current_user()

#Login Frame
login_frame_username_label = ttk.Label(login_frame, text="Enter Account Name (Letters and Spaces only):", style="TLabel")
login_frame_username_box = ttk.Entry(login_frame, width=15, style="TEntry")
login_frame_username_box.focus()

login_frame_password_label = ttk.Label(login_frame, text="Enter Password (10-100 Characters Required):", style="TLabel")
login_frame_password_box = ttk.Entry(login_frame, width=15, style="TEntry", show="*")

login_frame_signup_btn = ttk.Button(login_frame, text="Sign Up", style="TButton", command=signup)
login_frame_login_btn = ttk.Button(login_frame, text="Log In", style="TButton", command=login)

login_frame_widgets = [
    login_frame_username_label, 
    login_frame_username_box, 
    login_frame_password_label,
    login_frame_password_box, 
    login_frame_signup_btn, 
    login_frame_login_btn
]
widget_loader(login_frame, login_frame_widgets)

#Main Menu Frame
menu_frame_login_label= ttk.Label(menu_frame, text="", style="TLabel")
menu_frame_time_label = ttk.Label(menu_frame, text=f"Current time: {menu_time}", style="TLabel")
menu_frame_menu_label = ttk.Label(menu_frame, text="Main Menu", style="TLabel")
menu_frame_attendance_btn = ttk.Button(menu_frame, text="Attendance", style="TButton", command=attendance_menu)
menu_frame_settings_btn = ttk.Button(menu_frame, text="Settings", style="TButton", command=settings_menu)
menu_frame_logout_btn = ttk.Button(menu_frame, text="Log Out", style="TButton", command=logout)

menu_frame_widgets = [
    menu_frame_login_label, 
    menu_frame_time_label, 
    menu_frame_menu_label, 
    menu_frame_attendance_btn, 
    menu_frame_settings_btn, 
    menu_frame_logout_btn
]

widget_loader(menu_frame, menu_frame_widgets)

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

widget_loader(attendance_frame, attendance_frame_widgets)

# Attendance Frame: Create
today = datetime.now().strftime(constants.DATE_FORMAT)

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
create_frame_minutes_box = ttk.Spinbox(create_frame, from_=1, to=30, style="TSpinbox")

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

widget_loader(create_frame, create_widgets)

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

widget_loader(fillout_frame, fillout_frame_widgets)

# Settings Frame
settings_frame_label = ttk.Label(settings_frame, text="Settings", style="TLabel")
settings_frame_password_btn = ttk.Button(settings_frame, text="Change Password", style="TButton", command=show_password_frame)
settings_frame_appearance_btn = ttk.Button(settings_frame, text="Personalization", style="TButton", command=show_appearance_frame)
settings_frame_accessibility_btn = ttk.Button(settings_frame, text="Accessibility", style="TButton", command=show_accessibility_frame)

setting_menu_btn = ttk.Button(settings_frame, text="Back", width=15, style="TButton", command=main_menu)

settings_widgets = [
    settings_frame_label, 
    settings_frame_password_btn,
    settings_frame_appearance_btn,
    settings_frame_accessibility_btn,
    setting_menu_btn
]

widget_loader(settings_frame, settings_widgets)

# Settings - Reset password
password_frame_label = ttk.Label(password_frame, text="Change Password", style="TLabel")

password_frame_old_password_label = ttk.Label(password_frame, text="Enter Current Password", style="TLabel")
password_frame_old_password_box = ttk.Entry(password_frame, width=30, show="*", style="TEntry")

password_frame_new_password_label = ttk.Label(password_frame, text="Enter New Password", style="TLabel")
password_frame_new_password_box = ttk.Entry(password_frame, width=30, show="*", style="TEntry")

password_frame_change_password = ttk.Button(password_frame, text="Change Password",  style="TButton", command=read_change_password_entries)

password_frame_menu_btn = ttk.Button(password_frame, text="Back",  style="TButton", command=settings_menu)

reset_password_widgets = [
    password_frame_label,
    
    password_frame_old_password_label,
    password_frame_old_password_box,

    password_frame_new_password_label,
    password_frame_new_password_box,

    password_frame_change_password,

    password_frame_menu_btn
]

widget_loader(password_frame, reset_password_widgets)

# Settings - Attendance Frame
# [ To Be Added :( ]

# Settings - Personalization Frame
personalization_frame_label = ttk.Label(appearance_frame, text="Personalization", style="TLabel")
personalization_frame_light_btn = ttk.Button(appearance_frame, text="Light Mode",  style="TButton", command=light_screen)
personalization_frame_dark_btn = ttk.Button(appearance_frame, text="Dark Mode",  style="TButton", command=dark_screen)

personalization_frame_menu_btn = ttk.Button(appearance_frame, text="Back",  style="TButton", command=settings_menu)

appearance_widgets = [
    personalization_frame_label,
    personalization_frame_light_btn, 
    personalization_frame_dark_btn, 
    personalization_frame_menu_btn
]

widget_loader(appearance_frame, appearance_widgets)

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

widget_loader(accessibility_frame, accessibility_widgets)

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

widget_loader(adjustment_frame, adjustment_frame_widgets)

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

show_frame(login_frame)
update_clock()
win.mainloop()
# ===================================