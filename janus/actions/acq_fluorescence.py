"""
This is part of the janus package.
"""

__author__ = "Jan Meyer"
__email__ = "jan.meyer@desy.de"
__copyright__ = "(c)2019 DESY, FS-BMX, FS-Petra-D, P11"
__license__ = "GPL"


from time import time
from PyQt5.QtCore import QThread, pyqtSignal
from ..core import Object
from ..const import State

class AcqXrfSpectrum(QThread, Object):
 
    acq_started = pyqtSignal(object, name="acqStarted")
    acq_stopped = pyqtSignal(name="acqStopped")
    value_changed = pyqtSignal(name="valueChanged")

    title = "XRF Spectrum"
    used_devices = ["bs0", "bs1", "fs", "filter", "interlock", 
            "energy", "xspress3"]
    used_widgets = ["acqprogressdialog", "acqxrf", "acqrun"]
    needed_parameters = ["sample_name", "run_number", "path", "comment", 
            "energy", "orig_energy", "transmission", "orig_transmission", 
            "integration_interval", "roi_min", "roi_max"]
    conditions = {
            "InterlockSet": "False",
            "BS0open": "False",
            "BS1open": "False",
            "FSclosed": "False",
            "EnergySet": "False",
            "TransmissionSet": "False"}
    progress_details = {}
    prepare_timeout = 20.0 #s
    prepare_wait_interval = 200 #ms
    
    def __init__(self, devices={}, widgets={}):
        QThread.__init__(self)
        Object.__init__(self)
        self.alive = False
        if type(devices) is not dict:
            devices = {}
        self.devices = lambda: self.devices.__dict__
        for key in self.used_devices:
            if key in devices:
                self.devices.__dict__[key] = devices[key]
            elif key in self.janus.devices:
                self.devices.__dict__[key] = self.janus.devices[key]
            else:
                self.janus.utils["logger"].error("AcqXrfSpectrum.__init__() " +
                        "missing device " + str(key))
        if type(widgets) is not dict:
            widgets = {}
        self.widgets = lambda: self.widgets.__dict__
        for key in self.used_widgets:
            if key in widgets:
                self.widgets.__dict__[key] = widgets[key]
            elif key in self.janus.widgets:
                self.widgets.__dict__[key] = self.janus.widgets[key]
            else:
                self.janus.utils["logger"].error("AcqXrfSpectrum.__init__() " +
                        "missing widget " + str(key))
        self.parameters = lambda: self.parameters.__dict__
        for key in self.needed_parameters:
            self.parameters.__dict__[key] = None

    def set_active(self, flag):
        self.active = flag
        if flag:
            self.janus.utils["logger"].info("AcqXrfSpectrum.set_active() " +
                    "set active")
            self.acq_started.connect(self.widgets.acqprogressdialog.show)
            self.acq_stopped.connect(self.widgets.acqprogressdialog.hide)
            self.value_changed.connect(self.widgets.acqprogressdialog.update)
            self.widgets.acqprogressdialog.push_button.clicked.connect(
                self.stop)
        else:
            self.janus.utils["logger"].info("AcqXrfSpectrum.set_active() " +
                    "set inactive")
            self.acq_started.disconnect(self.widgets.acqprogressdialog.show)
            self.acq_stopped.disconnect(self.widgets.acqprogressdialog.hide)
            self.value_changed.disconnect(self.widgets.acqprogressdialog.update)
            self.widgets.acqprogressdialog.push_button.clicked.disconnect(
                self.stop)

    def set_parameters(self):
        #sample_name
        self.parameters.sample_name = \
                str(self.widgets.acqrun.ui.lineEditAcqSampleName.text())
        #path
        self.parameters.path = "/gpfs/commissioning/raw/" + self.parameters.sample_name
        #comment
        self.parameters.comment = \
                str(self.widgets.acqrun.ui.plainTextEditAcqComment.document().toPlainText())
        #energy
        if self.widgets.acqxrf.ui.checkBoxAcqXrfEnergy.isChecked():
            self.parameters.energy = self.devices.energy.energy()
            self.parameters.orig_energy = self.parameters.energy
        else:
            self.parameters.energy = \
                    int(self.widgets.acqxrf.ui.spinBoxAcqXrfEnergy.value())
            self.parameters.orig_energy = self.devices.energy.energy()
        #transmission
        if self.widgets.acqxrf.ui.checkBoxAcqXrfTransmission.isChecked():
            self.parameters.transmission = self.devices.filter.transmission() * 100
            self.parameters.orig_transmission = self.parameters.transmission
        else:
            self.parameters.transmission = \
                    float(self.widgets.acqxrf.ui.doubleSpinBoxAcqXrfTransmissiom.value())
            self.parameters.orig_transmission = self.devices.filter.transmission() * 100
        #integration_interval
        self.parameters.integration_interval = \
                float(self.widgets.acqxrf.ui.doubleSpinBoxAcqXrfInterval.value())
            
    def start(self):
        self.set_parameters()
        self.janus.utils["logger"].info("AcqXrfSpectrum.start() " +
                "data acquisition started")
        self.acq_started.emit(self)
        QThread.start(self)

    def stop(self):
        self.janus.utils["logger"].info("AcqXrfSpectrum.stop() " +
                "data acquisition stopped")
        self.alive = False
        self.wait()

    def run(self):
        self.alive = True
        if not self.prepare():
            self.execute()
            self.cleanup()
        self.alive = False
        self.acq_stopped.emit()

    def prepare(self):
        timeout = time() + self.prepare_timeout
        while time() < timeout and self.alive:
            #Interlock
            if not self.devices.interlock.value():
                self.conditions["InterlockSet"] = "False"
            else:
                self.conditions["InterlockSet"] = "True"
            #Fastshutter
            if self.devices.fs.value():
                self.conditions["FSclosed"] = "False"
                self.janus.utils["logger"].info("AcqXrfSpectrum.prepare() " +
                        "closing FS")
                self.devices.fs.close()
            else:
                self.conditions["FSclosed"] = "True"
            #BS0
            if not self.devices.bs0.value():
                self.conditions["BS0open"] = "False"
                self.janus.utils["logger"].info("AcqXrfSpectrum.prepare() " +
                        "opening BS0")
                self.devices.bs0.open()
            else:
                self.conditions["BS0open"] = "True"
            #BS1
            if not self.devices.bs1.value():
                self.conditions["BS1open"] = "False"
                self.janus.utils["logger"].info("AcqXrfSpectrum.prepare() " +
                        "opening BS1")
                self.devices.bs1.open()
            else:
                self.conditions["BS1open"] = "True"
            #Energy
            if not (self.parameters.energy - 2.5 < self.devices.energy.energy() and
                    self.parameters.energy + 2.5 > self.devices.energy.energy()) \
                    and self.devices.energy.state() == State.ON:
                self.janus.utils["logger"].info("AcqXrfSpectrum.prepare() " +
                        "setting energy to " + 
                        str(self.parameters.energy) + " eV")
                self.devices.energy.energy(self.parameters.energy)
            if not (self.parameters.energy - 2.5 < self.devices.energy.energy() and
                    self.parameters.energy + 2.5 > self.devices.energy.energy()):
                self.conditions["EnergySet"] = "False"
            else:
                self.conditions["EnergySet"] = "True"
            #Filters
            if self.conditions["EnergySet"] == "True" and \
                    self.parameters.transmission != self.parameters.orig_transmission \
                    and self.parameters.transmission != self.devices.filter.transmission() \
                    and self.devices.filter.state() == State.ON:
                self.janus.utils["logger"].info("AcqXrfSpectrum.prepare() " +
                        "setting transmission to " + 
                        str(self.parameters.transmission) + "%")
                self.devices.filter.transmission(self.parameters.transmission)
            if self.parameters.transmission != self.devices.filter.transmission_set() and \
                    self.parameters.transmission != self.parameters.orig_transmission:
                self.conditions["TransmissionSet"] = "False"
            else:
                self.conditions["TransmissionSet"] = "True"
            #check end conditions
            self.value_changed.emit()
            conditions_met = True
            for key in self.conditions:
                conditions_met &= eval(self.conditions[key])
            if conditions_met:
                return False
            self.msleep(self.prepare_wait_interval)
        if self.alive and self.conditions["InterlockSet"] == "False":
            self.janus.utils["logger"].error("AcqXrfSpectrum.prepare() " +
                    "interlock not set, timed out")
        elif self.alive:
            self.janus.utils["logger"].error("AcqXrfSpectrum.prepare() " +
                    "timed out")
        else:
            self.janus.utils["logger"].info("AcqXrfSpectrum.prepare() " +
                    "aborted")
        return True

    def execute(self):
        self.janus.utils["logger"].debug("AcqXrfSpectrum.execute() " +
                "data acquisition running")
        self.devices.xspress3.file_name(self.parameters.sample_name)
        self.devices.xspress3.file_dir(self.parameters.path)
        self.devices.xspress3.exposure_time(self.parameters.integration_interval)
        self.devices.xspress3.trigger_mode(1)
        self.devices.xspress3.frames(1)
        self.devices.fs.open()
        self.msleep(50)
        self.devices.xspress3.start_acquisition()
        self.msleep(self.parameters.integration_interval / 1000 + 10)
        self.devices.fs.close()
        self.write_info()
        self.process_data()
    
    def cleanup(self):
        self.janus.utils["logger"].debug("AcqXrfSpectrum.cleanup() " +
                "cleaning up")
        timeout = time() + self.prepare_timeout
        done = False
        while time() < timeout and self.alive and not done:
            done = True
            #Energy
            if self.parameters.energy != self.parameters.orig_energy and \
                    self.devices.energy.state() == State.ON:
                self.janus.utils["logger"].info("AcqXrfSpectrum.cleanup() " +
                        "setting energy to " + 
                        str(self.parameters.orig_energy) + " eV")
                self.devices.energy.energy(self.parameters.orig_energy)
            if not (self.parameters.orig_energy - 2.5 < self.devices.energy.energy() and
                    self.parameters.orig_energy + 2.5 > self.devices.energy.energy()):
                done = False
            #Filters
            if done and self.devices.filter.state() == State.ON and \
                    self.parameters.transmission != self.parameters.orig_transmission:
                self.janus.utils["logger"].info("AcqXrfSpectrum.cleanup() " +
                        "setting transmission to " + 
                        str(self.parameters.orig_transmission) + "%")
                self.devices.filter.transmission(self.parameters.orig_transmission)
            if self.parameters.orig_transmission != self.devices.filter.transmission() and \
                    self.parameters.transmission != self.parameters.orig_transmission:
                done = False

    def write_info(self):
        pass
    def process_data(self):
        pass
    def remaining_time(self):
        return 0.0

class AcqXanesScan(Object):

    def set_active(self, flag):
        self.active = flag
        if flag:
            print("xanes set active")
        else:
            print("xanes set inactive")

    def start(self):
        print("xanes acq started")

    def stop(self):
        pass
    def prepare(self):
        pass
    def execute(self):
        pass
    def cleanup(self):
        pass
