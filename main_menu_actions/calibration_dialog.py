from PyQt6.QtCore import QObject, pyqtSlot, Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QSpacerItem, QSizePolicy, QApplication
from services.calibration_service import CalibrationService
from services.audio_processor import AudioProcessor
from models.calibration_data import CalibrationData
import numpy as np


class CalibrationWorker(QThread):
    progress = pyqtSignal(int)

    def __init__(self, calibration_service, parent=None):
        super().__init__(parent)
        print("CalibrationWorker init")
        self.calibration_service = calibration_service

    def run(self):
        print("CalibrationWorker run")
        self.calibration_service.calibrate(self.report_progress)

    def report_progress(self, value):
        self.progress.emit(value)

class CalibrationDialog(QObject):
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.calibration_service = CalibrationService()
    
    @pyqtSlot()
    def calibrate(self):
        """Shows the calibration dialog"""
        app = QApplication.instance()  # Ensure QApplication is active
        if app is None:
            raise RuntimeError("QApplication instance is not created")
        self.calibrate_modal = CalibrateModal()
        self.calibrate_modal.exec_calibration()
        # Start the calibration in a separate thread
        self.worker = CalibrationWorker(self.calibration_service)
        self.worker.progress.connect(self.calibrate_modal.update_progress)
        self.worker.start()

    @pyqtSlot()
    def test(self):
        """Test CalibrationDialog"""
        calibrationData = CalibrationData.load_calibration_data()
        audioProcessor = AudioProcessor(calibrationData)
        test_audio = self.calibration_service.record_audio_and_return()
        audioProcessor.process_audio(test_audio)
        audioProcessor.plot_energy_levels()

    def update_progress(self, value):
        """Callback to update the progress in the modal."""
        self.calibrate_modal.update_progress(value)
        if(value >= 100):
            print("Calibration complete")
            self.calibration_thread.join()

class CalibrateModal(QDialog):
    def __init__(self, parent=None):
        super(CalibrateModal, self).__init__(parent)

        # Set dialog properties
        self.setWindowTitle("Calibrating...")
        self.setModal(True)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Remove the title bar
        self.setFixedSize(300, 200)

        # Set up the layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Add label
        self.label = QLabel("Calibrating...", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.label)

        # Add progress bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setFixedWidth(200)
        self.progressBar.setTextVisible(False)
        self.progressBar.setRange(0, 0)  # Indeterminate progress bar
        layout.addWidget(self.progressBar, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add spacer
        spacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

        # Set layout to the dialog
        self.setLayout(layout)

    def update_progress(self, value):
        print(f"Progress: {value}%")
        self.progressBar.setRange(0, 100)  # Indeterminate progress bar
        self.progressBar.setValue(value)
        if value >= 100:
            self.accept()

    def exec_calibration(self):
        """Execute the dialog and prevent closing it with Esc or clicking outside."""
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.show()  # This will block until the dialog is closed
