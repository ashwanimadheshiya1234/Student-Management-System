from database import get_connection


def add_student():
    print("\n===== Add Student =====")

    name = input("Enter Student Name: ")
    roll = input("Enter Roll Number: ")
    course = input("Enter Course: ")
    semester = int(input("Enter Semester: "))
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")
    attendance = float(input("Enter Attendance (%): "))
    marks = float(input("Enter Marks (%): "))

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO students
    (name, roll_number, course, semester, email, phone, attendance, marks)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        name,
        roll,
        course,
        semester,
        email,
        phone,
        attendance,
        marks
    )

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

    print("\nStudent added successfully!")


def view_students():
    print("\n===== All Students =====")

    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM students"
    cursor.execute(query)

    students = cursor.fetchall()

    if len(students) == 0:
        print("No student records found.")
    else:
        for student in students:
            print("----------------------------")
            print("ID:", student[0])
            print("Name:", student[1])
            print("Roll Number:", student[2])
            print("Course:", student[3])
            print("Semester:", student[4])
            print("Email:", student[5])
            print("Phone:", student[6])
            print("Attendance:", student[7], "%")
            print("Marks:", student[8], "%")

        print("----------------------------")

    cursor.close()
    connection.close()


def search_student():
    print("\n===== Search Student =====")

    roll = input("Enter Roll Number: ")

    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM students WHERE roll_number = %s"
    cursor.execute(query, (roll,))

    student = cursor.fetchone()

    if student:
        print("\nStudent Found!")
        print("----------------------------")
        print("ID:", student[0])
        print("Name:", student[1])
        print("Roll Number:", student[2])
        print("Course:", student[3])
        print("Semester:", student[4])
        print("Email:", student[5])
        print("Phone:", student[6])
        print("Attendance:", student[7], "%")
        print("Marks:", student[8], "%")
        print("----------------------------")
    else:
        print("Student not found.")

    cursor.close()
    connection.close()


def update_student():
    print("\n===== Update Student =====")

    roll = input("Enter Roll Number: ")

    connection = get_connection()
    cursor = connection.cursor()

    check_query = "SELECT * FROM students WHERE roll_number = %s"
    cursor.execute(check_query, (roll,))

    student = cursor.fetchone()

    if student:
        print("\nStudent found.")

        name = input("Enter New Name: ")
        course = input("Enter New Course: ")
        semester = int(input("Enter New Semester: "))
        email = input("Enter New Email: ")
        phone = input("Enter New Phone: ")
        attendance = float(input("Enter New Attendance (%): "))
        marks = float(input("Enter New Marks (%): "))

        query = """
        UPDATE students
        SET name = %s,
            course = %s,
            semester = %s,
            email = %s,
            phone = %s,
            attendance = %s,
            marks = %s
        WHERE roll_number = %s
        """

        values = (
            name,
            course,
            semester,
            email,
            phone,
            attendance,
            marks,
            roll
        )

        cursor.execute(query, values)
        connection.commit()

        print("\nStudent updated successfully!")

    else:
        print("Student not found.")

    cursor.close()
    connection.close()


def delete_student():
    print("\n===== Delete Student =====")

    roll = input("Enter Roll Number: ")

    connection = get_connection()
    cursor = connection.cursor()

    query = "DELETE FROM students WHERE roll_number = %s"

    cursor.execute(query, (roll,))
    connection.commit()

    if cursor.rowcount > 0:
        print("Student deleted successfully!")
    else:
        print("Student not found.")

    cursor.close()
    connection.close()


def attendance_status():
    print("\n===== Attendance Status =====")

    roll = input("Enter Roll Number: ")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT name, attendance
    FROM students
    WHERE roll_number = %s
    """

    cursor.execute(query, (roll,))
    student = cursor.fetchone()

    if student:
        name = student[0]
        attendance = float(student[1])

        print("\nStudent Name:", name)
        print("Attendance:", attendance, "%")

        if attendance >= 75:
            print("Status: Eligible")
        else:
            print("Status: Low Attendance")
    else:
        print("Student not found.")

    cursor.close()
    connection.close()


def show_result():
    print("\n===== Student Result =====")

    roll = input("Enter Roll Number: ")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT name, marks
    FROM students
    WHERE roll_number = %s
    """

    cursor.execute(query, (roll,))
    student = cursor.fetchone()

    if student:
        name = student[0]
        marks = float(student[1])

        print("\nStudent Name:", name)
        print("Roll Number:", roll)
        print("Marks:", marks, "%")

        if marks >= 90:
            print("Grade: A+")
        elif marks >= 80:
            print("Grade: A")
        elif marks >= 70:
            print("Grade: B")
        elif marks >= 60:
            print("Grade: C")
        elif marks >= 50:
            print("Grade: D")
        else:
            print("Grade: F")
    else:
        print("Student not found.")

    cursor.close()
    connection.close()


while True:

    print("\n======================================")
    print("       STUDENT MANAGEMENT SYSTEM")
    print("======================================")

    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Check Attendance")
    print("7. View Result")
    print("8. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        update_student()

    elif choice == "5":
        delete_student()

    elif choice == "6":
        attendance_status()

    elif choice == "7":
        show_result()

    elif choice == "8":
        print("\nThank you for using Student Management System!")
        break

    else:
        print("\nInvalid choice. Please try again.")
