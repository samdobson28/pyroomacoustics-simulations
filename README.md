Below is a single Markdown file that you can copy and paste into your README.md. It includes all details—the project overview, directory structure, setup, usage, sample files, microphone model details, and guidance on where to obtain IR files.

```markdown
# Audio Simulation Package

This package implements a comprehensive simulation framework for room acoustics and audio recording scenarios. It was designed to support advanced research requirements, including:

- **Scenario Specification:**  
  Each scenario is defined in a JSON configuration file and includes:

  - **Room parameters:** Either the room dimensions with a desired reverberation time (RT60) _or_ a precomputed impulse response (IR) file.
  - **Microphone array:** Positions of the microphones.
  - **Sources:**
    - **Speech source:** Defined by its position and a path to a speech audio file.
    - **Noise sources:** Supports both music noise (via an audio file) and Gaussian noise with specified amplitude.
  - **Microphone model:** Includes a frequency response (FIR filter), sampling rate, and noise floor. This allows modeling of real-world microphone characteristics.

- **Simulation Process:**
  - The room impulse responses (RIRs) are generated using Pyroomacoustics (via the image source model).
  - Each source’s contribution is simulated individually and then mixed.
  - Microphone processing is applied (convolution with the frequency response and addition of a noise floor).
  - The final multi-channel output is saved to a WAV file with clear, descriptive naming.

---

## Directory Structure
```

project_root/
├── simulate_audio.py
├── config/
│ ├── scenario_basic.json
│ ├── scenario_precomputed_ir.json
│ └── scenario_complex.json
├── samples/
│ ├── speech.wav # A mono speech recording sample.
│ ├── music.wav # A music sample to be used as a noise source.
│ └── background_music.wav # An alternative music file (if you wish to simulate different noise environments).
├── mic_models/
│ ├── freq_response.txt # A flat, ideal frequency response (e.g., 10 taps).
│ ├── high_quality_response.txt # A 21-tap low-pass filter response (simulating a high-quality mic).
│ └── standard_response.txt # An 11-tap smoothing filter representing a typical mic response.
├── ir/
│ └── room_ir.wav # A precomputed room impulse response file (if used).
└── output/
└── (Simulated output WAV files will be written here)

````

---

## Setup and Requirements

- **Python 3.x**

- **Dependencies:**
  - `numpy`
  - `scipy`
  - `pyroomacoustics`
  - `matplotlib`

Install the dependencies with:

```bash
pip install numpy scipy pyroomacoustics matplotlib
````

---

## Running the Simulation

1. **Choose a Scenario:**  
   Edit or choose one of the JSON configuration files in the `config/` folder (e.g., `scenario_basic.json`).

2. **Run the Simulation Script:**  
   Use the following command (adjust the paths as needed):

```bash
python simulate_audio.py --config config/scenario_basic.json --output output/basic_output.wav
```

This command will:

- Load the settings from `scenario_basic.json`
- Set up the room (using dimensions and RT60, or a precomputed IR if specified)
- Add the speech and noise sources at their specified positions
- Apply the microphone model (frequency response filtering and noise floor)
- Save the final multi-channel output to `output/basic_output.wav`

3. **Other Scenarios:**  
   You can also run the precomputed IR scenario or a complex scenario:

```bash
python simulate_audio.py --config config/scenario_precomputed_ir.json --output output/precomputed_output.wav
python simulate_audio.py --config config/scenario_complex.json --output output/complex_output.wav
```

---

## Sample Files and Microphone Model Files

- **Audio Samples (`samples/`):**

  - `speech.wav`: Use any mono speech recording (e.g., from an open dataset like TIMIT or CMU Arctic).
  - `music.wav`: A music sample for the noise source.
  - `background_music.wav`: An alternative music sample to simulate different noise characteristics.  
    _Note:_ If you do not need two distinct music files, you can use the same file for both cases.

- **Microphone Models (`mic_models/`):**

  - **`freq_response.txt`:** An example of an ideal, flat response (10 taps):
    ```
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
    ```
  - **`high_quality_response.txt`:** A 21-tap symmetric low-pass filter impulse response:
    ```
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
    ```
  - **`standard_response.txt`:** An 11-tap smoothing filter:
    ```
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
    ```

- **Precomputed IR File (`ir/`):**
  - `room_ir.wav`: You can download free IR files from resources such as:
    - [Waves IR Convolution Reverb Library](https://www.waves.com/downloads/ir-convolution-reverb-library)
    - [RoyJames/room-impulse-responses on GitHub](https://github.com/RoyJames/room-impulse-responses)
      Choose one that best fits your simulation needs.

---

## Script to Run

The main script to run is **simulate_audio.py**. For example, to run the basic scenario, execute:

```bash
python simulate_audio.py --config config/scenario_basic.json --output output/basic_output.wav
```

Output files will be saved in the `output/` folder with descriptive names (e.g., `basic_output.wav`, `precomputed_output.wav`, `complex_output.wav`).

---

## Additional Information

- **Advanced Simulation:**  
  The microphone model section can be extended to include more parameters (such as directional patterns or sensitivity) based on further research.

- **Research Context:**  
  This framework is designed to help simulate realistic acoustic environments and microphone recordings, incorporating room acoustics, spatial noise sources, and advanced microphone characteristics—all critical elements for your PhD research.

- **License:**  
  Specify your chosen license here (e.g., MIT License).

- **Contact and Contribution:**  
  Feel free to modify this package to suit your research needs. For questions or contributions, please contact [Your Contact Information].
