class Bed:
    def __init__(self, room_number, bed_number):
        self.room_number = room_number
        self.bed_number = bed_number

    def __eq__(self, other):
        return self.room_number == other.room_number and self.bed_number == other.bed_number

    def __lt__(self, other):
        return self.room_number < other.room_number or (self.room_number == other.room_number
                                                        and self.bed_number < other.bed_number)

    def __repr__(self):
        return f"{self.room_number}/{self.bed_number}"
