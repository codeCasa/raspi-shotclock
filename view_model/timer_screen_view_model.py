from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, QTimer, pyqtSlot
from PyQt6.QtCore import QTime, QElapsedTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
from enum import IntEnum
import os
import time
from models.drill_results import DrillResults

class TimerRunState(IntEnum):
    STARTED = 0
    RUNNING = 1
    PAUSED = 2
    STOPPED = 3
    COUNTDOWN = 4

class TimerScreenViewModel(QObject):
    timerStateChanged = pyqtSignal(int)
    shotsFiredChanged = pyqtSignal(int)
    elapsedTimeChanged = pyqtSignal(str)
    splitsChanged = pyqtSignal(list)
    countdownChanged = pyqtSignal(int)
    wasStartedChanged = pyqtSignal(bool)

    def __init__(self, drills, drillResultsRepo, parent=None):
        super().__init__(parent)
        self._drills = drills
        self._drill = None
        self._selectedIndex = -1
        self._elapsedTime = QTime(0, 0, 0)
        self._shotsFired = 0
        self._timerRunningState = TimerRunState.STOPPED
        self._splits = []
        self._countdownTime = 0
        self.drill_results_repository = drillResultsRepo

        self._timer = QTimer()
        self._timer.setInterval(10)
        self._timer.timeout.connect(self.updateTime)

        self._soundPlayer = QMediaPlayer()
        self._audioOutput = QAudioOutput()
        self._soundPlayer.setAudioOutput(self._audioOutput)
        self._audioOutput.setVolume(100.0)
        beep_file = os.path.abspath('./sounds/beep_2.wav')
        self._soundPlayer.setSource(QUrl.fromLocalFile(beep_file))

        self._elapsedTimer = QElapsedTimer()

        self._soundPlayer.mediaStatusChanged.connect(self.onMediaStatusChanged)
        self._start_time = 0
        self._end_time = 0
        self._was_started = False

    def onMediaStatusChanged(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            if self._countdownTime < 1:
                self._startTimerNow()
            else:
                self.updateCountdown()  # Trigger countdown when media ends

    @pyqtProperty(int, notify=timerStateChanged)
    def timerState(self):
        return self._timerRunningState

    @timerState.setter
    def timerState(self, value):
        if self._timerRunningState != value:
            self._timerRunningState = value
            self.timerStateChanged.emit(value)

    @pyqtProperty(int)
    def selectedIndex(self):
        return self._selectedIndex

    @pyqtProperty(str)
    def drillName(self):
        return self._drill._name if self._drill else ""
    
    @pyqtProperty(str)
    def drillDescription(self):
        return self._drill._description if self._drill else ""
    
    @pyqtProperty(str)
    def numberOfShots(self):
        return f'{self._drill._numberOfShots}' if self._drill else ""

    @selectedIndex.setter
    def selectedIndex(self, value):
        if self._selectedIndex != value:
            self._selectedIndex = value
            self._drill = self._drills[value]
            self._countdownTime = self._drill._timerCountDown

    @pyqtProperty(str, notify=elapsedTimeChanged)
    def elapsedTime(self):
        return self._elapsedTime.toString("mm:ss.zzz")

    @pyqtProperty(int, notify=shotsFiredChanged)
    def shotsFired(self):
        return self._shotsFired

    @pyqtProperty(list, notify=splitsChanged)
    def splits(self):
        return self._splits

    @pyqtProperty(int, notify=countdownChanged)
    def countdownTime(self):
        return self._countdownTime

    @pyqtProperty(bool, notify=wasStartedChanged)
    def wasStarted(self):
        return self._was_started

    @pyqtSlot()
    def startTimer(self):
        if self._timerRunningState == TimerRunState.STOPPED:
            if self._drill and self._drill._timerCountDown > 0:
                self._countdownTime = self._drill._timerCountDown
                self._timerRunningState = TimerRunState.COUNTDOWN
                self.timerStateChanged.emit(TimerRunState.COUNTDOWN)
                self._soundPlayer.play()  # Play the first beep
                self.countdownChanged.emit(self._countdownTime)
            else:
                self._startTimerNow()

    @pyqtSlot()
    def _startTimerNow(self):
        self._was_started = True
        self.wasStartedChanged.emit(self._was_started)
        self._start_time = round(time.time() * 1000)
        self._elapsedTimer.start()
        self._timer.start()
        self._splits = []
        self._timerRunningState = TimerRunState.STARTED
        self.timerStateChanged.emit(TimerRunState.STARTED)

    @pyqtSlot()
    def pauseTimer(self):
        if self._timerRunningState in [TimerRunState.RUNNING, TimerRunState.STARTED]:
            self._timer.stop()
            self._timerRunningState = TimerRunState.PAUSED
            self.timerStateChanged.emit(TimerRunState.PAUSED)

    @pyqtSlot()
    def resumeTimer(self):
        if self._timerRunningState == TimerRunState.PAUSED:
            self._timer.start()
            self._timerRunningState = TimerRunState.RUNNING
            self.timerStateChanged.emit(TimerRunState.RUNNING)

    @pyqtSlot()
    def stopTimer(self):
        if self._timerRunningState != TimerRunState.STOPPED:
            self._end_time = round(time.time() * 1000)
            self._timer.stop()
            self._elapsedTime = QTime(0, 0, 0).addMSecs(self._elapsedTimer.elapsed())
            self.elapsedTimeChanged.emit(self._elapsedTime.toString("mm:ss.zzz"))
            self._timerRunningState = TimerRunState.STOPPED
            self.timerStateChanged.emit(TimerRunState.STOPPED)
            self._countdownTime = self._drill._timerCountDown

    @pyqtSlot()
    def updateTime(self):
        if self._timerRunningState in [TimerRunState.RUNNING, TimerRunState.STARTED]:
            self._elapsedTime = QTime(0, 0, 0).addMSecs(self._elapsedTimer.elapsed())
            self.elapsedTimeChanged.emit(self._elapsedTime.toString("mm:ss.zzz"))

    @pyqtSlot()
    def updateCountdown(self):
        if self._timerRunningState != TimerRunState.COUNTDOWN:
            return
        if self._countdownTime > 0:
            self._countdownTime -= 1
            self.countdownChanged.emit(self._countdownTime)
            if self._countdownTime > 0:
                self._soundPlayer.play()  # Play the next beep sound
            else:
                beep_file = os.path.abspath('./sounds/go_beep.wav')
                self._soundPlayer.setSource(QUrl.fromLocalFile(beep_file))
                self._soundPlayer.play()  # Play the next beep sound
        else:
            beep_file = os.path.abspath('./sounds/go_beep.wav')
            self._soundPlayer.setSource(QUrl.fromLocalFile(beep_file))
            self._soundPlayer.play()  # Play the next beep sound

    @pyqtSlot()
    def addShotFired(self):
        self._shotsFired += 1
        self.shotsFiredChanged.emit(self._shotsFired)

        split_time = self._elapsedTime.toString("mm:ss.zzz")
        self._splits.append(split_time)
        self.splitsChanged.emit(self._splits)

    def calculate_average_split_time(self):
        if not self._splits:
            return 0.0

        total_split_time = 0.0
        for split in self._splits:
            time_parts = split.split(":")
            minutes = int(time_parts[0])
            seconds, milliseconds = map(int, time_parts[1].split("."))
            total_split_time += (minutes * 60 * 1000) + (seconds * 1000) + milliseconds

        average_split_time = total_split_time / len(self._splits)
        return average_split_time

    def calculate_fastest_split_time(self):
        if not self._splits:
            return "N/A"

        fastest_split_time = float('inf')
        for split in self._splits:
            time_parts = split.split(":")
            minutes = int(time_parts[0])
            seconds, milliseconds = map(int, time_parts[1].split("."))
            split_time = (minutes * 60 * 1000) + (seconds * 1000) + milliseconds
            if split_time < fastest_split_time:
                fastest_split_time = split_time
        return fastest_split_time

    def calculate_slowest_split_time(self):
        if not self._splits:
            return "N/A"

        slowest_split_time = float('-inf')
        for split in self._splits:
            time_parts = split.split(":")
            minutes = int(time_parts[0])
            seconds, milliseconds = map(int, time_parts[1].split("."))
            split_time = (minutes * 60 * 1000) + (seconds * 1000) + milliseconds
            if split_time > slowest_split_time:
                slowest_split_time = split_time
        return slowest_split_time

    @pyqtSlot(float, str)
    def saveResults(self, score, notes):
        if self._drill:
            drill_results = DrillResults(
                drill_name=self._drill._name,  # Make sure this is set appropriately
                start_time=self._start_time,  # These should be set from when the drill started
                end_time=self._end_time,  # You may need to calculate end time
                elapsed_time=self._elapsedTimer.elapsed(),
                shots_fired=self._shotsFired,
                splits=self._splits,
                average_split_time=self.calculate_average_split_time(),  # Implement these methods
                fastest_split_time=self.calculate_fastest_split_time(),
                slowest_split_time=self.calculate_slowest_split_time(),
                score=score,
                notes=notes
            )
            print(drill_results.to_json())
            self.drill_results_repository.upsert(drill_results)
