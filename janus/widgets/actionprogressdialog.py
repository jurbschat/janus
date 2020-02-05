from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QDialog, QLabel, QCheckBox, QLayout, \
        QProgressBar, QPushButton, QLineEdit, QGridLayout, QVBoxLayout
from ..core import Object

class ProgressDialog(QObject, Object):

    abort_signal = pyqtSignal()

    def __init__(self, progress_data, parent=None):
        QObject.__init__(self)
        Object.__init__(self)
        self.parent = parent
        self.grid = None
        self.progress_bar = None
        self.push_button = None
        self.setup_ui(progress_data)
        self.connect_signals()

    def destroy(self):
        self.widget.deleteLater()

    def setup_ui(self, progress_data):
        self.widget = QDialog(self.parent, \
                      (Qt.Dialog | Qt.WindowSystemMenuHint) & \
                      ~Qt.WindowCloseButtonHint)
        self.widget.setWindowTitle(progress_data["windowTitle"])
        self.widget.setLayout(QVBoxLayout())
        self.widget.setModal(True)
        self.details_container = QGridLayout()
        self.widget.layout().addLayout(self.details_container)
        self.conditions_container = QVBoxLayout()
        self.widget.layout().addLayout(self.conditions_container)
        self.progress_bar = QProgressBar(self.widget)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setMinimumWidth(300)
        self.progress_bar.setProperty("value", progress_data["progress"])
        self.widget.layout().addWidget(self.progress_bar)
        self.push_button = QPushButton(self.widget)
        self.push_button.setText("Stop\nData Collection")
        self.push_button.clicked.connect(self.stop_clicked)
        self.widget.layout().addWidget(self.push_button)
        self.widget.layout().setSizeConstraint(QLayout.SetFixedSize)
        self.build(progress_data)
        self.update_data(progress_data)
        self.widget.show()

    def connect_signals(self):
        pass

    def stop_clicked(self):
        self.abort_signal.emit()

    def build(self, progress_data):
        horz = 0
        vert = 0
        for key, val in progress_data["details"].items():
            name = "{}.{}".format("details", key)
            widget = self.widget.findChild(QObject, name=name)
            if not widget:
                label = QLabel(self.widget)
                label.setText(key)
                line_edit = QLineEdit(self.widget)
                line_edit.setReadOnly(True)
                line_edit.setText(key)
                line_edit.setObjectName(name)
                self.details_container.addWidget(label, vert, horz, 1, 1)
                self.details_container.addWidget(line_edit, vert, horz + 1, 1, 1)
                vert += 1
                horz %= 2
        for key, val in progress_data["conditions"].items():
            name = "{}.{}".format("conditions", key)
            widget = self.widget.findChild(QObject, name=name)
            if not widget:
                checkbox = QCheckBox(key, self.widget)
                checkbox.setChecked(val)
                checkbox.setEnabled(False)
                checkbox.setObjectName(name)
                self.conditions_container.addWidget(checkbox)

    def update_data(self, progress_data):
        for key, val in progress_data["conditions"].items():
            name = "{}.{}".format("conditions", key)
            widget = self.widget.findChild(QObject, name=name)
            if widget:
                widget.setChecked(val)
        for key, val in progress_data["details"].items():
            name = "{}.{}".format("details", key)
            widget = self.widget.findChild(QObject, name=name)
            if widget:
                widget.setText(val)
        self.progress_bar.setValue(progress_data["progress"] * 100)
        self.widget.setWindowTitle(progress_data["windowTitle"])