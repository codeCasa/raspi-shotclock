from scipy.signal import butter, lfilter
import sounddevice as sd
import numpy as np
import json
import os

class CalibrationService:
    def __init__(self, duration=10, sample_rate=44100):
        self.duration = duration
        self.sample_rate = sample_rate
        self.audio_data = None
        self.filtered_audio = None
        self.noise_profile = None
        self.progress_callback = None

    def record_audio(self):
        """Record audio for the specified duration."""
        print("Recording...")
        self.audio_data = sd.rec(int(self.duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='float32')
        sd.wait()  # Wait until recording is finished
        print("Recording finished.")

    def process_audio(self):
        """Process recorded audio to isolate environmental noise and gunshots."""
        print("Processing audio...")
        audio_np = np.array(self.audio_data).flatten()
        if self.progress_callback is not None:
            self.progress_callback(60)
        # Apply a bandpass filter to isolate relevant frequencies
        self.filtered_audio = self.bandpass_filter(audio_np, 300, 3000, self.sample_rate)
        if self.progress_callback is not None:
            self.progress_callback(80)
        # Create a basic noise profile (mean and standard deviation of the filtered audio)
        self.noise_profile = {
            'mean': float(np.mean(self.filtered_audio)),
            'std': float(np.std(self.filtered_audio))
        }

        if self.progress_callback is not None:
            self.progress_callback(90)
        # Save the filtered audio and noise profile
        self.save_filtered_audio('filtered_audio.npy')
        self.save_noise_profile('noise_profile.json')
        
        print("Audio processed and saved.")

    def record_audio_and_return(self):
        """Record audio for the specified duration and apply a bandpass filter."""
        print("Recording...")
        data = sd.rec(int(self.duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='float32')
        sd.wait()
        print("Recording finished.")
        audio_np = np.array(data).flatten()
        return audio_np

    def calibrate(self, progress_callback):
        """Run the calibration process."""
        self.progress_callback = progress_callback
        self.record_audio()
        progress_callback(50)
        self.process_audio()
        progress_callback(100)
        # Notify calibration progress if necessary

    def bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        """Apply a bandpass filter to the data."""
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq

        if low >= high or low <= 0 or high >= 1:
            raise ValueError("Cutoff frequencies must be in the range (0, 0.5) and low < high")

        b, a = butter(order, [low, high], btype='band')
        y = lfilter(b, a, data)
        return y


    def save_filtered_audio(self, file_path):
        """Save the filtered audio data to a file."""
        if self.filtered_audio is not None:
            np.save(file_path, self.filtered_audio)
            print(f"Filtered audio data saved to {file_path}")
        else:
            print("No filtered audio data to save.")

    def save_noise_profile(self, file_path):
        """Save the noise profile data to a JSON file."""
        if self.noise_profile is not None:
            with open(file_path, 'w') as file:
                json.dump(self.noise_profile, file)
            print(f"Noise profile saved to {file_path}")
        else:
            print("No noise profile data to save.")
