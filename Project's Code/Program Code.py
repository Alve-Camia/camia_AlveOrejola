import tkinter as tk 
from tkinter import messagebox
import bcrypt

def hash_password(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash
def attendance_create_menu():
    show_frame(create_frame)

def settings_menu():
    show_frame(settings_frame)

def demo_msg():
    messagebox.showwarning("Error - Part not coded", "This part is yet to be made.")

def main_menu():
    show_frame(menu_frame)

def attendance_menu():
    show_frame(attendance_frame)

def logout():
    menu_frame_msg_label.config(text="")
    login_frame_username_box.delete(0, tk.END)
    login_frame_password_box.delete(0, tk.END)
    show_frame(login_frame)

# Function that hides all frames and shows the frame used as an argument
def show_frame(frame): 
    for f in (login_frame, menu_frame, attendance_frame, create_frame, settings_frame):
        f.pack_forget() 
    frame.pack(pady=20)

def signup():
    username = login_frame_username_box.get()
    password = login_frame_password_box.get()

    if username == "":
        messagebox.showwarning("Error", "Please enter a username.")
        return

    if all(c.isspace() for c in username):
        messagebox.showwarning("Error - Empty Username", "Please do not make your username only spaces.")
        return
    
    if not all(c.isalpha() or c.isspace() for c in username):
        messagebox.showwarning("Error", "Username must contain letters and spaces only.")
        return

    if len(password) < 8:
        messagebox.showwarning("Error", "Password must be at least 8 characters long.")
        return
    
    with open("users.txt", "a") as f:
        hashed = hash_password(password).decode('utf-8')
        f.write(f"{username},{hashed}\n")
    
    messagebox.showinfo("Signed Up", "Sign Up Successful!")
    login_frame_username_box.delete(0, tk.END)
    login_frame_password_box.delete(0, tk.END)

def login():
    username = login_frame_username_box.get()
    password = login_frame_password_box.get()

    if username == "" or password == "":
        messagebox.showwarning("Error", "Please enter username and password.")
        return

    try:
        with open("users.txt", "r") as f:
            for line in f:
                user, pw = line.strip().split(",", 1)
                if user == username:
                    stored_hash = pw.encode('utf-8')
                    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        menu_frame_msg_label.config(text=f"{username} logged IN at {time}")
                        show_frame(menu_frame)

                        with open("attendance.txt", "a") as file:
                            file.write(f"{username} logged in at {time}\n")
                        return
    except FileNotFoundError:
        messagebox.showwarning("Error", "No users signed up yet.")
        return

    messagebox.showwarning("Error", "Invalid account name or password.")


# For updating the clock in main menu every second 
def update_clock():
    current_time = datetime.now().strftime("%B %d, %Y - %H:%M:%S (%a)")
    menu_frame_time_label.config(text=f"Current time: {current_time}")
    win.after(1000, update_clock) 
    
win = tk.Tk()
win.title("Attendance Checker")
win.geometry("650x650")

login_frame = tk.Frame(win)
menu_frame = tk.Frame(win)
attendance_frame = tk.Frame(win)
create_frame = tk.Frame(win)
settings_frame = tk.Frame(win)

title = tk.Label(win, text="Attendance Checker", font=("Montserrat", 24))
title.pack(pady=(20,10))

menu_time = datetime.now().strftime("%B %d, %Y - %H:%M:%S (%a)")

#Login Frame
login_frame_username_label = tk.Label(login_frame, text="Enter Account Name (letters and spaces only):", font=("Arial", 12))
login_frame_username_box = tk.Entry(login_frame, width=30)
login_frame_password_label = tk.Label(login_frame, text="Enter Password (must contain 8 characters or more):", font=("Arial", 12))
login_frame_password_box = tk.Entry(login_frame, width=30, show="*")
login_frame_signup_btn = tk.Button(login_frame, text="Sign Up", width=15, font=("Montserrat", 12), command=signup)
login_frame_login_btn = tk.Button(login_frame, text="Log In", width=15, font=("Montserrat", 12), command=login)

login_frame_widgets = [login_frame_username_label, login_frame_username_box, login_frame_password_label, login_frame_password_box, login_frame_signup_btn, login_frame_login_btn]
for login_widgets in login_frame_widgets:
    login_widgets.pack(pady=5)

#Main Menu Frame
menu_frame_msg_label = tk.Label(menu_frame, text="", fg="green", font=("Arial", 12))
menu_frame_time_label = tk.Label(menu_frame, text=f"Current time: {menu_time}", font=("Arial", 12))
menu_frame_menu_label = tk.Label(menu_frame, text="Main Menu", font=("Arial", 12))
menu_frame_attendance_btn = tk.Button(menu_frame, text="Attendance", width=15, font=("Montserrat", 12), command=attendance_menu)
menu_frame_settings_btn = tk.Button(menu_frame, text="Settings", width=15, font=("Montserrat", 12), command=settings_menu)
menu_frame_logout_btn = tk.Button(menu_frame, text="Log Out", width=15, font=("Montserrat", 12), command=logout)

menu_frame_widgets = [menu_frame_msg_label, menu_frame_time_label, menu_frame_menu_label, menu_frame_attendance_btn, menu_frame_settings_btn, menu_frame_logout_btn]
for menu_widgets in menu_frame_widgets:
    menu_widgets.pack(pady=5)

# Sub-menu Attendance Frame
attendance_frame_attendance_label = tk.Label(attendance_frame, text="Attendance Options", font=("Arial", 12))
attendance_frame_attendance_create_btn = tk.Button(attendance_frame, text="Create Attendance", width=15, font=("Montserrat", 12), command=attendance_create_menu)
attendance_frame_attendance_view_btn = tk.Button(attendance_frame, text="View Attendances", width=15, font=("Montserrat", 12), command=demo_msg)
attendance_frame_attendance_fillout_btn = tk.Button(attendance_frame, text="Fill out Attendance", width=15, font=("Montserrat", 12), command=demo_msg)
attendance_frame_menu_btn1 = tk.Button(attendance_frame, text="Main menu", width=15, font=("Montserrat", 12), command=main_menu)

attendance_frame_widgets = [attendance_frame_attendance_label, attendance_frame_attendance_create_btn, attendance_frame_attendance_view_btn, attendance_frame_attendance_fillout_btn, attendance_frame_menu_btn1]
for attendance_widgets in attendance_frame_widgets:
    attendance_widgets.pack(pady=5)

# Attendance: Create Frame
create_frame_label_label = tk.Label(create_frame, text="Create Attendance", font=("Arial", 15))
create_frame_name_label = tk.Label(create_frame, text="Attendance Name: ", font=("Arial", 12))
create_frame_name_box = tk.Entry(create_frame, width=30)

create_frame_startdate_label = tk.Label(create_frame, text="Start: DATE checking attendance (MM-DD-YYYY): ", font=("Arial", 12))
create_frame_startdate_box = tk.Entry(create_frame, width=30)
create_frame_starttime_label = tk.Label(create_frame, text="Start: TIME checking attendance (HH-MM-SS): ", font=("Arial", 12))
create_frame_starttime_box = tk.Entry(create_frame, width=30)

create_frame_enddate_label = tk.Label(create_frame, text="End: Date checking attendance (MM-DD-YYYY): ", font=("Arial", 12))
create_frame_enddate_box = tk.Entry(create_frame, width=30)
create_frame_endtime_label = tk.Label(create_frame, text="END: TIME checking attendance (HH-MM-SS): ", font=("Arial", 12))
create_frame_endtime_box = tk.Entry(create_frame, width=30)

create_frame_password_label = tk.Label(create_frame, text="Assign attendance a password: ", font=("Arial", 12))
create_frame_password_box = tk.Entry(create_frame, width=30, show="*")

create_attendance_btn = tk.Button(create_frame, text="Make attendance", width=15, font=("Montserrat", 12), command=demo_msg)

menu_btn2 = tk.Button(create_frame, text="Main menu", width=15, font=("Montserrat", 12), command=main_menu)

create_frame_label_label.pack(pady=5)
create_frame_name_label.pack(pady=5)
create_frame_name_box.pack(pady=5)

create_frame_startdate_label.pack(pady=5)
create_frame_startdate_box.pack(pady=5)
create_frame_starttime_label.pack(pady=5)
create_frame_starttime_box.pack(pady=5)

create_frame_enddate_label.pack(pady=5)
create_frame_enddate_box.pack(pady=5)
create_frame_endtime_label.pack(pady=5)
create_frame_endtime_box.pack(pady=5)

create_frame_password_label.pack(pady=5)
create_frame_password_box.pack(pady=5)

create_attendance_btn.pack(pady=5)
menu_btn2.pack(pady=5)

# Settings Frame
settings_frame_label_label = tk.Label(settings_frame, text="Settings", font=("Arial", 12))
settings_frame_password_btn = tk.Button(settings_frame, text="Change Account Password", width=30, font=("Montserrat", 12), command=demo_msg)
settings_frame_appearance_btn = tk.Button(settings_frame, text="Appearance", width=30, font=("Montserrat", 12), command=demo_msg)
menu_btn3 = tk.Button(settings_frame, text="Main Menu", width=15, font=("Montserrat", 12), command=main_menu)

settings_frame_label_label.pack(pady=5)
settings_frame_password_btn.pack(pady=5)
settings_frame_appearance_btn.pack(pady=5)
menu_btn3.pack(pady=5)

show_frame(login_frame)
update_clock()
win.mainloop()
