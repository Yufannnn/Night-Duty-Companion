from datetime import date

import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QFileDialog, QFrame, QTextEdit, QApplication
from PyQt5.QtCore import Qt

import DataUtils as DataUtils
import MessageUtils as MessageUtils


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NightDutyCompanion")
        self.setFixedSize(800, 425)

        self.create_column_0()
        self.create_column_1()

    def create_column_0(self):
        column0_x = 0
        column0_y = 0

        file_label_width = 450
        file_label_height = 15
        self.file_label = QLabel("No file selected.", self)
        self.file_label.setStyleSheet("font-size: 15px;")
        self.file_label.setGeometry(column0_x + 10, column0_y + 5, file_label_width, file_label_height)

        select_button_width = 450
        select_button_height = 30
        self.select_file_button = QPushButton("Select CSV File", self)
        self.select_file_button.clicked.connect(self.select_csv_file)
        self.select_file_button.setGeometry(column0_x + 10, column0_y + 35, select_button_width, select_button_height)

        drag_frame_width = 450
        drag_frame_height = 100
        self.drag_frame = QFrame(self)
        self.drag_frame.setGeometry(column0_x + 10, column0_y + 75, drag_frame_width, drag_frame_height)
        self.drag_frame.setStyleSheet("QFrame { border: 2px dashed #AAAAAA; }")
        self.drag_frame.setAcceptDrops(True)
        self.drag_frame.setToolTip("Drag and drop a CSV file here")
        self.drag_frame.installEventFilter(self)

        self.drag_label = QLabel("Drag and drop a CSV file here", self.drag_frame)
        self.drag_label.setGeometry(0, 0, drag_frame_width, drag_frame_height)
        self.drag_label.setAlignment(Qt.AlignCenter)

        generate_label_width = 450
        generate_label_height = 15
        self.generate_label = QLabel("Generated Message", self)
        self.generate_label.setStyleSheet("font-size: 12px;")
        self.generate_label.setGeometry(column0_x + 10, column0_y + 180, generate_label_width, generate_label_height)
        self.generate_label.setAlignment(Qt.AlignCenter)

        text_area_width = 450
        text_area_height = 170
        self.text_area = QTextEdit(self)
        self.text_area.setGeometry(column0_x + 10, column0_y + 200, text_area_width, text_area_height)
        self.text_area.setStyleSheet("font-size: 12px;")

        copy_button_width = 450
        copy_button_height = 30
        self.copy_button = QPushButton("Copy Generated Message", self)
        self.copy_button.clicked.connect(self.copy_message)
        self.copy_button.setGeometry(column0_x + 10, column0_y + 380, copy_button_width, copy_button_height)

    def create_column_1(self):
        column1_x = 450
        column1_y = 0

        absent_label_width = 225
        absent_label_height = 30
        self.absent_label = QLabel("Absent Boarders", self)
        self.absent_label.setStyleSheet("font-size: 12px;")
        self.absent_label.setGeometry(column1_x + 125, column1_y + 15, absent_label_width, absent_label_height)

        absent_area_width = 318
        absent_area_height = 170
        self.absent_area = QTextEdit(self)
        self.absent_area.setGeometry(column1_x + 20, column1_y + 40, absent_area_width, absent_area_height)
        self.absent_area.setStyleSheet("font-size: 12px;")

        leave_label_width = 225
        leave_label_height = 30
        self.leave_label = QLabel("Boarders on Leave", self)
        self.leave_label.setStyleSheet("font-size: 12px;")
        self.leave_label.setGeometry(column1_x + 125, column1_y + 210, leave_label_width, leave_label_height)

        leave_area_width = 318
        leave_area_height = 170
        self.leave_area = QTextEdit(self)
        self.leave_area.setGeometry(column1_x + 20, column1_y + 235, leave_area_width, leave_area_height)
        self.leave_area.setStyleSheet("font-size: 12px;")

    def eventFilter(self, obj, event):
        if obj == self.drag_frame:
            if event.type() == event.DragEnter:
                DataUtils.handle_drag_enter(event)
            elif event.type() == event.Drop:
                self.handle_drop(event)
        return super().eventFilter(obj, event)

    def handle_drop(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.file_label.setText(file_path)
        try:
            message, absent_text, leave_text = self.generate_message(file_path)
            self.text_area.setText(message)
            self.absent_area.setText(absent_text)
            self.leave_area.setText(leave_text)
        except:
            self.file_label.setText("File selected is not today's attendance file.")

        event.acceptProposedAction()

    def select_csv_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)", options=options)

        if file_path:
            self.file_label.setText(file_path)
            try:
                message, absent_text, leave_text = self.generate_message(file_path)
                self.text_area.setText(message)
                self.absent_area.setText(absent_text)
                self.leave_area.setText(leave_text)
            except:
                self.file_label.setText("File selected is not today's attendance file.")
        else:
            self.file_label.setText("No file selected.")

    def generate_message(self, file_path):
        df = pd.read_csv(file_path)

        try:
            DataUtils.check_if_file_is_attendance_file(df)
        except:
            self.file_label.setText("File selected is not a valid attendance file.")

        # Check if Date column contains the current date
        current_date = date.today().strftime("%d/%m/%Y")
        # if not all dates are equal to current date
        if not df['Date'].eq(current_date).all():
            DataUtils.send_not_current_date_message()
            return

        # Identify absent students
        absent_students = DataUtils.get_absent_students(df)
        absent_text = DataUtils.format_absent_students(absent_students)

        # Check if leaves are due today
        leave_due_today = DataUtils.get_leave_due_tonight(df, current_date)
        leave_text = DataUtils.format_leave_due(leave_due_today)

        if len(absent_students) == 0:
            return MessageUtils.generate_message_when_no_absentees(leave_due_today), absent_text, leave_text
        elif len(absent_students) == 1:
            return MessageUtils.generate_message_when_one_absentee(absent_students,
                                                                   leave_due_today), absent_text, leave_text
        elif len(absent_students) > 1:
            return MessageUtils.generate_message_when_multiple_absentees(absent_students,
                                                                         leave_due_today), absent_text, leave_text

    def copy_message(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_area.toPlainText())
