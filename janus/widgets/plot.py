"""
This is part of the janus package.
"""

__author__ = "Jan Meyer"
__email__ = "jan.meyer@desy.de"
__copyright__ = "(c)2019 DESY, FS-PE, P11"
__license__ = "GPL"


import time
import numpy
from PyQt5.QtCore import QTimer, QObject, Qt
from PyQt5.QtGui import QPen, QBrush, QColor
from pyqtgraph import PlotWidget, PlotDataItem
from ..core import Object


class Plot(QObject, Object):
    """Generic widget to plot data series. The data series have to be added
    first, then one may add plot items using two them as x and y values. The
    series will be automatically updated when the master attribute fires a
    value_changed signal or based on an internal update timer. This master
    series has to be defined while adding it.
    
    .. todo:: Currently only setting both series of a plot item to the same,
        fixed length works. Find a better handling for this.
    """
    TYPE_STATIC = 0
    TYPE_TIME = 1
    TYPE_SCALAR = 2
    TYPE_SPECTRUM = 3

    ROLE_SLAVE = 0
    ROLE_MASTER = 1

    def __init__(self, parent=None):
        """Construct a new Plot instance.
        
        :param parent: Optional, but needed for painting.
        :type parent: QGraphicsItem
        """
        QObject.__init__(self)
        Object.__init__(self)
        self.parent = parent
        self.items = {} #plot items
        self.data = {} #data series to the plot items
        self.master = None #id of the data series which triggers the update
        self.x_range = -1 #id of the data series which range defines the plot range
        self.update_timer = QTimer(self)
        self.update_timer_start = None
        self.setup_ui()

    def setup_ui(self):
        """Setup the internal widget object. Called by :func:`__init__()`."""
        self.widget = PlotWidget(self.parent)
        self.widget.setBackgroundBrush(QBrush(Qt.NoBrush))
        count = len(self.janus.widgets["mainwindow"].findChildren(PlotWidget))
        self.widget.setObjectName("plotWidgetPlot{0}".format(count))
        self.widget.getAxis("bottom").setPen(QPen(Qt.black))
        self.widget.getAxis("left").setPen(QPen(Qt.black))

    def update_values(self, attribute=None):
        """Update all data of TYPE_TIME, TYPE_SCALAR, TYPE_SPECTRUM and plot it.

        This method is connected to either the the value_changed signal of the
        device instance that the master attribute belongs to or the internal
        update_timer if the master is of TYPE_TIME. 

        :param attribute: Name of the master attribute
            which triggered the update or None if master is of TYPE_TIME.
        :type attribute: str|None
        """
        if not ((attribute is None and \
                self.data[self.master]["data_type"] == Plot.TYPE_TIME) or \
                (attribute == self.data[self.master]["name"] and \
                self.data[self.master]["data_type"] in \
                [Plot.TYPE_SCALAR, Plot.TYPE_SPECTRUM])):
            return
        if self.update_timer_start is not None:
            time_stamp = time.time() - self.update_timer_start
        update = len(self.items) * [False]
        #retrieve new data and cycle the buffer if max_length is reached
        for i in range(len(self.data)):
            if self.data[i]["data_type"] == Plot.TYPE_TIME:
                if self.data[i]["data"].shape[0] > self.data[i]["max_length"]:
                    self.data[i]["data"].resize(self.data[i]["max_length"])
                if self.data[i]["data"].shape[0] == self.data[i]["max_length"]:
                    self.data[i]["data"] = numpy.concatenate( \
                            (self.data[i]["data"][1:], self.data[i]["data"][:1]))
                    self.data[i]["data"][-1] = time_stamp
                else:
                    numpy.concatenate(self.data[i]["data"], time_stamp)
            elif self.data[i]["data_type"] == Plot.TYPE_SCALAR:
                if self.data[i]["data"].shape[0] > self.data[i]["max_length"]:
                    self.data[i]["data"].resize(self.data[i]["max_length"])
                if self.data[i]["data"].shape[0] == self.data[i]["max_length"]:
                    self.data[i]["data"] = numpy.concatenate( \
                            (self.data[i]["data"][1:], self.data[i]["data"][:1]))
                    self.data[i]["data"][-1] = self.data[i]["getter"](refresh=True)
                else:
                    numpy.concatenate(self.data[i]["data"], \
                            self.data[i]["getter"](refresh=True))
            elif self.data[i]["data_type"] == Plot.TYPE_SPECTRUM:
                self.data[i]["data"] = numpy.ndarray(self.data[i]["getter"](refresh=True))
                if self.data[i]["data"].shape[0] >= self.data[i]["max_length"] or \
                        self.data[i]["data"].shape[0] < self.data[i]["min_length"]:
                    self.data[i]["data"].resize(self.data[i]["max_length"])
            else:
                continue
            for item in self.data[i]["items"]:
                update[item] = True
        #set view boundaries if tie_x_range is set to a dataset
        if self.x_range > -1:
            if self.data[self.x_range]["data_type"] == Plot.TYPE_TIME:
                self.widget.setLimits( \
                        xMin=self.data[self.x_range]["data"][1], \
                        xMax=self.data[self.x_range]["data"][-1])
            else:
                self.widget.setLimits( \
                        xMin=numpy.amin(self.data[self.x_range]["data"]), \
                        xMax=numpy.amax(self.data[self.x_range]["data"]))
        #replot items
        for i in range(len(self.items)):
            if update[i]:
                self.items[i]["plot"].setData( \
                        self.data[self.items[i]["x"]]["data"], \
                        self.data[self.items[i]["y"]]["data"])

    def add_plot_data(self, i, data=None, attr=None, data_type=TYPE_STATIC, \
                role=ROLE_SLAVE, interval=1.0, \
                min_length=0, length=-1, max_length=-1):
        """Add a data series to the plot.
        
        :param i: Id of the data series. Should be ascending natural numbers 
            from 0 up.
        :type i: int
        :param data: Initial series of values. May be omited if not of
            TYPE_STATIC.
        :type data: numpy.ndarray|None
        :param attr: Reference to the getter function for an attribute of an
            device object. May be omited if not of TYPE_SCALAR or TYPE_SPECTRUM.
        :type attr: Device.method
        :param data_type: How the data is updated. May be one of the following 
            - TYPE_STATIC no update,
            - TYPE_TIME append time stamp at trigger point,
            - TYPE_SCALAR append attribute value at trigger point,
            - or TYPE_SPECTRUM exchange data series by attribute values at
                trigger point.
        :type data_type: int|TYPE_STATIC|TYPE_TIME|TYPE_SCALAR|TYPE_SPECTRUM
        :param role: Should be ROLE_MASTER for data series which triggers the
            plot update.
        :type role: int|ROLE_SLAVE|ROLE_MASTER
        :param interval: Interval, to which the update_timer is set if of
            TYPE_TIME and ROLE_MASTER. May be omited otherwise.
        :type interval: float
        :param min_length: Data series will be extended to this length. May be
            omited.
        :type min_length: int
        :param length: Sets min_length and max_length to this value. -1 will
            will disable this feature. May be omited.
        :type length: int
        :param max_length: Data series will be shortened to this length. -1 will
            will disable this feature. May be omited.
        :type max_length: int
        :return: False on errors, True otherwise.
        :rtype: bool
        """
        if length > -1:
            min_length = length
            max_length = length
        if data is not None and data.shape[0] < min_length:
            data.resize(min_length)
        if data is not None and data.shape[0] > max_length:
            data.resize(max_length)
        datum = { \
                "data": data, \
                "data_type": data_type, \
                "min_length": min_length, \
                "length": length, \
                "max_length": max_length, \
                "items" : []}
        if data_type in [Plot.TYPE_SCALAR, Plot.TYPE_SPECTRUM]:
            try:
                if callable(attr):
                    device = attr.__self__
                    name = attr.__name__
                else:
                    return False
            except:
                return False
            datum["device"] = device #device instance
            datum["name"] = name #attribute name
            datum["getter"] = attr #attribute getter method
            if data is None and data_type == Plot.TYPE_SCALAR:
                start_value = attr(refresh=True)
                datum["data"] = numpy.full(min_length, start_value)
            elif data is None:
                datum["data"] = attr(refresh=True)
                if datum["data"].shape[0] < min_length:
                    datum["data"].resize(min_length)
                if datum["data"].shape[0] > max_length:
                    datum["data"].resize(max_length)
        elif data_type == Plot.TYPE_TIME:
            datum["interval"] = interval
            if data is None:
                datum["data"] = numpy.linspace( \
                        -(min_length-1)*interval, 0, min_length)
        elif data_type != Plot.TYPE_STATIC:
            return False
        self.data[i] = datum
        if role == Plot.ROLE_MASTER:
            self.set_master(i)
        return True

    def add_plot_item(self, i, x, y, colour=Qt.red):
        """Add a plot item representing two already added data series.
        
        :param i: Id of the plot item. Should be ascending natural numbers 
            from 0 up.
        :type i: int
        :param x: Id of the data series holding the x values.
        :type x: int
        :param y: Id of the data series holding the y values.
        :type y: int
        :param colour: Colour of the plot item. The default is red.
        :type colour: str|QRgb|QColor|Qt.GlobalColor
        """
        self.items[i] = {"x": x, "y": y}
        self.data[x]["items"].append(i)
        self.data[y]["items"].append(i)
        self.items[i]["plot"] = PlotDataItem( \
                self.data[x]["data"], \
                self.data[y]["data"], \
                pen=QColor(colour))
        self.widget.addItem(self.items[i]["plot"])

    def set_master(self, i):
        """Set which data series will trigger a plot update.
        
        :param data: Id of the data series which triggers the update.
        :type data: int
        """
        if self.master is not None and self.master != i:
            if self.data[self.master]["data_type"] in \
                    [Plot.TYPE_SCALAR, Plot.TYPE_SPECTRUM]:
                self.data[self.master]["device"].value_changed.disconnect( \
                        self.update_values)
            elif self.data[self.master]["data_type"] == Plot.TYPE_TIME:
                self.update_timer.timeout.disconnect(self.update_values)
                self.update_timer.stop()
            self.data[i]["device"].value_changed.disconnect(self.update_values)
        if self.data[i]["data_type"] in [Plot.TYPE_SCALAR, Plot.TYPE_SPECTRUM]:
            self.data[i]["device"].value_changed.connect(self.update_values)
        elif self.data[i]["data_type"] == Plot.TYPE_TIME:
            self.update_timer.timeout.connect(self.update_values)
            self.update_timer_start = time.time()
            self.update_timer.start(self.data[i]["interval"] * 1000.)
        self.master = i

    def tie_x_range(self, data=-1):
        """Sets the plot x range to be the same as the given data series.
        
        :param data: Id of the data series holding the x values.
        :type data: int
        """
        self.x_range = data
