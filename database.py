import mysql.connector


def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ashwani@1234",
        database="student_management"
    )

    return connection   