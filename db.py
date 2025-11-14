# db.py
import sqlite3

class Database:
    def __init__(self, path="clinic.db"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self._setup()

    def _setup(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
        """)
        self.conn.commit()

    # Patient operations
    def add_patient(self, name):
        self.cur.execute("INSERT INTO patients (name) VALUES (?)", (name,))
        self.conn.commit()
        return self.cur.lastrowid

    def list_patients(self):
        self.cur.execute("SELECT * FROM patients ORDER BY name")
        return [dict(row) for row in self.cur.fetchall()]

    # Appointment operations
    def add_appt(self, pid, date, start, end):
        self.cur.execute(
            "INSERT INTO appointments (patient_id, date, start_time, end_time) VALUES (?, ?, ?, ?)",
            (pid, date, start, end)
        )
        self.conn.commit()
        return self.cur.lastrowid

    def list_appts(self):
        self.cur.execute("""
            SELECT a.id, p.name, a.date, a.start_time, a.end_time
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            ORDER BY a.date, a.start_time
        """)
        return [dict(row) for row in self.cur.fetchall()]

    def appts_on_date(self, date):
        self.cur.execute("""
            SELECT a.id, p.name, a.date, a.start_time, a.end_time
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            WHERE a.date = ?
        """, (date,))
        return [dict(row) for row in self.cur.fetchall()]

    def delete_appt(self, appt_id):
        self.cur.execute("DELETE FROM appointments WHERE id = ?", (appt_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
