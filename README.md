Below is an updated README in Markdown format. You can copy and paste it into your README.md file and adjust as needed.

---

````markdown
# Audio Simulation Package

This package implements a comprehensive framework for simulating room acoustics and audio recording scenarios. It supports two modes for applying room impulse responses (RIRs) to speech and noise signals:

1. **Precomputed RIR Mode**  
   In this mode, the simulation uses precomputed impulse responses (IRs) located in the `ir/` folder. These IRs are “narrow impulse” responses (i.e. high-energy, short-duration events that capture the room's acoustic characteristics) sourced from the [OpenSLR #28 dataset](https://www.openslr.org/28/). The precomputed IR files currently available are:

   - `RVB2014_type2_rir_simroom1_near_angla.wav`
   - `RWCP_type4_rir_p30r.wav`
   - `RWCP_type2_rir_cirline_ofc_imp090.wav`
   - `air_type1_air_binaural_stairway_1_2_60.wav`

   **Configuration:**

   - Config files such as `config11.json` and `config12.json` use this mode.
   - In these config files, the `"room"` section should set `"dimensions"` and `"rt60"` to `null` and specify the `"ir_file"` path (e.g., `"ir/RVB2014_type2_rir_simroom1_near_angla.wav"`).
   - The simulation will load the precomputed IR and convolve it with the speech (and noise) signals.

2. **PyroomAcoustics Simulated RIR Mode**  
   In this mode, the simulation generates the room impulse response on the fly using PyroomAcoustics.
   - You specify the room dimensions and a desired reverberation time (`rt60`) in the config file.
   - This mode also supports the inclusion of music and Gaussian noise sources.
   - Config files such as `config1.json` through `config10.json` use this mode.

---

## Directory Structure

```bash
project_root/
├── simulate_audio.py      # Module for simulating a single configuration.
├── simulate_all.py        # Script that iterates over all config files.
├── analyze.py             # (Optional) Module for analyzing simulation outputs.
├── config/                # JSON configuration files for different scenarios.
│   ├── config1.json       # Example: Simulated RIR via PyroomAcoustics.
│   ├── config2.json
│   ├── ...
│   ├── config10.json
│   ├── config11.json      # Example: Precomputed RIR mode.
│   └── config12.json      # Example: Precomputed RIR mode.
├── ir/                   # Precomputed impulse response (IR) files.
│   ├── RVB2014_type2_rir_simroom1_near_angla.wav
│   ├── RWCP_type4_rir_p30r.wav
│   ├── RWCP_type2_rir_cirline_ofc_imp090.wav
│   └── air_type1_air_binaural_stairway_1_2_60.wav
├── samples/              # Audio samples for sources.
│   ├── speech1.wav        # A sample speech file.
│   └── music.wav          # A sample music noise file.
├── mic_models/           # Microphone model files (frequency responses).
│   ├── freq_response.txt
│   ├── high_quality_response.txt
│   └── standard_response.txt
└── output/               # Simulated output WAV files will be saved here.
```
````

---

## Usage

### Single Configuration Simulation

Run a single simulation using a specific configuration file:

```bash
python simulate_audio.py --config config/config1.json --output output/config1_output.wav
```

- **Input:** A JSON config file (e.g., `config/config1.json`).
- **Output:** A multi-channel WAV file with the simulated, convolved audio saved in the `output/` folder.

### Batch Simulation

Simulate all scenarios in the `config/` folder with a specified speech file:

```bash
python simulate_all.py samples/speech1.wav
```

- **Input:** A speech file (e.g., `samples/speech1.wav`) that overrides the speech file specified in each config.
- **Output:** WAV files named `<speechName>-<configName>-out.wav` saved in the `output/` folder.

---

## RIR Options

### Precomputed RIRs

- **Location:** `ir/` folder.
- **Files:**
  - `RVB2014_type2_rir_simroom1_near_angla.wav`
  - `RWCP_type4_rir_p30r.wav`
  - `RWCP_type2_rir_cirline_ofc_imp090.wav`
  - `air_type1_air_binaural_stairway_1_2_60.wav`
- **Usage:**  
  Configure the `"room"` section in your JSON as follows:
  ```json
  "room": {
    "dimensions": null,
    "rt60": null,
    "ir_file": "ir/RVB2014_type2_rir_simroom1_near_angla.wav"
  }
  ```
  This mode uses a precomputed, narrow impulse response (a “one-click” IR) from the OpenSLR #28 dataset. The IR is convolved with the entire speech (and noise) signal to simulate the room acoustics.

### PyroomAcoustics Simulated RIRs

- **Usage:**  
  Configure the `"room"` section with the room dimensions and desired `rt60`:
  ```json
  "room": {
    "dimensions": [6, 5, 3],
    "rt60": 0.4,
    "ir_file": null
  }
  ```
  In this mode, PyroomAcoustics generates the RIR based on the specified dimensions and reverberation time. This mode also supports additional music or Gaussian noise sources.

---

## Dependencies

- Python 3.x
- numpy
- scipy
- pyroomacoustics
- matplotlib (for any analysis/visualization)

Install the dependencies with:

```bash
pip install numpy scipy pyroomacoustics matplotlib
```

---

## Contact

For questions or contributions, please contact Sam Dobson, sed2191@columbia.edu.

```

---

This updated README emphasizes the two RIR modes, explains the corresponding config files, and provides clear usage instructions. Let me know if you need any further modifications!
```
