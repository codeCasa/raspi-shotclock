import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal
from dal.db_manager import DatabaseManager
from dal.drill_results_repository import DrillResultsRepository
from models.drill_model import DrillModel, DrillModelList
from main_menu_actions.calibration_dialog import CalibrationDialog
from view_model.timer_screen_view_model import TimerScreenViewModel
from view_model.view_history_screen_view_model import ViewHistoryScreenViewModel
from view_model.view_analytics_screen_view_model import ViewAnalyticsScreenViewModel


class ShotTimerApp:
    def __init__(self):
        # Initialize database manager
        self.db_manager = DatabaseManager()
        self.drills_model = None

    def start(self):
        # Load drills using the static method from DrillModel
        json_file = os.path.join(os.path.dirname(__file__), 'drills.json')
        drills = DrillModel.load_drills(json_file)

        # Create DrillModelList
        self.drills_model = DrillModelList(drills)

        # Connect to the database
        self.db_manager.connect()

        # Initialize the Qt application
        app = QApplication(sys.argv)
        engine = QQmlApplicationEngine()
        self.calibrate_dialog = CalibrationDialog(engine)
        self.view_model = ShotTimerAppViewModel()
        drillResultsRepo = DrillResultsRepository(self.db_manager)
        self.timer_screen_view_model = TimerScreenViewModel(drills, drillResultsRepo)
        self.view_history_screen_view_model = ViewHistoryScreenViewModel(drills, drillResultsRepo)
        self.view_analytics_screen_view_model = ViewAnalyticsScreenViewModel(drills, drillResultsRepo)

        # Expose the drills model to QML
        context = engine.rootContext()
        context.setContextProperty("drillsModel", self.drills_model)
        context.setContextProperty("calibrator", self.calibrate_dialog)
        context.setContextProperty("vm", self.view_model)
        context.setContextProperty("timerScreenViewModel", self.timer_screen_view_model)
        context.setContextProperty("viewHistoryScreenViewModel", self.view_history_screen_view_model)
        context.setContextProperty("viewAnalyticsScreenViewModel", self.view_analytics_screen_view_model)

        # Load the QML file from the views directory
        qml_file = os.path.join(os.path.dirname(__file__), 'views', 'main.qml')
        engine.load(qml_file)

        if not engine.rootObjects():
            sys.exit(-1)

        # Execute the application
        sys.exit(app.exec())

    def close(self):
        # Close the database connection
        self.db_manager.close()

class ShotTimerAppViewModel(QObject):
    selectedIndexChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selectedIndex = -1

    @pyqtProperty(int, notify=selectedIndexChanged)
    def selectedIndex(self):
        return self._selectedIndex

    @selectedIndex.setter
    def selectedIndex(self, value):
        if self._selectedIndex != value:
            self._selectedIndex = value
            self.selectedIndexChanged.emit(value)
