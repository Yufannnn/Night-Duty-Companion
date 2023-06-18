import pandas as pd
import re
from datetime import datetime, timedelta

from PyQt5.QtWidgets import QMessageBox


def send_not_current_date_message():
    message_box = QMessageBox()
    message_box.setWindowTitle("Error")
    message_box.setText("Please select a file that is dated today.")
    message_box.setIcon(QMessageBox.Critical)
    message_box.exec_()
    raise Exception("Not today's file, Please check the file you selected.")


def handle_drag_enter(event):
    if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path.lower().endswith('.csv'):
            event.acceptProposedAction()


def check_if_file_is_attendance_file(df):
    required_columns = ['ContactNo', 'Boarder', 'Bed', 'Date', 'Terminal Number', 'Scanned Time', 'Leave']

    # Check if all required columns are present
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"

    # Check data types and format of specific columns
    if not df['ContactNo'].astype(str).str.match(r'^\d{8}$').all():
        return False

    if not df['Boarder'].apply(lambda x: isinstance(x, str)).all():
        return False

    # All checks passed, it is an attendance file
    return True


def get_absent_students(df):
    absent_students = []
    leave_pattern = r"Come back on (\d{2}/\d{2}/\d{4}).*?(\d{2}:\d{2})"

    for _, row in df.iterrows():
        scanned_time = row['Scanned Time']
        leave = row['Leave']

        if pd.isnull(scanned_time):
            if pd.isnull(leave):
                absent_students.append(row)
            else:
                match = re.search(leave_pattern, leave)
                if match:
                    try:
                        return_datetime = datetime.strptime(match.group(1) + " " + match.group(2), "%d/%m/%Y %H:%M")
                        current_datetime = datetime.now()

                        if return_datetime < current_datetime:
                            absent_students.append(row)
                    except ValueError:
                        pass

    # return a df of absent students
    return pd.DataFrame(absent_students)


def format_absent_students(absent_students):
    # return - { Name, Room, Number}
    # return as a string
    if len(absent_students) == 0:
        return "No absentees."

    data = absent_students[['Boarder', 'Bed', 'ContactNo']]
    absent_text = ""
    for _, row in data.iterrows():
        # use regex to get the room number everything after the first /
        room_number = re.sub(r'^[^/]+/', '', row['Bed']).strip()
        absent_text += str(row['ContactNo']) + " - " + room_number + " - " + row['Boarder'] + "\n"

    return absent_text


def get_leave_due_tonight(df, current_date):
    leave_pattern = r"Come back on (\d{2}/\d{2}/\d{4}).*?(\d{2}:\d{2})"
    leave_due_today = []

    for _, row in df.iterrows():
        leave = row['Leave']
        if not pd.isnull(leave):
            match = re.search(leave_pattern, leave)
            if match:
                if match.group(1) == current_date:
                    return_datetime = datetime.strptime(match.group(1) + " " + match.group(2), "%d/%m/%Y %H:%M")
                    current_datetime = datetime.now()
                    if return_datetime < current_datetime:
                        continue
                    leave_due_today.append(row)
                # if the date is tomorrow, check if the time is before 2:00 am
                if match.group(1) == (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y"):
                    return_datetime = datetime.strptime(match.group(1) + " " + match.group(2), "%d/%m/%Y %H:%M")
                    # if it is earlier than 2:00 am midnight, add it to the list
                    if return_datetime < (datetime.now() + timedelta(days=1)).replace(hour=2, minute=0, second=0,
                                                                                      microsecond=0):
                        leave_due_today.append(row)

    # return a df of leave due tonight
    return leave_due_today


def format_leave_due(leave_due_today):
    leave_text = ""
    if len(leave_due_today) == 0:
        return "No leaves due today."

    leave_due_today = sorted(leave_due_today, key=lambda x: x['Bed'])
    leave_list = []
    for row in leave_due_today:
        room_number = re.sub(r'^[^/]+/', '', row['Bed']).strip()
        boarder_name = row['Boarder']
        match = re.search(r"(\d{2}:\d{2})$", row['Leave'])
        leave_due = match.group(1)
        number = row['ContactNo']
        leave_list.append((room_number, number, boarder_name, leave_due))

    sorted_leave_list = sorted(leave_list, key=lambda x: x[3])

    for room_number, number, boarder_name, leave_due in sorted_leave_list:
        leave_text += str(leave_due) + " - " + str(number) + " - " + room_number + " - " + boarder_name + "\n"

    return leave_text