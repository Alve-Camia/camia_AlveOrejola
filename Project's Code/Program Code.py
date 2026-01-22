import tkinter as tk # For user interface
from tkinter import messagebox # For error handling and messages
from datetime import datetime # For checking log in time


def demo_msg():
    demo_label.config(text="Still in development...")
    menu_btn.pack(pady=5)

def main_menu():
    msg_label.config(text="")
    demo_label.config(text="")
    menu_btn.pack_forget()
    attendance_label.pack_forget()
    attendance_create_btn.pack_forget()
    attendance_view_btn.pack_forget()
    attendance_fillout_btn.pack_forget()

    menu_time_label.pack(pady=5)

    main_menu_label.pack(pady=10)
    attendance_btn.pack(pady=5)
    
    
    logout_btn.pack(pady=5)

def attendance_menu():
    menu_time_label.pack_forget()
    main_menu_label.pack_forget()
    logout_btn.pack_forget()
    attendance_btn.pack_forget()

    
    attendance_label.pack(pady=5)
    attendance_create_btn.pack(pady=5)
    attendance_view_btn.pack(pady=5)
    attendance_fillout_btn.pack(pady=5)


def logout():
    
    msg_label.config(text="")
    username_box.delete(0, tk.END)
    password_box.delete(0, tk.END)
    menu_time_label.pack_forget()
    
    username_label.pack(pady=(10,3))
    username_box.pack(pady=(3,10))
    password_label.pack(pady=(5,3))
    password_box.pack(pady=(3,10))
    signup_btn.pack(pady=5)
    login_btn.pack(pady=5)
    
    logout_btn.pack_forget()
    main_menu_label.pack_forget()
    attendance_btn.pack_forget()

def signup():
    username = username_box.get()
    password = password_box.get()

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
        f.write(username + "," + password + "\n")
    
    messagebox.showinfo("Signed Up", "Sign Up Successful!")
    username_box.delete(0, tk.END)
    password_box.delete(0, tk.END)

def login():
    username = username_box.get()
    password = password_box.get()

    if username == "" or password == "":
        messagebox.showwarning("Error", "Please enter username and password.")
        return

    found = False
    try:
        with open("users.txt", "r") as f:
            for line in f:
                user, pw = line.strip().split(",")
                if user == username and pw == password:
                    found = True
                    break
    except FileNotFoundError:
        messagebox.showwarning("Error", "No users signed up yet.")
        return

    if found:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg_label.config(text=username + " logged IN at " + time)
        username_label.pack_forget()
        username_box.pack_forget()
        password_label.pack_forget()
        password_box.pack_forget()
        signup_btn.pack_forget()
        login_btn.pack_forget()

        menu_btn.pack(pady=5)
        
        with open("attendance.txt", "a") as file:
            file.write(username + " logged IN at " + time + "\n")
    else:
        messagebox.showwarning("Error", "Invalid account name or password. Please try again.")

#GUI

win = tk.Tk()
win.title("Attendance Checker")
win.geometry("500x500")

title = tk.Label(win, text="Attendance Checker", font=("Montserrat", 24))
title.pack(pady=(20,10))

# Widgets: Username
username_label = tk.Label(win, text="Enter Account Name (letters only):", font=("Arial", 12))
username_label.pack(pady=(10,3))
username_box = tk.Entry(win, width=30)
username_box.pack(pady=(3,10))

# Widgets: Password
password_label = tk.Label(win, text="Enter Password (must contain 8 characters or more):", font=("Arial", 12))
password_label.pack(pady=(5,3))
password_box = tk.Entry(win, width=30, show="*")
password_box.pack(pady=(3,10))

# Widgets: Sign up and Log in 
signup_btn = tk.Button(win, text="Sign Up", width=15, font=("Montserrat", 12), command=signup)
signup_btn.pack(pady=5)

login_btn = tk.Button(win, text="Log In", width=15, font=("Montserrat", 12), command=login)
login_btn.pack(pady=5)

menu_btn = tk.Button(win, text="Main menu", width=15, font=("Montserrat", 12), command=main_menu)
main_menu_label = tk.Label(win, text="Main Menu", font=("Arial", 12))
attendance_btn = tk.Button(win, text="Attendance", width=15, font=("Montserrat", 12), command=attendance_menu)
logout_btn = tk.Button(win, text="Log Out", width=15, font=("Montserrat", 12), command=logout)
menu_time = datetime.now().strftime("%B %d, %Y - %H:%M:%S (%a)")
menu_time_label = tk.Label(win, text=f"Current time: {menu_time}", font=("Arial", 12))

attendance_label = tk.Label(win, text="Attendance Options", font=("Arial", 12))
attendance_create_btn = tk.Button(win, text="Create Attendance", width=15, font=("Montserrat", 12), command=demo_msg)
attendance_view_btn = tk.Button(win, text="View Attendances", width=15, font=("Montserrat", 12), command=demo_msg)
attendance_fillout_btn = tk.Button(win, text="Fill out Attendance", width=15, font=("Montserrat", 12), command=demo_msg)

#msg
msg_label = tk.Label(win, text="", fg="green", font=("Arial", 12))
msg_label.pack(pady=10)

demo_label = tk.Label(win, text="", fg="orange", font=("Arial", 12))
demo_label.pack(pady=10)

win.mainloop()
