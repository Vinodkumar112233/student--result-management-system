import sqlite3
from tkinter import *

def connect_db():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            roll TEXT UNIQUE,
            marks INTEGER
        )
    """)
    conn.commit()
    conn.close()

connect_db()

def add_student():
    name = name_var.get()
    roll = roll_var.get()
    marks = marks_var.get()

    if name == "" or roll == "" or marks == "":
        print("All fields are required.")
        return

    try:
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO student (name, roll, marks) VALUES (?, ?, ?)",
                       (name, roll, marks))
        conn.commit()
        conn.close()
        print("Student added successfully!")

        name_var.set("")
        roll_var.set("")
        marks_var.set("")
    except sqlite3.IntegrityError:
        print("Error: Roll No must be unique.")

def view_students():
    view_win = Toplevel(root)
    view_win.title("Student Records")
    view_win.geometry("400x300")

    Label(view_win, text="Name", width=10, borderwidth=2, relief="ridge").grid(row=0, column=0)
    Label(view_win, text="Roll No", width=10, borderwidth=2, relief="ridge").grid(row=0, column=1)
    Label(view_win, text="Marks", width=10, borderwidth=2, relief="ridge").grid(row=0, column=2)

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, roll, marks FROM student")
    rows = cursor.fetchall()
    conn.close()

    for index, row in enumerate(rows):
        for col_index, item in enumerate(row):
            Label(view_win, text=item, width=10, borderwidth=2, relief="ridge").grid(row=index+1, column=col_index)

def update_student():
    roll = roll_var.get()
    new_marks = marks_var.get()

    if roll == "" or new_marks == "":
        print("Roll No and Marks are required for update.")
        return

    try:
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE student SET marks = ? WHERE roll = ?", (new_marks, roll))
        if cursor.rowcount == 0:
            print("No student found with that Roll No.")
        else:
            print("Student record updated successfully!")
        conn.commit()
        conn.close()

        roll_var.set("")
        marks_var.set("")
    except Exception as e:
        print("Error:", e)

def delete_student():
    roll = roll_var.get()

    if roll == "":
        print("Roll No is required for deletion.")
        return

    try:
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE roll = ?", (roll,))
        if cursor.rowcount == 0:
            print("No student found with that Roll No.")
        else:
            print("Student deleted successfully!")
        conn.commit()
        conn.close()

        # Clear Roll No field
        roll_var.set("")
    except Exception as e:
        print("Error:", e)
        

root = Tk()
root.title("Student Result Management System")
root.geometry("500x400")

# Labels
Label(root, text="Student Name").place(x=30, y=30)
Label(root, text="Roll No").place(x=30, y=70)
Label(root, text="Marks").place(x=30, y=110)

# Entry Widgets
name_var = StringVar()
roll_var = StringVar()
marks_var = StringVar()
Button(root, text="Save", command=add_student, bg="green", fg="white").place(x=150, y=150)
Button(root, text="View Records", command=view_students, bg="blue", fg="white").place(x=220, y=150)
Button(root, text="Update", command=update_student, bg="orange", fg="black").place(x=150, y=190)
Button(root, text="Delete", command=delete_student, bg="red", fg="white").place(x=220, y=190)


Entry(root, textvariable=name_var).place(x=150, y=30)
Entry(root, textvariable=roll_var).place(x=150, y=70)
Entry(root, textvariable=marks_var).place(x=150, y=110)

# Keep window running
root.mainloop()
