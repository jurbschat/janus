from ..core import Object
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget
from ..widgets.ui.autofocus_ui import Ui_Autofocus
from ..controllers.axiscontroller import GridAxisNames
import janus.utils.mathhelpers as mh

class FocusCorners:
    UpperLeft="ul"
    UpperRight="ur"
    LowerRight="lr"
    LowerLeft = "ll"

class AutoFocusControls(QObject, Object):

    def __init__(self, focus_controller=None, axis_controller=None, parent=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.axis_controller = axis_controller
        self.focus_controller = focus_controller
        self.setup_ui()
        self.validInputs = {}
        self.focus_corners = {
            #'ul': [0.0, -0.0, 140.0],
            #'ur': [-200.0, -0.0, 120.0],
            #'lr': [-200.0, -200.0, 100.0],
            #'ll': [0.0, -200.0, 80.0]
        }
        self.label_lookup = {
            FocusCorners.LowerLeft: self.ui.label_ll,
            FocusCorners.UpperLeft: self.ui.label_ul,
            FocusCorners.UpperRight: self.ui.label_ur,
            FocusCorners.LowerRight: self.ui.label_lr
        }
        self.log = self.janus.utils["logger"]
        self.afc = None #self.janus.devices["autofocus"]
        self.focusRunning = False
        self.connect_signals()
        self.validate_corners()

    def connect_signals(self):
        self.ui.quantSlider.valueChanged.connect(self.quantSliderChanged)
        self.ui.delaySlider.valueChanged.connect(self.delaySliderChanged)
        self.ui.goalSlider.valueChanged.connect(self.goalSliderChanged)
        self.ui.quantEdit.textChanged.connect(self.quantEditChanged)
        self.ui.delayEdit.textChanged.connect(self.delayEditChanged)
        self.ui.goalEdit.textChanged.connect(self.goalEditChanged)
        self.ui.startFocus.clicked.connect(self.startClicked)
        #self.afc.focus_done.connect(self.focusDone)
        self.ui.button_ll.clicked.connect(lambda: self.on_focus_btn_clicked(FocusCorners.LowerLeft))
        self.ui.button_ul.clicked.connect(lambda: self.on_focus_btn_clicked(FocusCorners.UpperLeft))
        self.ui.button_ur.clicked.connect(lambda: self.on_focus_btn_clicked(FocusCorners.UpperRight))
        self.ui.button_lr.clicked.connect(lambda: self.on_focus_btn_clicked(FocusCorners.LowerRight))
        self.ui.clear_ll.clicked.connect(lambda: self.on_clear_btn_clicked(FocusCorners.LowerLeft))
        self.ui.clear_ul.clicked.connect(lambda: self.on_clear_btn_clicked(FocusCorners.UpperLeft))
        self.ui.clear_ur.clicked.connect(lambda: self.on_clear_btn_clicked(FocusCorners.UpperRight))
        self.ui.clear_lr.clicked.connect(lambda: self.on_clear_btn_clicked(FocusCorners.LowerRight))
        self.ui.clear_all.clicked.connect(self.on_clear_all_clicked)
        self.ui.checkbox_enable_continuous_focus.toggled.connect(self.enable_continuous_toggle)


    def is_number(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def is_int(self, str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    def quantSliderChanged(self, value):
        self.log.info("quant!")
        editText = "{0:.2f}".format(value / self.ui.quantSlider.maximum()).rstrip('0').rstrip('.')
        self.ui.quantEdit.setText(editText)
        pass

    def goalSliderChanged(self, value):
        self.log.info("goal!")
        editText = "{0:.2f}".format(value / self.ui.quantSlider.maximum()).rstrip('0').rstrip('.')
        self.ui.goalEdit.setText(editText)
        pass

    def delaySliderChanged(self, value):
        self.log.info("delay!")
        editText = str(value)
        self.ui.delayEdit.setText(editText)
        pass

    def quantEditChanged(self, value):
        if not self.process_and_validate_edit_input(value, "quant", self.is_number):
            return
        value = int(float(value) * self.ui.quantSlider.maximum())
        self.ui.quantSlider.setValue(value)

    def goalEditChanged(self, value):
        if not self.process_and_validate_edit_input(value, "goal", self.is_number):
            return
        value = int(float(value) *  self.ui.quantSlider.maximum())
        self.ui.goalSlider.setValue(value)

    def delayEditChanged(self, value):
        if not self.process_and_validate_edit_input(value, "delay", self.is_int):
            return
        value = int(value)
        self.ui.delaySlider.setValue(value)

    def process_and_validate_edit_input(self, value, name, validateFct):
        if not validateFct(value):
            self.validInputs[name] = False
            self.set_start_focus_btn_state()
            return False
        self.validInputs[name] = True
        self.set_start_focus_btn_state()
        return True

    def set_start_focus_btn_state(self):
        if self.focusRunning:
            return False
        for key in self.validInputs:
            val = self.validInputs[key]
            if not val:
                self.ui.startFocus.setEnabled(False)
                return
        self.ui.startFocus.setEnabled(True)

    def startClicked(self):
        self.focusRunning = True
        self.set_start_focus_btn_state()
        quant = self.ui.quantSlider.value() / self.ui.quantSlider.maximum()
        goal = self.ui.goalSlider.value() / self.ui.goalSlider.maximum()
        delay = self.ui.delaySlider.value()
        #self.afc.start_autofocus(quant, goal, delay)

    def focusDone(self):
        self.focusRunning = False
        self.set_start_focus_btn_state()

    def validate_corners(self):
        if len(self.focus_corners) == 4:
            points = self.build_rect_from_corners()
            self.ui.label_error.setText("")
            if mh.get_winding_order(points) != mh.WindingOrder.Clockwise:
                self.ui.label_error.setText("invalid windng order, check the order in which the points are specified")
                return []
            if mh.is_zero_size(points):
                self.ui.label_error.setText("points specify a rect with zero size")
                return []
            if not mh.start_point_is_ll(points):
                self.ui.label_error.setText("first point is not the upper left corner")
                return []
            if len(points) == 4:
                self.ui.checkbox_enable_continuous_focus.setEnabled(True)
                self.ui.checkbox_enable_continuous_focus.setChecked(True)
                self.focus_controller.set_focus_points(points)
        else:
            self.ui.checkbox_enable_continuous_focus.setEnabled(False)
            self.ui.checkbox_enable_continuous_focus.setChecked(False)
            self.ui.label_error.setText("")
            self.focus_controller.set_focus_points([])

    def build_rect_from_corners(self):
        corners_correct_order = [
            # we mix this up to match a cw order starting with lower left
            self.focus_corners[FocusCorners.LowerRight],
            self.focus_corners[FocusCorners.UpperRight],
            self.focus_corners[FocusCorners.UpperLeft],
            self.focus_corners[FocusCorners.LowerLeft]
        ]
        # create rectangle from corner points, we assume that they generally
        # represent a rectangle and just use the mean value for each side
        q11 = corners_correct_order[0]
        q12 = corners_correct_order[1]
        q22 = corners_correct_order[2]
        q21 = corners_correct_order[3]

        x1 = (q11[0] + q12[0]) / 2
        x2 = (q22[0] + q21[0]) / 2
        y1 = (q11[1] + q21[1]) / 2
        y2 = (q12[1] + q22[1]) / 2
        points = [
            [x1, y1, q11[2]],
            [x1, y2, q12[2]],
            [x2, y2, q22[2]],
            [x2, y1, q21[2]],
        ]
        return points

    def on_focus_btn_clicked(self, corner):
        point = [
            self.axis_controller.get_position(GridAxisNames.AXIS_X),
            self.axis_controller.get_position(GridAxisNames.AXIS_Y),
            self.axis_controller.get_position(GridAxisNames.AXIS_Z)
        ]
        self.label_lookup[corner].setText("Z: {:d} (X: {:d}, Y: {:d})".format(int(point[2]), int(point[0]), int(point[1])))
        self.focus_corners[corner] = point
        self.validate_corners()

    def on_clear_btn_clicked(self, corner):
        if corner in self.focus_corners:
            del self.focus_corners[corner]
        self.label_lookup[corner].setText("Empty")
        self.validate_corners()

    def on_clear_all_clicked(self):
        for corner in self.focus_corners:
            self.label_lookup[corner].setText("Empty")
        self.focus_corners = {}
        self.validate_corners()

    def enable_continuous_toggle(self, checked):
        if checked:
            rect = self.build_rect_from_corners()
            self.focus_controller.set_focus_points(rect)
        else:
            self.focus_controller.set_focus_points([])

    def setup_ui(self):
        self.widget = QWidget(self.parent)
        self.ui = Ui_Autofocus()
        self.ui.setupUi(self.widget)