import tkinter as tk # For user interface
from tkinter import messagebox # For error handling and messages
from datetime import datetime # For checking log in time


def demo_msg():
    demo_label.config(text="Still in development...")

def main_menu():
    show_frame(menu_frame)

def attendance_menu():
    show_frame(attendance_frame)

def logout():
    msg_label.config(text="")
    username_box.delete(0, tk.END)
    password_box.delete(0, tk.END)
    show_frame(login_frame)

def show_frame(frame): # This takes in the argument when the function was called
    for f in (login_frame, menu_frame, attendance_frame): # List of frames that f is part of
        f.pack_forget() # Makes all frames not visible
    frame.pack(pady=20) # Packs the frame that was used an argument in the function

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
        show_frame(menu_frame)

        menu_btn.pack(pady=5)
        
        with open("attendance.txt", "a") as file:
            file.write(username + " logged IN at " + time + "\n")
    else:
        messagebox.showwarning("Error", "Invalid account name or password. Please try again.")

# Framework of the program
win = tk.Tk()
win.title("Attendance Checker")
win.geometry("500x500")

# Instantiates the frames
login_frame = tk.Frame(win)
menu_frame = tk.Frame(win)
attendance_frame = tk.Frame(win)

title = tk.Label(win, text="Attendance Checker", font=("Montserrat", 24))
title.pack(pady=(20,10))

menu_time = datetime.now().strftime("%B %d, %Y - %H:%M:%S (%a)")

#Configs the menu_time label after 1 sec
def update_clock():
    current_time = datetime.now().strftime("%B %d, %Y - %H:%M:%S (%a)")
    menu_time_label.config(text=f"Current time: {current_time}")
    win.after(1000, update_clock) #Configs the menu_time label after 1 sec

#Login Frame
username_label = tk.Label(login_frame, text="Enter Account Name (letters only):", font=("Arial", 12))
username_box = tk.Entry(login_frame, width=30)

password_label = tk.Label(login_frame, text="Enter Password (must contain 8 characters or more):", font=("Arial", 12))
password_box = tk.Entry(login_frame, width=30, show="*")

signup_btn = tk.Button(login_frame, text="Sign Up", width=15, font=("Montserrat", 12), command=signup)
login_btn = tk.Button(login_frame, text="Log In", width=15, font=("Montserrat", 12), command=login)

username_label.pack(pady=(10,3))
username_box.pack(pady=(3,10))
password_label.pack(pady=(5,3))
password_box.pack(pady=(3,10))
signup_btn.pack(pady=5)
login_btn.pack(pady=5)

#Main Menu Frame
msg_label = tk.Label(menu_frame, text="", fg="green", font=("Arial", 12))
menu_time_label = tk.Label(menu_frame, text=f"Current time: {menu_time}", font=("Arial", 12))
main_menu_label = tk.Label(menu_frame, text="Main Menu", font=("Arial", 12))
attendance_btn = tk.Button(menu_frame, text="Attendance", width=15, font=("Montserrat", 12), command=attendance_menu)
logout_btn = tk.Button(menu_frame, text="Log Out", width=15, font=("Montserrat", 12), command=logout)

msg_label.pack(pady=5)
menu_time_label.pack(pady=5)
main_menu_label.pack(pady=5)
attendance_btn.pack(pady=5)
logout_btn.pack(pady=5)


#Attendance Frame
demo_label = tk.Label(attendance_frame, text="", fg="orange", font=("Arial", 12))
attendance_label = tk.Label(attendance_frame, text="Attendance Options", font=("Arial", 12))
attendance_create_btn = tk.Button(attendance_frame, text="Create Attendance", width=15, font=("Montserrat", 12), command=demo_msg)
attendance_view_btn = tk.Button(attendance_frame, text="View Attendances", width=15, font=("Montserrat", 12), command=demo_msg)
attendance_fillout_btn = tk.Button(attendance_frame, text="Fill out Attendance", width=15, font=("Montserrat", 12), command=demo_msg)
menu_btn = tk.Button(attendance_frame, text="Main menu", width=15, font=("Montserrat", 12), command=main_menu)

demo_label.pack(pady=5)
attendance_label.pack(pady=5)
attendance_create_btn.pack(pady=5)
attendance_view_btn.pack(pady=5)
attendance_fillout_btn.pack(pady=5)
menu_btn.pack(pady=5)

show_frame(login_frame) 
update_clock()
win.mainloop()

