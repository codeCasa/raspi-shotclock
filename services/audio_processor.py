import numpy as np
from scipy.signal import butter, lfilter, stft
from scipy.fft import fft
import pandas as pd

class AudioProcessor:
    def __init__(self, calibration_data, sample_rate=44100):
        self.calibration_data = calibration_data
        self.filtered_audio = None
        self.sample_rate = sample_rate

    def process_audio(self, new_audio):
        """Process new audio using the calibration data."""
        noise_profile = self.calibration_data.get_noise_profile()
        if not noise_profile:
            print("No calibration data available.")
            return

        # # Apply the same bandpass filter as used during calibration
        print("Processing audio...")
        self.filtered_audio = self.bandpass_filter(new_audio, 300, 3000, self.sample_rate)

        # Apply initial gunshot detection
        gunshot_indices = self.detect_gunshot(self.filtered_audio)
        print(f"Initial gunshots: {len(gunshot_indices)}")

        # Further refine detection with analyze_audio
        final_gunshots = self.analyze_audio(self.filtered_audio, noise_profile)
        print(f"Final gunshots: {len(final_gunshots)}")
        print("Audio processed.")

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
    
    def detect_gunshot(self, audio_data):
        """Detect potential gunshots in the audio data."""
        # Calculate energy of the audio
        energy = np.abs(audio_data) ** 2
        
        # Use a higher threshold based on visual inspection
        threshold = np.percentile(energy, 99.8)
        
        # Detect peaks above the threshold
        peaks = np.where(energy > threshold)[0]
        
        # Filter peaks to avoid multiple detections for the same shot
        filtered_peaks = []
        min_distance = int(self.sample_rate * 0.2)  # 200ms between shots
        last_peak = -min_distance
        
        for peak in peaks:
            if peak - last_peak > min_distance:
                filtered_peaks.append(peak)
                last_peak = peak
        
        return np.array(filtered_peaks)

    def analyze_audio(self, audio_data, noise_profile):
        """Analyze the audio and filter out gunshots based on calibration."""
        window_size = int(0.02 * self.sample_rate)  # 20ms window
        stride = int(0.01 * self.sample_rate)  # 10ms stride
        mean_noise = noise_profile['mean']
        std_noise = noise_profile['std']
        
        # Set thresholds based on observed gunshot energy levels
        min_energy_threshold = 0.08  # Slightly below the lowest observed gunshot energy
        max_energy_threshold = 0.12  # Slightly above the highest observed gunshot energy
        
        detected_shots = []

        for i in range(0, len(audio_data) - window_size, stride):
            window = audio_data[i:i + window_size]

            # Calculate energy
            energy = np.mean(np.abs(window)**2)

            # Only consider the window if its energy is within the expected range for gunshots
            if min_energy_threshold <= energy <= max_energy_threshold:
                # Frequency analysis using FFT
                spectrum = np.abs(fft(window))[:window_size // 2]
                spectrum_energy = np.sum(spectrum[800:3000])  # Focus on gunshot range

                # Combine energy and spectral information
                combined_score = (energy - min_energy_threshold) + (spectrum_energy - mean_noise)
                
                # Adjust dynamic threshold based on combined score
                if combined_score > 0:
                    detected_shots.append(i)

        print(f"Detected {len(detected_shots)} gunshots after refinement.")
        return np.array(detected_shots)


    
    def plot_energy_levels(self, output_file="energy_levels.xlsx"):
        """Plot the energy levels of the processed audio and save them in an Excel sheet."""
        if self.filtered_audio is None:
            print("No audio data available for plotting.")
            return

        # Calculate the energy in sliding windows
        window_size = int(self.sample_rate * 0.1)  # 100ms window
        energy_levels = []

        for i in range(0, len(self.filtered_audio) - window_size, window_size):
            window = self.filtered_audio[i:i + window_size]
            energy = np.mean(np.abs(window) ** 2)
            energy_levels.append(energy)

        # Create a DataFrame to store the energy levels
        df = pd.DataFrame({
            "Time (s)": [i / self.sample_rate for i in range(0, len(self.filtered_audio) - window_size, window_size)],
            "Energy": energy_levels
        })

        # Save the DataFrame to an Excel file
        df.to_excel(output_file, index=False)
        print(f"Energy levels saved to {output_file}.")
