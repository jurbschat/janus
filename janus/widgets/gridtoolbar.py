from ..core import Object
from PyQt5.QtGui import *
from janus.widgets.ui.gridtoolbar_ui import Ui_GridToolbar
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from janus.widgets.gridwidget import GridWidgetAction
from janus.utils.eventhub import global_event_hub, Event as EHEvent, EventType as EHEventType
import sys

class GridToolBar(QObject, Object):

    def __init__(self, parent=None, gridWidget=None):
        QObject.__init__(self, parent)
        Object.__init__(self)
        self.parent = parent
        self.setup_ui()
        self.actionMapping = {}
        self.modifyGridActionGroup = None
        self.gridWidget = gridWidget
        self.setupToolbar()
        self.connect_signals()

    def setupToolbar(self):
        moveIcon = QIcon("icons:grid/move.png")
        placeChipIcon = QIcon("icons:grid/bychip.png")
        placeSizeIcon = QIcon("icons:grid/bysize.png")
        #placeFreeIcon = QIcon("icons:grid/free.png")
        poiMoveIcon = QIcon("icons:grid/poimove.png")
        screenshotIcon = QIcon("icons:grid/camera.png")
        beamprofileIcon = QIcon("icons:grid/beamprofile.png")
        clearGridIcon = QIcon("icons:grid/cross.png")
        setOriginIcon = QIcon("icons:grid/set_origin.png")

        self.toolBar = QToolBar("Grid Toolbar")

        self.modifyGridActionGroup = QActionGroup(self.toolBar)
        self.modifyGridActionGroup.setExclusive(True)
        self.modifyGridActionGroup.checkedAction()

        def create_action(icon, name, grid_widget_action, checkable = False, group = None):
            action = QAction(icon, name, self.toolBar)
            action.setCheckable(checkable)
            if group is not None:
                group.addAction(action)
            self.actionMapping[grid_widget_action] = action
            return action

        #
        # transform
        #
        transformAction = create_action(moveIcon, "Transform Grid", GridWidgetAction.TRANSFORM, True, self.modifyGridActionGroup)
        transformAction.triggered.connect(lambda: self.action_executed(GridWidgetAction.TRANSFORM))
        # this will not fire an event, the initial action for the grid has to be set manually in the grid widget
        transformAction.setChecked(True)
        self.toolBar.addAction(transformAction)
        self.transformAction = transformAction

        #
        # place grid
        #
        pm1 = create_action(placeChipIcon, "Place grid by orientation", GridWidgetAction.PLACE_BY_LINE, True, self.modifyGridActionGroup)
        pm1.triggered.connect(lambda: self.action_executed(GridWidgetAction.PLACE_BY_LINE))
        self.toolBar.addAction(pm1)

        pm2 = create_action(placeSizeIcon, "Place grid by extend", GridWidgetAction.PLACE_BY_THREE_POINT, True, self.modifyGridActionGroup)
        pm2.triggered.connect(lambda: self.action_executed(GridWidgetAction.PLACE_BY_THREE_POINT))
        self.toolBar.addAction(pm2)

        #pm3 = create_action(placeFreeIcon, "Manualy place grid", GridWidgetAction.PLACE_BY_FREE, True, self.modifyGridActionGroup)
        #pm3.triggered.connect(lambda: self.normal_action_executed(pm3))
        #self.toolBar.addAction(pm3)

        #
        # poi move
        #
        poiMoveAction = create_action(poiMoveIcon, "POI Move", GridWidgetAction.POI_MOVE, True)
        poiMoveAction.triggered.connect(lambda: self.action_executed(GridWidgetAction.POI_MOVE))
        self.toolBar.addAction(poiMoveAction)

        #
        # chip origin
        #
        setGridOriginAction = create_action(setOriginIcon, "Set chip origin", GridWidgetAction.SET_CHIP_ORIGIN, True)
        setGridOriginAction.triggered.connect(lambda: self.action_executed(GridWidgetAction.SET_CHIP_ORIGIN))
        self.toolBar.addAction(setGridOriginAction)

        #
        # clear
        #
        clearGridAction = create_action(clearGridIcon, "Clear Grid", GridWidgetAction.CLEAR_GRID)
        clearGridAction.triggered.connect(lambda: self.action_executed(GridWidgetAction.CLEAR_GRID))
        self.toolBar.addAction(clearGridAction)

        self.toolBar.addSeparator()

        #
        # beam profile
        #
        beamprofileAction = create_action(beamprofileIcon, 'Show Beamprofile', GridWidgetAction.SHOW_BEAMPROFILE, True)
        beamprofileAction.triggered.connect(lambda: self.action_executed(GridWidgetAction.SHOW_BEAMPROFILE))
        self.toolBar.addAction(beamprofileAction)

        #
        # screenshot
        #
        screenshotAction = create_action(screenshotIcon, 'Take Screenshot', GridWidgetAction.TAKE_SNAPSHOT)
        screenshotAction.triggered.connect(lambda: self.action_executed(GridWidgetAction.TAKE_SNAPSHOT))
        self.toolBar.addAction(screenshotAction)

        if self.ui.toolbarFrame.layout() is None:
            layout = QHBoxLayout(self.ui.toolbarFrame)
            layout.addWidget(self.toolBar)
            self.ui.toolbarFrame.setLayout(layout)
        else:
            self.ui.toolbarFrame.layout().addWidget(self.toolBar)

    def action_executed(self, grid_widget_action):
        print("action: {}".format(grid_widget_action))
        grid_action = self.actionMapping[grid_widget_action]
        checked = grid_action.isChecked()
        self.gridWidget.change_grid_state(grid_widget_action, checked)

    def external_toolbar_change(self, event):
        if event.data == GridWidgetAction.POI_MOVE:
            action = self.actionMapping[GridWidgetAction.POI_MOVE]
            isChecked = action.isChecked()
            action.setChecked(not isChecked)
        else:
            for name, action in self.actionMapping.items():
                if event.data == name:
                    action.setChecked(True)

    def connect_signals(self):
        global_event_hub().register(EHEventType.TOOLBAR_CHANGE_SELECTED, self.external_toolbar_change)

    def setup_ui(self):
        self.widget = QWidget(self.parent)
        self.ui = Ui_GridToolbar()
        self.ui.setupUi(self.widget)

    def get_toolbar_frame(self):
        return self.widget