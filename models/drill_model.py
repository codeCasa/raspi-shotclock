from PyQt6.QtCore import QObject, pyqtProperty, QAbstractListModel, QModelIndex, Qt
import json
import logging
from enum import IntEnum, auto

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DrillModelRoles(IntEnum):
    NAME = auto()
    DESCRIPTION = auto()


_role_names = {
    DrillModelRoles.NAME: b'name',
    DrillModelRoles.DESCRIPTION: b'description',
}

class DrillModel(QObject):
    def __init__(self, name, description, timerCountDown, numberOfShots, distanceFromTarget, parent=None):
        super().__init__(parent)
        self._name = name
        self._description = description
        self._timerCountDown = timerCountDown
        self._numberOfShots = numberOfShots
        self._distanceFromTarget = distanceFromTarget

    @pyqtProperty("QString")
    def name(self):
        return self._name

    @pyqtProperty("QString")
    def description(self):
        return self._description
    
    @staticmethod
    def load_drills(json_file_path):
        """Load drills from the provided JSON file path and return a list of DrillModel instances."""
        with open(json_file_path, 'r') as file:
            drills_data = json.load(file)

        # Sort drills alphabetically by name
        drills_data.sort(key=lambda drill: drill["name"])

        # Create and return a list of DrillModel instances
        return [DrillModel(drill["name"], drill["description"], drill["timerCountDown"], drill["numberOfShots"], drill["distanceFromTarget"]) for drill in drills_data]

class DrillModelList(QAbstractListModel):
    def __init__(self, drills: list, parent=None):
        super().__init__(parent)
        self._drills = drills
        self._data = []
        self.formatDataToFitRoles()

    def rowCount(self, parent=QModelIndex()):
        return len(self._drills)
    
    def formatDataToFitRoles(self):
        for drill in self._drills:
            self._data.append({
                DrillModelRoles.NAME: drill.name,
                DrillModelRoles.DESCRIPTION: drill.description
            })
    
    def roleNames(self):
        return _role_names

    def data(self, index, role=DrillModelRoles.NAME):
        if role not in list(DrillModelRoles):
            return None

        try:
            device = self._data[index.row()]
        except IndexError:
            return None

        if role in device:
            return device[role]
        return None
