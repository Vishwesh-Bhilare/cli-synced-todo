from datetime import datetime, timedelta
import re
from pathlib import Path

TODO_FILE = Path("todo.md")
DONE_FILE = Path("done.md")

DATE_FMT = "%d-%m-%Y"
TODAY = datetime.today().strftime(DATE_FMT)
WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

def next_due_date(due, rule):
    if rule == "daily":
        return due + timedelta(days=1)
    if rule == "weekly":
        return due + timedelta(weeks=1)
    if rule == "monthly":
        month = due.month + 1
        year = due.year
        if month > 12:
            month = 1
            year += 1
        return due.replace(year=year, month=month)
    if rule == "yearly":
        return due.replace(year=due.year + 1)
    if "," in rule:
        today_idx = due.weekday()
        days = [WEEKDAYS.index(d) for d in rule.split(",")]
        for i in range(1, 8):
            if (today_idx + i) % 7 in days:
                return due + timedelta(days=i)
    return None

todo_lines = TODO_FILE.read_text().splitlines()
done_lines = DONE_FILE.read_text().splitlines() if DONE_FILE.exists() else []

new_todo = []
completed_today = []

for line in todo_lines:
    if line.startswith("- [x]"):
        completed_today.append(line)

        if "repeat:" in line:
            due_match = re.search(r"due:(\d{2}-\d{2}-\d{4})", line)
            repeat_match = re.search(r"repeat:([a-z,]+)", line)

            if due_match and repeat_match:
                due = datetime.strptime(due_match.group(1), DATE_FMT)
                rule = repeat_match.group(1)
                next_due = next_due_date(due, rule)

                if next_due:
                    new_task = re.sub(
                        r"due:\d{2}-\d{2}-\d{4}",
                        f"due:{next_due.strftime(DATE_FMT)}",
                        line.replace("- [x]", "- [ ]")
                    )
                    new_todo.append(new_task)
    else:
        new_todo.append(line)

# Write updated todo.md
TODO_FILE.write_text("\n".join(new_todo) + "\n")

# Append to done.md under today's date
if completed_today:
    if f"# {TODAY}" not in done_lines:
        done_lines.append(f"# {TODAY}")
    done_lines.extend(completed_today)

DONE_FILE.write_text("\n".join(done_lines) + "\n")
