from datetime import datetime, timedelta


class Leave:
    def __init__(self, leave_type, return_time):
        self.leave_type = leave_type
        self.return_time = return_time

    def is_today(self):
        return self.return_time.date() == datetime.now().date()

    def is_tomorrow_earlier_than_2am(self):
        return self.return_time.date() ==  (datetime.now() + timedelta(days=1)).date() and self.return_time.hour < 2

    def is_overdue(self):
        return self.return_time < datetime.now()

    def get_message_string(self):
        return f"with {self.leave_type} Leave till {self.return_time.strftime('%H:%M')}"

    def get_time_string(self):
        return f"{self.return_time.strftime('%H:%M')}"

    def __repr__(self):
        return f"Leave({self.leave_type}, {self.return_time})"

    def __lr__(self, other):
        return self.return_time < other.return_time
