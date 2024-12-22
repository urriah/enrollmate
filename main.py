import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Database setup
def setup_database():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        birthdate TEXT,
                        program TEXT,
                        scholarship TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Scholarships (
    scholarshipID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    criteria TEXT NOT NULL,
    status TEXT CHECK(status IN ('active', 'inactive')) NOT NULL
)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Applicants (
    applicantID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    number TEXT(15),
    birthdate DATE,
    address TEXT,
    status TEXT CHECK(status IN ('active', 'inactive')) NOT NULL
)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Applicants_Scholarships (
    applicants_scholarshipID INTEGER PRIMARY KEY AUTOINCREMENT,
    applicantID INTEGER NOT NULL,
    studentID INTEGER NOT NULL,
    scholarshipID INTEGER NOT NULL,
    status TEXT CHECK(status IN ('approved', 'pending', 'rejected')) NOT NULL,
    FOREIGN KEY (applicantID) REFERENCES Applicants(applicantID),
    FOREIGN KEY (studentID) REFERENCES Students(StudentID),
    FOREIGN KEY (scholarshipID) REFERENCES Scholarships(scholarshipID)
)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Applications (
    ApplicationID INTEGER PRIMARY KEY AUTOINCREMENT,
    applicantID INTEGER NOT NULL,
    programID INTEGER NOT NULL,
    date DATE NOT NULL,
    status TEXT CHECK(status IN ('submitted', 'under review', 'approved', 'rejected')) NOT NULL,
    FOREIGN KEY (applicantID) REFERENCES Applicants(applicantID),
    FOREIGN KEY (programID) REFERENCES Programs(ProgramID)
)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Admins (
    adminID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT CHECK(role IN ('admin', 'staff', 'supervisor')) NOT NULL
)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Documents (
    DocumentsID INTEGER PRIMARY KEY AUTOINCREMENT,
    applicantID INTEGER NOT NULL,
    type TEXT NOT NULL,
    date DATE NOT NULL,
    path TEXT NOT NULL,
    FOREIGN KEY (applicantID) REFERENCES Applicants(applicantID)
)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Programs (
    ProgramID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    departmentID INTEGER NOT NULL,
    unit INTEGER NOT NULL,
    requirements TEXT,
    FOREIGN KEY (departmentID) REFERENCES Departments(departmentID)
)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Departments (
    departmentID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    faculty TEXT NOT NULL
)''')

    conn.commit()
    conn.close()

# Add new student (for the application form)
def submit_application():
    name = entry_name.get()
    birthdate = entry_birthdate.get()
    program = entry_program.get()
    scholarship = entry_scholarship.get()

    if name and birthdate and program and scholarship:
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, birthdate, program, scholarship) VALUES (?, ?, ?, ?)", 
                       (name, birthdate, program, scholarship))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Application submitted successfully!")
        clear_application_form()
    else:
        messagebox.showwarning("Input Error", "All fields are required!")

# Clear application form fields
def clear_application_form():
    entry_name.delete(0, tk.END)
    entry_birthdate.delete(0, tk.END)
    entry_program.delete(0, tk.END)
    entry_scholarship.delete(0, tk.END)

# Admin dashboard: Fetch and display students
def fetch_students():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert("", tk.END, values=row)

# Update student information
def update_student():
    try:
        selected_item = tree.selection()[0]
        student_id = tree.item(selected_item, "values")[0]

        name = entry_name.get()
        birthdate = entry_birthdate.get()
        program = entry_program.get()
        scholarship = entry_scholarship.get()

        if name and birthdate and program and scholarship:
            conn = sqlite3.connect("university.db")
            cursor = conn.cursor()
            cursor.execute("""UPDATE students 
                              SET name = ?, birthdate = ?, program = ?, scholarship = ?
                              WHERE id = ?""", (name, birthdate, program, scholarship, student_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student updated successfully!")
            fetch_students()
        else:
            messagebox.showwarning("Input Error", "All fields are required!")
    except IndexError:
        messagebox.showerror("Selection Error", "No student selected!")

# Accept application (placeholder functionality for now)
def accept_application():
    try:
        selected_item = tree.selection()[0]
        student_id = tree.item(selected_item, "values")[0]
        messagebox.showinfo("Accepted", f"Application ID {student_id} has been accepted!")
    except IndexError:
        messagebox.showerror("Selection Error", "No student selected!")

# Reject application (delete from database)
def reject_application():
    try:
        selected_item = tree.selection()[0]
        student_id = tree.item(selected_item, "values")[0]

        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Rejected", f"Application ID {student_id} has been rejected and deleted.")
        fetch_students()
    except IndexError:
        messagebox.showerror("Selection Error", "No student selected!")

# Show admin dashboard
def show_dashboard():
    for widget in app.winfo_children():
        widget.destroy()

    tk.Label(app, text="Admin Dashboard", font=("Arial", 16)).pack(pady=10)

    frame_inputs = tk.Frame(app)
    frame_inputs.pack(pady=10)

    tk.Label(frame_inputs, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    global entry_name
    entry_name = tk.Entry(frame_inputs)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_inputs, text="Birthdate (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
    global entry_birthdate
    entry_birthdate = tk.Entry(frame_inputs)
    entry_birthdate.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_inputs, text="Program:").grid(row=2, column=0, padx=5, pady=5)
    global entry_program
    entry_program = tk.Entry(frame_inputs)
    entry_program.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_inputs, text="Scholarship (Yes/No):").grid(row=3, column=0, padx=5, pady=5)
    global entry_scholarship
    entry_scholarship = tk.Entry(frame_inputs)
    entry_scholarship.grid(row=3, column=1, padx=5, pady=5)

    frame_buttons = tk.Frame(app)
    frame_buttons.pack(pady=10)

    tk.Button(frame_buttons, text="Update", command=update_student).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(frame_buttons, text="Accept", command=accept_application).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(frame_buttons, text="Reject", command=reject_application).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(frame_buttons, text="Back", command=show_main_menu).grid(row=0, column=3, padx=5, pady=5)

    frame_tree = tk.Frame(app)
    frame_tree.pack(pady=10)

    global tree
    columns = ("ID", "Name", "Birthdate", "Program", "Scholarship")
    tree = ttk.Treeview(frame_tree, columns=columns, show="headings")
    tree.pack()

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    fetch_students()

# Main menu
def show_main_menu():
    for widget in app.winfo_children():
        widget.destroy()

    tk.Label(app, text="Welcome to EnrollMate!", font=("Arial", 16)).pack(pady=20)
    tk.Button(app, text="Student Application Form", command=show_application_form).pack(pady=10)
    tk.Button(app, text="Admin Login", command=show_login).pack(pady=10)

# Show application form
def show_application_form():
    for widget in app.winfo_children():
        widget.destroy()

    tk.Label(app, text="Student Application Form", font=("Arial", 16)).pack(pady=10)

    frame_application = tk.Frame(app)
    frame_application.pack(pady=10)

    tk.Label(frame_application, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    global entry_name
    entry_name = tk.Entry(frame_application)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_application, text="Birthdate (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
    global entry_birthdate
    entry_birthdate = tk.Entry(frame_application)
    entry_birthdate.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_application, text="Program:").grid(row=2, column=0, padx=5, pady=5)
    global entry_program
    entry_program = tk.Entry(frame_application)
    entry_program.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_application, text="Scholarship (Yes/No):").grid(row=3, column=0, padx=5, pady=5)
    global entry_scholarship
    entry_scholarship = tk.Entry(frame_application)
    entry_scholarship.grid(row=3, column=1, padx=5, pady=5)

    tk.Button(app, text="Submit Application", command=submit_application).pack(pady=10)
    tk.Button(app, text="Back to Main Menu", command=show_main_menu).pack(pady=10)

# Admin login
def show_login():
    for widget in app.winfo_children():
        widget.destroy()

    tk.Label(app, text="Admin Login", font=("Arial", 16)).pack(pady=20)
    tk.Label(app, text="Username:").pack()
    entry_username = tk.Entry(app)
    entry_username.pack(pady=5)
    tk.Label(app, text="Password:").pack()
    entry_password = tk.Entry(app, show="*")
    entry_password.pack(pady=5)

    def login():
        if entry_username.get() == "admin" and entry_password.get() == "admin":
            show_dashboard()
        else:
            messagebox.showerror("Login Error", "Invalid username or password!")

    tk.Button(app, text="Login", command=login).pack(pady=20)

# Main application
app = tk.Tk()
app.title("University Admission and Scholarship System")
app.geometry("600x400")

setup_database()
show_main_menu()

app.mainloop()