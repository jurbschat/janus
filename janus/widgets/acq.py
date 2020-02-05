"""
This is part of the janus package.
"""

__author__ = "Jan Meyer"
__email__ = "jan.meyer@desy.de"
__copyright__ = "(c)2019 DESY, FS-BMX, FS-Petra-D, P11"
__license__ = "GPL"


from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import QWidget, QDialog, QLabel, QCheckBox, QLayout, \
        QProgressBar, QPushButton, QLineEdit, QGridLayout, QVBoxLayout
from ..core import Object

class AcqRunParameters(QObject, Object):

    def __init__(self, parent=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.setup_ui()
        self.register_persistents()
        self.connect_signals()

    def setup_ui(self):
        from janus.widgets.ui.acq_run_parameters_ui import Ui_FormAcqRun
        self.widget = QWidget(self.parent)
        self.ui = Ui_FormAcqRun()
        self.ui.setupUi(self.widget)
        self.update_values("number")

    def connect_signals(self):
        self.ui.lineEditAcqSampleName.textChanged.connect( \
                self.janus.utils["path"].set_user_and_sample_dir)
        self.janus.utils["path"].value_changed.connect(self.update_values)

    def register_persistents(self):
        self.janus.utils["config"].add_persistent( \
                "acq", "sample_name", self.ui.lineEditAcqSampleName.text,
                self.ui.lineEditAcqSampleName.setText, str)
        self.janus.utils["config"].add_persistent( \
                "acq", "comment", self.ui.plainTextEditAcqComment.toPlainText,
                self.ui.plainTextEditAcqComment.setPlainText, str)

    def update_values(self, value):
        if value == "number":
            self.ui.lineEditAcqRunNumer.setText( \
                str(self.janus.utils["path"].number))
        else:
            self.ui.lineEditAcqPath.setText( \
                    self.janus.utils["path"].get_path( \
                    "/beamline/beamtime/raw/user/sample"))


class AcqProgressDialog(QObject, Object):

    def __init__(self, parent=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.acq_method = None
        self.grid = None
        self.progress_bar = None
        self.push_button = None
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        self.widget = QDialog(self.parent, \
                (Qt.Dialog | Qt.WindowSystemMenuHint) & \
                ~Qt.WindowCloseButtonHint)
        self.widget.setWindowTitle("AcqProgress")
        self.widget.setLayout(QVBoxLayout())
        self.widget.setModal(True)
        self.details_container = QGridLayout()
        self.widget.layout().addLayout(self.details_container)
        self.conditions_container = QVBoxLayout()
        self.widget.layout().addLayout(self.conditions_container)
        self.progress_bar = QProgressBar(self.widget)
        self.progress_bar.setMinimumWidth(300)
        self.progress_bar.setProperty("value", 0)
        self.widget.layout().addWidget(self.progress_bar)
        self.push_button = QPushButton(self.widget)
        self.push_button.setText("Stop\nData Collection")
        self.widget.layout().addWidget(self.push_button)
        self.widget.layout().setSizeConstraint(QLayout.SetFixedSize)

    def connect_signals(self):
        pass

    def show(self, acq_method = None):
        if acq_method is not None:
            self.acq_method = acq_method
            self.reset()
        self.widget.show()

    def hide(self):
        self.widget.hide()
    
    def reset(self):
        for widget in self.widget.findChildren(QCheckBox):
            self.details_container.removeWidget(widget)
            widget.deleteLater()
            widget = None
        for widget in self.widget.findChildren(QLineEdit):
            self.conditions_container.removeWidget(widget)
            widget.deleteLater()
            widget = None
        for widget in self.widget.findChildren(QLabel):
            self.conditions_container.removeWidget(widget)
            widget.deleteLater()
            widget = None
        if self.acq_method is not None:
            self.widget.setWindowTitle(self.acq_method.title)
            if len(self.acq_method.progress_details) > 0:
                horz = 0
                vert = 0
                for key, getter in self.acq_method.progress_details.items():
                    label = QLabel(self.widget)
                    label.setText(key)
                    line_edit = QLineEdit(self.widget)
                    line_edit.setReadOnly(True)
                    line_edit.setText(eval(getter))
                    line_edit.setObjectName("QLineEdit" + key)
                    self.details_container.addWidget(label, vert, horz, 1, 1)
                    self.details_container.addWidget(line_edit, vert+1, horz, 1, 1)
                    vert += 2
                    horz ^= 1
            if len(self.acq_method.conditions) > 0:
                for key, getter in self.acq_method.conditions.items():
                    checkbox = QCheckBox(key, self.widget)
                    checkbox.setChecked(eval(getter))
                    checkbox.setEnabled(False)
                    checkbox.setObjectName("QCheckBox" + key)
                    self.conditions_container.addWidget(checkbox)
        else:
            self.widget.setWindowTitle("AcqProgress")
        
    def update(self):
        for key, getter in self.acq_method.progress_details.items():
            line_edit = self.widget.findChild(QLineEdit, "QLineEdit" + key)
            line_edit.setText(eval(getter))
        for key, getter in self.acq_method.conditions.items():
            checkbox = self.widget.findChild(QCheckBox, "QCheckBox" + key)
            checkbox.setChecked(eval(getter))
        if self.acq_method.time_total > 0:
            percent = (self.acq_method.time_total -
                     self.acq_method.time_remaining()) / self.acq_method.time_total
            if self.acq_method.time_remaining() < 0:
                percent = 1.0
            self.progress_bar.setProperty("value", percent * 100)
            


