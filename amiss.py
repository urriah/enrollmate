import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
def setup_database():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER,
                        program TEXT,
                        scholarship TEXT
                    )''')
    conn.commit()
    conn.close()

# Add new student
def add_student():
    name = entry_name.get()
    age = entry_age.get()
    program = entry_program.get()
    scholarship = entry_scholarship.get()
    
    if name and age and program and scholarship:
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, program, scholarship) VALUES (?, ?, ?, ?)", 
                       (name, age, program, scholarship))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully!")
        clear_entries()
        fetch_students()
    else:
        messagebox.showwarning("Input Error", "All fields are required!")

# Fetch all students
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

# Search for a student
def search_student():
    search_query = entry_search.get()
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name LIKE ? OR id = ?", (f"%{search_query}%", search_query))
    rows = cursor.fetchall()
    conn.close()
    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert("", tk.END, values=row)

# Update selected student
def update_student():
    try:
        selected_item = tree.selection()[0]
        student_id = tree.item(selected_item, "values")[0]
        
        name = entry_name.get()
        age = entry_age.get()
        program = entry_program.get()
        scholarship = entry_scholarship.get()

        if name and age and program and scholarship:
            conn = sqlite3.connect("university.db")
            cursor = conn.cursor()
            cursor.execute("""UPDATE students 
                              SET name = ?, age = ?, program = ?, scholarship = ?
                              WHERE id = ?""", (name, age, program, scholarship, student_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student updated successfully!")
            clear_entries()
            fetch_students()
        else:
            messagebox.showwarning("Input Error", "All fields are required!")
    except IndexError:
        messagebox.showerror("Selection Error", "No student selected!")

# Delete selected student
def delete_student():
    try:
        selected_item = tree.selection()[0]
        student_id = tree.item(selected_item, "values")[0]
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student deleted successfully!")
        fetch_students()
    except IndexError:
        messagebox.showerror("Selection Error", "No student selected!")

# Clear input fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_program.delete(0, tk.END)
    entry_scholarship.delete(0, tk.END)

# GUI setup
app = tk.Tk()
app.title("Amiss")
app.geometry("800x600")

# Input fields
frame_inputs = tk.Frame(app)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Name:").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_inputs)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Age:").grid(row=1, column=0, padx=5, pady=5)
entry_age = tk.Entry(frame_inputs)
entry_age.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Program:").grid(row=2, column=0, padx=5, pady=5)
entry_program = tk.Entry(frame_inputs)
entry_program.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Scholarship (Yes/No):").grid(row=3, column=0, padx=5, pady=5)
entry_scholarship = tk.Entry(frame_inputs)
entry_scholarship.grid(row=3, column=1, padx=5, pady=5)

# Buttons
frame_buttons = tk.Frame(app)
frame_buttons.pack(pady=10)

btn_add = tk.Button(frame_buttons, text="Add Student", command=add_student)
btn_add.grid(row=0, column=0, padx=5, pady=5)

btn_update = tk.Button(frame_buttons, text="Update Student", command=update_student)
btn_update.grid(row=0, column=1, padx=5, pady=5)

btn_delete = tk.Button(frame_buttons, text="Delete Student", command=delete_student)
btn_delete.grid(row=0, column=2, padx=5, pady=5)

btn_clear = tk.Button(frame_buttons, text="Clear Fields", command=clear_entries)
btn_clear.grid(row=0, column=3, padx=5, pady=5)

# Search field
frame_search = tk.Frame(app)
frame_search.pack(pady=10)

tk.Label(frame_search, text="Search (by Name or ID):").pack(side=tk.LEFT, padx=5)
entry_search = tk.Entry(frame_search)
entry_search.pack(side=tk.LEFT, padx=5)
btn_search = tk.Button(frame_search, text="Search", command=search_student)
btn_search.pack(side=tk.LEFT, padx=5)

# Treeview for displaying students
frame_tree = tk.Frame(app)
frame_tree.pack(pady=10)

columns = ("ID", "Name", "Age", "Program", "Scholarship")
tree = ttk.Treeview(frame_tree, columns=columns, show="headings")
tree.pack()

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

# Fetch students on startup
setup_database()
fetch_students()

app.mainloop()