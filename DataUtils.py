import re
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox

from Bed import Bed
from Boarder import Boarder
from BoarderList import BoarderList
from Leave import Leave


def send_not_current_date_message():
    """
    Send a message box to inform the user that the file selected is not dated today.

    :return: None
    """
    message_box = QMessageBox()
    message_box.setWindowTitle("Error")
    message_box.setText("Please select a file that is dated today.")
    message_box.setIcon(QMessageBox.Critical)
    message_box.exec_()
    raise Exception("Not today's file, Please check the file you selected.")


def handle_drag_enter(event):
    """
    Handle the drag enter event.

    :param event: the drag enter event
    :return: None
    """
    if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path.lower().endswith('.csv'):
            event.acceptProposedAction()


def build_name(name_string):
    return name_string.strip()


def build_contact_no(contact_no_string):
    return str(contact_no_string).strip()


def build_terminal_number(terminal_number_string):
    """
    Build the terminal number from the string.

    :param terminal_number_string: the string of the terminal number
    :return: the terminal number
    """
    if str(terminal_number_string) == 'nan':
        return ''
    return str(terminal_number_string).strip()


def build_scanned_time(scanned_time_string):
    """
    Build the scanned time from the string.

    :param scanned_time_string: the string of the scanned time
    :return: the scanned time
    """
    if str(scanned_time_string) == 'nan':
        return None
    return datetime.strptime(str(scanned_time_string).strip(), "%H:%M")


def build_bed(bed_string):
    """
    Build the bed from the string.

    :param bed_string: the string of the bed
    :return: the bed
    """
    pattern = r'([^/]+)/(\d+\.\d+)/([A-Z]+)'
    match = re.match(pattern, bed_string)
    if match:
        room_number = match.group(2)
        bed_number = match.group(3)

        bed = Bed(room_number, bed_number)
        return bed


def build_leave(leave_string):
    """
    Build the leave from the string.

    :param leave_string: the string of the leave
    :return: the leave
    """
    if str(leave_string) == 'nan':
        return None
    leave_type = None
    come_back_time = None

    type_pattern = r'(\w+) Leave'
    match = re.search(type_pattern, leave_string)
    if match:
        leave_type = match.group(1)

    back_pattern = r'Come back on (\d{2}/\d{2}/\d{4} \w{3} \d{2}:\d{2})'
    match = re.search(back_pattern, leave_string)
    if match:
        come_back_time_str = match.group(1)
        come_back_time = datetime.strptime(come_back_time_str, "%d/%m/%Y %a %H:%M")

    return Leave(leave_type, come_back_time)


def build_boarder(row):
    """
    Build the boarder from the row.

    :param row: the row of the csv file
    :return: the boarder
    """
    name = build_name(row['Boarder'])
    contact_no = build_contact_no(row['ContactNo'])
    terminal_number = build_terminal_number(row['Terminal Number'])
    scanned_time = build_scanned_time(row['Scanned Time'])
    bed = build_bed(row['Bed'])
    leave = build_leave(row['Leave'])

    return name, bed, contact_no, terminal_number, scanned_time, leave


def build_boarder_list(df):
    """
    Build the boarder list from the dataframe.

    :param df: the dataframe
    :return: the boarder list
    """
    boarder_list = BoarderList()
    for _, row in df.iterrows():
        name, bed, contact_no, terminal_number, scanned_time, leave = build_boarder(row)
        boarder_list.add_boarder(Boarder(name, bed, contact_no, terminal_number, scanned_time, leave))

    return boarder_list


def format_leave_due(leave_due_today):
    """
    Format the leave due today.

    :param leave_due_today: the list of leave due today
    :return: the formatted leave due today
    """
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
