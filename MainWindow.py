# -*- coding: utf-8 -*-
import os

import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QFileDialog, QFrame, QTextEdit, QApplication, QCheckBox, \
    QVBoxLayout, QWidget, QScrollArea
from PyQt5.QtCore import Qt, QFile

import DataUtils as DataUtils
import MessageUtils as MessageUtils
import ValidationUtils


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NightDutyCompanion")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setFixedSize(800, 425)

        self.create_column_0()
        self.create_column_1()

        # Get the path of the current file (MainWindow.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the styling.css file
        css_file = os.path.join(current_dir, "styling.css")

        # Set the stylesheet for the application
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

    def create_column_0(self):
        column0_x = 0
        column0_y = 0

        file_label_width = 700
        file_label_height = 20
        self.file_label = QLabel("No file selected.", self)
        self.file_label.setObjectName("file_label")
        self.file_label.setGeometry(column0_x + 10, column0_y + 5, file_label_width, file_label_height)

        select_button_width = 400
        select_button_height = 30
        self.select_file_button = QPushButton("Select CSV File", self)
        self.select_file_button.clicked.connect(self.select_csv_file)
        self.select_file_button.setGeometry(column0_x + 10, column0_y + 35, select_button_width, select_button_height)

        drag_frame_width = 400
        drag_frame_height = 95
        self.drag_frame = QFrame(self)
        self.drag_frame.setGeometry(column0_x + 10, column0_y + 72, drag_frame_width, drag_frame_height)
        self.drag_frame.setObjectName("drag_frame")
        self.drag_frame.setAcceptDrops(True)
        self.drag_frame.setToolTip("Drag and drop a CSV file here")
        self.drag_frame.installEventFilter(self)

        self.drag_label = QLabel("Drag and drop a CSV file here", self.drag_frame)
        self.drag_label.setGeometry(0, 0, drag_frame_width, drag_frame_height)
        self.drag_label.setAlignment(Qt.AlignCenter)

        generate_label_width = 400
        generate_label_height = 20
        self.generate_label = QLabel("Generated Message", self)
        self.generate_label.setGeometry(column0_x + 10, column0_y + 172, generate_label_width, generate_label_height)
        self.generate_label.setAlignment(Qt.AlignCenter)

        text_area_width = 400
        text_area_height = 170
        self.text_area = QTextEdit(self)
        self.text_area.setGeometry(column0_x + 10, column0_y + 200, text_area_width, text_area_height)

        copy_button_width = 400
        copy_button_height = 30
        self.copy_button = QPushButton("Copy Generated Message", self)
        self.copy_button.clicked.connect(self.copy_message)
        self.copy_button.setGeometry(column0_x + 10, column0_y + 380, copy_button_width, copy_button_height)

    def create_column_1(self):
        column1_x = 400
        column1_y = 0

        absent_label_width = 275
        absent_label_height = 30
        self.absent_label = QLabel("Absent Boarders", self)
        self.absent_label.setGeometry(column1_x + 150, column1_y + 25, absent_label_width, absent_label_height)

        absent_area_width = 368
        absent_area_height = 170
        self.absent_area_scroll = QScrollArea(self)
        self.absent_area_scroll.setGeometry(column1_x + 20, column1_y + 50, absent_area_width, absent_area_height)

        self.absent_area = QWidget()
        self.absent_area.setObjectName("absent_area")
        self.absent_area_scroll.setWidget(self.absent_area)
        self.absent_area_scroll.setWidgetResizable(True)
        self.absent_area_layout = QVBoxLayout(self.absent_area)

        # make all the widgets in teh absent area layout align to the top
        self.absent_area_layout.setAlignment(Qt.AlignTop)

        leave_label_width = 275
        leave_label_height = 30
        self.leave_label = QLabel("Boarders on Leave", self)
        self.leave_label.setGeometry(column1_x + 150, column1_y + 215, leave_label_width, leave_label_height)

        leave_area_width = 368
        leave_area_height = 170
        self.leave_area_scroll = QScrollArea(self)
        self.leave_area_scroll.setGeometry(column1_x + 20, column1_y + 240, leave_area_width, leave_area_height)

        self.leave_area = QWidget()
        self.leave_area.setObjectName("leave_area")
        self.leave_area_scroll.setWidget(self.leave_area)
        self.leave_area_scroll.setWidgetResizable(True)
        self.leave_area_layout = QVBoxLayout(self.leave_area)

    def eventFilter(self, obj, event):
        if obj == self.drag_frame:
            if event.type() == event.DragEnter:
                DataUtils.handle_drag_enter(event)
            elif event.type() == event.Drop:
                self.handle_drop(event)
        return super().eventFilter(obj, event)

    def handle_drop(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path:
            self.file_label.setText(file_path)

            try:
                message, absent_boarders, on_leave_boarders = self.generate_message(file_path)
                self.text_area.setText(message)
                self.populate_absent_area(absent_boarders)
                self.populate_leave_area(on_leave_boarders)

            except ValueError as e:
                self.file_label.setText(e.args[0])
                self.text_area.setText("")
                self.populate_absent_area([])
                self.populate_leave_area([])
        else:
            self.file_label.setText("No file selected.")

        event.acceptProposedAction()

    def select_csv_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)", options=options)

        if file_path:
            self.file_label.setText(file_path)

            try:
                message, absent_boarders, on_leave_boarders = self.generate_message(file_path)
                self.text_area.setText(message)
                self.populate_absent_area(absent_boarders)
                self.populate_leave_area(on_leave_boarders)

            except ValueError as e:
                self.file_label.setText("File selected is not today's attendance file.")
        else:
            self.file_label.setText("No file selected.")

    def generate_message(self, file_path):
        df = pd.read_csv(file_path)

        is_valid, error_message = ValidationUtils.check_if_file_is_attendance_file(df)
        if not is_valid:
            raise ValueError(error_message)

        boarders_list = DataUtils.build_boarder_list(df)
        absent_boarders = boarders_list.get_absent_boarders()
        on_leave_boarders = boarders_list.get_on_leave_boarders()
        generated_message = MessageUtils.generate_message(absent_boarders, on_leave_boarders)

        return generated_message, absent_boarders, on_leave_boarders

    def copy_message(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_area.toPlainText())

    def populate_absent_area(self, absent_boarders):
        # Clear previously added widgets
        while self.absent_area_layout.count():
            widget = self.absent_area_layout.takeAt(0).widget()
            if widget:
                widget.setParent(None)

        for boarder in absent_boarders:
            absent_boarder_checkbox = QCheckBox(boarder.to_absent_string(), self)
            self.absent_area_layout.addWidget(absent_boarder_checkbox)

        self.absent_area_layout.addStretch(1)

    def populate_leave_area(self, on_leave_boarders):
        # Clear previously added widgets
        while self.leave_area_layout.count():
            widget = self.leave_area_layout.takeAt(0).widget()
            if widget:
                widget.setParent(None)

        for boarder in on_leave_boarders:
            on_leave_boarder_checkbox = QCheckBox(boarder.to_leave_string(), self)
            self.leave_area_layout.addWidget(on_leave_boarder_checkbox)

        self.leave_area_layout.addStretch(1)
