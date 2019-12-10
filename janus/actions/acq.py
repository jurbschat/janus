"""
This is part of the janus package.
"""

__author__ = "Jan Meyer"
__email__ = "jan.meyer@desy.de"
__copyright__ = "(c)2019 DESY, FS-BMX, FS-Petra-D, P11"
__license__ = "GPL"


from ..core import Object

class AcqHandler(Object):
    
    def __init__(self, widget, start_button):
        Object.__init__(self)
        self.associations = {}
        self.widget = widget
        self.widget.currentChanged.connect(self.set_active)
        self.current = self.widget.currentIndex()
        start_button.clicked.connect(self.start)
        self.janus.application.init_done.connect(self.init_active)

    def init_active(self):
        self.current = self.widget.currentIndex()
        self.associations[self.current].set_active(True)

    def set_active(self, index):
        self.associations[self.current].set_active(False)
        self.associations[index].set_active(True)
        self.current = index

    def get_active(self):
        return self.associations[self.current]

    def start(self):
        self.associations[self.current].start()

    def associate(self, tab, action):
        index = self.widget.indexOf(tab)
        self.associations[index] = action
