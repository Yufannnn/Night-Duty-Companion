def generate_message(absent_students, boarders_on_leave):
    if len(absent_students) == 0:
        return generate_message_when_no_absentees(boarders_on_leave)
    elif len(absent_students) == 1:
        return generate_message_when_one_absentee(absent_students, boarders_on_leave)
    else:
        return generate_message_when_multiple_absentees(absent_students, boarders_on_leave)


def generate_message_when_no_absentees(boarders_on_leave):
    if len(boarders_on_leave) == 0:
        return "Hi BMs, all boarders are in and there is no one with leaves today.\nThank you!"
    else:
        absent_message = "Hi BMs, all boarders are in, except for those with leaves:"
        leave_message = ""
        for boarder in boarders_on_leave:
            leave_message += f"- {boarder.bed} {boarder.name} ({boarder.leave.return_time})"

    return f"{absent_message}\n{leave_message}\nThank you!"


def generate_message_when_one_absentee(absent_students, boarders_on_leave):
    absent_message = "Hi BMs, all boarders are in except:\n"
    for boarder in absent_students:
        absent_message += f"- {boarder.bed} {boarder.name}\n"

    absent_message += "I have asked him to scan at level 1, will update again later.\n"

    leave_message = ""
    if len(boarders_on_leave) > 0:
        leave_message += "And those with leaves:\n"
        for boarder in boarders_on_leave:
            leave_message += f"- {boarder.bed} {boarder.name} ({boarder.leave.get_message_string()})\n"

    return f"{absent_message}{leave_message}Thank you!"


def generate_message_when_multiple_absentees(absent_students, boarders_on_leave):
    absent_message = "Hi BMs, all boarders are in except:\n"
    for boarder in absent_students:
        absent_message += f"- {boarder.bed} {boarder.name}\n"

    absent_message += "I have asked them to scan at level 1, will update again later.\n"

    leave_message = ""
    if len(boarders_on_leave) > 0:
        leave_message += "And those with leaves:\n"
        for boarder in boarders_on_leave:
            leave_message += f"- {boarder.bed} {boarder.name} ({boarder.leave.get_message_string()})\n"

    return f"{absent_message}{leave_message}Thank you!"
