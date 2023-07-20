class BoarderList:
    def __init__(self):
        self.boarderList = []

    def add_boarder(self, boarder):
        self.boarderList.append(boarder)

    def get_absent_boarders(self):
        """
        Return all boarders who are absent, sorted by bed number.

        :return: all boarders who are absent, sorted by bed number
        """
        absent_boarders = []
        for boarder in self.boarderList:
            if boarder.is_absent():
                absent_boarders.append(boarder)

        return sorted(absent_boarders, key=lambda boarder: boarder.bed)

    def get_on_leave_boarders(self):
        """
        Return all boarders who are on leave, sorted by return time.

        :return: all boarders who are on leave, sorted by return time
        """
        on_leave_boarders = []
        for boarder in self.boarderList:
            if boarder.is_on_leave():
                if not boarder.leave.is_overdue():
                    on_leave_boarders.append(boarder)

        return sorted(on_leave_boarders, key=lambda boarder: boarder.leave.return_time)
