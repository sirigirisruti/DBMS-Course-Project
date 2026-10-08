import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def connect_db():
    """Connect to the recruitmentdb MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="recruitmentdb"
    )


def clear_fields():
    """Clear all input fields."""
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    qualification_entry.delete(0, tk.END)
    dept_entry.delete(0, tk.END)


def view_applicants():
    """Read applicant records from MySQL and display them in the table."""
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT applicant_id, applicant_name, email, phone,
                   qualification, experience_years
            FROM applicant
        """)
        rows = cursor.fetchall()

        for item in table.get_children():
            table.delete(item)

        for row in rows:
            table.insert("", tk.END, values=row)

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def insert_applicant():
    """Insert a new applicant record into MySQL."""
    try:
        applicant_id = id_entry.get().strip()
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        phone = phone_entry.get().strip()
        qualification = qualification_entry.get().strip()
        department_id = dept_entry.get().strip()

        if not all([applicant_id, name, email, phone, qualification, department_id]):
            messagebox.showwarning(
                "Missing Data",
                "Please fill all fields."
            )
            return

        conn = connect_db()
        cursor = conn.cursor()

        query = """
            INSERT INTO applicant
            (applicant_id, applicant_name, email, phone,
             qualification, experience_years)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            int(applicant_id),
            name,
            email,
            phone,
            qualification,
            int(department_id)
        )

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Applicant inserted successfully!"
        )

        clear_fields()
        view_applicants()

    except ValueError:
        messagebox.showerror(
            "Invalid Data",
            "Applicant ID and Department ID must be numbers."
        )
    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def delete_applicant():
    """Delete an applicant using Applicant ID."""
    try:
        applicant_id = id_entry.get().strip()

        if not applicant_id:
            messagebox.showwarning(
                "Missing ID",
                "Enter Applicant ID to delete."
            )
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM applicant WHERE applicant_id = %s",
            (int(applicant_id),)
        )

        if cursor.rowcount == 0:
            conn.rollback()
            cursor.close()
            conn.close()
            messagebox.showwarning(
                "Not Found",
                "No applicant found with that ID."
            )
            return

        conn.commit()

        cursor.close()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Applicant deleted successfully!"
        )

        clear_fields()
        view_applicants()

    except ValueError:
        messagebox.showerror(
            "Invalid ID",
            "Applicant ID must be a number."
        )
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

root = tk.Tk()
root.title("Recruitment Database Management System")
root.geometry("900x650")

title_label = tk.Label(
    root,
    text="Recruitment Database Management System",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=20)

form_frame = tk.Frame(root)
form_frame.pack(pady=5)

tk.Label(form_frame, text="Applicant ID").grid(
    row=0, column=0, padx=10, pady=8, sticky="e"
)
id_entry = tk.Entry(form_frame, width=22)
id_entry.grid(row=0, column=1, padx=10, pady=8)

tk.Label(form_frame, text="Email").grid(
    row=1, column=0, padx=10, pady=8, sticky="e"
)
email_entry = tk.Entry(form_frame, width=22)
email_entry.grid(row=1, column=1, padx=10, pady=8)

tk.Label(form_frame, text="Qualification").grid(
    row=2, column=0, padx=10, pady=8, sticky="e"
)
qualification_entry = tk.Entry(form_frame, width=22)
qualification_entry.grid(row=2, column=1, padx=10, pady=8)

tk.Label(form_frame, text="Name").grid(
    row=0, column=2, padx=10, pady=8, sticky="e"
)
name_entry = tk.Entry(form_frame, width=22)
name_entry.grid(row=0, column=3, padx=10, pady=8)

tk.Label(form_frame, text="Phone").grid(
    row=1, column=2, padx=10, pady=8, sticky="e"
)
phone_entry = tk.Entry(form_frame, width=22)
phone_entry.grid(row=1, column=3, padx=10, pady=8)

tk.Label(form_frame, text="Department ID").grid(
    row=2, column=2, padx=10, pady=8, sticky="e"
)
dept_entry = tk.Entry(form_frame, width=22)
dept_entry.grid(row=2, column=3, padx=10, pady=8)

button_frame = tk.Frame(root)
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="INSERT",
    width=15,
    command=insert_applicant
).grid(row=0, column=0, padx=10)

tk.Button(
    button_frame,
    text="DELETE",
    width=15,
    command=delete_applicant
).grid(row=0, column=1, padx=10)

tk.Button(
    button_frame,
    text="VIEW",
    width=15,
    command=view_applicants
).grid(row=0, column=2, padx=10)

tk.Button(
    button_frame,
    text="CLEAR",
    width=15,
    command=clear_fields
).grid(row=0, column=3, padx=10)

columns = (
    "Applicant ID",
    "Name",
    "Email",
    "Phone",
    "Qualification",
    "Department ID"
)

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=12
)

for column in columns:
    table.heading(column, text=column)
    table.column(column, width=140)

table.pack(
    pady=10,
    padx=10,
    fill="both",
    expand=True
)

view_applicants()

root.mainloop()
