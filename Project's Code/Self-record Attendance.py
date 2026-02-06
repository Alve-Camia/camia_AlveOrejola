# ==================================
# Imports

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime 
import bcrypt
from datetime import timedelta
import sqlite3
# ==================================

db_name = "attendance.db"

def get_db():
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash TEXT NOT NULL
    )
    """)

    # Attendance sessions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendances (
        name TEXT PRIMARY KEY,
        start_datetime TEXT,
        end_datetime TEXT,
        minutes_late INTEGER,
        password_hash TEXT,
        creator TEXT,
        countercheck INTEGER,
        question TEXT,
        answer TEXT
    )
    """)

    # Attendance submissions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attendance_name TEXT,
        user TEXT,
        login_time TEXT,
        status TEXT,
        late_minutes INTEGER,
        response TEXT,
        FOREIGN KEY (attendance_name) REFERENCES attendances(name),
        FOREIGN KEY (user) REFERENCES users(username),
        UNIQUE(attendance_name, user)
    )
    """)

    # Login logs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS login_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        timestamp TEXT
    )
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_sub_user ON submissions(user)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sub_attendance ON submissions(attendance_name)")

    conn.commit()
    conn.close()

def show_attendance_view():
    show_frame(view_frame)
    creator_table_rows.clear()

    for table in (creator_table, participant_table):
        for row in table.get_children():
            table.delete(row)

    user = win.current_user
    conn = get_db()
    cur = conn.cursor()

    # Creator view
    cur.execute("""
        SELECT a.name, s.user, s.login_time, s.status, s.late_minutes, s.response
        FROM attendances a
        LEFT JOIN submissions s ON a.name = s.attendance_name
        WHERE a.creator=?
    """, (user,))

    for row in cur.fetchall():
        row_id = creator_table.insert("", tk.END, values=row)
        creator_table_rows.append(row_id)

    # Participant view
    cur.execute("""
        SELECT attendance_name, status, login_time, user, response
        FROM submissions
        WHERE user=?
    """, (user,))

    for row in cur.fetchall():
        participant_table.insert("", tk.END, values=row)

    conn.close()


# ---------- Function to search creator table ----------
def search_attendance(event=None):
    if not creator_table_rows:
        return

    query = search_box.get().lower().strip()

    for row_id in creator_table_rows:
        values = creator_table.item(row_id, "values")
        row_text = " ".join(str(v).lower() for v in values)

        if query in row_text:
            creator_table.reattach(row_id, "", tk.END)
        else:
            creator_table.detach(row_id)

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

def clear_login_frame():
    login_frame_username_box.delete(0, tk.END)
    login_frame_password_box.delete(0, tk.END)

def light_screen():
    apply_theme(bg="#f0f0f0", fg="black", entry_bg="white")
    messagebox.showinfo("Background Change", "Light Mode Enabled")

def dark_screen():
    apply_theme(bg="#1c1c1c", fg="white", entry_bg="#2b2b2b")
    messagebox.showinfo("Background Change", "Dark Mode Enabled")

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

# Function that hides all frames and shows the frame used as an argument
def show_frame(frame): 
    for f in frames:
        f.pack_forget() 
    frame.pack(pady=10)

def clear_create_attendance():
    create_frame_name_box.delete(0, tk.END)
    create_frame_startdate_box.delete(0, tk.END)
    create_frame_start_time_box.delete(0, tk.END)
    create_frame_enddate_box.delete(0, tk.END)
    create_frame_endtime_box.delete(0, tk.END)
    create_frame_password_box.delete(0, tk.END)

def create_attendance():
    attendance_name = create_frame_name_box.get().strip().lower()
    input_start_date = create_frame_startdate_box.get()
    input_start_time = create_frame_start_time_box.get()
    input_end_date = create_frame_enddate_box.get()
    input_end_time = create_frame_endtime_box.get()
    attendance_password = create_frame_password_box.get()
    minutes_late = create_frame_minutes_box.get()
    user = win.current_user

    if not attendance_name.strip():
        messagebox.showwarning("Error", "Empty Attendance Name")
        return

    if not input_start_date.strip():
        messagebox.showwarning("Error", "Empty Start Date")
        return

    if not input_start_time.strip():
        messagebox.showwarning("Error", "Empty Start Time")
        return

    if not input_end_date.strip():
        messagebox.showwarning("Error", "Empty End Date")
        return

    if not input_end_time.strip():
        messagebox.showwarning("Error", "Empty End Time")
        return

    if not attendance_password.strip():
        messagebox.showwarning("Error", "Empty Password")
        return

    if len(attendance_password) < 10:
        messagebox.showwarning("Error", "Please make password at least 10 characters long")
        return
    
    if not minutes_late.strip():
        messagebox.showwarning("Error", "Empty minutes till late")
        return

    try:
        start_date = datetime.strptime(input_start_date, "%m-%d-%Y").date()
        start_time = datetime.strptime(input_start_time, "%H:%M").time()
        
        end_date = datetime.strptime(input_end_date, "%m-%d-%Y").date()
        end_time = datetime.strptime(input_end_time, "%H:%M").time()
        
        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(end_date, end_time)


        minutes_late = int(minutes_late)

        if start_datetime > end_datetime:
            messagebox.showwarning("Error", "End Time is earlier than start time")
            return
        
        if start_datetime == end_datetime:
            messagebox.showwarning("Error", "Start Time is the same time as end time")
            return

        if minutes_late < 0:
            messagebox.showwarning("Error", "Minutes till late cannot be negative")
            return
        
        question = ""
        answer = ""

        required_countercheck = messagebox.askyesno("Required Countercheck", "Require counterchecking for attendees?")
        if required_countercheck == True:
            question = simpledialog.askstring("Countercheck Question", "Enter the counterchecking question here: ", parent=win)
            while not question or not question.strip():
                question = simpledialog.askstring("Error", "Empty Input. Please enter counterchecking question here: ", parent=win)
            answer = ""
            answer = simpledialog.askstring("Countercheck Question", "Enter the counterchecking answer here: ", parent=win)
            while not answer or not answer.strip():
                answer = simpledialog.askstring("Error", "Empty Input. Please enter counterchecking answer here: ", parent=win)
        
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT 1 FROM attendances WHERE LOWER(name)=LOWER(?)",
            (attendance_name,)
        )

        if cur.fetchone():
            messagebox.showwarning("Error", "Attendance name already exists")
            conn.close()
            return
        
        hashed_attendance_password = hash_password(attendance_password).decode("utf-8")


        cur.execute("""
            INSERT INTO attendances
            (name, start_datetime, end_datetime, minutes_late, password_hash, creator,
            countercheck, question, answer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                attendance_name,
                start_datetime.isoformat(),
                end_datetime.isoformat(),
                minutes_late,
                hashed_attendance_password,
                user,
                int(required_countercheck),
                question,
                answer
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Attendance created successfully")
        clear_create_attendance()
        show_frame(attendance_frame)

    except ValueError:
        messagebox.showwarning("Error", "Invalid Inputs")
        return

def fillout_attendance():
    attendance_name = fillout_frame_name_box.get().strip().lower()
    attendance_password = fillout_frame_password_box.get()

    if not attendance_name or not attendance_password:
        messagebox.showwarning("Error", "Please enter attendance name and password")
        return

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT start_datetime, end_datetime, minutes_late,
               password_hash, countercheck, question, answer
        FROM attendances
        WHERE LOWER(name)=LOWER(?)
    """, (attendance_name,))

    row = cur.fetchone()
    conn.close()

    if not row:
        messagebox.showwarning("Error", "Attendance name or password is incorrect")
        return

    start_dt, end_dt, minutes_late, stored_hash, countercheck, question, answer = row

    if not bcrypt.checkpw(attendance_password.encode(), stored_hash.encode()):
        messagebox.showwarning("Error", "Attendance name or password is incorrect")
        return
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT 1 FROM submissions
        WHERE LOWER(attendance_name)=LOWER(?) AND user=(?)
    """, (attendance_name, win.current_user))

    if cur.fetchone():
        messagebox.showwarning("Error", "You have already submitted this attendance")
        conn.close()
        return

    conn.close()


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

    response = ""
    if countercheck:
        response = simpledialog.askstring("Countercheck", question)
        if not response or response.strip().lower() != answer.strip().lower():
            messagebox.showwarning("Error", "Incorrect countercheck response")
            return

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO submissions
        (attendance_name, user, login_time, status, late_minutes, response)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        attendance_name,
        win.current_user,
        now.strftime("%m-%d-%Y %H:%M"),
        status,
        late_minutes,
        response
    ))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", f"Attendance recorded: {status}")
    clear_fillout_attendance()


def hash_password(password):
    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(pw_bytes, salt)
    return hashed_pw

def logout():
    logout_decision = messagebox.askyesno("Logging Out", "Are you sure you want to log out?")
    if logout_decision == True:
        menu_frame_msg_label.config(text="")
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
    
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM users WHERE LOWER(username)=LOWER(?)",
        (username,)
    )

    if cur.fetchone():
        messagebox.showwarning("Error", "Username already exists")
        conn.close()
        clear_login_frame()
        return

    hashed = hash_password(password).decode("utf-8")

    cur.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, hashed)
    )

    conn.commit()
    conn.close()
    
    messagebox.showinfo("Notice", "Sign Up Successful")
    clear_login_frame()
    return

def login():
    username = login_frame_username_box.get()
    password = login_frame_password_box.get()

    if not username or not password:
        messagebox.showwarning("Error", "Please enter username and password.")
        return

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT password_hash FROM users WHERE LOWER(username)=LOWER(?)",
        (username,)
    )

    row = cur.fetchone()
    conn.close()

    if not row:
        messagebox.showwarning("Error", "User not found")
        clear_login_frame()
        return

    stored_hash = row[0].encode("utf-8")

    if not bcrypt.checkpw(password.encode("utf-8"), stored_hash):
        messagebox.showwarning("Error", "Incorrect password")
        clear_login_frame()
        return

    #Successful login
    win.current_user = username
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    menu_frame_msg_label.config(text=f"{username} logged IN at {time}")
    fillout_frame_currentuser_label.config(text=f"Current User: {username}")
    show_frame(menu_frame)

    # Log login
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO login_logs (user, timestamp) VALUES (?, ?)",
        (username, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def update_clock():
    """Updates the clock in the main menu every second"""
    current_time = datetime.now().strftime("%B %d, %Y - %H:%M:%S (%a)")
    menu_frame_time_label.config(text=f"Current time: {current_time}")
    win.after(1000, update_clock)

win = tk.Tk()
init_db()

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
win.geometry("1200x1200")
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
    settings_frame,
    fillout_frame,
    appearance_frame,
    view_frame
]

title = tk.Label(win, text="Attendance Checker", font=("Montserrat", 24))
title.pack(pady=(10,10))

menu_time = datetime.now().strftime("%B %d, %Y - %H:%M:%S (%a)")

#Login Frame
login_frame_username_label = tk.Label(login_frame, text="Enter Account Name (letters and spaces only):", font=("Arial", 12))
login_frame_username_box = tk.Entry(login_frame, width=30)
login_frame_password_label = tk.Label(login_frame, text="Enter Password (must contain 10 characters or more):", font=("Arial", 12))
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
attendance_frame_attendance_label = tk.Label(attendance_frame, text="Attendance Options", font=("Arial", 12))
attendance_frame_attendance_create_btn = tk.Button(attendance_frame, text="Create Attendance", width=15, font=("Montserrat", 12), command=attendance_create_menu)



    
attendance_frame_attendance_view_btn = tk.Button(attendance_frame, text="View Attendances", width=15, font=("Montserrat", 12), command=show_attendance_view)
attendance_frame_attendance_fillout_btn = tk.Button(attendance_frame, text="Fill out Attendance", width=15, font=("Montserrat", 12), command=attendance_fillout_menu)
attendance_frame_menu_btn1 = tk.Button(attendance_frame, text="Main Menu", width=15, font=("Montserrat", 12), command=main_menu)

attendance_frame_widgets = [
    attendance_frame_attendance_label, 
    attendance_frame_attendance_create_btn, 
    attendance_frame_attendance_view_btn, 
    attendance_frame_attendance_fillout_btn, 
    attendance_frame_menu_btn1
]

for attendance_widgets in attendance_frame_widgets:
    attendance_widgets.pack(pady=5)

# Attendance Frame: Create
create_frame_label = tk.Label(create_frame, text="Create Attendance", font=("Arial", 15))
create_frame_name_label = tk.Label(create_frame, text="Attendance Name: ", font=("Arial", 12))
create_frame_name_box = tk.Entry(create_frame, width=30)

create_frame_startdate_label = tk.Label(create_frame, text="Start: Date checking attendance (MM-DD-YYYY): ", font=("Arial", 12))
create_frame_startdate_box = tk.Entry(create_frame, width=15)
create_frame_start_time_label = tk.Label(create_frame, text="Start: Time checking attendance (HH:MM): ", font=("Arial", 12))
create_frame_start_time_box = tk.Entry(create_frame, width=15)

create_frame_enddate_label = tk.Label(create_frame, text="End: Date checking attendance (MM-DD-YYYY): ", font=("Arial", 12))
create_frame_enddate_box = tk.Entry(create_frame, width=15)
create_frame_endtime_label = tk.Label(create_frame, text="End: Time checking attendance (HH:MM): ", font=("Arial", 12))
create_frame_endtime_box = tk.Entry(create_frame, width=15)
create_frame_notice_label = tk.Label(create_frame, text="*Use 24-hour format", font=("Arial", 10))

create_frame_minutes_late = tk.Label(create_frame, text="Minutes past start time until late ", font=("Arial", 12))
create_frame_minutes_box = tk.Entry(create_frame, width=15)

create_frame_password_label = tk.Label(create_frame, text="Assign attendance a password: ", font=("Arial", 12))
create_frame_password_box = tk.Entry(create_frame, width=30, show="*")

create_attendance_btn = tk.Button(create_frame, text="Make attendance", width=15, font=("Montserrat", 12), command=create_attendance)

menu_btn2 = tk.Button(create_frame, text="Main Menu", width=15, font=("Montserrat", 12), command=main_menu)

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
    menu_btn2
]

for create_widget in create_widgets:
    create_widget.pack(pady=5)

# Attendance Frame: Fill out
fillout_frame_currentuser_label = tk.Label(fillout_frame, text=f"Current User: {win.current_user}", font=("Arial", 12))
fillout_frame_attendance_label = tk.Label(fillout_frame, text=f"Enter Attendance Name", font=("Arial", 12))
fillout_frame_name_box = tk.Entry(fillout_frame, width=30)
fillout_frame_password_label = tk.Label(fillout_frame, text="Enter Attendance Password", font=("Arial", 12))
fillout_frame_password_box = tk.Entry(fillout_frame, width=30, show="*")
fillout_frame_record_btn = tk.Button(fillout_frame, text="Record Attendance", width=15, font=("Montserrat", 12), command=fillout_attendance)
menu_btn4 = tk.Button(fillout_frame, text="Main Menu", width=15, font=("Montserrat", 12), command=main_menu)

fillout_frame_widgets = [
    fillout_frame_currentuser_label, 
    fillout_frame_attendance_label, 
    fillout_frame_name_box, 
    fillout_frame_password_label, 
    fillout_frame_password_box, 
    fillout_frame_record_btn,
    menu_btn4
]

for fillout_widgets in fillout_frame_widgets:
    fillout_widgets.pack(pady=5)

# Settings Frame
settings_frame_label = tk.Label(settings_frame, text="Settings", font=("Arial", 12))
settings_frame_password_btn = tk.Button(settings_frame, text=f"Reset Password", width=30, font=("Montserrat", 12), command=demo_msg)
settings_frame_appearance_btn = tk.Button(settings_frame, text="Appearance", width=30, font=("Montserrat", 12), command=show_appearance_frame)
menu_btn3 = tk.Button(settings_frame, text="Main Menu", width=15, font=("Montserrat", 12), command=main_menu)

settings_widgets = [
    settings_frame_label, 
    settings_frame_password_btn, 
    settings_frame_appearance_btn, 
    menu_btn3
]

for setting_widget in settings_widgets:
    setting_widget.pack(pady=5)

# Settings - Appearance Frame
appearance_frame_light_btn = tk.Button(appearance_frame, text=f"Light Mode", width=30, font=("Montserrat", 12), command=light_screen)
appearance_frame_dark_btn = tk.Button(appearance_frame, text=f"Dark Mode", width=30, font=("Montserrat", 12), command=dark_screen)
menu_btn5 = tk.Button(appearance_frame, text="Main Menu", width=15, font=("Montserrat", 12), command=main_menu)

appearance_widgets = [
    appearance_frame_light_btn, 
    appearance_frame_dark_btn, 
    menu_btn5
]

for appearance_widget in appearance_widgets:
    appearance_widget.pack(pady=5)


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

creator_table = ttk.Treeview(view_frame, columns=("Attendance", "User", "Login", "Status", "Minutes Late ", "Response"), show="headings", height=8)
for col in creator_table["columns"]:
    creator_table.heading(col, text=col)
creator_table.pack(pady=5)
creator_table_rows = []

# Participant Table
participant_table_label = tk.Label(view_frame, text="Participant View: Your Attendances", font=("Arial", 12))
participant_table_label.pack(pady=5)

participant_table = ttk.Treeview(
    view_frame,
    columns=("Attendance", "Status", "Login", "User", "Response"),
    show="headings",
    height=8
)
for col in participant_table["columns"]:
    participant_table.heading(col, text=col)
participant_table.pack(pady=5)

menu_btn6 = tk.Button(view_frame, text="Main Menu", width=15, font=("Montserrat", 12), command=main_menu)
menu_btn6.pack(pady=10)

show_frame(login_frame)
update_clock()
win.mainloop()
