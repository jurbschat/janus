"""
This is part of the janus package.
"""

__author__ = "Jan Meyer"
__email__ = "jan.meyer@desy.de"
__copyright__ = "(c)2019 DESY, FS-BMX, FS-Petra-D, P11"
__license__ = "GPL"


from time import time
import os
import numpy
import matplotlib, matplotlib.pyplot as pyplot
from PyQt5.QtCore import QObject, QThread, QMutex, pyqtSignal
from ..core import Object
from ..const import State, ChemicalElement
from ..widgets.plot import Plot

class AcqXrfSpectrum(QThread, Object):
 
    acq_started = pyqtSignal(object, name="acqStarted")
    acq_updated = pyqtSignal(name="acqUpdated")
    acq_stopped = pyqtSignal(name="acqStopped")
    value_changed = pyqtSignal(name="valueChanged")
    start_processing = pyqtSignal(name="startProcessing")

    title = "XRF Spectrum"
    used_devices = ["bs0", "bs1", "fs", "filter", "interlock", 
            "energy", "machine", "xspress3"]
    used_widgets = ["acqprogressdialog", "acqxrf", "acqrun", "plot",
            "elementtable"]
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
    info_txt = \
            "run type:            xrf spectrum\n" + \
            "run name:            {name:s}\n" + \
            "integration interval:{integration_interval:f}ms\n" + \
            "energy:              {energy:f}keV\n" + \
            "wavelength:          {wavelength:f}A\n" + \
            "filter transmission: {filter_transmission:f}%\n" + \
            "filter thickness:    {filter_thickness:d}um\n" + \
            "ring current:        {beam_current:f}mA\n"
    
    def __init__(self, devices={}, widgets={}, parent=None):
        QThread.__init__(self, parent)
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
        self.data = 4096 * [0.0]
        self.time_total = 0
        self.presenter = PresenterXrfScan(self)

    def set_active(self, flag):
        self.active = flag
        if self.active:
            self.janus.utils["logger"].info("AcqXrfSpectrum.set_active() " +
                    "set active")
            self.acq_started.connect(self.widgets.acqprogressdialog.show)
            self.acq_stopped.connect(self.widgets.acqprogressdialog.hide)
            self.acq_updated.connect(self.widgets.acqprogressdialog.update)
            self.widgets.acqprogressdialog.push_button.clicked.connect(
                    self.stop)
            self.janus.utils["path"].set_run_number_check(
                    "/beamline/beamtime/raw/user/sample/xrf_number/sample_number.csv")
            self.janus.utils["path"].inc_run_number()
            self.presenter.plot_data()
        else:
            self.janus.utils["logger"].info("AcqXrfSpectrum.set_active() " +
                    "set inactive")
            self.acq_started.disconnect(self.widgets.acqprogressdialog.show)
            self.acq_stopped.disconnect(self.widgets.acqprogressdialog.hide)
            self.acq_updated.disconnect(self.widgets.acqprogressdialog.update)
            self.widgets.acqprogressdialog.push_button.clicked.disconnect(
                    self.stop)
            self.widgets.elementtable.hide()

    def set_parameters(self):
        #sample_name
        self.janus.utils["path"].inc_run_number()
        self.parameters.sample_name = self.janus.utils["path"].get_filename()
        #path
        self.parameters.path = self.janus.utils["path"].get_path(
                "/beamline/beamtime/raw/user/sample/xrf_number/", force=True)
        #comment
        self.parameters.comment = \
                str(self.widgets.acqrun.ui.plainTextEditAcqComment.toPlainText())
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
            if (self.parameters.energy - 0.5 > self.devices.energy.energy() or
                    self.parameters.energy + 0.5 < self.devices.energy.energy()) \
                    and self.devices.energy.state(refresh=True) == State.ON:
                self.janus.utils["logger"].info("AcqXrfSpectrum.prepare() " +
                        "setting energy to " + 
                        str(self.parameters.energy) + " eV")
                self.devices.energy.energy(self.parameters.energy)
            if (self.parameters.energy - 0.5 > self.devices.energy.energy() or
                    self.parameters.energy + 0.5 < self.devices.energy.energy()) \
                    or self.devices.energy.state(refresh=True) != State.ON:
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
            self.acq_updated.emit()
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
        bin_count = int(self.parameters.energy / self.devices.xspress3.bin_width())
        self.data = self.devices.xspress3.channel1()[:bin_count]
        self.value_changed.emit()
        self.write_data()
        self.write_info()
        self.process_data()
        self.acq_updated.emit()
    
    def cleanup(self):
        self.janus.utils["logger"].debug("AcqXrfSpectrum.cleanup() " +
                "cleaning up")
        timeout = time() + self.prepare_timeout
        done = False
        #Fastshutter
        self.devices.fs.close()
        while time() < timeout and self.alive and not done:
            done = True
            #Energy
            if self.parameters.energy != self.parameters.orig_energy and \
                    self.devices.energy.state() == State.ON:
                self.janus.utils["logger"].info("AcqXrfSpectrum.cleanup() " +
                        "setting energy to " + 
                        str(self.parameters.orig_energy) + " eV")
                self.devices.energy.energy(self.parameters.orig_energy)
            if self.parameters.orig_energy - 0.5 > self.devices.energy.energy() or \
                    self.parameters.orig_energy + 0.5 < self.devices.energy.energy():
                done = False
            #Filters
            if done and self.devices.filter.state() == State.ON and \
                    self.parameters.transmission != self.parameters.orig_transmission:
                self.janus.utils["logger"].info("AcqXrfSpectrum.cleanup() " +
                        "setting transmission to " + 
                        str(self.parameters.orig_transmission) + "%")
                self.devices.filter.transmission(self.parameters.orig_transmission)
            if self.parameters.orig_transmission != self.devices.filter.transmission_set() and \
                    self.parameters.transmission != self.parameters.orig_transmission:
                done = False
            if not done:
                self.msleep(self.prepare_wait_interval)
        self.janus.utils["path"].inc_run_number()

    def write_data(self):
        filepath = self.parameters.path + self.parameters.sample_name + ".csv"
        bin_width = self.devices.xspress3.bin_width()
        output = "#energy[eV]\tevents\n"
        for i in range(len(self.data)):
            output += "{:d}\t{:d}\n".format(int(bin_width * i), self.data[i])
        try:
            f = open(filepath, "w")
            f.write(output)
            f.close()
        except:
            self.janus.utils["logger"].error(
                    "AcqXrfSpectrum().write_data() unable to write data file")
            self.janus.utils["logger"].debug("", exc_info=True)
        
    def write_info(self):
        filepath = self.parameters.path + "/info.txt"
        wavelength = 12398.4/(self.parameters.energy) #in Angstrom
        output = self.info_txt.format( \
            name = self.parameters.sample_name, \
            integration_interval = self.parameters.integration_interval * 1000, \
            energy = self.parameters.energy, \
            wavelength = wavelength, \
            filter_transmission = self.devices.filter.transmission(), \
            filter_thickness = 0, \
            beam_current = self.devices.machine.current()
        )
        try:
            f = open(filepath, "w")
            f.write(output)
            f.close()
        except:
            self.janus.utils["logger"].error(
                    "AcqXrfSpectrum().write_info() unable to write info file")
            self.janus.utils["logger"].debug("", exc_info=True)

    def process_data(self):
        self.start_processing.emit()

    def time_remaining(self):
        return 0.0


class EmissionLineSearchMap(Object):

    def __init__(self, excitation_energy, window_width=50, bin_width=10):
        self.map = [[] for index in range(int(excitation_energy / bin_width))]
        width = int(window_width / bin_width)
        lower = int(width / 2)
        upper = int(width / 2)
        if width % 2:
            upper += 1
        lines = ["k_alpha1", "k_alpha2", "k_beta1", "l_alpha1", "l_alpha2", 
                "l_beta1", "l_beta2", "l_gamma1"]
        for z in range(1, 119):
            element = ChemicalElement(z)
            for line in lines:
                if not line in element.__dict__:
                    continue
                center_bin = int(element.__dict__[line] / 10)
                for bin_nr in range(center_bin - lower, center_bin + upper):
                    if bin_nr >= 0 and bin_nr < len(self.map):
                        self.map[bin_nr].append(z)
    
    def get_element_list(self, lines):
        found = []
        for line in lines:
            for element in self.map[line]:
                found.append(element)
        weighted = {}
        for element in found:
            if element in weighted:
                weighted[element] += 1
            else:
                weighted[element] = 1
        result = []
        for element, matches in weighted.items():
            if len(result) == 0:
                result.append(element)
                continue
            i = 0
            while weighted[result[i]] > matches:
                i += 1
            result.insert(i, element)
        return result


class PresenterXrfScan(QObject, Object):

    def __init__(self, acq_thread):
        QObject.__init__(self, acq_thread)
        Object.__init__(self)
        self.acq_thread = acq_thread
        self.elements = []
        self.connect_signals()

    def connect_signals(self):
        self.acq_thread.start_processing.connect(self.process_data)
        self.acq_thread.widgets.elementtable.widget.itemSelectionChanged.connect( \
                self.plot_lines)

    def plot_data(self):
        data = self.acq_thread.data
        table = self.acq_thread.widgets.elementtable
        plot = self.acq_thread.widgets.plot
        plot.clear()
        plot.add_plot_data(0, data_type=Plot.TYPE_STATIC,
                data=self.acq_thread.devices.xspress3.bin_energies()[:len(data)])
        plot.add_plot_data(1, data_type=Plot.TYPE_STATIC,
                data=data)
        plot.add_plot_item(0, 0, 1)
        plot.tie_x_range(0)
        table.clear()
        if len(self.elements) > 0:
            for element in self.elements:
                self.acq_thread.widgets.elementtable.add_element_row(element)
            table.show()
        else:
            table.hide()

    def plot_lines(self):
        symbols = {"k_alpha1": "Kα1", "k_alpha2": "Kα2", "k_beta1": "Kβ1", 
                "l_alpha1": "Lα1", "l_alpha2": "Lα2", "l_beta1": "Lβ1", 
                "l_beta2": "Lβ2", "l_gamma1": "Lγ1"}
        elements = self.acq_thread.widgets.elementtable.get_selected_elements()
        max_energy = self.acq_thread.parameters.energy
        for line in list(self.acq_thread.widgets.plot.lines.keys()):
            self.acq_thread.widgets.plot.remove_line_item(line)
        i = 0
        for z in elements:
            element = ChemicalElement(z)
            for key in symbols:
                if key in element.__dict__:
                    energy = element.__dict__[key]
                    if energy < max_energy:
                        self.acq_thread.widgets.plot.add_line_item(i, 
                            label=element.symbol + "\n" + symbols[key],
                            pos=energy, labelOpts={"color": "000000"})
                        i += 1

    def process_data(self):
        search = EmissionLineSearchMap(self.acq_thread.parameters.energy,
                bin_width=self.acq_thread.devices.xspress3.bin_width())
        data = numpy.asarray(self.acq_thread.data)
        #running average with window width 3
        smoothed = numpy.convolve(data, numpy.ones(3), "valid") / 3 
        #find local maxima
        maxima = (numpy.diff(numpy.sign(numpy.diff(smoothed))) < 0).nonzero()[0] + 1
        #only take into account peaks higher than 1/2 std deviation
        filtered_maxima = list(maxima[(data[maxima] > (data.std() / 2))])
        #find elements to emission lines
        self.elements = search.get_element_list(filtered_maxima)
        self.plot_data()


class AcqXanesScan(QThread, Object):

    acq_started = pyqtSignal(object, name="acqStarted")
    acq_updated = pyqtSignal(name="acqUpdated")
    acq_stopped = pyqtSignal(name="acqStopped")
    start_processing = pyqtSignal(name="start_processing")
    value_changed = pyqtSignal(name="valueChanged")

    title = "XANES Scan"
    used_devices = ["bs0", "bs1", "fs", "filter", "interlock", 
            "energy", "machine", "xspress3"]
    used_widgets = ["acqprogressdialog", "acqxanes", "acqrun", "plot"]
    needed_parameters = ["sample_name", "run_number", "path", "comment", 
            "start_energy", "stop_energy", "orig_energy", "transmission",
            "orig_transmission", "velocity", "emission_energy", "bins"]
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
    info_txt = \
            "run type:            xanes scan\n" + \
            "run name:            {name:s}\n" + \
            "integration interval:{integration_interval:f}ms\n" + \
            "start energy:        {start_energy:f}keV\n" + \
            "start wavelength:    {start_wavelength:f}A\n" + \
            "stop energy:         {stop_energy:f}keV\n" + \
            "stop wavelength:     {stop_wavelength:f}A\n" + \
            "filter transmission: {filter_transmission:f}%\n" + \
            "filter thickness:    {filter_thickness:d}um\n" + \
            "ring current:        {beam_current:f}mA\n"
    
    def __init__(self, devices={}, widgets={}, parent=None):
        QThread.__init__(self, parent)
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
                self.janus.utils["logger"].error("AcqXanesScan.__init__() " +
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
                self.janus.utils["logger"].error("AcqXanesScan.__init__() " +
                        "missing widget " + str(key))
        self.parameters = lambda: self.parameters.__dict__
        for key in self.needed_parameters:
            self.parameters.__dict__[key] = None
        self.data = 4096 * [0.0]
        self.data_energies = self.devices.xspress3.bin_energies()
        self.time_total = 0
        self.mutex = QMutex()

    def set_active(self, flag):
        self.active = flag
        if self.active:
            self.janus.utils["logger"].info("AcqXanesScan.set_active() " +
                    "set active")
            self.acq_started.connect(self.widgets.acqprogressdialog.show)
            self.acq_stopped.connect(self.widgets.acqprogressdialog.hide)
            self.acq_updated.connect(self.widgets.acqprogressdialog.update)
            self.value_changed.connect(self.plot_data)
            self.widgets.acqprogressdialog.push_button.clicked.connect(
                    self.stop)
            self.janus.utils["path"].set_run_number_check(
                    "/beamline/beamtime/raw/user/sample/xanes_number/sample_number.csv")
            self.janus.utils["path"].inc_run_number()
            self.plot_data()
        else:
            self.janus.utils["logger"].info("AcqXanesScan.set_active() " +
                    "set inactive")
            self.acq_started.disconnect(self.widgets.acqprogressdialog.show)
            self.acq_stopped.disconnect(self.widgets.acqprogressdialog.hide)
            self.acq_updated.disconnect(self.widgets.acqprogressdialog.update)
            self.value_changed.disconnect(self.plot_data)
            self.widgets.acqprogressdialog.push_button.clicked.disconnect(
                    self.stop)

    def set_parameters(self):
        #sample_name
        self.janus.utils["path"].inc_run_number()
        self.parameters.sample_name = self.janus.utils["path"].get_filename()
        #path
        self.parameters.path = self.janus.utils["path"].get_path(
                "/beamline/beamtime/raw/user/sample/xanes_number/", force=True)
        #comment
        self.parameters.comment = \
                str(self.widgets.acqrun.ui.plainTextEditAcqComment.toPlainText())
        #energy
        self.parameters.start_energy = \
                int(self.widgets.acqxanes.ui.spinBoxAcqXanesEnergyStart.value())
        self.parameters.stop_energy = \
                int(self.widgets.acqxanes.ui.spinBoxAcqXanesEnergyStop.value())
        self.parameters.orig_energy = self.devices.energy.energy()
        #transmission
        if self.widgets.acqxanes.ui.checkBoxAcqXanesTransmission.isChecked():
            self.parameters.transmission = self.devices.filter.transmission() * 100
            self.parameters.orig_transmission = self.parameters.transmission
        else:
            self.parameters.transmission = \
                    float(self.widgets.acqxanes.ui.doubleSpinBoxAcqXanesTransmission.value())
            self.parameters.orig_transmission = self.devices.filter.transmission() * 100
        #integration_interval
        self.parameters.integration_interval = \
                float(self.widgets.acqxanes.ui.doubleSpinBoxAcqXanesInterval.value())
        #velocity - always 1eV/s
        self.parameters.velocity = \
                float(self.widgets.acqxanes.ui.doubleSpinBoxAcqXanesVelocity.value())
        self.time_counter = (self.parameters.stop_energy - \
                self.parameters.start_energy) / self.parameters.velocity
        self.time_total = self.time_counter
        #emission
        self.parameters.emission_energy = \
                int(self.widgets.acqxanes.ui.spinBoxAcqXanesEmissionEnergy.value())
        self.parameters.bins = [int(self.parameters.emission_energy / \
                self.devices.xspress3.bin_width())]
        if self.parameters.bins[0] > 0:
            self.parameters.bins.append(self.parameters.bins[0] - 1)
        if self.parameters.bins[0] < 4095:
            self.parameters.bins.append(self.parameters.bins[0] + 1)
            
    def start(self):
        self.set_parameters()
        self.janus.utils["logger"].info("AcqXanesScan.start() " +
                "data acquisition started")
        self.acq_started.emit(self)
        QThread.start(self)

    def stop(self):
        self.janus.utils["logger"].info("AcqXanesScan.stop() " +
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
        brake_released = False
        while time() < timeout and self.alive:
            #Interlock
            if not self.devices.interlock.value():
                self.conditions["InterlockSet"] = "False"
            else:
                self.conditions["InterlockSet"] = "True"
            #Fastshutter
            if self.devices.fs.value():
                self.conditions["FSclosed"] = "False"
                self.janus.utils["logger"].info("AcqXanesScan.prepare() " +
                        "closing FS")
                self.devices.fs.close()
            else:
                self.conditions["FSclosed"] = "True"
            #BS0
            if not self.devices.bs0.value():
                self.conditions["BS0open"] = "False"
                self.janus.utils["logger"].info("AcqXanesScan.prepare() " +
                        "opening BS0")
                self.devices.bs0.open()
            else:
                self.conditions["BS0open"] = "True"
            #BS1
            if not self.devices.bs1.value():
                self.conditions["BS1open"] = "False"
                self.janus.utils["logger"].info("AcqXanesScan.prepare() " +
                        "opening BS1")
                self.devices.bs1.open()
            else:
                self.conditions["BS1open"] = "True"
            #Energy
            if not brake_released:
                self.janus.utils["logger"].info("AcqXanesScan.prepare() " +
                        "setting energy to " + 
                        str(self.parameters.start_energy) + " eV")
                self.devices.energy.auto_brake(False)
                self.devices.energy.energy(self.parameters.start_energy)
                brake_released = True
            if not brake_released or self.devices.energy.state(refresh=True) != State.ON:
                self.conditions["EnergySet"] = "False"
            else:
                self.conditions["EnergySet"] = "True"
            #Filters
            if self.conditions["EnergySet"] == "True" and \
                    self.parameters.transmission != self.parameters.orig_transmission \
                    and self.parameters.transmission != self.devices.filter.transmission() \
                    and self.devices.filter.state() == State.ON:
                self.janus.utils["logger"].info("AcqXanesScan.prepare() " +
                        "setting transmission to " + 
                        str(self.parameters.transmission) + "%")
                self.devices.filter.transmission(self.parameters.transmission)
            if self.parameters.transmission != self.devices.filter.transmission_set() and \
                    self.parameters.transmission != self.parameters.orig_transmission:
                self.conditions["TransmissionSet"] = "False"
            else:
                self.conditions["TransmissionSet"] = "True"
            #check end conditions
            self.acq_updated.emit()
            conditions_met = True
            for key in self.conditions:
                conditions_met &= eval(self.conditions[key])
            if conditions_met:
                return False
            self.msleep(self.prepare_wait_interval)
        if self.alive and self.conditions["InterlockSet"] == "False":
            self.janus.utils["logger"].error("AcqXanesScan.prepare() " +
                    "interlock not set, timed out")
        elif self.alive:
            self.janus.utils["logger"].error("AcqXanesScan.prepare() " +
                    "timed out")
        else:
            self.janus.utils["logger"].info("AcqXanesScan.prepare() " +
                    "aborted")
        return True

    def execute(self):
        self.janus.utils["logger"].debug("AcqXanesScan.execute() " +
                "data acquisition running")
        frames = int(((self.parameters.stop_energy - self.parameters.start_energy) \
                / self.parameters.velocity) / self.parameters.integration_interval)
        self.devices.xspress3.file_name(self.parameters.sample_name)
        self.devices.xspress3.file_dir(self.parameters.path)
        self.devices.xspress3.exposure_time(self.parameters.integration_interval)
        self.devices.xspress3.trigger_mode(1)
        self.devices.xspress3.frames(frames)
        self.devices.fs.open()
        self.msleep(20)
        self.devices.energy.move(self.parameters.start_energy,
                self.parameters.stop_energy, self.parameters.velocity)
        self.devices.xspress3.start_acquisition()
        self.msleep(10)
        self.mutex.lock()
        self.data = []
        self.data_energies = []
        self.mutex.unlock()
        for frame in range(frames):
            if not self.alive:
                self.devices.energy.stop()
                return
            self.msleep(self.parameters.integration_interval * 1000)
            data = self.devices.xspress3.channel1()
            value = 0
            for i in self.parameters.bins:
                value += data[i]
            energy = self.parameters.start_energy + (self.parameters.velocity \
                    * self.parameters.integration_interval * frame)
            self.mutex.lock()
            self.data.append(value)
            self.data_energies.append(energy)
            self.mutex.unlock()
            self.time_counter -= self.parameters.integration_interval
            self.value_changed.emit()
            self.acq_updated.emit()
        self.devices.fs.close()
        while self.devices.energy.state() != State.ON and self.alive:
            self.msleep(self.prepare_wait_interval)
        self.write_data()
        self.write_info()
        self.value_changed.emit()
        self.process_data()
    
    def cleanup(self):
        self.janus.utils["logger"].debug("AcqXanesScan.cleanup() " +
                "cleaning up")
        timeout = time() + self.prepare_timeout
        done = False
        brake_engaged = False
        #Fastshutter
        self.devices.fs.close()
        while time() < timeout and self.alive and not done:
            done = True
            #Energy
            if self.devices.energy.state() == State.ON:
                self.janus.utils["logger"].info("AcqXanesScan.cleanup() " +
                        "setting energy to " + 
                        str(self.parameters.orig_energy) + " eV")
                self.devices.energy.energy(self.parameters.orig_energy)
            if self.parameters.orig_energy - 0.5 > self.devices.energy.energy() or \
                    self.parameters.orig_energy + 0.5 < self.devices.energy.energy():
                done = False
            if not brake_engaged and self.devices.energy.state() == State.ON:
                self.janus.utils["logger"].info("AcqXanesScan.cleanup() " +
                        "setting energy to " + 
                        str(self.parameters.orig_energy) + " eV")
                self.devices.energy.auto_brake(True)
                self.devices.energy.energy(self.parameters.orig_energy)
                brake_engaged = True
            if not brake_engaged or self.devices.energy.state(refresh=True) != State.ON:
                done = False
            #Filters
            if done and self.devices.filter.state() == State.ON and \
                    self.parameters.transmission != self.parameters.orig_transmission:
                self.janus.utils["logger"].info("AcqXanesScan.cleanup() " +
                        "setting transmission to " + 
                        str(self.parameters.orig_transmission) + "%")
                self.devices.filter.transmission(self.parameters.orig_transmission)
            if self.parameters.orig_transmission != self.devices.filter.transmission_set() and \
                    self.parameters.transmission != self.parameters.orig_transmission:
                done = False
            if not done:
                self.msleep(self.prepare_wait_interval)
        self.janus.utils["path"].inc_run_number()

    def plot_data(self):
        self.mutex.lock()
        self.widgets.plot.clear()
        self.widgets.plot.add_plot_data(0, data_type=Plot.TYPE_STATIC,
                data=self.data_energies)
        self.widgets.plot.add_plot_data(1, data_type=Plot.TYPE_STATIC,
                data=self.data)
        self.widgets.plot.add_plot_item(0, 0, 1)
        self.widgets.plot.tie_x_range(0)
        self.mutex.unlock()
 
    def write_data(self):
        filepath = self.parameters.path + self.parameters.sample_name + ".csv"
        output = "#energy[eV]\tevents\n"
        i = 0
        for energy in self.data_energies:
            output += "{:d}\t{:d}\n".format(int(energy), self.data[i])
            i += 1
        try:
            f = open(filepath, "w")
            f.write(output)
            f.close()
        except:
            self.janus.utils["logger"].error(
                    "AcqXanesScan().write_data() unable to write data file")
            self.janus.utils["logger"].debug("", exc_info=True)
        
    def write_info(self):
        filepath = self.parameters.path + "/info.txt"
        start_wavelength = 12398.4/(self.parameters.start_energy) #in Angstrom
        stop_wavelength = 12398.4/(self.parameters.stop_energy) #in Angstrom
        output = self.info_txt.format( \
            name = self.parameters.sample_name, \
            integration_interval = self.parameters.integration_interval * 1000, \
            start_energy = self.parameters.start_energy, \
            start_wavelength = start_wavelength, \
            stop_energy = self.parameters.stop_energy, \
            stop_wavelength = stop_wavelength, \
            filter_transmission = self.devices.filter.transmission(), \
            filter_thickness = 0, \
            beam_current = self.devices.machine.current()
        )
        try:
            f = open(filepath, "w")
            f.write(output)
            f.close()
        except:
            self.janus.utils["logger"].error(
                    "AcqXanesScan().write_info() unable to write info file")
            self.janus.utils["logger"].debug("", exc_info=True)

    def process_data(self):
        self.start_processing.emit()

    def time_remaining(self):
        return self.time_counter


class PresenterXanesScan(QObject, Object):

    def __init__(self, acq_thread):
        QObject.__init__(self, acq_thread)
        Object.__init__(self)
        self.acq_thread = acq_thread
        self.chooch_path = self.janus.utils["config"].get(
                "pathes", "chooch", "chooch")
        self.elements = []
        self.connect_signals()

    def connect_signals(self):
        self.acq_thread.start_processing.connect(self.process_data)
        self.acq_thread.value_changed.connect(self.plot_data)

    def plot_data(self):
        self.acq_thread.mutex.lock()
        plot = self.acq_thread.widgets.plot
        plot.clear()
        plot.add_plot_data(0, data_type=Plot.TYPE_STATIC,
                data=self.acq_thread.data_energies)
        plot.add_plot_data(1, data_type=Plot.TYPE_STATIC,
                data=self.acq_thread.data)
        plot.add_plot_item(0, 0, 1)
        plot.tie_x_range(0)
        self.acq_thread.mutex.unlock()

    def process_data(self):
        #start chooch
        element = self.acq_thread.widgets.acqxanes.ui.elementChooserAcqXanesElement.currentIndex()
        element_symbol = ChemicalElement(element).symbol
        sample_name = self.janus.utils["path"].get_filename()
        raw_path = self.janus.utils["path"].get_path(
                "/beamline/beamtime/raw/user/sample/xanes_number/")
        processed_path = self.janus.utils["path"].get_path(
                "/beamline/beamtime/processed/user/sample/xanes_number/",
                force=True)
        data_file = "{0}{1}.csv".format(raw_path, sample_name)
        plot_file = "{0}{1}.ps".format(processed_path, sample_name)
        out_file = "{0}{1}.efs".format(processed_path, sample_name)
        term_file = "{0}{1}.txt".format(processed_path, sample_name)
        cmd = "{0} -e {1} -o {2} -p {3} {4} &>{5}".format(self.chooch_path,
                element_symbol, out_file, plot_file, data_file, term_file)
        os.system(cmd)
        #read peak and inflection point
        try:
            f = open(term_file, "r")
            msg = f.read()
            f.close()
        except:
            self.janus.utils["logger"].error("PresenterXanesScan()" +
                    ".process_data() unable to read {0}".format(
                    term_file))
            self.janus.utils["logger"].debug("", exc_info=True)
            return
        pos = msg.find('Table of results')
        if pos == -1 or pos != len(msg) - 209:
            self.janus.utils["logger"].error("PresenterXanesScan()" +
                    ".process_data() unable to read chooch output")
            return
        else:
            peak_energy = float(msg[pos+103:pos+111])
            peak_amp_dprime = float(msg[pos+115:pos+120])
            peak_amp_prime = float(msg[pos+123:pos+128])
            infl_energy = float(msg[pos+141:pos+149])
            infl_amp_dprime = float(msg[pos+153:pos+158])
            infl_amp_prime = float(msg[pos+161:pos+166])
        #read normalized curve and derivative
        values_x2 = []
        values_y21 = []
        values_y22 = []
        try:
            f = open(out_file, "r")
            for line in f:
                values_x2.append(float(line[0:10]))
                values_y21.append(float(line[12:19]))
                values_y22.append(float(line[21:28]))
            f.close()
        except:
            self.janus.utils["logger"].error("PresenterXanesScan()" +
                    ".process_data() unable to read {0}".format(
                    out_file))
            self.janus.utils["logger"].debug("", exc_info=True)
            return
        #save combined plot
        plot_file = "{0}{1}.svg".format(processed_path, sample_name)
        colors = matplotlib.rcParams['axes.prop_cycle'].by_key()['color']
        fig, ax = pyplot.subplots()
        ax2 = ax.twinx()
        line1 = ax.plot(self.acq_thread.data_energies, self.acq_thread.data,
                label="raw", color=colors[0])
        line2 = ax2.plot(values_x2, values_y21, label="f''", color=colors[1])
        line3 = ax2.plot(values_x2, values_y22, label="f'", color=colors[2])
        lower2, upper2 = ax2.get_ylim()
        lower, upper = ax.get_ylim()
        lower = (upper / upper2) * lower2
        ax.set_ylim(lower, upper)
        lines = line1+line2+line3
        labs = [l.get_label() for l in lines]
        ax.legend(lines, labs, loc='upper left')
        try:
            pyplot.savefig(plot_file, format="svg", transparent=True)
        except:
            self.janus.utils["logger"].error("PresenterXanesScan()" +
                    ".process_data() unable to save {0}.svg".format(
                    sample_name))
            self.janus.utils["logger"].debug("", exc_info=True)
            return

            
            