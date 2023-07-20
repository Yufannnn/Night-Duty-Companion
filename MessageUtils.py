def generate_message(absent_boarders, on_leave_boarders):
    """
    Generate the message to be sent to BMs based on the list of absentees and those on leave.

    :param absent_boarders: list of boarders who are absent
    :param on_leave_boarders: list of boarders who are on leave
    :return: the message to be sent to BMs
    """
    if len(absent_boarders) == 0:
        return generate_message_when_no_absentees(on_leave_boarders)
    elif len(absent_boarders) == 1:
        return generate_message_when_one_absentee(absent_boarders, on_leave_boarders)
    else:
        return generate_message_when_multiple_absentees(absent_boarders, on_leave_boarders)


def generate_message_when_no_absentees(on_leave_boarders):
    """
    Generate the message to be sent to BMs when there are no absentees.

    :param on_leave_boarders:
    :return: the message to be sent to BMs
    """
    if len(on_leave_boarders) == 0:
        return "Hi BMs, all boarders are in and there is no one with leaves today.\nThank you!"
    else:
        absent_message = "Hi BMs, all boarders are in, except for those with leaves:"
        leave_message = ""
        for boarder in on_leave_boarders:
            leave_message += f"- {boarder.bed} {boarder.name} ({boarder.leave.return_time})"

    return f"{absent_message}\n{leave_message}\nThank you!"


def generate_message_when_one_absentee(absent_boarders, on_leave_boarders):
    absent_message = "Hi BMs, all boarders are in except:\n"
    for boarder in absent_boarders:
        absent_message += f"- {boarder.bed} {boarder.name}\n"

    absent_message += "I have asked him to scan at level 1, will update again later.\n"

    leave_message = ""
    if len(on_leave_boarders) > 0:
        leave_message += "And those with leaves:\n"
        for boarder in on_leave_boarders:
            leave_message += f"- {boarder.bed} {boarder.name} ({boarder.leave.get_message_string()})\n"

    return f"{absent_message}{leave_message}Thank you!"


def generate_message_when_multiple_absentees(absent_boarders, on_leave_boarders):
    absent_message = "Hi BMs, all boarders are in except:\n"
    for boarder in absent_boarders:
        absent_message += f"- {boarder.bed} {boarder.name}\n"

    absent_message += "I have asked them to scan at level 1, will update again later.\n"

    leave_message = ""
    if len(on_leave_boarders) > 0:
        leave_message += "And those with leaves:\n"
        for boarder in on_leave_boarders:
            leave_message += f"- {boarder.bed} {boarder.name} ({boarder.leave.get_message_string()})\n"

    return f"{absent_message}{leave_message}Thank you!"


def generate_message_from_dropdown_list(still_absent_boarders, still_on_leave_boarders):
    if not still_absent_boarders and not still_on_leave_boarders:
        return ""

    starting_prompt = "Hi BMs, now only left with:\n"
    absent_message = ""
    for checkbox in still_absent_boarders:
        boarder = checkbox.boarder
        absent_message += f"- {boarder.name}\n"

    leave_message = ""
    for checkbox in still_on_leave_boarders:
        boarder = checkbox.boarder
        leave_message += f"- {boarder.name} ({boarder.leave.get_message_string()})\n"

    return f"{starting_prompt}{absent_message}{leave_message}"
