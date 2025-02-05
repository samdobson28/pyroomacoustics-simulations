#!/usr/bin/env python
"""
simulate_audio.py

This script simulates synthetic room acoustics on a dry speech signal using the Pyroomacoustics library.
It processes an input WAV file (speech1.wav) and outputs several WAV files corresponding to different
room and microphone configurations. In this example, we simulate five different rooms, each with five microphones.

Output files are saved in the subfolder:
    speech1-modified/
with filenames following the convention:
    speech1-roomX-micY.wav
where X is the room number (1-5) and Y is the microphone number (1-5).

Dependencies:
    - numpy
    - scipy
    - pyroomacoustics

Usage:
    Place speech1.wav in the same directory as this script and run:
        python simulate_audio.py
"""

import os
import numpy as np
import pyroomacoustics as pra
from scipy.io import wavfile

def simulate_audio_in_rooms(audio_signal, sampling_rate, rooms, source_position):
    """
    Simulates audio in multiple rooms with specified microphone positions.
    
    Parameters:
        audio_signal (np.ndarray): The dry input speech signal (mono).
        sampling_rate (int): Sampling rate of the audio signal.
        rooms (list): List of dictionaries, each containing:
            - 'dimensions': list of room dimensions [length, width, height] in meters.
            - 'rt60': Desired reverberation time (seconds).
            - 'microphones': List of microphone positions (each a list [x, y, z]).
        source_position (list): The [x, y, z] position of the audio source.
        
    Returns:
        dict: Keys as 'room_X_mic_Y', values as the simulated microphone signals.
    """
    simulated_signals = {}
    
    for i, room_info in enumerate(rooms):
        room_dim = room_info['dimensions']
        rt60 = room_info['rt60']
        mic_positions = room_info['microphones']
        
        # Calculate the energy absorption coefficient and max order using Sabine's formula.
        e_absorption, max_order = pra.inverse_sabine(rt60, room_dim)
        
        # Create a shoebox room using the specified dimensions and acoustics parameters.
        room = pra.ShoeBox(
            room_dim,
            fs=sampling_rate,
            materials=pra.Material(e_absorption),
            max_order=max_order
        )
        
        # Add the source signal at the given position.
        room.add_source(source_position, signal=audio_signal)
        
        # Create the microphone array.
        # The MicrophoneArray expects a 2D array where each column corresponds to a mic position.
        mic_array = np.array(mic_positions).T
        room.add_microphone_array(pra.MicrophoneArray(mic_array, room.fs))
        
        # Run the room simulation (i.e. convolve the source signal with the room impulse responses).
        room.simulate()
        
        # Store simulated signals for each microphone.
        for j, mic_signal in enumerate(room.mic_array.signals):
            key = f'room_{i+1}_mic_{j+1}'
            simulated_signals[key] = mic_signal

    return simulated_signals

def main():
    # Input file (dry speech signal)
    input_file = 'speech1.wav'
    sampling_rate, audio_signal = wavfile.read(input_file)
    
    # Convert to mono if stereo
    if audio_signal.ndim > 1 and audio_signal.shape[1] > 1:
        audio_signal = np.mean(audio_signal, axis=1)
    
    # Define five room configurations, each with five microphones.
    rooms = [
        {
            'dimensions': [9, 7.5, 3.5],
            'rt60': 0.5,
            'microphones': [
                [2.0, 3.0, 1.5],
                [3.0, 3.0, 1.5],
                [4.0, 3.0, 1.5],
                [5.0, 3.0, 1.5],
                [6.0, 3.0, 1.5]
            ]
        },
        {
            'dimensions': [8, 6, 3.0],
            'rt60': 0.6,
            'microphones': [
                [2.0, 2.0, 1.5],
                [3.0, 2.0, 1.5],
                [4.0, 2.0, 1.5],
                [5.0, 2.0, 1.5],
                [6.0, 2.0, 1.5]
            ]
        },
        {
            'dimensions': [10, 8, 3.5],
            'rt60': 0.7,
            'microphones': [
                [2.0, 4.0, 1.5],
                [3.0, 4.0, 1.5],
                [4.0, 4.0, 1.5],
                [5.0, 4.0, 1.5],
                [6.0, 4.0, 1.5]
            ]
        },
        {
            'dimensions': [7, 5, 3.0],
            'rt60': 0.5,
            'microphones': [
                [1.0, 1.0, 1.2],
                [2.0, 1.0, 1.2],
                [3.0, 1.0, 1.2],
                [4.0, 1.0, 1.2],
                [5.0, 1.0, 1.2]
            ]
        },
        {
            'dimensions': [6, 6, 3.0],
            'rt60': 0.8,
            'microphones': [
                [1.5, 2.0, 1.2],
                [2.5, 2.0, 1.2],
                [3.5, 2.0, 1.2],
                [4.5, 2.0, 1.2],
                [5.5, 2.0, 1.2]
            ]
        }
    ]
    
    # Define a common source position (ensure this is within the boundaries of all rooms).
    source_position = [2.5, 3.73, 1.76]
    
    # Run simulation
    simulated_signals = simulate_audio_in_rooms(audio_signal, sampling_rate, rooms, source_position)
    
    # Define the output folder.
    output_folder = 'speech1-modified'
    os.makedirs(output_folder, exist_ok=True)
    
    # Save each output with the naming convention: speech1-roomX-micY.wav inside the output folder.
    for key, signal in simulated_signals.items():
        parts = key.split('_')
        room_num = parts[1]
        mic_num = parts[3]
        output_filename = os.path.join(output_folder, f'speech1-room{room_num}-mic{mic_num}.wav')
        wavfile.write(output_filename, sampling_rate, signal.astype(np.int16))
        print(f"Saved: {output_filename}")

if __name__ == "__main__":
    main()
