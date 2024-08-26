import numpy as np
import json
import os

class CalibrationData:
    def __init__(self, audio_file='filtered_audio.npy', noise_file='noise_profile.json'):
        self.audio_file = audio_file
        self.noise_file = noise_file
        self.filtered_audio = None
        self.noise_profile = None

    def load_data(self):
        """Load the filtered audio and noise profile data from files."""
        if os.path.exists(self.audio_file):
            self.filtered_audio = np.load(self.audio_file)
            print(f"Filtered audio data loaded from {self.audio_file}")
        else:
            print(f"No filtered audio file found at {self.audio_file}")

        if os.path.exists(self.noise_file):
            with open(self.noise_file, 'r') as file:
                self.noise_profile = json.load(file)
            print(f"Noise profile loaded from {self.noise_file}")
        else:
            print(f"No noise profile file found at {self.noise_file}")
    
    @staticmethod
    def load_calibration_data(audio_file='filtered_audio.npy', noise_file='noise_profile.json'):
        """Load the calibration data from the specified files and return a CalibrationData instance."""
        calibration_data = CalibrationData(audio_file, noise_file)
        calibration_data.load_data()
        return calibration_data

    def get_noise_profile(self):
        """Return the loaded noise profile."""
        return self.noise_profile

    def get_filtered_audio(self):
        """Return the loaded filtered audio."""
        return self.filtered_audio
