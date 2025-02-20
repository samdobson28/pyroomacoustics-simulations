#!/usr/bin/env python3
"""
simulate_all.py

This script iterates over all JSON configuration files in the config/ folder (e.g., config1.json to config30.json).
It allows specifying a speech file via a command-line argument (e.g., samples/speech1.wav), overriding the speech file
in the config. It then simulates each scenario, applies the microphone model, and writes an output WAV file in the output/ folder.

Usage:
    python simulate_all.py samples/speech1.wav
"""

import glob
import json
import os
import sys
from simulate_audio import simulate_room, apply_microphone_model, write_output

def extract_filename(filepath):
    """Extracts the base filename without extension from a given path."""
    return os.path.splitext(os.path.basename(filepath))[0]

def main():
    # Ensure a speech file argument is provided.
    if len(sys.argv) < 2:
        print("Usage: python simulate_all.py <speech_file>")
        sys.exit(1)

    speech_file_path = sys.argv[1]  # Get speech file from command-line argument.

    # Ensure the provided speech file exists.
    if not os.path.exists(speech_file_path):
        print(f"Error: Speech file '{speech_file_path}' not found.")
        sys.exit(1)

    # Extract the speech file name (e.g., "speech1" from "samples/speech1.wav").
    speech_name = extract_filename(speech_file_path)

    # Get all configuration files.
    config_files = sorted(glob.glob("config/config*.json"))
    if not config_files:
        print("No configuration files found in the config/ folder.")
        return

    for cfg_file in config_files:
        with open(cfg_file, "r") as f:
            config = json.load(f)

        # Extract the config file name (e.g., "config1" from "config1.json").
        config_name = extract_filename(cfg_file)

        print(f"Simulating scenario with {config_name} and {speech_name}...")

        # Override the speech file in the configuration.
        config.setdefault("sources", {}).setdefault("speech", {})["signal_file"] = speech_file_path

        # Run the simulation.
        signals, room = simulate_room(config)

        # Apply microphone model if defined.
        mic_model_cfg = config.get("microphone_model")
        if mic_model_cfg:
            signals = apply_microphone_model(signals, mic_model_cfg)

        # Create output filename: <speechName>-<configName>-out.wav.
        output_filename = os.path.join("output", f"{speech_name}-{config_name}-out.wav")
        write_output(signals, room.fs, output_filename)
        print(f"Simulation complete: {output_filename}\n")

if __name__ == "__main__":
    main()
