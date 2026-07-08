"""
main.py
This module is the main entry point of using the program.
Aside from that, it contains:
    - ttk widget style configurations
    - ttk frames and widgets
    - widget binds .binds()
    - UI helper functions
Additionally, it contains the frontend's request functions that are sent to the backend.
"""
# =============== IMPORTANT ===============
# Note: Please run the following program by inputting the following lines.
# Ensure the attendance_app folder is at desktop directory / desktop screen.

# For Windows:
# 1. cd "C:\[Parent Directory]\[Other Parent Directory]\Desktop"
# 2. python -m attendance_app.main

# For macOS:
# 1. cd ~/[Parent Directory]/[Other Parent Directory]/Desktop
# 2. python3 -m attendance_app.main

# This is because the code program uses relative importing,
# so things may not run properly if you run the code directly.

# =========================================

# ===================================
# Imports

# ===== Standard Library =====
from typing import Callable, Optional
from datetime import datetime

import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, messagebox

#Third-party
from tkcalendar import DateEntry

# Code Files
from .db import db
from .utils import constants, helpers
from .services import auth_service, attendance_service
from .ui import components
# ===================================

# ===================================
# Attendance Logic
class AttendanceSession():
    """Holds and handles selected attendance session info during attendance marking

    Attributes:
        attendance_id (None | int): ID of attendance ; used for info querying
        attendance_grade (None | int): Gr. level of attendance; used for info querying and UI
            session info
        attendance_section (None | str) Gr. section of attendance; used for info querying and UI
            session info
    """
    def __init__(self):
        """Sets the initial state of attendance session tracking for instances"""
        self.attendance_id = None
        self.attendance_grade = None
        self.attendance_section = None

    def hold_attendance_session_info(self, attendance_id, grade_level, grade_section):
        """Tracks the current attendance session info"""
        self.attendance_id = attendance_id
        self.attendance_grade = grade_level
        self.attendance_section = grade_section

    def clear_attendance_session_info(self):
        """Clears the tracked attendance session info"""
        self.attendance_id = None
        self.attendance_grade = None
        self.attendance_section = None

# ===== Attendance Create =====
def attendance_creation_shortcut_handler(
        _: tk.Event,
        session_info: AccountSession,
        attendance_info: AttendanceSession
    ):
    """
    Purpose is similar to read_attendance_input but handles user creating the form
    when a field is focused and the user presses the enter key.

    Parameters:
    ----------
    session_info: account_session
        class instance for storing and tracking user info while being logged in
    attendance_info: AttendanceSession
        class instance for tracking attendance info during attendance marking

    Returns:
    -------
    This function does not return anything.
    """
    entered_attendance_grade =  selected_attendance_grade.get()
    entered_attendance_section = selected_attendance_section.get()
    entered_attendance_subject = selected_attendance_subject.get()
    entered_attendance_date = attendance_date_picker.get_date()
    entered_attendance_period = attendance_start_period_spinbox.get()
    current_user_id = session_info.id

    created_attentance_session = helpers.AttendanceSessionInfo(
        entered_attendance_grade, entered_attendance_section,
        entered_attendance_subject, entered_attendance_date,
        entered_attendance_period, current_user_id
    )

    call_attendance_creation_processer(
        created_attentance_session, session_info,
        attendance_info
    )

def read_attendance_input(
        session_info: AccountSession,
        attendance_info: AttendanceSession
    ):
    """
    Gets the user's ID and input from the attendance creation form.
    These inputs are then turned into a dataclass instance since
    it's 6 variables being passed around.

    Parameters:
    ----------
    session_info: account_session
        class instance for storing and tracking user info while being logged in
    attendance_info: AttendanceSession
        class instance for tracking attendance info during attendance marking

    Returns:
    -------
    This function does not return anything.
    """
    entered_attendance_grade =  selected_attendance_grade.get()
    entered_attendance_section = selected_attendance_section.get()
    entered_attendance_subject = selected_attendance_subject.get()
    entered_attendance_date = attendance_date_picker.get()
    entered_attendance_period = attendance_start_period_spinbox.get()
    current_user_id = session_info.id
    created_attentance_session = helpers.AttendanceSessionInfo(
        entered_attendance_grade, entered_attendance_section,
        entered_attendance_subject, entered_attendance_date,
        entered_attendance_period, current_user_id
    )
    call_attendance_creation_processer(
        created_attentance_session, session_info,
        attendance_info
    )
def call_attendance_creation_processer(
        created_attendance_info: helpers.AttendanceSessionInfo,
        session_info: AccountSession,
        attendance_info: AttendanceSession
    ) -> None:
    """
    Sends an attendance session creation request to the service layer.
    Input errors display a warning popup, otherwise, the user is brought back
    to the dashboard frame.
    
    Parameters:
    ----------
    created_attendance_info: helpers.AttendanceSessionInfo
        dataclass instance for storing attendance field entries; avoids long parameter lists
    session_info: account_session
        class instance for storing and tracking user info while being logged in
    attendance_info: AttendanceSession
        class instance for tracking attendance info during attendance marking

    Returns:
    --------
    This function does not return anything
    """
    attendance_creation_results = attendance_service.process_attendance_creation(
        created_attendance_info
    )

    if not attendance_creation_results.success:
        display_warning_popup(
            attendance_creation_results.error_title,
            attendance_creation_results.error_message
        )
        return
    clear_attendance_creation()
    display_info_popup(
        "Info",
        "Attendance has been successfully made.\n\nProceeding to attendance dashboard:"
        )
    show_dashboard_frame(session_info, attendance_info)
    show_frame(dashboard_frame)
    return
# ============================
# ===== Attendance Dashboard =====
def table_info_loader(
        table: ttk.Treeview,
        fetched_table_info: tuple[tuple[any, ...], ...]
    ) -> None:
    """
    UI helper function for filling a ttk table with specified rows

    Parameters:
    ----------
    table: ttk.Treeview
        table to fill rows with
    attendance_info: AttendanceSession
        tuple consisting of tuples to fill the specified table

    Returns:
    -------
    This function does not return anything.
    """
    for treeview_row in table.get_children():
        table.delete(treeview_row)

    for info in fetched_table_info:
        table.insert("", tk.END, values=info)

def show_dashboard_frame(
        session_info: AccountSession,
        attendance_info: AttendanceSession
    ) -> None:
    show_frame(dashboard_frame)
    reset_attendance_session(attendance_info)

    creator_id = session_info.id
    attendance_dashboard_info = attendance_service.lookup_creator_attendances(creator_id)
    table_info_loader(dashboard_table, attendance_dashboard_info)

def reset_attendance_session(
        attendance_info: AttendanceSession
    ) -> None:

    attend_attendance_info.config(text="")
    selected_attendance_punctuality.set("")

    combobox_reseter([selected_attendance_punctuality])
    spinbox_reseter([attendance_tardy_minutes_spinbox, attendance_cutting_minutes_spinbox])

    attendance_info.clear_attendance_session_info()

def call_attendance_exporter(session_info: AccountSession) -> None:
    teacher_id = session_info.id
    current_datetime = datetime.now().strftime('%Y-%m-%d, %H-%M-%S')
    export_attendance_results = attendance_service.process_attendance_export(
        teacher_id, current_datetime
    )
    if not export_attendance_results.success:
        display_warning_popup(
            export_attendance_results.error_title,
            export_attendance_results.error_message
        )
        return

    display_info_popup(
        "Info", 
        "Your attendance data has been successfully exported as CSV."
        "\nTry checking for a folder named 'Attendance Record Exports' on your device."
    )

# ================================

# ===== Marking Attendnace =====

def retrieve_selected_attendance_session(attendance_session_row):
    attendance_id = int(attendance_session_row[0])
    attendance_date = datetime.strptime(attendance_session_row[1], "%Y-%m-%d")
    attendance_grade = int(attendance_session_row[2])
    attendance_section = attendance_session_row[3]
    attendance_subject =  attendance_session_row[4]
    attendance_period = attendance_session_row[5]
    selected_attendance_session = helpers.SelectedAttendanceSessionInfo(
        attendance_id, attendance_date,
        attendance_grade, attendance_section,
        attendance_subject, attendance_period
    )
    return selected_attendance_session

def read_selected_attendance(_: tk.Event) -> None:
    selected_row = dashboard_table.focus()
    load_attendance_marking_table(selected_row, current_attendance)

def load_attendance_marking_table(
        selected_row: str,
        attendance_info: AttendanceSession
    ) -> None:
    if not selected_row:
        return

    attendance_marking_table_rows.clear()
    show_frame(attendance_marking_frame)
    attendance_marking_query.focus()

    dashboard_row_values = dashboard_table.item(selected_row, 'values')
    selected_attendance = retrieve_selected_attendance_session(dashboard_row_values)

    attendance_info.hold_attendance_session_info(
        selected_attendance.id, selected_attendance.grade_level,
        selected_attendance.grade_section
    )

    grade_level = selected_attendance.grade_level
    grade_section = selected_attendance.grade_section
    grade_level_section_info = f"Grade {grade_level} - {grade_section}"
    subject_info = selected_attendance.subject
    period_info = f"Period {selected_attendance.period}"
    date_info = selected_attendance.date
    attend_attendance_info.config(
        text=f"{grade_level_section_info} | {subject_info} | {period_info} | {date_info}")

    populate_attendance_marking_table(
        selected_attendance.id, selected_attendance.grade_level,
        selected_attendance.grade_section
    )

def populate_attendance_marking_table(
        attendance_id: int,
        attendance_grade: int,
        attendance_section: str
    ) -> None:
    attendance_marking_info = attendance_service.fetch_attendance_marking_info(
        attendance_id, attendance_grade,
        attendance_section
    )

    table_info_loader(attendance_table, attendance_marking_info)

    for attendance_info in attendance_marking_info:
        attendance_marking_table_rows.append(attendance_info)

def filter_marking_table(_: tk.Event) -> None:
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
def filter_view_attendance(_: tk.Event) -> None:
    view_attendance_filter = view_attendance_query_entry.get().strip().lower()

    for row in student_view_attendance_table.get_children():
        student_view_attendance_table.delete(row)

    for row in view_attendance_rows:
        row_info =  " ".join(map(str, row)).lower()

        if view_attendance_filter in row_info:
            student_view_attendance_table.insert("", tk.END, values=row)

def attendance_marking_shortcut_handler(
        _: tk.Event,
        attendance_info: AttendanceSession
    ) -> None:

    selected_student_id = attendance_student_id_spinbox.get().strip()
    attendance_punctuality = selected_attendance_punctuality.get()
    tardy_minutes = attendance_tardy_minutes_spinbox.get()
    cutting_minutes = attendance_cutting_minutes_spinbox.get()
    attendance_id = attendance_info.attendance_id

    entered_attendance_marking = helpers.AttendanceMarkingInfo(
        selected_student_id, attendance_punctuality,
        tardy_minutes, cutting_minutes,
        attendance_id
    )

    record_attendance_marking(entered_attendance_marking, attendance_info)


def read_entered_attendance_marking(attendance_info: AttendanceSession) -> None:
    selected_student_id = attendance_student_id_spinbox.get().strip()
    attendance_punctuality = selected_attendance_punctuality.get()
    tardy_minutes = attendance_tardy_minutes_spinbox.get()
    cutting_minutes = attendance_cutting_minutes_spinbox.get()
    attendance_id = attendance_info.attendance_id

    entered_attendance_marking = helpers.AttendanceMarkingInfo(
        selected_student_id, attendance_punctuality,
        tardy_minutes, cutting_minutes,
        attendance_id
    )

    record_attendance_marking(entered_attendance_marking, attendance_info)
def record_attendance_marking(
        attendance_marking_info: helpers.AttendanceMarkingInfo,
        attendance_info: AttendanceSession
    ) -> None:

    attendance_marking_processing_results = attendance_service.process_attendance_marking(
        attendance_marking_info,
        attendance_info.attendance_id
    )

    if not attendance_marking_processing_results.success:
        display_warning_popup(
            attendance_marking_processing_results.error_title,
            attendance_marking_processing_results.error_message
        )
        return

    populate_attendance_marking_table(
    attendance_info.attendance_id, attendance_info.attendance_grade,
    attendance_info.attendance_section)

def delete_all_attendance_made(session_info: AccountSession) -> None:
    if session_info.role != constants.TEACHER_ACCOUNT_STATUS.title():
        display_error_popup(
            "Access Denied",
            f"You're currently using a/an {session_info.role.lower()} account.\n"
            "Only teachers can delete attendance."
        )
        return
    if yes_or_no(
        "Confirm Action",
        "Are you sure you want to delete all the attendances you have made?\n"
        "Please ensure that you have at least exported your attendance data."
        ):

        teacher_id = session_info.id
        attendance_service.process_attendace_deletion(teacher_id)
        display_info_popup("Info", "All attendance you have made are now deleted.")

# Student Attendance Feature
def show_student_attendance(session_info: AccountSession) -> None:
    show_frame(student_attendance_frame)

    view_attendance_info = attendance_service.fetch_student_attendances(session_info.id)
    view_attendance_rows.clear()

    for student_attendance_record_info in view_attendance_info:
        view_attendance_rows.append(student_attendance_record_info)

    table_info_loader(student_view_attendance_table, view_attendance_info)


# ===================================

# ===================================
# Authentication (Login & Logout / Signup)
class AccountSession:
    """Holds and handles user info while logged int

    Attributes:
        given_name (None | str): given name/first name of the account
        surname (None | str): surname of the account
        role (None | str): Role assigned to accountl either teacher or student
        id (None | str): Unique ID assinged to the account; used for database querying
    """
    def __init__(self):
        """Sets the initial state of account session info tracking for instances"""
        self.given_name = None
        self.surname = None
        self.role = None
        self.id = None

    def clear_session_info(self) -> None:
        """Clears account session info on logout"""
        self.given_name = None
        self.surname = None
        self.role = None
        self.id = None

def clean_text(text: str):
    """Removes leading and trailing spaces of an str string; defaults to empty string if empty"""
    return " ".join(text.split()) if text else ""

def account_creation_shortcut_handler(_: tk.Event) -> None:

    entered_given_name = clean_text(given_name_entry.get())
    entered_surname = clean_text(surname_entry.get())
    entered_username = clean_text(username_signup_entry.get())
    grade_level = selected_grade_level.get()
    grade_section = selected_grade_section.get()
    account_role = selected_account_role.get()
    entered_password = account_password_entry.get()

    entered_account_registration_info = helpers.AccountRegistration(
        entered_given_name, entered_surname,
        entered_username, grade_level,
        grade_section, account_role,
        entered_password)

    process_account_creation(entered_account_registration_info)


def read_account_creation_fields():
    entered_given_name = clean_text(given_name_entry.get())
    entered_surname = clean_text(surname_entry.get())
    entered_username =  clean_text(username_signup_entry.get())
    grade_level = selected_grade_level.get()
    grade_section = selected_grade_section.get()
    account_role = selected_account_role.get()
    entered_password = account_password_entry.get()

    entered_account_registration_info = helpers.AccountRegistration(
        entered_given_name, entered_surname,
        entered_username, grade_level,
        grade_section, account_role,
        entered_password)
    process_account_creation(entered_account_registration_info)

def process_account_creation(registration_info: helpers.AccountRegistration):

    account_registration_results = auth_service.account_registration_processer(registration_info)

    if not account_registration_results.success:
        display_warning_popup(
            account_registration_results.error_title,
            account_registration_results.error_message
        )
        return

    display_info_popup("Info", "Account has been created.")
    clear_signup_page()
    return

def login_shortcut_handler(_: tk.Event) -> None:
    entered_password = login_password_entry.get()
    entered_username = login_username_entry.get()
    process_login(entered_password, entered_username, current_session)

def read_login_entries():
    entered_password = login_password_entry.get()
    entered_username = login_username_entry.get()
    process_login(entered_password, entered_username, current_session)

def process_login(
        entered_password: str,
        entered_username: str,
        session_info: AccountSession
    ) -> None:

    login_results, authenticated_account_info = auth_service.process_account_login(
        entered_password, entered_username
    )

    if not login_results.success:
        display_warning_popup(
            login_results.error_title,
            login_results.error_message,
        )

        clear_login_page()
        return

    track_user_session_info(authenticated_account_info, session_info)
    clear_login_page()
    win.focus_set()
    show_respective_menu(session_info)
    return

def track_user_session_info(
        authenticated_account_info: helpers.LoginSessionInfo,
        session_info: AccountSession
    ) -> None:

    session_info.given_name = authenticated_account_info.given_name
    session_info.surname = authenticated_account_info.surname
    session_info.role = authenticated_account_info.role
    session_info.id = authenticated_account_info.id

# ===================================

# ===================================
# Navigation / Frame Management
def assign_widget_shortcut(
        list_of_widgets: tuple[ttk.Widget, ...],
        corresponding_shortcut_key: str,
        corresponding_command: Optional[Callable] = None
    ) -> None:

    for widget in list_of_widgets:
        widget.bind(corresponding_shortcut_key, corresponding_command)

def menu_logout(session_info: AccountSession) -> None:
    log_out_decision = yes_or_no("Info", "Logging out:\nAre you sure you want to log out?")
    if log_out_decision:
        session_info.clear_session_info()
        show_frame(login_page)

def show_signup_page():
    show_frame(signup_page)

def clear_attendance_creation():
    selected_attendance_grade.set('')
    selected_attendance_section.set('')
    selected_attendance_subject.set('')
    attendance_date_picker.set_date(datetime.today())
    attendance_start_period_spinbox.delete(0, tk.END)

def show_respective_menu(session_info: AccountSession) -> None:

    match session_info.role.lower():
        case constants.TEACHER_ACCOUNT_STATUS:
            show_frame(teacher_frame)
            settings_frame_attendance_deletion.config(state=constants.BUTTON_NORMAL_STATE)
        case constants.STUDENT_ACCOUNT_STATUS:
            show_frame(student_frame)
            settings_frame_attendance_deletion.config(state="DISABLED")
        case constants.ADMIN_ACCOUNT_STATUS:
            show_frame(admin_frame)
            settings_frame_attendance_deletion.config(state="DISABLED")
        case _:
            pass

# ========== Reseters ==========
def entry_reseter(entries: list[ttk.Entry]) -> None:
    """UI helper function for removing inputs in entries"""
    for entry in entries:
        entry.delete(0, tk.END)

def combobox_reseter(combobox_value_holders: list[tk.StringVar]) -> None:
    """UI helper function for removing inputs in comboboxes"""
    for combobox_value_holder in combobox_value_holders:
        combobox_value_holder.set('')

def spinbox_reseter(spinbox_widget_list: list[ttk.Spinbox]) -> None:
    """UI helper function for removing inputs in spinboxes"""
    for current_spinbox_value in spinbox_widget_list:
        current_spinbox_value.delete(0, tk.END)
# ==============================
def clear_login_page():
    """Clears login page entry fileds"""
    entry_reseter([
         login_password_entry, login_username_entry
    ])

def on_closing():
    """Prompts user for confirmation for exiting the program in case of accidental closing"""
    if yes_or_no("Quit", "Exiting the program:\nAre you sure you want to quit the program?"):
        win.destroy()

def clear_signup_page():
    selected_account_role.set("")
    selected_grade_level.set("")
    selected_grade_section.set("")
    entry_reseter([
        given_name_entry, surname_entry,
        account_password_entry, username_signup_entry
    ])
    widget_remover([
        grade_year_label, grade_level_selector,
        grade_section_label, grade_section_selector
    ])

def show_accessibility_frame():
    show_frame(accessibility_frame)

def show_text_adjust():
    show_frame(adjustment_frame)

def not_logged_message():
    """Shows a popup error in case program detects no account session info while logged in."""
    display_error_popup(
        constants.AUTH_ERROR,
        "There was not account detected in your current login session."
        "\nPlease ensure you're logged in, and try again."
    )

def settings_menu():
    """Shows user the settings frame"""
    show_frame(settings_frame)

def demo_msg():
    """Displays a popup message for a feature that is not available yet"""
    display_info_popup(
        "Info",
        "The following feature is not yet implemented."
        "\nPlease wait for later updates. "
    )

def show_frame(frame_to_show: ttk.Frame) -> None:
    for frame in frames:
        frame.grid_forget()

    frame_to_show.grid(row=1, column=0, sticky="nsew")

def display_warning_popup(warning_title: str, warning_message: str) -> None:
    """UI helper function for displaying warning popups"""
    messagebox.showwarning(warning_title, warning_message)

def display_error_popup(error_title: str, error_message: str) -> None:
    """UI helper function for displaying error popups"""
    messagebox.showerror(error_title, error_message)

def display_info_popup(info_title: str, info_message: str) -> None:
    """UI helper function for displaying info popups"""
    messagebox.showinfo(info_title, info_message)

def yes_or_no(popup_title: str, popup_question: str):
    """UI helper function for displaying askyesno popup and returning response"""
    response = messagebox.askyesno(popup_title, popup_question)
    return response

# ===================================

# ===================================
# Theme / Appearance

def adjust_text_size(
        selected_text_size: float,
        text_size_option: str) -> None:
    text_size_multiplier(selected_text_size)
    display_info_popup("Info", f"{text_size_option} text size has been enabled.")

def text_size_multiplier(text_size_multiplier: float) -> None:
    components.FontStyles.label_font.configure(size=int(12 * text_size_multiplier))
    components.FontStyles.header_page_font.configure(size=int(14 * text_size_multiplier))
    components.FontStyles.title_label.configure(size=int(24 * text_size_multiplier))

    style = ttk.Style()
    style.configure("TLabel", font=components.FontStyles.label_font)
    style.configure("Header.TLabel", font=components.FontStyles.header_page_font)
    style.configure("Title.TLabel", font=components.FontStyles.title_label)

def default_screen():
    components.change_theme("#f0f0f0", "#1c1c1c", win)
    components.apply_default_table_styling()
    display_info_popup("Info", "Default Mode Enabled")

def dark_screen():
    components.change_theme("#1c1c1c", "#f0f0f0")
    display_info_popup("Info", "Dark Mode Enabled")

def high_contrast_mode():
    components.change_theme("#000000", "#FFFFFF")
    components.apply_high_contrast_button()
    display_info_popup("Info", "High contrast mode enabled")

def show_attendance_creation():
    attendance_grade_selector.focus()
    show_frame(attendance_create)

# ===================================

# ===================================
# UI
def check_truancy_input_length(_: tk.Event) -> None:

    tardy_minutes_input = attendance_tardy_minutes_spinbox.get()
    cutting_minutes_input = attendance_cutting_minutes_spinbox.get()

    if len(tardy_minutes_input) >= 3:
        attendance_tardy_minutes_spinbox.delete(2, tk.END)

    if len(cutting_minutes_input) >= 3:
        attendance_cutting_minutes_spinbox.delete(2, tk.END)

def check_entered_truancy_characters(_: tk.Event) -> None:

    entered_tardy_minutes = attendance_tardy_minutes_spinbox.get()
    unjoined_cleaned_tardy_minutes = [char for char in entered_tardy_minutes if char.isdigit()]
    joined_cleaned_tardy_minutes = "".join(unjoined_cleaned_tardy_minutes)
    attendance_tardy_minutes_spinbox.set(joined_cleaned_tardy_minutes)

    entered_cutting_minutes = attendance_cutting_minutes_spinbox.get()
    unjoined_cleaned_cutting_minutes = [char for char in entered_cutting_minutes if char.isdigit()]
    joined_cleaned_cutting_minutes = "".join(unjoined_cleaned_cutting_minutes)
    attendance_cutting_minutes_spinbox.set(joined_cleaned_cutting_minutes)

def process_punctuality_input(_: tk.Event) -> None:
    selected_student_punctuality = selected_attendance_punctuality.get()

    is_selected_tardy_status = selected_student_punctuality == constants.TARDY_STATUS
    is_selected_cutting_status = selected_student_punctuality == constants.CUTTING_STATUS

    configure_attendance_marking_spinbox(
        attendance_tardy_minutes_spinbox,
        is_selected_tardy_status,
        1 if is_selected_tardy_status else 0
    )

    configure_attendance_marking_spinbox(
        attendance_cutting_minutes_spinbox,
        is_selected_cutting_status,
        1 if is_selected_cutting_status else 0
    )

    match selected_student_punctuality:
        case constants.TARDY_STATUS:
            # print("Tardy Status Selected")
            attendance_tardy_minutes_spinbox.config(style="TSpinbox")
            attendance_cutting_minutes_spinbox.config(style="Disabled.TSpinbox")
        case constants.CUTTING_STATUS:
            # print("Cutting Status Selected")
            attendance_tardy_minutes_spinbox.config(style="Disabled.TSpinbox")
            attendance_cutting_minutes_spinbox.config(style="TSpinbox")
        case _:
            # print("Present or Absent Selected")
            attendance_tardy_minutes_spinbox.config(style="Disabled.TSpinbox")
            attendance_cutting_minutes_spinbox.config(style="Disabled.TSpinbox")

def configure_attendance_marking_spinbox(
        spinbox: ttk.Spinbox,
        enabled: bool,
        value: int
    ) -> None:
    state = constants.BUTTON_NORMAL_STATE if enabled else "disabled"
    spinbox.config(state=state)
    spinbox.set(value)

def frame_row_configure_looper(
        frame: ttk.Frame,
        counter_limit: int
    ) -> None:

    for counter in range(counter_limit):
        frame.rowconfigure(counter, weight=1)

def calendar_focus(event: tk.Event) -> None:
    event.widget._top_cal.focus_set()

def widget_remover(widget_list: list[ttk.Widget]) -> None:
    for widget in widget_list:
        widget.grid_forget()

def grid_layout_manager(widget_tuples: list[tuple[ttk.Widget, int, int, int, int, str]]) -> None:
    for widget_name, widget_row, widget_column, x_spacing, y_spacing, sticky in widget_tuples:
        widget_name.grid(
            row=widget_row, column=widget_column,
            padx=x_spacing, pady=y_spacing,
            sticky=sticky
        )

def pack_widget_loader(parent, widgets):
    for widget in widgets:
        widget.pack(in_=parent, pady=5)

def has_role_student(_: tk.Event) -> None:
    current_account_role = selected_account_role.get()
    grade_level_selector.set("")
    grade_section_selector.set("")
    if current_account_role.lower() == constants.STUDENT_ACCOUNT_STATUS:
        grid_layout_manager([
            (grade_year_label, 6, 0, (220, 10), 5, "w"),
            (grade_level_selector, 6, 1, (10, 220), 5, "")
        ])
    else:
        widget_remover([
            grade_level_selector, grade_section_selector,
            grade_year_label, grade_section_label
        ])

def show_section_selector(_: tk.Event) -> None:
    grade_section_selector.set("")
    selected_grade = int(selected_grade_level.get())
    if selected_grade in constants.POSSIBLE_GRADE_SECTIONS:
        grade_section_selector.config(values=constants.POSSIBLE_GRADE_SECTIONS[selected_grade])
        grid_layout_manager([
            (grade_section_label, 7, 0, (220, 10), 5, "w"),
            (grade_section_selector, 7, 1, (10, 220), 5, "")
        ])

# ===== ===== FIXME: Code Duplication - Needs Abstraction ===== =====
def show_possible_sections(_: tk.Event) -> None:
    selected_grade_level = int(selected_attendance_grade.get())
    selected_attendance_section.set('')
    attendance_section_selector.config(
        values=constants.POSSIBLE_GRADE_SECTIONS[selected_grade_level]
    )

def show_possible_subjects(_: tk.Event) -> None:
    entered_attendance_grade = int(selected_attendance_grade.get())
    selected_attendance_subject.set('')
    attendance_subject_selector.config(values=constants.GRADE_SUBJECTS[entered_attendance_grade])
# ===================================================================

def on_grade_selected(event: tk.Event) -> None:
    show_possible_sections(event)
    show_possible_subjects(event)

win = tk.Tk()
db.init_db()
components.apply_default_styles()

win.title("APACE - v0.5.2 (In Development)")

screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
center_x = int(screen_width/2 - constants.WINDOW_WIDTH / 2)
center_y = int(screen_height/2 - constants.WINDOW_HEIGHT / 2)

win.geometry(f"{constants.WINDOW_WIDTH}x{constants.WINDOW_HEIGHT}+{center_x}+{center_y}")
win.resizable(False, False)

# Frames
start_menu = ttk.Frame(win, style="TFrame")
signup_page = ttk.Frame(win, style="TFrame")
login_page = ttk.Frame(win, style="TFrame")

teacher_frame = ttk.Frame(win, style="TFrame")
dashboard_frame = ttk.Frame(win, style="TFrame")
attendance_marking_frame = ttk.Frame(win, style="TFrame")
attendance_create = ttk.Frame(win, style="TFrame")

student_frame = ttk.Frame(win, style="TFrame")
student_attendance_frame = ttk.Frame(win, style="TFrame")

admin_frame = ttk.Frame(win, style="TFrame")

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
    admin_frame,

    settings_frame,
    accessibility_frame,
    adjustment_frame
]

title = components.label_constructor(win, "Attendance Checker", "Title.TLabel")
title.grid(row=0, column=0, padx=10, pady=20, sticky="n")

current_session = AccountSession()
current_attendance = AttendanceSession()

signup_button = components.button_constructor(
    start_menu, "Sign Up",
    constants.BUTTON_NORMAL_STATE,
    "TButton", lambda: show_frame(signup_page)
)
login_button = components.button_constructor(
    start_menu, "Login",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: show_frame(login_page)
)

start_menu_widgets = [
    (signup_button, 1, 0, 315, 5, ""),
    (login_button, 2, 0, 315, 5, ""),
]

for counter in range(4):
    start_menu.rowconfigure(counter, minsize=20)
    start_menu.columnconfigure(counter, weight=1)
    grid_layout_manager(start_menu_widgets)
        
# ========== Logged Out ==========


# ================================
# ========== Sign Up ==========

# Account Name
signup_page_title = components.label_constructor(signup_page, "Account Creation", "Header.TLabel")
given_name_label = components.label_constructor(signup_page, "Given Name: ")
given_name_entry = components.entry_constructor(signup_page, 15)
surname_label = components.label_constructor(signup_page, "Surname: ")
surname_entry = components.entry_constructor(signup_page, 15)

# Account username
username_signup_label = components.label_constructor(signup_page, "Account Username: ")
username_signup_entry = components.entry_constructor(signup_page, 15)

# Account Role Selection
selected_account_role = tk.StringVar()
account_role_label = components.label_constructor(signup_page, "Account Role: ")
possible_account_roles = tuple(
    allowed_account_role.title()
    for allowed_account_role
    in constants.ALLOWED_ACCOUNT_ROLES
)
account_role_selector = components.combobox_constructor(
    frame=signup_page, input_holder=selected_account_role,
    values=possible_account_roles, state='readonly',
    width=15
)
account_role_selector.bind("<<ComboboxSelected>>", has_role_student)

# Grade Yr. and Section (If applicable)
grade_year_label = components.label_constructor(signup_page, "Grade Level: ")
selected_grade_level = tk.StringVar()
grade_level_selector = components.combobox_constructor(
    frame=signup_page, input_holder=selected_grade_level,
    values=constants.GRADE_LEVELS, state='readonly',
    width=15
)
grade_level_selector.bind("<<ComboboxSelected>>", show_section_selector)

selected_grade_section = tk.StringVar()
grade_section_label = components.label_constructor(signup_page, "Section: ")
grade_section_selector = components.combobox_constructor(
    frame=signup_page, input_holder=selected_grade_section,
    values=[], state='readonly',
    width=15
)

# Account Password

account_password_label = components.label_constructor(signup_page, "Account Password: ")
account_password_entry = components.entry_constructor(signup_page, 15)

account_password_entry.config(show="*")

create_account_button = components.button_constructor(
    signup_page, "Create Account",
    constants.BUTTON_NORMAL_STATE, "TButton",
    read_account_creation_fields
)
signup_back_button = components.button_constructor(
    signup_page, "Back",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: show_frame(start_menu)
)

signup_page_widgets = [
    (signup_page_title, 1, 0, (345, 10), 5, ""),

    (given_name_label, 2, 0, (220, 10), 5, "w"),
    (given_name_entry, 2, 1, (10, 220), 5, ""),
    (surname_label, 3, 0, (220, 10), 5, "w"),
    (surname_entry, 3, 1, (10, 220), 5, ""),
    (username_signup_label, 4, 0, (220, 10), 5, "w"),
    (username_signup_entry, 4, 1, (10, 220), 5, ""),

    (account_role_label, 5, 0, (220, 10), 5, "w"),
    (account_role_selector, 5, 1, (10, 220), 5, ""),
    (account_password_label, 8, 0, (220, 10), 5, "w"),
    (account_password_entry, 8, 1, (10, 220), 5, ""),

    (signup_back_button, 9, 0, (120, 5), 10, ""),
    (create_account_button, 9, 1, (5, 210) , 10, "")
]

for counter in range(10):
    signup_page.rowconfigure(counter, weight=1)

assign_widget_shortcut(
    (given_name_entry,
    surname_entry,
    username_signup_entry,
    account_role_selector,
    grade_level_selector,
    grade_section_selector,
    account_password_entry),

    constants.ENTER_KEY_SHORTCUT,

    account_creation_shortcut_handler
)

grid_layout_manager(signup_page_widgets)
# =============================

# ========== Login Page ==========
login_page_title = components.label_constructor(login_page, "Login", "Header.TLabel")
login_username_label = components.label_constructor(login_page, "Account Username: ")
login_username_entry = components.entry_constructor(login_page, 15)
login_password_label = components.label_constructor(login_page, "Password: ")
login_password_entry = components.entry_constructor(login_page, 15)
login_password_entry.config(show="*")

login_account_button = components.button_constructor(
    login_page, "Login",
    constants.BUTTON_NORMAL_STATE, "TButton",
    read_login_entries
)
login_back_button = components.button_constructor(
    login_page, "Back",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: show_frame(start_menu)
)

login_page_widgets = [
    (login_page_title, 1, 0, (380, 10), 5, ""), 
    (login_username_label, 2, 0, (220, 10), 5, "w"),
    (login_username_entry, 2, 1, (10, 220), 5, ""),
    (login_password_label, 3, 0, (220, 10), 5, "w"),
    (login_password_entry, 3, 1, (10, 220), 5, ""),
    (login_account_button, 4, 1, (15, 240), 10, ""),
    (login_back_button, 4, 0, (200, 15), 10, "")
]

assign_widget_shortcut(
    (login_username_entry,
    login_password_entry),

    constants.ENTER_KEY_SHORTCUT,
    login_shortcut_handler
)

grid_layout_manager(login_page_widgets)

frame_row_configure_looper(login_page, 10)

# ========== Teacher Menu ==========
# Main Menu Frame
menu_frame_menu_label = components.label_constructor(teacher_frame, "Main Menu", "Header.TLabel")
menu_frame_attendance_button = components.button_constructor(
    teacher_frame, "Dashboard",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: show_dashboard_frame(current_session, current_attendance)
)
teacher_menu_settings_button = components.button_constructor(
    teacher_frame, "Settings",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: show_frame(settings_frame)
)
teacher_menu_logout_button = components.button_constructor(
    teacher_frame, "Log Out",
    "TButton", command=lambda: menu_logout(current_session)
)

teacher_menu_widgets = [
    (menu_frame_menu_label, 1, 0, 345, 5, "w"),
    (menu_frame_attendance_button, 3, 0, 310, 5, "w"),
    (teacher_menu_settings_button, 5, 0, 310, 5, "w"),
    (teacher_menu_logout_button, 6, 0, 310, 5, "w")
]

grid_layout_manager(teacher_menu_widgets)


# Attendance Create
create_attendance_label = components.label_constructor(attendance_create, "Create Attendance", "Header.TLabel")

# Grade Level
attendance_grade_label = components.label_constructor(attendance_create, "Grade Level:")
selected_attendance_grade = tk.StringVar()
attendance_grade_selector = components.combobox_constructor(
    frame=attendance_create, input_holder=selected_attendance_grade,
     values=constants.GRADE_LEVELS, state='readonly',
     width=15
)

# Grade Section
attendance_section_label = components.label_constructor(attendance_create, "Grade Section: ")
selected_attendance_section = tk.StringVar()
attendance_section_selector = components.combobox_constructor(
    frame=attendance_create, input_holder=selected_attendance_section,
    values=[], state='readonly',
    width=15
)
attendance_grade_selector.current(0)

# Subject
attendance_subject_label = components.label_constructor(attendance_create, "Subject: ")
selected_attendance_subject = tk.StringVar()
attendance_subject_selector = components.combobox_constructor(
    frame=attendance_create, input_holder=selected_attendance_subject,
    values=[], state='readonly',
    width=15
)

attendance_grade_selector.bind("<<ComboboxSelected>>", on_grade_selected)

# Attendance Date
today = datetime.now().strftime(constants.DATE_FORMAT)
attendance_date_label = components.label_constructor(attendance_create, "Date: ")

attendance_date_picker = DateEntry(
    attendance_create, width=15,
    background='#003566', foreground='#f0f0f0',
    borderwidth=2, date_pattern='mm-dd-yyyy',
    maxdate=datetime.today())

attendance_date_picker.bind("<<DateEntryPopup>>", calendar_focus)

# Start Class schedule
attendance_period_label = components.label_constructor(attendance_create, "Period: ")
attendance_start_period_spinbox = ttk.Spinbox(
    attendance_create, from_=1,
    to=10, style="TSpinbox"
)


# Attendance Submission and back button
attendance_create_back = components.button_constructor(
    attendance_create, "Back",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: show_frame(teacher_frame)
)
attendance_create_button = components.button_constructor(
    attendance_create, "Create Attendance",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: read_attendance_input(current_session, current_attendance)
)


attendance_create_widgets = [
    (create_attendance_label, 1, 0, (320, 10), 5, ""),

    (attendance_grade_label, 2, 0, (225, 10), 5, "w"),
    (attendance_grade_selector, 2, 1, (10, 225), 5, ""),

    (attendance_section_label, 3, 0, (225, 10), 5, "w"),
    (attendance_section_selector, 3, 1, (10, 225), 5, ""),

    (attendance_subject_label, 4, 0, (225, 10), 5, "w"),
    (attendance_subject_selector, 4, 1, (10, 225), 5, ""),

    (attendance_date_label, 5, 0, (225, 10), 5, "w"),
    (attendance_date_picker, 5, 1, (10, 225), 5, ""),

    (attendance_period_label, 6, 0, (225, 10), 5, "w"),
    (attendance_start_period_spinbox, 6, 1, (10, 225), 5, ""),

    (attendance_create_back, 7, 0, (205, 20), 5, ""),
    (attendance_create_button, 7, 1, (20, 245), 5, "")
]

assign_widget_shortcut(
    (attendance_grade_selector,
    attendance_section_selector,
    attendance_subject_selector,
    attendance_date_picker,
    attendance_start_period_spinbox),

    constants.ENTER_KEY_SHORTCUT,

    lambda event: attendance_creation_shortcut_handler(
        event, current_session, current_attendance
    )
)

grid_layout_manager(attendance_create_widgets)

# ========== Student Menu ==========

student_menu_label = components.label_constructor(student_frame, "Main Menu", "Header.TLabel")
student_view_attendance_button = components.button_constructor(
    student_frame, "View Attendance",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: show_student_attendance(current_session)
)
teacher_menu_settings_button = components.button_constructor(
    student_frame, "Settings",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: show_frame(settings_frame)
)
student_menu_logout_button = components.button_constructor(
    student_frame, "Log Out",
    "TButton", command=lambda: menu_logout(current_session)
)

student_menu_widgets = [
    (student_menu_label, 1, 0, 5, 5, ""),
    (student_view_attendance_button, 2, 0, 300, 5, ""),
    (teacher_menu_settings_button, 3, 0, 300, 5, ""),
    (student_menu_logout_button, 4, 0, 300, 5, "")
]

grid_layout_manager(student_menu_widgets)


student_frame.columnconfigure(0, weight=1)
student_frame.columnconfigure(1, weight=0)
student_frame.columnconfigure(2, weight=0)

# ========== Admin Menu ==========
admin_menu_label = components.label_constructor(admin_frame, "Main Menu", "Header.TLabel")
admin_manage_users_button = components.button_constructor(
    admin_frame, "Manage Users",
    constants.BUTTON_NORMAL_STATE, "TButton",
    demo_msg
)
admin_activity_log_button = components.button_constructor(
    admin_frame, "Activity Log",
    constants.BUTTON_NORMAL_STATE, "TButton",
    demo_msg
)
admin_menu_settings_button = components.button_constructor(
    admin_frame, "Settings",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: show_frame(settings_frame)
)
admin_menu_logout_button = components.button_constructor(
    admin_frame, "Log Out",
    constants.BUTTON_NORMAL_STATE, "TButton",
    command=lambda: menu_logout(current_session)
)
admin_menu_widgets = [
    (admin_menu_label, 1, 0, 5, 5, ""),
    (admin_manage_users_button, 2, 0, 5, 5, ""),
    (admin_activity_log_button, 3, 0, 5, 5, ""),
    (admin_menu_settings_button, 4, 0, 5, 5, ""),
    (admin_menu_logout_button, 5, 0, 5, 5, "")
]

grid_layout_manager(admin_menu_widgets)

# ========== Settings Frame ==========
settings_frame_label = components.label_constructor(settings_frame, "Settings", "Header.TLabel")
settings_frame_accessibility_btn = components.button_constructor(
    settings_frame, "Accessibility",
    constants.BUTTON_NORMAL_STATE, "TButton",
    show_accessibility_frame
)
settings_frame_attendance_deletion = components.button_constructor(
    settings_frame, "Delete Attendances",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: delete_all_attendance_made(current_session)
)

setting_menu_btn = components.button_constructor(
    settings_frame, "Back",
    constants.BUTTON_NORMAL_STATE, widget_style="TButton",
    command=lambda: show_respective_menu(current_session)
)

settings_widgets = [
    (settings_frame_label, 1, 0, 300, 5, ""),
    (settings_frame_accessibility_btn, 2, 0, 300, 5, ""),
    (settings_frame_attendance_deletion, 3, 0, 300, 5, ""),
    (setting_menu_btn, 4, 0, 300, 10, "")
]

grid_layout_manager(settings_widgets)

# Settings - Accessibility Frame
accessibility_frame_label = components.label_constructor(
    accessibility_frame, "Accessibility",
    "Header.TLabel"
)

accessibility_frame_default_mode = components.button_constructor(
    accessibility_frame, "Default Display Mode",
    constants.BUTTON_NORMAL_STATE, "TButton",
    default_screen
)

accessibility_frame_high_contrast_btn = components.button_constructor(
    accessibility_frame, "High Contrast Mode",
    constants.BUTTON_NORMAL_STATE, "TButton",
    high_contrast_mode
)
accessibility_frame_text_adjustment_btn = components.button_constructor(
    accessibility_frame, "Display Adjustment",
    constants.BUTTON_NORMAL_STATE, "TButton",
    show_text_adjust
)
accessibility_frame_back_btn = components.button_constructor(
    accessibility_frame, "Back",
    constants.BUTTON_NORMAL_STATE, "TButton",
    command=settings_menu
)

accessibility_widgets = [
    (accessibility_frame_label, 1, 0, 300, 5, ""),
    (accessibility_frame_default_mode, 2, 0, 300, 5, ""),
    (accessibility_frame_high_contrast_btn, 3, 0, 300, 5, ""),
    (accessibility_frame_text_adjustment_btn, 4, 0, 300, 5, ""),
    (accessibility_frame_back_btn, 5, 0, 300, 10, "")
]

grid_layout_manager(accessibility_widgets)

# Accessibility -  Text Adjustment Frame

adjustment_frame_label = components.label_constructor(
    adjustment_frame, "Text and Display Size Adjustment",
    "Header.TLabel"
)

adjust_text_size_label = components.label_constructor(adjustment_frame, text="Adjust Text Size")
small_text_size_button = components.button_constructor(
    adjustment_frame, "Small Text",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: adjust_text_size(0.75, "Small")
)
default_text_size_button = components.button_constructor(
    adjustment_frame, "Default Text",
    constants.BUTTON_NORMAL_STATE, "TButton", lambda: adjust_text_size(1.00, "Default")
)
large_text_size_button = components.button_constructor(
    adjustment_frame, "Large Text",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: adjust_text_size(1.25, "Large")
)

adjustment_frame_menu_btn = components.button_constructor(
    adjustment_frame, "Back",
    constants.BUTTON_NORMAL_STATE,
    "TButton", show_accessibility_frame
)

adjustment_frame_widgets = [
    (adjustment_frame_label, 1, 0, 275, 5, ""),
    (adjust_text_size_label, 2, 0, 275, 5, ""),

    (small_text_size_button, 3, 0, 275, 5, ""),
    (default_text_size_button, 4, 0, 275, 5, ""),
    (large_text_size_button, 5, 0, 275, 5, ""),

    (adjustment_frame_menu_btn, 6, 0, 275, 5, ""),
]

grid_layout_manager(adjustment_frame_widgets)


# Attendance dashboard
dashboard_label = components.label_constructor(dashboard_frame, "Attendance dashboard", "Header.TLabel")
dashboard_label.grid(row=1, column=0, padx=5, pady=10)

dashboard_create_attendance = components.button_constructor(
    dashboard_frame, "Create Attendance",
    constants.BUTTON_NORMAL_STATE, "TButton", show_attendance_creation
)
dashboard_refersh = components.button_constructor(
    dashboard_frame, "Refresh",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: show_dashboard_frame(current_session, current_attendance)
)
dashboard_export = components.button_constructor(
    dashboard_frame, "Export CSV",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: call_attendance_exporter(current_session)
)

dashboard_attendance_sessions_label= components.label_constructor(dashboard_frame, "Attendance Sessions")

dashboard_back_button = components.button_constructor(
    dashboard_frame, "Back",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: show_frame(teacher_frame)
)

dashboard_widgets = [
    (dashboard_label, 1, 0, 50, 10, ""),
    (dashboard_create_attendance, 2, 0, (70, 10), 5, ""),
    (dashboard_refersh, 2, 1, (10, 10), 5, ""),
    (dashboard_export , 2, 2, (10, 70), 5, ""),
    (dashboard_attendance_sessions_label, 3, 0, (70, 70), 5, ""),
    (dashboard_back_button, 5, 1, 50, 10, "")
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

dashboard_table.grid(row=0, column=0, padx=(70, 0), pady=10, sticky="nsew")

dashboard_table.bind("<Double-Button-1>", read_selected_attendance)

for attendance_marking_table_column in dashboard_table["columns"]:
    dashboard_table.heading(
        attendance_marking_table_column, text=attendance_marking_table_column
    )

#  ========== Students' View Attendance Feature ==========
view_attendance_label = components.label_constructor(
    student_attendance_frame, "Student Attendance Records",
    "Header.TLabel"
)
view_attendance_back_button = components.button_constructor(
    student_attendance_frame, "Back",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: show_frame(student_frame)
)

student_view_attendance_widgets = [
    (view_attendance_label, 1, 0, 175, 10, ""),
    (view_attendance_back_button, 4, 0, 325, 10, "")
]

grid_layout_manager(student_view_attendance_widgets)

# ===== Student's Attendance Query =====
student_attendance_query_frame = ttk.Frame(student_attendance_frame)
student_attendance_query_frame.grid(row=2, column=0, columnspan=2)

view_attendance_query_label = components.label_constructor(
    student_attendance_query_frame, "Attendance Query: "
)
view_attendance_query_entry = components.entry_constructor(student_attendance_query_frame, 15)

view_attendance_query_entry.bind("<KeyRelease>", filter_view_attendance)

student_attendance_query_widgets = [
    (view_attendance_query_label, 2, 0, 5, 10, ""),
    (view_attendance_query_entry, 2, 1, 5, 10, ""),
]

grid_layout_manager(student_attendance_query_widgets)

# ======================================

view_student_attendance_table_frame = ttk.Frame(student_attendance_frame)

view_student_attendance_table_frame.grid(
    row=3, column=0,
    columnspan=2, sticky="nsew",
    padx=(10, 10)
)

view_attendance_scrollbar = ttk.Scrollbar(
    view_student_attendance_table_frame, orient="vertical"
)
view_attendance_scrollbar.grid(row=0, column=1, pady=5, sticky="ns")

student_view_attendance_table = ttk.Treeview(
    view_student_attendance_table_frame,
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

student_view_attendance_table.column("Attendance ID", width=100)
student_view_attendance_table.column("Date", width=100)
student_view_attendance_table.column("Subject", width=150)
student_view_attendance_table.column("Period", width=50)
student_view_attendance_table.column("Status", width=100)

view_attendance_rows = []

for student_attendance_column in student_view_attendance_table["columns"]:
    student_view_attendance_table.heading(
        student_attendance_column, text=student_attendance_column
    )

student_view_attendance_table.configure(yscrollcommand=view_attendance_scrollbar.set)
view_attendance_scrollbar.config(command=student_view_attendance_table.yview)

student_view_attendance_table.grid(row=0, column=0, padx=(125, 0), pady=20, sticky="nsew")

# ========== Attendance Marking Widgets ==========
attend_marking_label = components.label_constructor(attendance_marking_frame, "Session Info: ")
attend_attendance_info = components.label_constructor(attendance_marking_frame, "")
attendance_query_label = components.label_constructor(attendance_marking_frame, "Search Student: ")
attendance_marking_query = components.entry_constructor(attendance_marking_frame, 15, "TEntry")

attendance_marking_query.bind("<KeyRelease>", filter_marking_table)

attendance_widgets = [
    (attend_marking_label, 1, 0, 10, 10, "w"),
    (attend_attendance_info, 2, 0, 10, 10, ""),
    (attendance_query_label, 3, 0, (100, 10), 10, "w"),
    (attendance_marking_query, 3, 1, (10, 100), 10, "w")
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

for attendance_marking_column in attendance_table["columns"]:
    attendance_table.heading(attendance_marking_column, text=attendance_marking_column)

attendance_table.configure(yscrollcommand=attendance_scrollbar.set)
attendance_scrollbar.config(command=attendance_table.yview)

attendance_table.grid(row=0, column=0, padx=(100, 0), pady=10, sticky="nsew")

# ========== Attendance Marking Form ==========
attendance_marking_form_frame = ttk.Frame(attendance_marking_frame)
attendance_marking_form_frame.grid(row=5, column=0, columnspan=2, padx=75, sticky="e")

attendance_student_id_label = components.label_constructor(attendance_marking_form_frame, "Student ID: ")
attendance_student_id_spinbox = ttk.Spinbox(
    attendance_marking_form_frame, from_=1,
    style="TSpinbox"
)

selected_attendance_punctuality = tk.StringVar()
possible_attendance_punctuality = ("Present", "Absent", "Cutting", "Tardy")
attendance_punctuality_label = components.label_constructor(
    attendance_marking_form_frame, "Select Punctuality:"
)

attendance_punctuality_selector = components.combobox_constructor(
    frame=attendance_marking_form_frame, input_holder=selected_attendance_punctuality,
    values=possible_attendance_punctuality, state='readonly',
    width=15)

attendance_punctuality_selector.bind("<<ComboboxSelected>>", process_punctuality_input)

attendance_tardy_minutes_label = components.label_constructor(
    attendance_marking_form_frame, "Tardy Minutes: "
)
attendance_tardy_minutes_spinbox = ttk.Spinbox(
    attendance_marking_form_frame, from_=1,
    to=50, state='disabled',
    style="TSpinbox")

attendance_cutting_minutes_label = components.label_constructor(
    attendance_marking_form_frame, "Cutting Minutes: "
)
attendance_cutting_minutes_spinbox = ttk.Spinbox(
    attendance_marking_form_frame, from_=1,
    to=50, state='disabled',
    style="TSpinbox")
# =============================================

attendance_apply_changes = components.button_constructor(
    attendance_marking_form_frame, "Apply Changes",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: read_entered_attendance_marking(current_attendance)
)
attendance_back_button = components.button_constructor(
    attendance_marking_form_frame, "Back",
    constants.BUTTON_NORMAL_STATE, "TButton",
    lambda: show_dashboard_frame(current_session, current_attendance)
)

attendance_marking_widgets = [
    (attendance_student_id_label, 5, 0, (100, 10), 10, "w"),
    (attendance_student_id_spinbox, 5, 1, (10, 100), 10, "e"),

    (attendance_punctuality_label, 6, 0, (100, 10), 10, "w"),
    (attendance_punctuality_selector, 6, 1, (10, 100), 10, "e"),

    (attendance_tardy_minutes_label, 7, 0, (100, 10), 10, "w"),
    (attendance_tardy_minutes_spinbox, 7, 1, (10, 100), 10, "e"),

    (attendance_cutting_minutes_label, 8, 0 , (100, 10), 10, "w"),
    (attendance_cutting_minutes_spinbox, 8, 1, (10, 100), 10, "e"),

    (attendance_back_button, 9, 0, 5, 5, ""),
    (attendance_apply_changes, 9, 1, 5, 5, "")
]

assign_widget_shortcut(
    (attendance_student_id_spinbox,
     attendance_punctuality_selector,
     attendance_tardy_minutes_spinbox,
     attendance_cutting_minutes_spinbox),

    constants.ENTER_KEY_SHORTCUT,

    lambda event: attendance_marking_shortcut_handler(event, current_attendance)

)

assign_widget_shortcut(
    (attendance_tardy_minutes_spinbox,
     attendance_cutting_minutes_spinbox,
     attendance_student_id_spinbox), # <--
    # NOTE: This isn't technically part of the tardy/cutting
    # minutes, but the core purpose of the this function can also be applicable for here

    "<KeyRelease>",

    check_entered_truancy_characters
)

# NOTE: This is a temporary workaround for binding the widget/s to multiple functions
attendance_tardy_minutes_spinbox.bind("<KeyRelease>", check_truancy_input_length, add="+")
attendance_cutting_minutes_spinbox.bind("<KeyRelease>", check_truancy_input_length, add="+")

grid_layout_manager(attendance_marking_widgets)

attendance_marking_table_rows = []

win.protocol("WM_DELETE_WINDOW", on_closing)

if __name__ == "__main__":
    show_frame(start_menu)
    win.mainloop()
# ===================================
