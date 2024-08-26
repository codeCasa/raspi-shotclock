from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, QAbstractListModel, QModelIndex, Qt, pyqtSlot
from enum import IntEnum, auto
from utils.time_utils import milliseconds_to_datetime



class DrillResultsRoles(IntEnum):
    DRILL_NAME = auto()
    START_TIME = auto()
    END_TIME = auto()
    ELAPSED_TIME = auto()
    SHOTS_FIRED = auto()
    SPLITS = auto()
    AVERAGE_SPLIT_TIME = auto()
    FASTEST_SPLIT_TIME = auto()
    SLOWEST_SPLIT_TIME = auto()
    SCORE = auto()
    NOTES = auto()

_role_names = {
    DrillResultsRoles.DRILL_NAME: b'drill_name',
    DrillResultsRoles.START_TIME: b'start_time',
    DrillResultsRoles.END_TIME: b'end_time',
    DrillResultsRoles.ELAPSED_TIME: b'elapsed_time',
    DrillResultsRoles.SHOTS_FIRED: b'shots_fired',
    DrillResultsRoles.SPLITS: b'splits',
    DrillResultsRoles.AVERAGE_SPLIT_TIME: b'average_split_time',
    DrillResultsRoles.FASTEST_SPLIT_TIME: b'fastest_split_time',
    DrillResultsRoles.SLOWEST_SPLIT_TIME: b'slowest_split_time',
    DrillResultsRoles.SCORE: b'score',
    DrillResultsRoles.NOTES: b'notes',
}

class DrillResultsModel(QAbstractListModel):
    def __init__(self, results: list = [], parent=None):
        super().__init__(parent)
        self._results = results
        self._data = []
        self.formatDataToFitRoles()

    def rowCount(self, parent=QModelIndex()):
        return len(self._results)

    def formatDataToFitRoles(self):
        for result in self._results:
            self._data.append({
                DrillResultsRoles.DRILL_NAME: result.drill_name,
                DrillResultsRoles.START_TIME: milliseconds_to_datetime(result.start_time),
                DrillResultsRoles.END_TIME: milliseconds_to_datetime(result.end_time),
                DrillResultsRoles.ELAPSED_TIME: round(result.elapsed_time / 1000, 2),
                DrillResultsRoles.SHOTS_FIRED: result.shots_fired,
                DrillResultsRoles.SPLITS: result.splits,
                DrillResultsRoles.AVERAGE_SPLIT_TIME: round(result.average_split_time / 1000, 1),
                DrillResultsRoles.FASTEST_SPLIT_TIME: round(result.fastest_split_time / 1000,1),
                DrillResultsRoles.SLOWEST_SPLIT_TIME: round(result.slowest_split_time/1000, 1),
                DrillResultsRoles.SCORE: result.score,
                DrillResultsRoles.NOTES: result.notes
            })

    def roleNames(self):
        return _role_names

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role not in list(DrillResultsRoles):
            return None

        try:
            result = self._data[index.row()]
        except IndexError:
            return None

        if role in result:
            return result[role]
        return None
    
    def setResults(self, results):
        self.beginResetModel()
        self._results = results
        self._data = []
        self.formatDataToFitRoles()
        self.endResetModel()

class ViewHistoryScreenViewModel(QObject):
    dataChanged = pyqtSignal()

    def __init__(self, drills, drillResultsRepo, parent=None):
        super().__init__(parent)
        self._drills = drills
        self._drill = None
        self._selectedIndex = -1
        self.drill_results_repository = drillResultsRepo
        self._results_model = DrillResultsModel()
        self._offset = 0
        self._limit = 25


    @pyqtProperty(int)
    def selectedIndex(self):
        return self._selectedIndex

    @selectedIndex.setter
    def selectedIndex(self, value):
        if self._selectedIndex != value:
            self._selectedIndex = value
            self._drill = self._drills[value]
            self.loadNextPage()  # Load initial results for the selected drill

    @pyqtProperty(DrillResultsModel, notify=dataChanged)
    def results(self):
        return self._results_model

    @pyqtSlot()
    def loadNextPage(self):
        if self._drill:
            results = self.drill_results_repository.get_results_for_drill(self._drill, self._offset, self._limit)
            current_results = self._results_model._results
            self._results_model.setResults(current_results + results)
            self._offset += self._limit
            self.dataChanged.emit()  # Notify QML about the data update

    def loadMoreResults(self):
        if self._drill:
            results = self.drill_results_repository.get_results_for_drill(self._drill, self._offset, self._limit)
            current_results = self._results_model._results
            self._results_model.setResults(current_results + results)
            self._offset += self._limit
            self.dataChanged.emit()  # Notify QML about the data update