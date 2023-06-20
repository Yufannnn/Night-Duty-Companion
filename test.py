import pandas as pd

import DataUtils


file_path = "C:\\Users\\YF\\Desktop\\123.csv"
df = pd.read_csv(file_path)

boarder_list = DataUtils.build_boarder_list(df)

absent_boarders = boarder_list.get_absent_boarders()
on_leave_boarders = boarder_list.get_on_leave_boarders()

print("Absent Boarders:")
for boarder in absent_boarders:
    print(boarder)

print("On Leave Boarders:")
for boarder in on_leave_boarders:
    print(boarder)
