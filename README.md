# Audio Simulation Package

This package implements a comprehensive simulation framework for room acoustics and audio recording scenarios. It supports advanced research requirements by allowing you to define scenarios using JSON files that specify:

- **Room Parameters:** Define the room dimensions along with a desired reverberation time (RT60) _or_ provide a precomputed impulse response (IR) file.
- **Microphone Array:** Specify the positions of one or more microphones.
- **Sources:**
  - **Speech Source:** A primary speech signal with its position, file path, and delay.
  - **Noise Sources:** Supports both music noise (via an audio file) and Gaussian noise with a specified amplitude.
- **Microphone Model:** Defines a frequency response (FIR filter), sampling rate, and noise floor to simulate real-world microphone characteristics.

## Simulation Process

- **Room Setup:**  
  The simulation generates room impulse responses (RIRs) using Pyroomacoustics (via the image source model) based on provided dimensions and RT60 or a precomputed IR file.
  
- **Source Simulation:**  
  Each source (speech and noise) is simulated individually. For music noise sources, if the signal is longer than the speech, it is clipped to match the speech duration.
  
- **Signal Processing:**  
  The simulated room signals are processed by applying the microphone model (convolution with a frequency response and addition of a noise floor).
  
- **Output:**  
  The final multi-channel output is written to a WAV file with descriptive naming.

---

## Directory Structure

```bash
project_root/
├── simulate_audio.py      # Module for simulating a single configuration.
├── simulate_all.py        # Script to iterate over all config files.
├── config/                # JSON configuration files for different scenarios.
│   ├── config1.json
│   ├── config2.json
│   ├── config3.json
│   ├── ...
│   └── config10.json
├── samples/
│   ├── speech.wav         # A mono speech recording sample.
│   └── music.wav          # A music sample for the noise source.
├── mic_models/
│   ├── freq_response.txt  # Flat, ideal frequency response (e.g., 10 taps).
│   ├── high_quality_response.txt  # 21-tap low-pass filter response.
│   └── standard_response.txt        # 11-tap smoothing filter response.
├── ir/                   # Folder for precomputed impulse response files.
│   └── room_ir.wav       # Example precomputed room impulse response.
└── output/               # Simulated output WAV files will be saved here.
```

---

## Setup and Requirements

- **Python 3.x**

- **Dependencies:**
  - numpy
  - scipy
  - pyroomacoustics
  - matplotlib

Install these dependencies using:

```bash
pip install numpy scipy pyroomacoustics matplotlib
```

---

## Running the Simulation

There are two primary ways to run the simulation:

### 1. Single Configuration

To run a single scenario using the `simulate_audio.py` module, use:

```bash
python simulate_audio.py --config config/config1.json --output output/config1_output.wav
```

This command will:
- Load settings from `config1.json`.
- Set up the room (using dimensions and RT60, or a precomputed IR if specified).
- Simulate the speech and noise sources.
- Apply the microphone model.
- Save the final multi-channel output to `output/config1_output.wav`.

### 2. Multiple Configurations

The script `simulate_all.py` iterates over all JSON configuration files in the `config/` folder (now including 10 configurations). You can run it as follows:

```bash
python simulate_all.py samples/speech.wav
```

This will:
- Override the speech file in each configuration with the provided `samples/speech.wav`.
- Simulate each scenario (from `config1.json` to `config10.json`).
- Write the output files to the `output/` folder with descriptive filenames.

---

## Sample Files and Microphone Model Files

### Audio Samples (`samples/` folder)

- **speech.wav:**  
  A mono speech recording sample (e.g., from TIMIT or CMU Arctic).
- **music.wav:**  
  A music sample for the noise source.

### Microphone Models (`mic_models/` folder)

- **freq_response.txt:** (Ideal, flat response; 10 taps)

      1.0
      0.0
      0.0
      0.0
      0.0
      0.0
      0.0
      0.0
      0.0
      0.0

- **high_quality_response.txt:** (21-tap symmetric low-pass filter)

      0.01
      0.02
      0.04
      0.08
      0.12
      0.16
      0.20
      0.22
      0.24
      0.26
      0.28
      0.26
      0.24
      0.22
      0.20
      0.16
      0.12
      0.08
      0.04
      0.02
      0.01

- **standard_response.txt:** (11-tap smoothing filter)

      0.05
      0.10
      0.15
      0.20
      0.25
      0.30
      0.25
      0.20
      0.15
      0.10
      0.05

### Precomputed IR File (`ir/` folder)

- **room_ir.wav:**  
  An example impulse response file. You can obtain free IR files from:
  - [Waves IR Convolution Reverb Library](https://www.waves.com/downloads/ir-convolution-reverb-library)
  - [RoyJames/room-impulse-responses on GitHub](https://github.com/RoyJames/room-impulse-responses)

---

## Additional Information

- **Advanced Simulation:**  
  You can extend the microphone model section with additional parameters (e.g., directional patterns, sensitivity) as required by your research.
  
- **Research Context:**  
  This framework simulates realistic acoustic environments by incorporating room acoustics, spatial noise sources, and advanced microphone characteristics—ideal for advanced research projects in acoustics and audio processing.

- **License:**  
  Specify your chosen license here (e.g., MIT License).

- **Contact and Contribution:**  
  For questions or contributions, please contact Sam Dobson.
