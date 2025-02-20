#!/usr/bin/env python3
"""
simulate_audio.py
A comprehensive simulation script that:
  - Reads a scenario from a JSON configuration file.
  - Sets up a room simulation using pyroomacoustics (via dimensions & RT60 or using a pre‐computed IR).
  - Adds a speech source and noise sources (music and Gaussian noise).
  - Applies a microphone model (frequency response filtering and noise floor).
  - Writes the multi-channel output to a WAV file in the output/ directory.
Usage:
    python simulate_audio.py --config config/scenario_basic.json --output output/basic_output.wav
"""

import os
import json
import argparse
import numpy as np
import pyroomacoustics as pra
from scipy.io import wavfile
from scipy.signal import fftconvolve, resample

def load_audio(filepath, target_fs=None):
    """Load an audio file as a mono normalized float32 signal, and optionally resample it."""
    fs, data = wavfile.read(filepath)
    if data.ndim > 1:
        data = data[:, 0]  # take first channel if stereo
    if np.issubdtype(data.dtype, np.integer):
        max_val = np.iinfo(data.dtype).max
        data = data.astype(np.float32) / max_val
    if target_fs is not None and fs != target_fs:
        num_samples = int(len(data) * target_fs / fs)
        data = resample(data, num_samples)
        fs = target_fs
    return fs, data

def load_frequency_response(filepath, target_length=None):
    """Load a microphone frequency response (as an impulse response) from a text file."""
    response = np.loadtxt(filepath)
    if target_length is not None:
        if len(response) < target_length:
            response = np.pad(response, (0, target_length - len(response)), 'constant')
        else:
            response = response[:target_length]
    return response

def simulate_room(config):
    """
    Set up and simulate the room based on the JSON configuration.
    Returns:
      - mixed_signals: numpy array (n_mics x n_samples) with final microphone signals.
      - room: the pyroomacoustics Room object.
    """
    # Room configuration
    room_cfg = config.get("room", {})
    dimensions = room_cfg.get("dimensions", None)
    rt60 = room_cfg.get("rt60", None)
    ir_file = room_cfg.get("ir_file", None)
    fs = config.get("microphone_model", {}).get("sampling_rate", 16000)
    
    if dimensions is None:
        raise ValueError("Room dimensions must be provided.")
    if rt60 is None and ir_file is None:
        raise ValueError("Either rt60 or an impulse response file must be provided.")

    # Create room using dimensions+RT60 (for a precomputed IR, you’d extend this code)
    if rt60 is not None:
        e_absorption, max_order = pra.inverse_sabine(rt60, dimensions)
        materials = pra.Material(e_absorption)
    else:
        materials = None
        max_order = 0

    room = pra.ShoeBox(dimensions, fs=fs, materials=materials, max_order=max_order)

    # Microphone positions
    mic_positions = config.get("microphone_positions", [])
    if not mic_positions:
        raise ValueError("No microphone positions specified.")
    mic_array = np.array(mic_positions).T  # shape (ndim, n_mics)
    room.add_microphone_array(mic_array)

    # Add sources
    sources_cfg = config.get("sources", {})

    # Speech source
    speech_cfg = sources_cfg.get("speech", None)
    if speech_cfg is None:
        raise ValueError("A speech source must be specified.")
    speech_pos = speech_cfg.get("position", None)
    speech_file = speech_cfg.get("signal_file", None)
    if speech_pos is None or speech_file is None:
        raise ValueError("Speech source must include 'position' and 'signal_file'.")
    fs_speech, speech_signal = load_audio(speech_file, target_fs=fs)
    delay = speech_cfg.get("delay", 0.0)
    room.add_source(speech_pos, signal=speech_signal, delay=delay)

    # Noise sources (list)
    noise_sources = sources_cfg.get("noise", [])
    for noise in noise_sources:
        noise_type = noise.get("type", "").lower()
        noise_pos = noise.get("position", None)
        amplitude = noise.get("amplitude", 1.0)
        if noise_pos is None or noise_type == "":
            raise ValueError("Each noise source must have a 'type' and 'position'.")
        if noise_type == "music":
            noise_file = noise.get("signal_file", None)
            if noise_file is None:
                raise ValueError("Music noise source must specify 'signal_file'.")
            fs_noise, noise_signal = load_audio(noise_file, target_fs=fs)
            noise_signal = amplitude * noise_signal
            room.add_source(noise_pos, signal=noise_signal, delay=0.0)
        elif noise_type == "gaussian":
            signal_length = len(speech_signal)
            noise_signal = amplitude * np.random.randn(signal_length)
            room.add_source(noise_pos, signal=noise_signal, delay=0.0)
        else:
            raise ValueError(f"Unknown noise source type: {noise_type}")

    # Simulate the room and return individual contributions (premix)
    premix = room.simulate(return_premix=True)
    mixed_signals = np.sum(premix, axis=0)
    return mixed_signals, room

def apply_microphone_model(signals, mic_model_cfg):
    """
    Apply the microphone model to the simulated signals:
      - Convolve with a frequency response if provided.
      - Add a noise floor.
    """
    processed = signals.copy()
    fs = mic_model_cfg.get("sampling_rate", None)
    noise_floor_db = mic_model_cfg.get("noise_floor", None)
    freq_resp_file = mic_model_cfg.get("frequency_response", None)

    if freq_resp_file is not None:
        freq_resp = load_frequency_response(freq_resp_file)
        for i in range(processed.shape[0]):
            processed[i, :] = fftconvolve(processed[i, :], freq_resp, mode='same')

    if noise_floor_db is not None:
        noise_std = 10 ** (noise_floor_db / 20.0)
        noise = noise_std * np.random.randn(*processed.shape)
        processed += noise

    return processed

def write_output(signals, fs, output_file):
    """
    Write the multi-channel signal to a WAV file.
    The output file is saved in the directory specified (typically under output/).
    """
    # Ensure output directory exists.
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    out = signals.T  # shape (n_samples, n_mics)
    max_val = np.max(np.abs(out))
    if max_val > 0:
        out = out / max_val
    out_int16 = np.int16(out * 32767)
    wavfile.write(output_file, fs, out_int16)
    print(f"Simulated output written to: {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Simulate audio scenarios using pyroomacoustics based on a JSON configuration."
    )
    parser.add_argument("--config", type=str, required=True,
                        help="Path to the JSON configuration file (e.g., config/scenario_basic.json).")
    parser.add_argument("--output", type=str, default="output/simulated_output.wav",
                        help="Path for the output WAV file (e.g., output/basic_output.wav).")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = json.load(f)

    print("Simulating room acoustics...")
    signals, room = simulate_room(config)
    fs = room.fs

    mic_model_cfg = config.get("microphone_model", None)
    if mic_model_cfg is not None:
        print("Applying microphone model processing...")
        signals = apply_microphone_model(signals, mic_model_cfg)

    write_output(signals, fs, args.output)

    # (Optional) Plotting
    import matplotlib.pyplot as plt
    if hasattr(room, "rir"):
        rir = room.rir[0][0]
        plt.figure()
        plt.plot(np.arange(len(rir)) / fs, rir)
        plt.title("Room Impulse Response (Mic 0, Source 0)")
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()

    n_mics = signals.shape[0]
    plt.figure(figsize=(10, 2 * n_mics))
    for i in range(n_mics):
        plt.subplot(n_mics, 1, i + 1)
        plt.plot(np.arange(signals.shape[1]) / fs, signals[i, :])
        plt.title(f"Microphone {i} Signal")
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
