import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection


# =====================================================
# LOGIN WINDOW
# =====================================================

login_window = tk.Tk()

login_window.title("Student Management System - Login")
login_window.geometry("450x400")
login_window.configure(bg="#f4f6f8")
login_window.resizable(False, False)


def login():

    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == "" or password == "":
        messagebox.showwarning(
            "Warning",
            "Please enter username and password."
        )
        return

    try:

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT * FROM users
        WHERE username = %s AND password = %s
        """

        cursor.execute(
            query,
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:

            login_window.destroy()
            open_dashboard()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =====================================================
# LOGIN UI
# =====================================================

tk.Label(
    login_window,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold"),
    bg="#f4f6f8"
).pack(pady=35)


tk.Label(
    login_window,
    text="Admin Login",
    font=("Arial", 16, "bold"),
    bg="#f4f6f8"
).pack(pady=5)


tk.Label(
    login_window,
    text="Username",
    font=("Arial", 11),
    bg="#f4f6f8"
).pack(pady=(20, 5))


username_entry = tk.Entry(
    login_window,
    width=30,
    font=("Arial", 12)
)

username_entry.pack()


tk.Label(
    login_window,
    text="Password",
    font=("Arial", 11),
    bg="#f4f6f8"
).pack(pady=(15, 5))


password_entry = tk.Entry(
    login_window,
    width=30,
    font=("Arial", 12),
    show="*"
)

password_entry.pack()


tk.Button(
    login_window,
    text="LOGIN",
    width=20,
    height=2,
    font=("Arial", 11, "bold"),
    bg="#2563eb",
    fg="white",
    command=login
).pack(pady=25)


# =====================================================
# DASHBOARD
# =====================================================

def open_dashboard():

    window = tk.Tk()

    window.title("Student Management System")
    window.geometry("1100x700")
    window.configure(bg="#f4f6f8")


    # =================================================
    # ADD STUDENT
    # =================================================

    def add_student():

        form = tk.Toplevel(window)
        form.title("Add Student")
        form.geometry("500x650")
        form.configure(bg="white")

        tk.Label(
            form,
            text="Add Student",
            font=("Arial", 20, "bold"),
            bg="white"
        ).pack(pady=15)

        fields = [
            "Name",
            "Roll Number",
            "Course",
            "Semester",
            "Email",
            "Phone",
            "Attendance (%)",
            "Marks (%)"
        ]

        entries = {}

        for field in fields:

            tk.Label(
                form,
                text=field,
                bg="white"
            ).pack()

            entry = tk.Entry(
                form,
                width=40
            )

            entry.pack(pady=5)

            entries[field] = entry


        def save_student():

            name = entries["Name"].get().strip()
            roll = entries["Roll Number"].get().strip()
            course = entries["Course"].get().strip()
            semester = entries["Semester"].get().strip()
            email = entries["Email"].get().strip()
            phone = entries["Phone"].get().strip()
            attendance = entries["Attendance (%)"].get().strip()
            marks = entries["Marks (%)"].get().strip()

            if name == "" or roll == "" or course == "":
                messagebox.showwarning(
                    "Warning",
                    "Name, Roll Number and Course are required."
                )
                return

            try:

                semester = int(semester)
                attendance = float(attendance)
                marks = float(marks)

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Semester, Attendance and Marks must be numbers."
                )

                return

            try:

                connection = get_connection()
                cursor = connection.cursor()

                query = """
                INSERT INTO students
                (name, roll_number, course, semester,
                 email, phone, attendance, marks)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """

                cursor.execute(
                    query,
                    (
                        name,
                        roll,
                        course,
                        semester,
                        email,
                        phone,
                        attendance,
                        marks
                    )
                )

                connection.commit()

                cursor.close()
                connection.close()

                messagebox.showinfo(
                    "Success",
                    "Student added successfully!"
                )

                form.destroy()

                refresh_dashboard()

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )


        tk.Button(
            form,
            text="Save Student",
            width=20,
            command=save_student
        ).pack(pady=20)


    # =================================================
    # VIEW STUDENTS
    # =================================================

    def view_students():

        view_window = tk.Toplevel(window)

        view_window.title("All Students")
        view_window.geometry("1100x550")

        tk.Label(
            view_window,
            text="ALL STUDENTS",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        frame = tk.Frame(view_window)

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "ID",
            "Name",
            "Roll",
            "Course",
            "Semester",
            "Email",
            "Phone",
            "Attendance",
            "Marks"
        )

        table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            table.heading(
                column,
                text=column
            )

            table.column(
                column,
                width=100
            )

        table.column("ID", width=50)
        table.column("Name", width=120)
        table.column("Email", width=170)
        table.column("Phone", width=120)

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=table.yview
        )

        table.configure(
            yscrollcommand=scrollbar.set
        )

        table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT * FROM students"
            )

            students = cursor.fetchall()

            cursor.close()
            connection.close()

            for student in students:

                table.insert(
                    "",
                    "end",
                    values=(
                        student[0],
                        student[1],
                        student[2],
                        student[3],
                        student[4],
                        student[5],
                        student[6],
                        f"{student[7]}%",
                        f"{student[8]}%"
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    # =================================================
    # SEARCH STUDENT
    # =================================================

    def search_student():

        search_window = tk.Toplevel(window)

        search_window.title("Search Student")
        search_window.geometry("550x500")

        tk.Label(
            search_window,
            text="Search Student",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        tk.Label(
            search_window,
            text="Enter Roll Number"
        ).pack()

        roll_entry = tk.Entry(
            search_window,
            width=30
        )

        roll_entry.pack(pady=10)

        result_label = tk.Label(
            search_window,
            text="",
            font=("Arial", 11),
            justify="left"
        )

        result_label.pack(pady=20)


        def search():

            roll = roll_entry.get().strip()

            if roll == "":
                messagebox.showwarning(
                    "Warning",
                    "Please enter Roll Number."
                )
                return

            try:

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    "SELECT * FROM students WHERE roll_number=%s",
                    (roll,)
                )

                student = cursor.fetchone()

                cursor.close()
                connection.close()

                if student:

                    result_label.config(
                        text=(
                            f"ID: {student[0]}\n"
                            f"Name: {student[1]}\n"
                            f"Roll Number: {student[2]}\n"
                            f"Course: {student[3]}\n"
                            f"Semester: {student[4]}\n"
                            f"Email: {student[5]}\n"
                            f"Phone: {student[6]}\n"
                            f"Attendance: {student[7]}%\n"
                            f"Marks: {student[8]}%"
                        )
                    )

                else:

                    result_label.config(
                        text="Student not found."
                    )

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )


        tk.Button(
            search_window,
            text="Search",
            width=18,
            command=search
        ).pack(pady=10)


    # =================================================
    # UPDATE STUDENT
    # =================================================

    def update_student():

        update_window = tk.Toplevel(window)

        update_window.title("Update Student")
        update_window.geometry("500x650")

        tk.Label(
            update_window,
            text="Update Student",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        fields = [
            "Roll Number",
            "Name",
            "Course",
            "Semester",
            "Email",
            "Phone",
            "Attendance (%)",
            "Marks (%)"
        ]

        entries = {}

        for field in fields:

            tk.Label(
                update_window,
                text=field
            ).pack()

            entry = tk.Entry(
                update_window,
                width=40
            )

            entry.pack(pady=4)

            entries[field] = entry


        def find_student():

            roll = entries["Roll Number"].get().strip()

            try:

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    "SELECT * FROM students WHERE roll_number=%s",
                    (roll,)
                )

                student = cursor.fetchone()

                cursor.close()
                connection.close()

                if student:

                    entries["Name"].delete(0, tk.END)
                    entries["Name"].insert(0, student[1])

                    entries["Course"].delete(0, tk.END)
                    entries["Course"].insert(0, student[3])

                    entries["Semester"].delete(0, tk.END)
                    entries["Semester"].insert(0, student[4])

                    entries["Email"].delete(0, tk.END)
                    entries["Email"].insert(0, student[5])

                    entries["Phone"].delete(0, tk.END)
                    entries["Phone"].insert(0, student[6])

                    entries["Attendance (%)"].delete(0, tk.END)
                    entries["Attendance (%)"].insert(0, student[7])

                    entries["Marks (%)"].delete(0, tk.END)
                    entries["Marks (%)"].insert(0, student[8])

                else:

                    messagebox.showwarning(
                        "Not Found",
                        "Student not found."
                    )

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )


        tk.Button(
            update_window,
            text="Find Student",
            width=18,
            command=find_student
        ).pack(pady=8)


        def update_data():

            roll = entries["Roll Number"].get().strip()
            name = entries["Name"].get().strip()
            course = entries["Course"].get().strip()
            semester = entries["Semester"].get().strip()
            email = entries["Email"].get().strip()
            phone = entries["Phone"].get().strip()
            attendance = entries["Attendance (%)"].get().strip()
            marks = entries["Marks (%)"].get().strip()

            try:

                semester = int(semester)
                attendance = float(attendance)
                marks = float(marks)

                connection = get_connection()
                cursor = connection.cursor()

                query = """
                UPDATE students
                SET name=%s,
                    course=%s,
                    semester=%s,
                    email=%s,
                    phone=%s,
                    attendance=%s,
                    marks=%s
                WHERE roll_number=%s
                """

                cursor.execute(
                    query,
                    (
                        name,
                        course,
                        semester,
                        email,
                        phone,
                        attendance,
                        marks,
                        roll
                    )
                )

                connection.commit()

                cursor.close()
                connection.close()

                messagebox.showinfo(
                    "Success",
                    "Student updated successfully!"
                )

                update_window.destroy()

                refresh_dashboard()

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Enter valid numeric values."
                )

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )


        tk.Button(
            update_window,
            text="Update Student",
            width=18,
            command=update_data
        ).pack(pady=10)


    # =================================================
    # DELETE STUDENT
    # =================================================

    def delete_student():

        delete_window = tk.Toplevel(window)

        delete_window.title("Delete Student")
        delete_window.geometry("500x350")

        tk.Label(
            delete_window,
            text="Delete Student",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        tk.Label(
            delete_window,
            text="Enter Roll Number"
        ).pack()

        roll_entry = tk.Entry(
            delete_window,
            width=30
        )

        roll_entry.pack(pady=10)


        def delete_data():

            roll = roll_entry.get().strip()

            if roll == "":
                messagebox.showwarning(
                    "Warning",
                    "Enter Roll Number."
                )
                return

            confirmation = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this student?"
            )

            if not confirmation:
                return

            try:

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    "DELETE FROM students WHERE roll_number=%s",
                    (roll,)
                )

                connection.commit()

                deleted = cursor.rowcount

                cursor.close()
                connection.close()

                if deleted > 0:

                    messagebox.showinfo(
                        "Success",
                        "Student deleted successfully!"
                    )

                    delete_window.destroy()

                    refresh_dashboard()

                else:

                    messagebox.showwarning(
                        "Not Found",
                        "Student not found."
                    )

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )


        tk.Button(
            delete_window,
            text="Delete Student",
            width=20,
            command=delete_data
        ).pack(pady=20)


    # =================================================
    # ATTENDANCE
    # =================================================

    def attendance_status():

        attendance_window = tk.Toplevel(window)

        attendance_window.title("Attendance")
        attendance_window.geometry("500x400")

        tk.Label(
            attendance_window,
            text="Attendance Check",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        tk.Label(
            attendance_window,
            text="Enter Roll Number"
        ).pack()

        roll_entry = tk.Entry(
            attendance_window,
            width=30
        )

        roll_entry.pack(pady=10)

        result_label = tk.Label(
            attendance_window,
            text="",
            font=("Arial", 12),
            justify="left"
        )

        result_label.pack(pady=20)


        def check_attendance():

            roll = roll_entry.get().strip()

            try:

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    """
                    SELECT name, roll_number, attendance
                    FROM students
                    WHERE roll_number=%s
                    """,
                    (roll,)
                )

                student = cursor.fetchone()

                cursor.close()
                connection.close()

                if student:

                    attendance = float(student[2])

                    if attendance >= 75:
                        status = "Eligible"
                    else:
                        status = "Low Attendance"

                    result_label.config(
                        text=(
                            f"Name: {student[0]}\n"
                            f"Roll Number: {student[1]}\n"
                            f"Attendance: {attendance}%\n"
                            f"Status: {status}"
                        )
                    )

                else:

                    result_label.config(
                        text="Student not found."
                    )

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )


        tk.Button(
            attendance_window,
            text="Check Attendance",
            width=20,
            command=check_attendance
        ).pack(pady=10)


    # =================================================
    # VIEW RESULT
    # =================================================

    def view_result():

        result_window = tk.Toplevel(window)

        result_window.title("View Result")
        result_window.geometry("500x450")

        tk.Label(
            result_window,
            text="Student Result",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        tk.Label(
            result_window,
            text="Enter Roll Number"
        ).pack()

        roll_entry = tk.Entry(
            result_window,
            width=30
        )

        roll_entry.pack(pady=10)

        result_label = tk.Label(
            result_window,
            text="",
            font=("Arial", 12),
            justify="left"
        )

        result_label.pack(pady=20)


        def show_result():

            roll = roll_entry.get().strip()

            try:

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    """
                    SELECT name, roll_number, course, semester, marks
                    FROM students
                    WHERE roll_number=%s
                    """,
                    (roll,)
                )

                student = cursor.fetchone()

                cursor.close()
                connection.close()

                if student:

                    marks = float(student[4])

                    if marks >= 90:
                        grade = "A+"
                    elif marks >= 80:
                        grade = "A"
                    elif marks >= 70:
                        grade = "B"
                    elif marks >= 60:
                        grade = "C"
                    elif marks >= 50:
                        grade = "D"
                    else:
                        grade = "F"

                    result_label.config(
                        text=(
                            f"Name: {student[0]}\n"
                            f"Roll Number: {student[1]}\n"
                            f"Course: {student[2]}\n"
                            f"Semester: {student[3]}\n"
                            f"Marks: {marks}%\n"
                            f"Grade: {grade}"
                        )
                    )

                else:

                    result_label.config(
                        text="Student not found."
                    )

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )


        tk.Button(
            result_window,
            text="View Result",
            width=20,
            command=show_result
        ).pack(pady=10)


    # =================================================
    # STATISTICS
    # =================================================

    def get_statistics():

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT COUNT(*) FROM students"
            )

            total = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM students WHERE attendance >= 75"
            )

            eligible = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM students WHERE attendance < 75"
            )

            low = cursor.fetchone()[0]

            cursor.execute(
                "SELECT AVG(marks) FROM students"
            )

            average = cursor.fetchone()[0]

            cursor.close()
            connection.close()

            if average is None:
                average = 0

            return (
                total,
                eligible,
                low,
                round(float(average), 2)
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return 0, 0, 0, 0


    # =================================================
    # REFRESH DASHBOARD
    # =================================================

    def refresh_dashboard():

        total, eligible, low, average = get_statistics()

        total_label.config(
            text=str(total)
        )

        eligible_label.config(
            text=str(eligible)
        )

        low_label.config(
            text=str(low)
        )

        average_label.config(
            text=f"{average}%"
        )


    # =================================================
    # LOGOUT
    # =================================================

    def logout():

        confirmation = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if confirmation:

            window.destroy()

            # Login window dobara create karne ke liye
            restart_login()


    # =================================================
    # RESTART LOGIN
    # =================================================

    def restart_login():

        new_login = tk.Tk()

        new_login.title(
            "Student Management System - Login"
        )

        new_login.geometry("450x400")

        new_login.configure(
            bg="#f4f6f8"
        )

        tk.Label(
            new_login,
            text="STUDENT MANAGEMENT SYSTEM",
            font=("Arial", 20, "bold"),
            bg="#f4f6f8"
        ).pack(pady=35)

        tk.Label(
            new_login,
            text="Admin Login",
            font=("Arial", 16, "bold"),
            bg="#f4f6f8"
        ).pack()

        tk.Label(
            new_login,
            text="Username",
            bg="#f4f6f8"
        ).pack(pady=(20, 5))

        user_entry = tk.Entry(
            new_login,
            width=30
        )

        user_entry.pack()

        tk.Label(
            new_login,
            text="Password",
            bg="#f4f6f8"
        ).pack(pady=(15, 5))

        pass_entry = tk.Entry(
            new_login,
            width=30,
            show="*"
        )

        pass_entry.pack()


        def new_login_function():

            username = user_entry.get().strip()
            password = pass_entry.get().strip()

            try:

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    """
                    SELECT * FROM users
                    WHERE username=%s AND password=%s
                    """,
                    (username, password)
                )

                user = cursor.fetchone()

                cursor.close()
                connection.close()

                if user:

                    new_login.destroy()

                    open_dashboard()

                else:

                    messagebox.showerror(
                        "Login Failed",
                        "Invalid username or password."
                    )

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )


        tk.Button(
            new_login,
            text="LOGIN",
            width=20,
            height=2,
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            command=new_login_function
        ).pack(pady=25)

        new_login.mainloop()


    # =================================================
    # DASHBOARD HEADER
    # =================================================

    header = tk.Frame(
        window,
        bg="#1e3a8a",
        height=100
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="STUDENT MANAGEMENT SYSTEM",
        font=("Arial", 26, "bold"),
        bg="#1e3a8a",
        fg="white"
    ).pack(
        side="left",
        padx=30,
        pady=30
    )

    tk.Button(
        header,
        text="Logout",
        width=12,
        command=logout
    ).pack(
        side="right",
        padx=30
    )


    # =================================================
    # STATISTICS CARDS
    # =================================================

    stats_frame = tk.Frame(
        window,
        bg="#f4f6f8"
    )

    stats_frame.pack(
        pady=25
    )


    def create_card(parent, title):

        card = tk.Frame(
            parent,
            bg="white",
            width=200,
            height=120,
            relief="solid",
            borderwidth=1
        )

        card.pack(
            side="left",
            padx=12
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack(pady=12)

        value = tk.Label(
            card,
            text="0",
            font=("Arial", 24, "bold"),
            bg="white"
        )

        value.pack()

        return value


    total_label = create_card(
        stats_frame,
        "Total Students"
    )

    eligible_label = create_card(
        stats_frame,
        "Attendance Eligible"
    )

    low_label = create_card(
        stats_frame,
        "Low Attendance"
    )

    average_label = create_card(
        stats_frame,
        "Average Marks"
    )


    # =================================================
    # BUTTONS
    # =================================================

    button_frame = tk.Frame(
        window,
        bg="#f4f6f8"
    )

    button_frame.pack(
        pady=15
    )

    buttons = [
        ("Add Student", add_student),
        ("View Students", view_students),
        ("Search Student", search_student),
        ("Update Student", update_student),
        ("Delete Student", delete_student),
        ("Attendance", attendance_status),
        ("View Result", view_result)
    ]


    for text, command in buttons:

        tk.Button(
            button_frame,
            text=text,
            width=18,
            height=2,
            font=("Arial", 10, "bold"),
            command=command
        ).pack(
            side="left",
            padx=5
        )


    # =================================================
    # REFRESH
    # =================================================

    tk.Button(
        window,
        text="Refresh Dashboard",
        width=22,
        height=2,
        font=("Arial", 11, "bold"),
        command=refresh_dashboard
    ).pack(
        pady=25
    )


    # =================================================
    # INITIAL DATA
    # =================================================

    refresh_dashboard()

    window.mainloop()


# =====================================================
# START LOGIN
# =====================================================

login_window.mainloop()