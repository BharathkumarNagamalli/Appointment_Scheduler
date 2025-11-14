# scheduler.py
from datetime import datetime

def parse_time(t):
    return datetime.strptime(t, "%H:%M").time()

def parse_date(d):
    return datetime.strptime(d, "%Y-%m-%d").date()

def overlap(s1, e1, s2, e2):
    return (s1 < e2) and (e1 > s2)

def can_schedule(db, pid, date, start, end):
    # Validate formats
    try:
        d = parse_date(date)
        s = parse_time(start)
        e = parse_time(end)
    except:
        return False, "Invalid date or time format."

    if e <= s:
        return False, "End time must be after start time."

    existing = db.appts_on_date(date)
    for a in existing:
        s2 = parse_time(a["start_time"])
        e2 = parse_time(a["end_time"])
        if overlap(s, e, s2, e2):
            return False, f"Overlaps with appointment {a['id']} for {a['name']}."

    return True, ""
