# Synthetic Room Acoustic Audio Simulation

This project demonstrates how to generate synthetic room acoustic data by convolving a dry speech signal with impulse responses that simulate various room environments and microphone placements. We use the [Pyroomacoustics](https://pyroomacoustics.readthedocs.io/en/pypi-release/pyroomacoustics.room.html) library to create realistic room simulations.

## Project Overview

Given a dry input speech file (e.g., `speech1.wav`), the script simulates five distinct rooms. Each room is configured with:

- Specific room dimensions (length, width, height)
- A target reverberation time (RT60)
- Five distinct microphone positions

The output of the simulation is a set of WAV files representing the audio captured at each microphone. The output files are saved in a subfolder called `speech1-modified` and are named following this convention:

- `speech1-roomX-micY.wav`
  - `X` denotes the room number (1 to 5)
  - `Y` denotes the microphone number (1 to 5)

## Input Speech File

The input speech file, **speech1.wav**, is derived from the file [OSR_us_000_0038_8k.wav](https://www.voiptroubleshooter.com/open_speech/american.html). This file is a recording of Harvard sentences spoken by a male speaker. It is encoded in 16-bit PCM format at an 8 kHz sampling rate. For the purposes of this project, the file has been renamed to `speech1.wav`.

## Prerequisites

Make sure you have Python 3 installed along with the following packages:

- [NumPy](https://numpy.org/)
- [SciPy](https://scipy.org/)
- [Pyroomacoustics](https://github.com/LCAV/pyroomacoustics)

You can install the necessary packages via pip:

```bash
pip install numpy scipy pyroomacoustics
```
