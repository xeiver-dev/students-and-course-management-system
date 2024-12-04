from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'


# Database initialization
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                course TEXT NOT NULL
            )
        ''')

        print("Database initialized")


@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Get total number of students
        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]

        # Get the most recently added student
        cursor.execute("SELECT name FROM students ORDER BY id DESC LIMIT 1")
        last_student = cursor.fetchone()
        last_student_name = last_student[0] if last_student else "No students yet"

    return render_template('index.html',
                           total_students=total_students,
                           last_student_name=last_student_name)


@app.route('/students')
def students():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
    return render_template('students.html', students=students)


@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        id = request.form['student_id']
        name = request.form['name']
        course = request.form['course']
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (id, name, course) VALUES (?, ?, ?)",
                (id, name, course))
        return redirect(url_for('students'))
    return render_template('add_student.html')


@app.route('/delete-student/<int:student_id>')
def delete_student(student_id: int):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    return redirect(url_for('students'))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
