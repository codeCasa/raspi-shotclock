from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QUrl
from datetime import datetime, timedelta
from utils.line_graph_plotter import LineGraphPlotter
from utils.time_utils import milliseconds_to_datetime
import random

class ViewAnalyticsScreenViewModel(QObject):
    dataChanged = pyqtSignal()
    drillNameChanged = pyqtSignal()
    timeSpanChanged = pyqtSignal()
    nextButtonEnabledChanged = pyqtSignal()

    def __init__(self, drills, drillResultsRepo, parent=None):
        super().__init__(parent)
        self._drills = drills
        self._drill = None
        self._selectedIndex = -1
        self.drill_results_repository = drillResultsRepo
        self._drillResults = []
        self._end_date = datetime.now()
        self._start_date = self._end_date - timedelta(weeks=1)

    @pyqtProperty(bool, notify=dataChanged)
    def hasDrills(self):
        return len(self._drillResults) > 0

    @pyqtProperty(str, notify=drillNameChanged)
    def drillName(self):
        return self._drill._name if self._drill else ""

    @pyqtProperty(str, notify=timeSpanChanged)
    def timeSpan(self):
        return f"{self._start_date.strftime('%m/%d/%Y')} - {self._end_date.strftime('%m/%d/%Y')}"
    
    @pyqtProperty(bool, notify=nextButtonEnabledChanged)
    def nextButtonEnabled(self):
        return self._end_date < datetime.now()

    @pyqtProperty(str, notify=dataChanged)
    def plotUrl(self):
        return QUrl.fromLocalFile('split_times.svg').toString()

    @pyqtProperty(int)
    def selectedIndex(self):
        return self._selectedIndex

    @selectedIndex.setter
    def selectedIndex(self, value):
        if self._selectedIndex != value:
            self._selectedIndex = value
            self._drill = self._drills[value]
            self._fetchDrillResults()
            self.create_plot_widget()
            self.dataChanged.emit()
            self.drillNameChanged.emit()

    def _fetchDrillResults(self):
        if self._drill:
            start = round(self._start_date.timestamp() * 1000)
            end = round(self._end_date.timestamp() * 1000)
            self._drillResults = self.drill_results_repository.get_results_for_drill_name(self._drill._name, between=(start, end))
    
    @pyqtSlot()
    def create_plot_widget(self):
        if len(self._drillResults) == 0:
            return
        data_json = {}
        fastest_splits = []
        slowest_splits = []
        average_splits = []
        tmformat = '%m/%d/%Y %H:%M'
        count = 0
        for result in self._drillResults:
            minusDays = 86400000 * count
            random_noise = abs(random.randint(0, 1) * 0.09)
            fastest_splits.append({'x': milliseconds_to_datetime(result.end_time - minusDays, tmformat), 'y': result.fastest_split_time + random_noise})
            slowest_splits.append({'x': milliseconds_to_datetime(result.end_time - minusDays, tmformat), 'y': result.slowest_split_time + random_noise})
            average_splits.append({'x': milliseconds_to_datetime(result.end_time - minusDays, tmformat), 'y': result.average_split_time + random_noise})
            count += 1
        data_json['Fastest'] = {'points': fastest_splits, 'color': 'blue'}
        data_json['Slowest'] = {'points': slowest_splits, 'color': 'red'}
        data_json['Average'] = {'points': average_splits, 'color': 'green'}
        config = {
            'x_label': 'Date', 
            'y_label': 'Time (s)', 
            'title': 'Split Times', 
            "title_location": "above",
            "y_min": 0,
            "x_label_orientation": 0,
            "y_label_orientation": 90,
            "x_grid": True,
            "y_grid": True,
            "grid_color": "#cccccc",
            "grid_line_style": "--",
            "grid_line_width": 0.7,
            "x_label_format": "datetime",
        }
        plotter = LineGraphPlotter(data_json, config)
        plotter.plot('split_times.svg')

    @pyqtSlot()
    def previousWeek(self):
        self._start_date -= timedelta(weeks=1)
        self._end_date -= timedelta(weeks=1)
        self._fetchDrillResults()
        self.create_plot_widget()
        self.dataChanged.emit()
        self.timeSpanChanged.emit()
        self.nextButtonEnabledChanged.emit()

    @pyqtSlot()
    def nextWeek(self):
        self._start_date += timedelta(weeks=1)
        self._end_date += timedelta(weeks=1)
        self._fetchDrillResults()
        self.create_plot_widget()
        self.dataChanged.emit()
        self.timeSpanChanged.emit()
        self.nextButtonEnabledChanged.emit()
