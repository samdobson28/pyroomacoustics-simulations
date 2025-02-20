# Audio Simulation Package

This package implements a comprehensive simulation framework for room acoustics and audio recording scenarios. It supports advanced research requirements by allowing you to define scenarios using JSON files that specify:

- **Room Parameters:** Either the room dimensions with a desired reverberation time (RT60) _or_ a precomputed impulse response (IR) file.
- **Microphone Array:** Positions of the microphones.
- **Sources:**
  - **Speech Source:** A primary speech signal with its position and file path.
  - **Noise Sources:** Supports both music noise (via an audio file) and Gaussian noise with a specified amplitude.
- **Microphone Model:** Defines a frequency response (FIR filter), sampling rate, and noise floor to simulate real-world microphone characteristics.

**Simulation Process:**

- Room impulse responses (RIRs) are generated using Pyroomacoustics (via the image source model).
- Each source’s contribution is simulated individually and then mixed.
- Microphone processing is applied (convolution with the frequency response and addition of a noise floor).
- The final multi-channel output is saved to a WAV file with clear, descriptive naming.

---

## Directory Structure
```bash
project_root/
├── simulate_audio.py
├── config/
│ ├── config1.json
│ ├── config2.json
│ └── config3.json
│ └── ...
├── samples/
│ ├── speech.wav # A mono speech recording sample.
│ ├── music.wav # A music sample to be used as a noise source.
├── mic_models/
│ ├── freq_response.txt # A flat, ideal frequency response (e.g., 10 taps).
│ ├── high_quality_response.txt # A 21-tap low-pass filter response (simulating a high-quality mic).
│ └── standard_response.txt # An 11-tap smoothing filter representing a typical mic response.
├── ir/
│ └── room_ir.wav # A precomputed room impulse response file (if used).
└── output/
└── (Simulated output WAV files will be saved here)
```
---

## Setup and Requirements

- **Python 3.x**

- **Dependencies:**
  - numpy
  - scipy
  - pyroomacoustics
  - matplotlib

Install these dependencies with:

    pip install numpy scipy pyroomacoustics matplotlib

---

## Running the Simulation

1. **Select a Scenario:**  
   Choose or edit one of the JSON configuration files in the `config/` folder (e.g., `scenario_basic.json`).

2. **Execute the Simulation Script:**  
   Run the script from the command line. For example, to run the basic scenario:

   python simulate_audio.py --config config/scenario_basic.json --output output/basic_output.wav

   This command will:

   - Load settings from `scenario_basic.json`.
   - Set up the room (using dimensions and RT60, or a precomputed IR if specified).
   - Add the speech and noise sources.
   - Apply the microphone model (frequency response filtering and noise floor).
   - Write the final multi-channel output to `output/basic_output.wav`.

3. **Additional Scenarios:**  
   You can also run the precomputed IR or complex scenarios:

   python simulate_audio.py --config config/scenario_precomputed_ir.json --output output/precomputed_output.wav
   python simulate_audio.py --config config/scenario_complex.json --output output/complex_output.wav

---

## Sample Files and Microphone Model Files

### Audio Samples (`samples/` folder)

- **speech.wav:**  
  Use any mono speech recording (e.g., from TIMIT or CMU Arctic).
- **music.wav:**  
  A music sample for the noise source.
- **background_music.wav:**  
  An alternative music sample to simulate different noise environments.  
  _Note:_ If you don't need two distinct music files, you can duplicate `music.wav`.

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
  Download a free IR file from resources such as:
  - [Waves IR Convolution Reverb Library](https://www.waves.com/downloads/ir-convolution-reverb-library)
  - [RoyJames/room-impulse-responses on GitHub](https://github.com/RoyJames/room-impulse-responses)  
    Choose one that fits your simulation needs.

---

## Script to Run

The main script is **simulate_audio.py**. To run the basic scenario, execute:

    python simulate_audio.py --config config/scenario_basic.json --output output/basic_output.wav

The output file will be saved in the `output/` folder with descriptive names (e.g., `basic_output.wav`, `precomputed_output.wav`, `complex_output.wav`).

---

## Additional Information

- **Advanced Simulation:**  
  The microphone model section can be extended with additional parameters (e.g., directional patterns, sensitivity) based on further research.

- **Research Context:**  
  This framework simulates realistic acoustic environments by incorporating room acoustics, spatial noise sources, and advanced microphone characteristics—critical elements for advanced research projects.

- **License:**  
  Specify your chosen license here (e.g., MIT License).

- **Contact and Contribution:**  
  Feel free to modify this package to suit your research needs. For questions or contributions, please contact [Your Contact Information].

---
