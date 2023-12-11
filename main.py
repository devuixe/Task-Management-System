import customtkinter
import sqlite3
import bcrypt
from tkinter import *
from tkinter import messagebox
from subprocess import call

login = customtkinter.CTk()
login.title('Task Manager - Login')
login.geometry('450x360') 
login.configure(bg= '0x00FF8800')

font1 = ('Helvetica', 25, 'bold')
font2 = ('Arial', 17, 'bold')
font3 = ('Arial', 13, 'bold')
font4 = ('Arial', 13, 'underline')

conn = sqlite3.connect('userlogin.db')
cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS users (
               username TEXT NOT NULL,
               password TEXT NOT NULL)''')

def open_taskman():
    call(["python", r"C:\Users\nicol\OneDrive\Documents\School\4th year\python\Final Project\Task-Management-System\task_manager.py"])


def signup():
    username = username_entry.get()
    password = password_entry.get()
    if username != '' and password != '':
        cursor.execute('SELECT username FROM users WHERE username=?', [username])
        if cursor.fetchone() is not None:
            messagebox.showerror('Error', 'Username already exists.')
        else:
            encoded_password = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            cursor.execute('INSERT INTO users VALUES (?, ?)', [username, hashed_password])
            conn.commit()
            messagebox.showinfo('Success', 'Account has been created.')
    else:
        messagebox.showerror('Error','Enter all data.')

def loginbutt():
    username = username_entry2.get()
    password = password_entry2.get()
    if username != '' and password != '':
        cursor.execute('SELECT password FROM users WHERE username=?', [username])
        result = cursor.fetchone()
        if result:
            if bcrypt.checkpw(password.encode('utf-8'), result[0]):
                #Success Login
                login.destroy()
                open_taskman()
            else:
                messagebox.showerror('Error', 'Invalid Password')
        else:
            messagebox.showerror('Error', 'Invalid username')
    else:
        messagebox.showerror('Error', 'Enter all data')

def loginn():
    frame1.destroy()
    frame2 = customtkinter.CTkFrame(login, bg_color='#001220', fg_color='#001220', width=470, height=360)
    frame2.place(x=0, y=0)

    image1 = PhotoImage(file=r"C:\Users\nicol\OneDrive\Documents\School\4th year\python\Final Project\Task-Management-System\assets\loginimg2.png")
    image1_label = Label(frame2, image = image1, bg = '#001220',width=215, height=360)
    image1_label.place(x = 0, y = 0)
    frame2.image1 = image1

    login_label = customtkinter.CTkLabel(frame2, font = font1, text = 'Log In', text_color='#fff', bg_color='#001220')
    login_label.place(x=280, y=20)

    global username_entry2
    global password_entry2

    username_entry2 = customtkinter.CTkEntry(frame2, font=font2, text_color='#fff', fg_color='#001a2e', bg_color='#121111', border_color='#004780', border_width = 3, placeholder_text='Username', placeholder_text_color='#a3a3a3', width=200, height=50)
    username_entry2.place(x = 230, y = 80)

    password_entry2 = customtkinter.CTkEntry(frame2, font=font2, show='*', text_color='#fff', fg_color='#001a2e', bg_color='#121111', border_color='#004780', border_width = 3, placeholder_text='Password', placeholder_text_color='#a3a3a3', width=200, height=50)
    password_entry2.place(x = 230, y = 150)

    login_button2 = customtkinter.CTkButton(frame2, command = loginbutt, font=font2, text_color='#fff', text='Log In', fg_color='#00965d', hover_color='#006e44', bg_color='#121111', cursor='hand2', corner_radius=5,width=120)
    login_button2.place(x = 230, y = 220)


frame1 = customtkinter.CTkFrame(login, bg_color='#001220', fg_color='#001220', width=470, height=360)
frame1.place(x = 0, y = 0)

#filepath = "assets/loginimg.png"

image1 = PhotoImage(file=r"C:\Users\nicol\OneDrive\Documents\School\4th year\python\Final Project\Task-Management-System\assets\loginimg2.png")
image1_label = Label(frame1, image = image1, bg = '#001220',width=215, height=360)
image1_label.place(x = 0, y = 0)

signup_label = customtkinter.CTkLabel(frame1, font = font1, text = 'Sign Up', text_color='#fff', bg_color='#001220')
signup_label.place(x = 280, y = 20)

username_entry = customtkinter.CTkEntry(frame1, font=font2, text_color='#fff', fg_color='#001a2e', bg_color='#121111', border_color='#004780', border_width = 3, placeholder_text='Username', placeholder_text_color='#a3a3a3', width=200, height=50)
username_entry.place(x=230, y=80)

password_entry = customtkinter.CTkEntry(frame1, font=font2, show='*', text_color='#fff', fg_color='#001a2e', bg_color='#121111', border_color='#004780', border_width = 3, placeholder_text='Password', placeholder_text_color='#a3a3a3', width=200, height=50)
password_entry.place(x=230, y=150)

signup_button = customtkinter.CTkButton(frame1, command=signup, font=font2, text_color='#fff', text='Sign Up', fg_color='#00965d', hover_color='#006e44', bg_color='#121111', cursor='hand2', corner_radius=5,width=120)
signup_button.place(x=230, y=220)

login_label = customtkinter.CTkButton(frame1, font=font3, text='Have an Account?', text_color='#fff', bg_color='#001220')
login_label.place(x=230, y=250)

login_button = customtkinter.CTkButton(frame1, command=loginn, font=font4, text_color='#00bf77',text='Login', fg_color='#001220', hover_color='#001220', width=40 )
login_button.place(x=375,y=250)

login.mainloop()
