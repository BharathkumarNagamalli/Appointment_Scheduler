# cli_demo.py
from db import Database
from scheduler import can_schedule

def main():
    db = Database()
    print("Appointment Scheduler (CLI Version)\n")

    while True:
        print("1. List Patients")
        print("2. Add Patient")
        print("3. List Appointments")
        print("4. Book Appointment")
        print("5. Delete Appointment")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            for p in db.list_patients():
                print(p["id"], p["name"])

        elif choice == "2":
            name = input("Patient name: ").strip()
            if name:
                pid = db.add_patient(name)
                print("Added patient with ID:", pid)
            else:
                print("Name cannot be empty.")

        elif choice == "3":
            for a in db.list_appts():
                print(a["id"], a["name"], a["date"], a["start_time"], "-", a["end_time"])

        elif choice == "4":
            pid = input("Patient ID: ").strip()
            date = input("Date (YYYY-MM-DD): ").strip()
            start = input("Start (HH:MM): ").strip()
            end = input("End (HH:MM): ").strip()

            ok, msg = can_schedule(db, int(pid), date, start, end)
            if ok:
                appt_id = db.add_appt(int(pid), date, start, end)
                print("Appointment booked with ID:", appt_id)
            else:
                print("Failed:", msg)

        elif choice == "5":
            appt_id = input("Appointment ID to delete: ")
            db.delete_appt(int(appt_id))
            print("Deleted")

        elif choice == "0":
            db.close()
            print("Goodbye!")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
