import re


def check_if_file_is_attendance_file(df):
    required_columns = ['ContactNo', 'Boarder', 'Bed', 'Date', 'Terminal Number', 'Scanned Time', 'Leave']

    # Check if all required columns are present
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"

    for _, row in df.iterrows():
        if not check_bed(row['Bed']):
            return False, f"Invalid Bed: {row['Bed']}"

        if not check_number(str(row['ContactNo'])):
            return False, f"Invalid ContactNo: {row['ContactNo']}"

        if not check_leave(str(row['Leave'])):
            return False, f"Invalid Leave: {row['Leave']}"

    return True, "File is a valid attendance file"


def check_bed(address):
    pattern = r'.+\/\d+\.\d+\/[A-Z]'
    match = re.match(pattern, address)

    if match:
        return True
    else:
        return False


def check_number(number):
    pattern = r'^\d+$'
    match = re.match(pattern, number)

    if match:
        return True
    else:
        return False


def check_leave(leave):
    if leave == "nan":
        return True

    pattern = r'^\w+\sLeave\[Out on \d{2}/\d{2}/\d{4} \w{3} \d{2}:\d{2} Come back on \d{2}/\d{2}/\d{4} \w{3} \d{' \
              r'2}:\d{2}$'
    match = re.match(pattern, leave)

    if match:
        return True
    else:
        return False
