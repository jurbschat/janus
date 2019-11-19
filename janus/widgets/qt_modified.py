"""
This is part of the janus package.
"""


from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget, QDialog, QLabel, QComboBox, QSpinBox, \
        QDoubleSpinBox
from PyQt5.QtCore import Qt, QPoint, QRect, QEvent
from PyQt5.Qt import QPushButton


class QNoWheelDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        QDoubleSpinBox.__init__(self, parent)
        self.installEventFilter(self)
        self.setFocusPolicy(Qt.StrongFocus)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Wheel:
            if not self.hasFocus():
                event.ignore()
                return True
        return QWidget.eventFilter(self, source, event)


class QNoWheelSpinBox(QSpinBox):
    def __init__(self, parent=None):
        QSpinBox.__init__(self, parent)
        self.installEventFilter(self)
        self.setFocusPolicy(Qt.StrongFocus)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Wheel:
            if not self.hasFocus():
                event.ignore()
                return True
        return QWidget.eventFilter(self, source, event)


class QElementChooser(QComboBox):

    def __init__(self, parent=None):
        QComboBox.__init__(self, parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        #combo box
        from ..const import ChemicalElement
        self.addItem("please choose")
        for element in [ChemicalElement(z) for z in range(1, 119)]:
            self.addItem(str(element.z) + " - " + element.name)
        #dialog
        from janus.widgets.ui.element_chooser_ui import Ui_Dialog
        self.dialog = QDialog(self.parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.dialog)
        for button in self.dialog.findChildren(QPushButton):
            z = int(str(button.objectName())[11:])
            element = ChemicalElement(z)
            tooltip = "{0} {1}<hr />".format(element.z, element.name)
            if "k_edge" in element.__dict__:
                tooltip += "K = {0} eV<br />".format(element.k_edge)
            if "l1_edge" in element.__dict__:
                tooltip += "L&#x2081; = {0} eV<br />".format(element.l1_edge)
            if "l2_edge" in element.__dict__:
                tooltip += "L&#x2082; = {0} eV<br />".format(element.l2_edge)
            if "l3_edge" in element.__dict__:
                tooltip += "L&#x2083; = {0} eV<br />".format(element.l3_edge)
            tooltip = tooltip[:-6]
            tooltip += "<hr />"
            if "k_alpha1" in element.__dict__:
                tooltip += "K&alpha;&#x2081; = {0} eV<br />".format(
                        element.k_alpha1)
            if "k_alpha2" in element.__dict__:
                tooltip += "K&alpha;&#x2082; = {0} eV<br />".format(
                        element.k_alpha2)
            if "k_beta1" in element.__dict__:
                tooltip += "K&beta;&#x2081; = {0} eV<br />".format(
                        element.k_beta1)
            if "l_alpha1" in element.__dict__:
                tooltip += "L&alpha;&#x2081; = {0} eV<br />".format(
                        element.l_alpha1)
            if "l_alpha2" in element.__dict__:
                tooltip += "L&alpha;&#x2082; = {0} eV<br />".format(
                        element.l_alpha2)
            if "l_beta1" in element.__dict__:
                tooltip += "L&beta;&#x2081; = {0} eV<br />".format(
                        element.l_beta1)
            if "l_beta2" in element.__dict__:
                tooltip += "L&beta;&#x2082; = {0} eV<br />".format(
                        element.l_beta2)
            if "l_gamma1" in element.__dict__:
                tooltip += "L&gamma;&#x2081; = {0} eV<br />".format(
                        element.l_gamma1)
            tooltip = tooltip[:-6]
            button.setToolTip(tooltip)
            button.clicked.connect(self.choose)
        self.dialog.rejected.connect(self.hidePopup)

    def choose(self):
        name = str(self.sender().objectName())
        if name[:10] == "pushButton":
            self.dialog.done(int(name[11:]))
        self.hidePopup()
        self.setCurrentIndex(int(name[11:]))

    def showPopup(self, *args, **kwargs):
        self.dialog.open()


class QPositionMonitor(QLabel):

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.bpmDiameter = 10
        self.bpmHorizontalGap = 0.2
        self.bpmVerticalGap = 0.5
        self.beamWidth = 3.5
        self.beamHeight = 2.2
        self.beamPosX = 0.0
        self.beamPosY = 0.0

    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        center = QPoint((width + 1) / 2, (height + 1) / 2)
        diameterBpm = width - 2
        if(height < width):
            diameterBpm = height - 2
        widthBeam = diameterBpm * (self.beamWidth / self.bpmDiameter)
        heightBeam = diameterBpm * (self.beamHeight / self.bpmDiameter)
        horizontalGapWidth = diameterBpm * (self.bpmHorizontalGap / self.bpmDiameter)
        horizontalGap = QRect(center.x() + 1 - horizontalGapWidth / 2, center.y() - diameterBpm / 2, horizontalGapWidth, diameterBpm + 2)
        verticalGapWidth = diameterBpm * (self.bpmVerticalGap / self.bpmDiameter)
        verticalGap = QRect(center.x() - 1 - diameterBpm / 2, center.y() + 1 - verticalGapWidth / 2, diameterBpm + 2, verticalGapWidth)
        posX = center.x() + self.beamPosX * center.x() / 2
        posY = center.y() + self.beamPosY * center.y() / 2

        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(Qt.white))
        painter.setBrush(Qt.white)
        painter.drawEllipse(center, diameterBpm / 2, diameterBpm / 2)
        painter.eraseRect(horizontalGap)
        painter.eraseRect(verticalGap)
        if(abs(self.beamPosX) <= 1 and abs(self.beamPosY) <= 1):
            painter.setPen(QPen(Qt.red))
            painter.setBrush(Qt.transparent)
            painter.drawEllipse(posX + 1 - widthBeam / 2, posY + 1 - heightBeam / 2, widthBeam, heightBeam)
        painter.end()

    def setBpmDiameter(self, diameter):
        self.bpmDiameter = diameter

    def setBpmHorizontalGap(self, gap):
        self.bpmHorizontalGap = gap

    def setBpmVerticalGap(self, gap):
        self.bpmVerticalGap = gap

    def setBeamWidth(self, width):
        self.beamWidth = width

    def setBeamHeight(self, height):
        self.beamHeight = height

    def setBeamPosX(self, pos):
        self.beamPosX = pos

    def setBeamPosY(self, pos):
        self.beamPosY = pos
