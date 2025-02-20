#!/usr/bin/env python
"""
analyze.py

This script processes each WAV file in the 'speech1-modified' folder,
generates a spectrogram, waveform, cepstrum, and MFCC plot for each file, and saves
the images in the 'spectrograms', 'waveforms', 'cepstrums', and 'mfccs' folders respectively.

Dependencies:
    - numpy
    - matplotlib
    - scipy
    - librosa
    - librosa.display
    - os

Usage:
    Ensure that the 'speech1-modified' folder (containing the simulated WAV files)
    exists in the same directory, then run:
        python spectrogram.py
"""

import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram

### 🟢 HELPER FUNCTIONS

def plot_and_save_waveform(signal, sampling_rate, title, output_filename):
    """Plots and saves a waveform."""
    time = np.linspace(0, len(signal) / sampling_rate, num=len(signal))
    plt.figure(figsize=(10, 4))
    plt.plot(time, signal, color='blue', linewidth=1)
    plt.title(title)
    plt.xlabel('Time [sec]')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.close()
    print(f"Saved waveform: {output_filename}")

def plot_and_save_spectrogram(signal, sampling_rate, title, output_filename):
    """Computes and saves a spectrogram."""
    f, t, Sxx = spectrogram(signal, fs=sampling_rate)
    Sxx_dB = 10 * np.log10(Sxx + 1e-10)  # Convert to dB
    plt.figure(figsize=(10, 4))
    plt.pcolormesh(t, f, Sxx_dB, shading='gouraud', cmap='viridis')
    plt.title(title)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.colorbar(label='Intensity [dB]')
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.close()
    print(f"Saved spectrogram: {output_filename}")

def plot_and_save_cepstrum(signal, sampling_rate, title, output_filename, zoom_limit=0.005):
    """Computes and saves the cepstrum with liftering for better visualization."""
    N = len(signal)
    spectrum = np.fft.fft(signal)
    log_spectrum = np.log(np.abs(spectrum) + 1e-10)
    cepstrum = np.fft.ifft(log_spectrum).real
    
    # Apply a simple liftering (remove DC component and smooth)
    lifter = np.hamming(len(cepstrum))
    cepstrum *= lifter  # Liftering to remove low quefrency dominance

    quefrency = np.arange(N) / sampling_rate
    plt.figure(figsize=(10, 4))
    plt.plot(quefrency, cepstrum, color='green')
    plt.title(title)
    plt.xlabel('Quefrency [s]')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.xlim(0, zoom_limit)  # Zoom into the first 5ms
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.close()
    print(f"Saved cepstrum: {output_filename}")

def plot_and_save_mfcc(signal, sampling_rate, title, output_filename, n_mfcc=13):
    """Computes and saves the Mel-Frequency Cepstral Coefficients (MFCCs)."""
    
    # Convert integer signal to float (Librosa requires float32)
    signal = signal.astype(np.float32)  # Convert to float
    signal /= np.max(np.abs(signal)) + 1e-10  # Normalize to [-1, 1] range

    mfccs = librosa.feature.mfcc(y=signal, sr=sampling_rate, n_mfcc=n_mfcc)
    
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mfccs, sr=sampling_rate, x_axis='time', cmap='magma')
    plt.title(title)
    plt.colorbar(label='MFCC Coefficients')
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.close()
    print(f"Saved MFCC: {output_filename}")


### 🟢 MAIN FUNCTION

def main():
    input_folder = 'speech1-modified'
    spectrogram_folder = 'spectrograms'
    waveform_folder = 'waveforms'
    cepstrum_folder = 'cepstrums'
    mfcc_folder = 'mfccs'

    os.makedirs(spectrogram_folder, exist_ok=True)
    os.makedirs(waveform_folder, exist_ok=True)
    os.makedirs(cepstrum_folder, exist_ok=True)
    os.makedirs(mfcc_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.wav'):
            file_path = os.path.join(input_folder, filename)
            sampling_rate, signal = wavfile.read(file_path)

            if signal.ndim > 1:
                signal = np.mean(signal, axis=1)  # Convert to mono if stereo
            
            base_filename = os.path.splitext(filename)[0]
            
            # Waveform
            wave_title = f"Waveform of {filename}"
            wave_output = os.path.join(waveform_folder, f"{base_filename}-waveform.png")
            plot_and_save_waveform(signal, sampling_rate, wave_title, wave_output)

            # Spectrogram
            spec_title = f"Spectrogram of {filename}"
            spec_output = os.path.join(spectrogram_folder, f"{base_filename}-spectrogram.png")
            plot_and_save_spectrogram(signal, sampling_rate, spec_title, spec_output)

            # Cepstrum
            cepstrum_title = f"Cepstrum of {filename}"
            cepstrum_output = os.path.join(cepstrum_folder, f"{base_filename}-cepstrum.png")
            plot_and_save_cepstrum(signal, sampling_rate, cepstrum_title, cepstrum_output)

            # MFCC
            mfcc_title = f"MFCCs of {filename}"
            mfcc_output = os.path.join(mfcc_folder, f"{base_filename}-mfcc.png")
            plot_and_save_mfcc(signal, sampling_rate, mfcc_title, mfcc_output)

if __name__ == "__main__":
    main()
