'''
Created on May 9, 2019

@author: janmeyer
'''

from ..core import Object
from PyQt5.QtCore import QSize, QObject
from PyQt5.QtWidgets import QSizePolicy, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QWidget
from PyQt5.QtGui import QPixmap

class CameraStream(QObject, Object):
    
    def __init__(self, parent=None, size=(), device=None):
        QObject.__init__(self)
        Object.__init__(self)
        if device == None and "camera" in self.janus.devices:
            device = self.janus.devices["camera"]
        if len(size) < 2:
            width = device.width_max(refresh=True, alt=640)
            height = device.height_max(refresh=True, alt=480)
            self.size = QSize(width, height)
        else:
            self.size = QSize(size[0], size[1])
        self.device = device
        self.parent = parent
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.stream_item = QGraphicsPixmapItem()
        self.stream_item.setZValue(-1)
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0., 0., float(self.size.width()), float(self.size.height()))
        self.scene.addItem(self.stream_item)
        self.widget = QGraphicsView(self.parent)
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(self.size)
        self.widget.setBaseSize(self.size)
        self.widget.setObjectName("graphicsViewCameraStream")
        self.widget.setTransformationAnchor(0)
        self.widget.setScene(self.scene)
        self.widget.setInteractive(True)
        self.widget.setMouseTracking(True)

    def connect_signals(self):
        self.device.value_changed.connect(self.update_values)
    
    def update_values(self, attribute):
        if attribute == "image":
            frame = self.device.image()
            if frame is None:
                return
            pixmap = QPixmap.fromImage(frame)        
            self.stream_item.setPixmap(pixmap)
            self.widget.update()


class CameraControls(Object, QObject):

    def __init__(self, parent=None, device=None):
        Object.__init__(self)
        QObject.__init__(self)
        if device == None and "onaxis_camera" in self.janus.devices:
            device = self.janus.devices["onaxis_camera"]
        self.device = device
        self.parent = parent
        self.setup_ui()
        self.ui.spinBoxCameraExposureTime.setValue(device.exposure_time(alt=0))
        self.ui.spinBoxCameraExposureTime.setMinimum(device.exposure_time_min(alt=0))
        self.ui.spinBoxCameraExposureTime.setMaximum(device.exposure_time_max(alt=200000))
        self.ui.horizontalSliderCameraExposureTime.setValue(device.exposure_time(alt=0))
        self.ui.horizontalSliderCameraExposureTime.setMinimum(device.exposure_time_min(alt=0))
        self.ui.horizontalSliderCameraExposureTime.setMaximum(device.exposure_time_max(alt=200000))
        self.ui.checkBoxCameraExposureTimeAuto.setChecked(device.exposure_time_auto(alt=False))
        self.ui.spinBoxCameraGain.setValue(device.gain(alt=0))
        self.ui.spinBoxCameraGain.setMinimum(device.gain_min(alt=0))
        self.ui.spinBoxCameraGain.setMaximum(device.gain_max(alt=200000))
        self.ui.horizontalSliderCameraGain.setValue(device.gain(alt=0))
        self.ui.horizontalSliderCameraGain.setMinimum(device.gain_min(alt=0))
        self.ui.horizontalSliderCameraGain.setMaximum(device.gain_max(alt=200000))
        self.ui.checkBoxCameraGainAuto.setChecked(device.gain_auto(alt=False))
        self.register_persistents()
        self.connect_signals()

    def connect_signals(self):
        self.ui.spinBoxCameraExposureTime.valueChanged.connect(self.device.exposure_time)
        self.ui.horizontalSliderCameraExposureTime.valueChanged.connect(self.device.exposure_time)
        self.ui.checkBoxCameraExposureTimeAuto.stateChanged.connect(self.device.exposure_time_auto)
        self.ui.spinBoxCameraGain.valueChanged.connect(self.device.gain)
        self.ui.horizontalSliderCameraGain.valueChanged.connect(self.device.gain)
        self.ui.checkBoxCameraGainAuto.stateChanged.connect(self.device.gain_auto)
        self.device.value_changed.connect(self.update_values)

    def register_persistents(self):
        self.janus.utils["config"].add_persistent( \
                "camera", "gain", self.ui.spinBoxCameraGain.value,
                self.ui.spinBoxCameraGain.setValue, int)
        self.janus.utils["config"].add_persistent( \
                "camera", "gain_auto", self.ui.checkBoxCameraGainAuto.isChecked,
                self.ui.checkBoxCameraGainAuto.setChecked, bool)
        self.janus.utils["config"].add_persistent( \
                "camera", "exposure_time", self.ui.spinBoxCameraExposureTime.value,
                self.ui.spinBoxCameraExposureTime.setValue, int)
        self.janus.utils["config"].add_persistent( \
                "camera", "exposure_time_auto", self.ui.checkBoxCameraExposureTimeAuto.isChecked,
                self.ui.checkBoxCameraExposureTimeAuto.setChecked, bool)

    def update_values(self, attribute):
        if attribute == "exposure_time":
            self.ui.spinBoxCameraExposureTime.blockSignals(True)
            self.ui.horizontalSliderCameraExposureTime.blockSignals(True)
            self.ui.spinBoxCameraExposureTime.setValue(self.device.exposure_time())
            self.ui.horizontalSliderCameraExposureTime.setValue(self.device.exposure_time())
            self.ui.spinBoxCameraExposureTime.blockSignals(False)
            self.ui.horizontalSliderCameraExposureTime.blockSignals(False)
        elif attribute == "exposure_time_auto":
            self.ui.checkBoxCameraExposureTimeAuto.blockSignals(True)
            self.ui.checkBoxCameraExposureTimeAuto.setChecked(self.device.exposure_time_auto())
            self.ui.checkBoxCameraExposureTimeAuto.blockSignals(False)
        elif attribute == "gain":
            self.ui.spinBoxCameraGain.blockSignals(True)
            self.ui.horizontalSliderCameraGain.blockSignals(True)
            self.ui.spinBoxCameraGain.setValue(self.device.gain())
            self.ui.horizontalSliderCameraGain.setValue(self.device.gain())
            self.ui.spinBoxCameraGain.blockSignals(False)
            self.ui.horizontalSliderCameraGain.blockSignals(False)
        elif attribute == "gain_auto":
            self.ui.checkBoxCameraGainAuto.blockSignals(True)
            self.ui.checkBoxCameraGainAuto.setChecked(self.device.gain_auto())
            self.ui.checkBoxCameraGainAuto.blockSignals(False)

    def setup_ui(self):
        from janus.widgets.ui.camera_controls_ui import Ui_QWidgetCamera
        self.widget = QWidget(self.parent)
        self.ui = Ui_QWidgetCamera()
        self.ui.setupUi(self.widget)
