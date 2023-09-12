from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication,
                             QHBoxLayout, QVBoxLayout, QGridLayout,
                             QMainWindow, QComboBox, QLineEdit, QPushButton,
                             QLabel, QDialog, QCheckBox, QPlainTextEdit, QMessageBox)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from Kholendar import *
from UserKholan import *


class KholGUI(QMainWindow):

    """
    Main screen of the calendar GUI. Consists of two main sections. The sidebar and the calendar itself.
    """

    def __init__(self):
        super(KholGUI, self).__init__()

        self.user = None
        self.current_month_year = (0, 2000)
        self.initial_setup = False

        global refresh
        refresh = self.select_date_action

        self.main = QHBoxLayout()

        # Setup user select window
        self.user_select = UserSelect(self)
        self.user_select.set_button(self.select_user_action)
        self.user_select.exec()

        # Setup sidebar
        self.sidebar = SideBar()
        self.sidebar.set_user_button(self.change_user_action)
        self.sidebar.set_select_button(self.select_date_action)
        self.sidebar.set_refresh_button(self.select_date_action)
        self.sidebar.set_create_button(self.create_event)
        self.main.addWidget(self.sidebar)

        # Setup Calendar
        self.calendar = MonthDisplay(*self.current_month_year, self.user)
        self.main.addWidget(self.calendar)

        # Window Adjustments
        central = QWidget()
        central.setLayout(self.main)
        self.setCentralWidget(central)
        self.setWindowTitle("Kholendar")
        self.setMinimumSize(1200, 800)
        self.initial_setup = True

    def change_user_action(self):
        self.user_select.exec()

    def select_date_action(self):
        self.current_month_year = self.sidebar.get_info()
        self.main.removeWidget(self.calendar)
        self.calendar = MonthDisplay(*self.current_month_year, self.user)
        self.main.addWidget(self.calendar)

    def select_user_action(self):
        new_user = self.user_select.new_user()
        # Update user
        try:
            self.user = UserKholen(self.user_select.get_user(), new=new_user)
            self.user_select.close()
        except:
            error = QMessageBox()
            error.setWindowTitle('Error')
            if new_user:
                error.setText("User Already Exists")
            else:
                error.setText("User Doesn't Exist")
            error.exec()

        # Update calendar
        if self.initial_setup:

            self.main.removeWidget(self.calendar)
            self.calendar = MonthDisplay(*self.current_month_year, self.user)
            self.main.addWidget(self.calendar)

    def create_event(self):
        event_window = EventScreen()
        event_window.create_mode(self.user)
        event_window.exec()


class SideBar(QWidget):

    """
    Sidebar of the main window. Contains a year/month selector. Create, refresh, change user and select button.
    """

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Add month dropdown
        self.months = QComboBox()
        self.months.addItems(["Days of Awn", "Arc", "Bar", "Cah", "Dal", "Ead", "Fax", "Gok", "Hya", "Iba",
                              "Jok", "Kaz", "Leb", "Mef", "Nya", "Oop", "Pac", "Qua", "Ros",
                              "Sla", "Tuv", "Uxa", "Vob", "Wek", "Xan"])
        layout.addWidget(self.months)

        # Add box for year
        self.year = QLineEdit()
        self.year.setMaxLength(4)
        self.year.setText("2000")
        self.year.setValidator(QIntValidator())
        layout.addWidget(self.year)

        # Add Search button
        self.select = QPushButton('Select')
        layout.addWidget(self.select)

        # Add Create Event button
        self.create = QPushButton('Create Event')
        layout.addWidget(self.create)

        # Add Change User button
        self.user_button = QPushButton('Change User')
        layout.addWidget(self.user_button)
        layout.setAlignment(self.user_button, Qt.AlignBottom)

        # Add Refresh button
        self.refresh = QPushButton('Refresh')
        layout.addWidget(self.refresh)

        self.setLayout(layout)
        self.setMaximumWidth(125)

    def set_select_button(self, fn):
        self.select.clicked.connect(fn)

    def set_user_button(self, fn):
        self.user_button.clicked.connect(fn)

    def set_refresh_button(self, fn):
        self.refresh.clicked.connect(fn)

    def set_create_button(self, fn):
        self.create.clicked.connect(fn)

    def get_info(self):
        return self.months.currentIndex(), abs(int(self.year.text()))


class UserSelect(QDialog):

    """
    User select/create screen that is a dialog.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        # Label
        title = QLabel("Enter User ID")
        font = title.font()
        font.setPointSize(15)
        title.setFont(font)
        title.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(title)

        # User Entry and Button
        layout2 = QHBoxLayout()
        entry_line = QWidget()

        # User Entry
        self.user_id = QLineEdit()
        self.user_id.setPlaceholderText("UserID")
        layout2.addWidget(self.user_id)

        # Button
        self.select = QPushButton('Select')
        layout2.addWidget(self.select)

        entry_line.setLayout(layout2)
        layout.addWidget(entry_line)

        # Checkbox
        self.checkbox = QCheckBox("New User")
        layout.addWidget(self.checkbox)

        self.setLayout(layout)
        self.setWindowTitle("User Selection")

    def new_user(self):
        return self.checkbox.isChecked()

    def set_button(self, fn):
        self.select.clicked.connect(fn)

    def get_user(self):
        return self.user_id.text()


class MonthDisplay(QWidget):

    """
    Main container for the calendar display. Contains the names of the weekdays and the name of the month.
    Also, contains a space for each day of the month. The daily spaces are widgets that act as a container for
    other widgets.
    """

    def __init__(self, month, year, user):
        super().__init__()

        khol = Kholendar()
        layout = QVBoxLayout()

        self.month = month
        self.year = year
        self.user = user

        # Month title
        title = "Days of Awn" if self.month == 0 else khol.months[self.month - 1]
        title = QLabel(title)
        title.setMaximumHeight(50)
        title.setAlignment(Qt.AlignHCenter)
        font = title.font()
        font.setPointSize(15)
        title.setFont(font)
        layout.addWidget(title)

        # Names of the days
        weekdays = QWidget()
        layout2 = QHBoxLayout()

        for day in khol.days:
            label = QLabel(day)
            label.setAlignment(Qt.AlignHCenter)
            font.setPointSize(10)
            label.setFont(font)
            label.setMinimumWidth(200)
            layout2.addWidget(label)

        weekdays.setLayout(layout2)
        weekdays.setMaximumHeight(50)
        layout.addWidget(weekdays)

        # Days
        month_layout = QGridLayout()
        days = QWidget()

        for i, week in enumerate(khol.create_month(self.month, self.year)):
            for j, day in enumerate(week):

                day = Day(day.day, day.month, day.year, self.user)
                month_layout.addWidget(day, i, j)

        days.setLayout(month_layout)
        layout.addWidget(days)

        layout.setSpacing(5)
        self.setLayout(layout)


class Day(QWidget):

    """
    The widget that is occupies a space for each day in the MonthDisplay widget. Contains the day of the month as
    well as widgets that represent the events taken place on the corresponding day.
    """

    def __init__(self, day, month, year, user):
        super().__init__()

        self.date = KholDate(day, month, year)
        self.user = user

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Add day of the month
        day = QLabel(str(self.date.day))
        day.setAlignment(Qt.AlignRight | Qt.AlignTop)
        day.setMaximumHeight(20)
        font = day.font()
        font.setPointSize(10)
        day.setFont(font)
        layout.addWidget(day)

        # Add events for the day
        events = user.get_events(self.date.get_date_key())
        if events != 0:

            for idx, event in enumerate(events):
                label = EventLabel(event, idx, self.user)
                layout.addWidget(label)
        else:
            label = QLabel("-")
            label.setAlignment(Qt.AlignTop | Qt.AlignRight)
            layout.addWidget(label)

        self.setLayout(layout)
        self.setMaximumWidth(200)


class EventLabel(QWidget):
    """
    Clickable label that opens a dialog box which enables the user to edit or delete the event that was clicked on.
    Placed within the Day widget.
    """

    def __init__(self, event, idx, user):
        super().__init__()

        self.event = event
        self.user = user
        self.idx = idx

        layout = QVBoxLayout()

        # Create the label
        label = QLabel(self.event.name)
        label.setStyleSheet("border: 1px solid black;")
        label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(label)
        layout.setAlignment(label, Qt.AlignTop)

        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

    def mouseDoubleClickEvent(self, e):
        event_screen = EventScreen(parent=self)
        event_screen.view_mode(self.event, self.idx, self.user)
        event_screen.exec()


class EventScreen(QDialog):

    """
    A dialog box with different modes that allow for user manipulation of an event.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.event = None
        self.user = None
        self.idx = None

        layout = QVBoxLayout()

        # Name Box
        self.name = QLineEdit()
        self.name.setPlaceholderText('Name')
        self.name.setMaxLength(25)
        layout.addWidget(self.name)

        # Day Month Year selectors
        layout2 = QHBoxLayout()
        date = QWidget()

        self.day = QComboBox()
        layout2.addWidget(self.day)

        self.month = QComboBox()
        self.month.addItems(["Days of Awn", "Arc", "Bar", "Cah", "Dal", "Ead", "Fax", "Gok", "Hya", "Iba",
                             "Jok", "Kaz", "Leb", "Mef", "Nya", "Oop", "Pac", "Qua", "Ros",
                             "Sla", "Tuv", "Uxa", "Vob", "Wek", "Xan"])
        self.month.currentIndexChanged.connect(self.set_days)
        layout2.addWidget(self.month)

        self.year = QLineEdit()
        self.year.setMaxLength(4)
        self.year.setValidator(QIntValidator())
        self.year.setPlaceholderText('Year')
        layout2.addWidget(self.year)
        
        date.setLayout(layout2)
        layout.addWidget(date)

        # Details Box
        self.details = QPlainTextEdit()
        self.details.setPlaceholderText('Details')
        layout.addWidget(self.details)

        # Buttons
        layout3 = QHBoxLayout()
        buttons = QWidget()
        
        self.edit_button = QPushButton('Edit')
        self.edit_button.clicked.connect(self.edit)
        layout3.addWidget(self.edit_button)
        
        self.save_button = QPushButton('Save')
        layout3.addWidget(self.save_button)

        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete)
        layout3.addWidget(self.delete_button)

        buttons.setLayout(layout3)
        layout.addWidget(buttons)

        self.setLayout(layout)
        self.setWindowTitle('Event')

    def set_days(self, i):
        self.day.clear()
        if i == 0:
            values = list(range(1, 6))
        else:
            values = list(range(1, 16))
        self.day.addItems(list(map(str, values)))

    def edit(self):
        self.edit_mode()
    
    def delete(self):

        self.user.delete_event((self.event.get_date_key(), self.idx))
        self.user.save()
        self.close()

    def save_edit(self):

        self.user.edit_event((self.event.get_date_key(), self.idx), day=int(self.day.currentText()),
                             month=self.month.currentIndex(), year=abs(int(self.year.text())),
                             event_name=self.name.text(), event_details=self.details.toPlainText())
        self.user.save()
        self.close()
        refresh()

    def save_create(self):

        self.user.create_event(day=int(self.day.currentText()),
                               month=self.month.currentIndex(), year=abs(int(self.year.text())),
                               event_name=self.name.text(), event_details=self.details.toPlainText())
        self.user.save()
        self.close()
        refresh()

    def view_mode(self, event, idx, user):

        self.event = event
        self.idx = idx
        self.user = user

        # Set Name
        self.name.setText(self.event.name)
        self.name.setReadOnly(True)

        # Set Date
        self.month.setCurrentIndex(1)
        self.month.setCurrentIndex(self.event.month)
        self.month.setEnabled(False)

        self.day.setCurrentIndex(self.event.day - 1)
        self.day.setEnabled(False)

        self.year.setText(str(self.event.year))
        self.year.setReadOnly(True)

        # Set Details
        self.details.setPlainText(self.event.details)
        self.details.setReadOnly(True)

        # Configure Buttons
        self.edit_button.setVisible(True)
        self.save_button.setVisible(False)
        self.delete_button.setVisible(False)

    def edit_mode(self):

        # Enable All Fields
        self.name.setReadOnly(False)
        self.month.setEnabled(True)
        self.day.setEnabled(True)
        self.year.setReadOnly(False)
        self.details.setReadOnly(False)

        # Configure Buttons
        self.edit_button.setVisible(False)
        self.save_button.setVisible(True)
        self.delete_button.setVisible(True)
        self.save_button.clicked.connect(self.save_edit)

    def create_mode(self, user):

        self.user = user

        # Set Name
        self.name.setText("")
        self.name.setReadOnly(False)

        # Set Date
        self.month.setCurrentIndex(1)
        self.month.setEnabled(True)

        self.day.setCurrentIndex(0)
        self.day.setEnabled(True)

        self.year.setText("")
        self.year.setReadOnly(False)

        # Set Details
        self.details.setPlainText("")
        self.details.setReadOnly(False)

        # Configure Buttons
        self.edit_button.setVisible(False)
        self.save_button.setVisible(True)
        self.delete_button.setVisible(False)
        self.save_button.clicked.connect(self.save_create)
