#!/usr/bin/env python3
"""
simulate_audio.py

This module defines functions to simulate a room acoustic scenario based on a configuration.
It loads a JSON configuration, sets up a room using Pyroomacoustics, adds sources (speech and noise),
and applies a microphone model (FIR filtering and noise floor). For music noise sources, if the music
signal is longer than the speech signal, it will be clipped to the speech signal length.
"""

import numpy as np
import pyroomacoustics as pra
from scipy.io import wavfile
from scipy.signal import fftconvolve, resample

def load_audio(filepath, target_fs=None):
    """
    Load an audio file as a mono normalized float32 signal.
    Optionally, resample it to target_fs.
    Assumes a WAV file with a RIFF header.
    """
    fs, data = wavfile.read(filepath)
    if data.ndim > 1:
        data = data[:, 0]  # use first channel if stereo
    if np.issubdtype(data.dtype, np.integer):
        max_val = np.iinfo(data.dtype).max
        data = data.astype(np.float32) / max_val
    if target_fs is not None and fs != target_fs:
        num_samples = int(len(data) * target_fs / fs)
        data = resample(data, num_samples)
        fs = target_fs
    return fs, data

def simulate_room(config):
    """
    Set up and simulate the room based on the JSON configuration.
    Returns:
      - mixed_signals: numpy array (n_mics x n_samples) with the final simulated signals.
      - room: the pyroomacoustics Room object.
    
    For music noise sources, if the music signal is longer than the speech signal,
    it is clipped to the speech signal length.
    """
    room_cfg = config.get("room", {})
    dimensions = room_cfg.get("dimensions")
    rt60 = room_cfg.get("rt60")
    ir_file = room_cfg.get("ir_file")
    fs = config.get("microphone_model", {}).get("sampling_rate", 16000)
    
    if dimensions is None:
        raise ValueError("Room dimensions must be provided in the configuration.")
    if rt60 is None and ir_file is None:
        raise ValueError("Either rt60 or an impulse response file must be provided.")

    # Create room using dimensions and RT60 if available.
    if rt60 is not None:
        e_absorption, max_order = pra.inverse_sabine(rt60, dimensions)
        materials = pra.Material(e_absorption)
    else:
        materials = None
        max_order = 0

    room = pra.ShoeBox(dimensions, fs=fs, materials=materials, max_order=max_order)

    # Add microphone array.
    mic_positions = config.get("microphone_positions", [])
    if not mic_positions:
        raise ValueError("No microphone positions provided in the configuration.")
    mic_array = np.array(mic_positions).T  # shape (ndim, n_mics)
    room.add_microphone_array(mic_array)

    # Add sources.
    sources_cfg = config.get("sources", {})

    # Speech source.
    speech_cfg = sources_cfg.get("speech")
    if speech_cfg is None:
        raise ValueError("A speech source must be specified.")
    speech_pos = speech_cfg.get("position")
    speech_file = speech_cfg.get("signal_file")
    if speech_pos is None or speech_file is None:
        raise ValueError("Speech source must include 'position' and 'signal_file'.")
    fs_speech, speech_signal = load_audio(speech_file, target_fs=fs)
    speech_length = len(speech_signal)
    delay = speech_cfg.get("delay", 0.0)
    room.add_source(speech_pos, signal=speech_signal, delay=delay)

    # Noise sources.
    noise_sources = sources_cfg.get("noise", [])
    for noise in noise_sources:
        noise_type = noise.get("type", "").lower()
        noise_pos = noise.get("position")
        amplitude = noise.get("amplitude", 1.0)
        if noise_pos is None or noise_type == "":
            raise ValueError("Each noise source must have a 'type' and 'position'.")
        if noise_type == "music":
            noise_file = noise.get("signal_file")
            if noise_file is None:
                raise ValueError("Music noise source must include a 'signal_file'.")
            fs_noise, noise_signal = load_audio(noise_file, target_fs=fs)
            # Clip music signal to speech length if needed.
            if len(noise_signal) > speech_length:
                noise_signal = noise_signal[:speech_length]
            noise_signal = amplitude * noise_signal
            room.add_source(noise_pos, signal=noise_signal, delay=0.0)
        elif noise_type == "gaussian":
            # Generate Gaussian noise with the same length as speech.
            noise_signal = amplitude * np.random.randn(speech_length)
            room.add_source(noise_pos, signal=noise_signal, delay=0.0)
        else:
            raise ValueError(f"Unknown noise source type: {noise_type}")

    # Simulate the room.
    premix = room.simulate(return_premix=True)
    mixed_signals = np.sum(premix, axis=0)
    return mixed_signals, room

def apply_microphone_model(signals, mic_model_cfg):
    """
    Apply the microphone model to the simulated signals.
    Convolve each channel with the frequency response if provided,
    then add a white noise floor.
    """
    processed = signals.copy()
    fs = mic_model_cfg.get("sampling_rate")
    noise_floor_db = mic_model_cfg.get("noise_floor")
    freq_resp_file = mic_model_cfg.get("frequency_response")
    
    if freq_resp_file is not None:
        freq_resp = np.loadtxt(freq_resp_file)
        for i in range(processed.shape[0]):
            processed[i, :] = fftconvolve(processed[i, :], freq_resp, mode='same')
    
    if noise_floor_db is not None:
        noise_std = 10 ** (noise_floor_db / 20.0)
        processed += noise_std * np.random.randn(*processed.shape)
    
    return processed

def write_output(signals, fs, output_file):
    """
    Write the multi-channel signal to a WAV file.
    """
    import os
    from scipy.io import wavfile
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    # Normalize to avoid clipping.
    out = signals.T
    max_val = np.max(np.abs(out))
    if max_val > 0:
        out = out / max_val
    wavfile.write(output_file, fs, np.int16(out * 32767))
    print(f"Output written to {output_file}")
