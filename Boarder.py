class Boarder:
    def __init__(self, name, bed, contact_number, terminal_number, scanned_time, leave):
        self.name = name
        self.bed = bed
        self.contact_number = contact_number
        self.terminal_number = terminal_number
        self.scanned_time = scanned_time
        self.leave = leave

    def is_on_leave(self):
        # check if the leave is due today or tomorrow before 2am
        if self.leave is not None:
            if self.leave.is_today() or self.leave.is_tomorrow_earlier_than_2am():
                return True

        return False

    def is_absent(self):
        if self.scanned_time is None and self.leave is None:
            return True

        if self.scanned_time is None and self.leave.is_overdue():
            return True

        return False

    def to_absent_string(self):
        return f"{self.bed} {self.contact_number} {self.name}"

    def to_leave_string(self):
        return f"{self.leave.get_time_string()} {self.bed} {self.contact_number} {self.name}"

    def __repr__(self):
        return f"Boarder({self.name}, {self.bed}, {self.contact_number}, {self.terminal_number}, " \
               f"{self.scanned_time}, {self.leave})"




