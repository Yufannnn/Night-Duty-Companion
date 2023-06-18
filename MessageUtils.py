import re


def generate_message_when_no_absentees(leave_due_today):
    if len(leave_due_today) == 0:
        final_message = "Hi BMs, All boarders are in and there are no one with leaves today.\nThank you!"
        return final_message
    else:
        absent_message = "Hi BMs, All boarders are in, except those with leaves:"
        leave_message = ""
        leave_due_today = sorted(leave_due_today, key=lambda x: x['Bed'])
        leave_pattern = r"(\w+) Leave\[Out on \d{2}/\d{2}/\d{4} \w+ \d{2}:\d{2} Come back on \d{2}/\d{2}/\d{4} \w+ (" \
                        r"\d{2}:\d{2})"
        for row in leave_due_today:
            room_number = re.sub(r'^[^/]+/', '', row['Bed']).strip()
            leave = row['Leave']
            match = re.search(leave_pattern, leave)
            if match:
                leave_type = match.group(1)
                return_time = match.group(2)
                leave_message += f"- {room_number} {row['Boarder']} ({leave_type} Leave till {return_time})\n"

    final_message = f"{absent_message}\n{leave_message}"
    return final_message + "Thank you!"


def generate_message_when_one_absentee(absent_students, leave_due_today):
    absent_message = "Hi BMs, all boarders are in except:\n"
    absent_students = absent_students.sort_values('Bed')
    for _, row in absent_students.iterrows():
        room_number = re.sub(r'^[^/]+/', '', row['Bed']).strip()
        absent_message += f"- {room_number} {row['Boarder']}\n"
    absent_message += "Have asked him to scan at level 1, will update again later."
    leave_message = ""

    if len(leave_due_today) > 0:
        leave_message = "And those with leaves:\n"
        leave_due_today = sorted(leave_due_today, key=lambda x: x['Bed'])
        leave_pattern = r"(\w+) Leave\[Out on \d{2}/\d{2}/\d{4} \w+ \d{2}:\d{2} Come back on \d{2}/\d{2}/\d{4} \w+ (" \
                        r"\d{2}:\d{2})"
        for row in leave_due_today:
            room_number = re.sub(r'^[^/]+/', '', row['Bed']).strip()
            leave = row['Leave']
            match = re.search(leave_pattern, leave)
            if match:
                leave_type = match.group(1)
                return_time = match.group(2)
                leave_message += f"- {room_number} {row['Boarder']} ({leave_type} Leave till {return_time})\n"

    final_message = f"{absent_message}\n{leave_message}"
    return final_message + "Thank you!"


def generate_message_when_multiple_absentees(absent_students, leave_due_today):
    absent_message = "Hi BMs, all boarders are in except:\n"
    absent_students = absent_students.sort_values('Bed')
    for _, row in absent_students.iterrows():
        room_number = re.sub(r'^[^/]+/', '', row['Bed']).strip()
        absent_message += f"- {room_number} {row['Boarder']}\n"
    absent_message += "Have asked them to scan at level 1, will update again later."

    leave_message = ""
    if len(leave_due_today) > 0:
        leave_message = "And those with leaves:\n"
        leave_due_today = sorted(leave_due_today, key=lambda x: x['Bed'])
        leave_pattern = r"(\w+) Leave\[Out on \d{2}/\d{2}/\d{4} \w+ \d{2}:\d{2} Come back on \d{2}/\d{2}/\d{4} \w+ (" \
                        r"\d{2}:\d{2})"
        for row in leave_due_today:
            room_number = re.sub(r'^[^/]+/', '', row['Bed']).strip()
            leave = row['Leave']
            match = re.search(leave_pattern, leave)
            if match:
                leave_type = match.group(1)
                return_time = match.group(2)
                leave_message += f"- {room_number} {row['Boarder']} ({leave_type} Leave till {return_time})\n"

    final_message = f"{absent_message}\n{leave_message}"
    return final_message + "Thank you!"
