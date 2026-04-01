# Vibrotactile Perception Study

A PyQt6-based experiment investigating cross-modal correspondences between vibrotactile stimuli and visual properties (colour and shape). Participants wear a bHaptics TactSuit X40 vest and match vibration patterns to colours and shapes across three experimental rounds.

---

## Requirements

- Python 3.10+
- [bHaptics Player](https://www.bhaptics.com/support/bhaptics-player) installed and running
- bHaptics TactSuit X40 connected and paired

---

## Installation

```bash
pip install -r requirements.txt
```

> **Note:** `bhaptics_python` may need to be installed manually. See [bHaptics developer documentation](https://developer.bhaptics.com) for details.

---

## Running the Experiment

```bash
python main.py
```

Make sure bHaptics Player is open and the vest is connected before launching.

---

## Project Structure

```
├── main.py                        # Entry point and main application controller
├── haptics_library.py             # Haptic pattern definitions and trial sequence generation
├── requirements.txt
│
├── assets/
│   └── shapes/svg/                # SVG shape files (kiki-bouba-1 copy.svg to kiki-bouba-20 copy.svg)
│
├── data/
│   ├── demographics.py            # DemographicsData dataclass
│   └── trial.py                   # TrialData dataclass
│
├── screens/
│   ├── demographics_screen.py     # Participant ID, age, gender input
│   ├── instructions_screen.py     # General study instructions
│   ├── round_instruction_screen.py# Per-round instruction screens
│   ├── playback_screen.py         # Haptic pattern playback with trial counter
│   ├── color_screen.py            # Colour selection task (Round 1)
│   ├── shape_screen.py            # Shape slider task (Round 2)
│   ├── combined_screen.py         # Combined colour + shape task (Round 3)
│   ├── practice_complete_screen.py# Transition screen after practice trials
│   ├── break_screen.py            # Timed break screen between rounds
│   ├── post_experiment_screen.py  # Optional post-session questionnaire
│   ├── completion_screen.py       # End screen with save/restart options
│   └── color_tile.py              # Reusable clickable colour tile widget
│
├── utils/
│   ├── colors.py                  # HSL colour scale generation
│   ├── csv_manager.py             # Trial-by-trial CSV saving
│   ├── haptics.py                 # bHaptics playback wrappers
│   └── theming.py                 # Global Qt stylesheet
│
└── tests/
    ├── test_bhaptics.py           # Shape screen test without main app
    ├── test_library.py            # Haptic library playback test
    ├── test_svg.py                # SVG rendering test
    └── test_window.py             # Basic Qt window test
```

---

## Experiment Design

### Session Flow

1. Demographics (participant ID, age, gender)
2. General instructions
3. Round 1 + 4 practice trials
4. 3-minute break
5. Round 2 + 4 practice trials
6. 3-minute break
7. Round 3 + 4 practice trials
8. Post-experiment questionnaire
9. Data saved to CSV

Total session duration: approximately 45–60 minutes.

### Rounds

| Round | Stimulus Variation | Response | Trials |
|-------|-------------------|----------|--------|
| 1 – Colour | Intensity only (10 levels, 10%–100%) | Colour hue + brightness | 30 |
| 2 – Shape | vibrotactile pattern only (6 patterns, constant 60% intensity) | Shape slider (1–20) | 18 |
| 3 – Combined | Intensity × vibrotactile pattern (3 × 6) | Colour + shape | 54 |

All trials use block randomization: each unique stimulus appears once per block before any repetitions.

---

### Round 1 – Colour

**What varies:** Vibration intensity only. The same single pattern (`color`) is played at 10 intensity levels (10%, 20%, ..., 100%), each repeated 3 times, for 30 trials total.

**What participants do:** After each vibration, they select one colour tile from a palette of 10 hues × 11 brightness levels. The row order is reshuffled on every trial to prevent position bias.

**What it measures:** Whether vibration intensity maps systematically to perceived colour brightness or hue. This round isolates intensity as the sole independent variable, so any observed colour-brightness relationship can be attributed specifically to intensity rather than to vibrotactile pattern differences.

**Dependent variables recorded:** `color_hue` (one of 10 hue labels) and `color_brightness` (integer 0–10, where 0 is darkest and 10 is lightest).

---

### Round 2 – Shape

**What varies:** vibrotactile activation pattern only. Six distinct patterns vary in where and how actuators fire across the vest. Intensity is held constant at 60% for all trials. Each pattern is repeated 3 times, for 18 trials total.

**What participants do:** After each vibration, they drag a slider to select one of 20 shapes ranging from angular/spiky (position 1, kiki-like) to smooth/rounded (position 20, bouba-like). The selected shape is displayed in real time as the slider moves.

**What it measures:** Whether different vibrotactile activation patterns map to different shape roundness. Patterns with discrete, abrupt, or spatially sparse activation are expected to associate with angular shapes; patterns with continuous and flowing  activation are expected to associate with rounded shapes. This round isolates vibrotactile structure while intensity is held constant.

**The six patterns:**

| Pattern name | Expected character |
|---|---|
| `expansion_bouba1` | Continuous, outward-spreading — expected: rounded |
| `circular_bouba2` | Circular sweep, smooth — expected: rounded |
| `inward_bouba3` | Continuous, inward-converging — expected: rounded |
| `diagonal_spiky3` | Diagonal, abrupt — expected: angular |
| `corner_spiky1` | Corner-activated, sparse — expected: angular |
| `star_spiky1` | Radiating, discrete bursts — expected: angular |

**Dependent variable recorded:** `shape_value` (integer 1–20).

---

### Round 3 – Combined

**What varies:** Both intensity and vibrotactile pattern simultaneously. Three intensity levels (low = 20%, medium = 60%, high = 100%) are fully crossed with the same six vibrotactile patterns, yielding 18 unique stimulus combinations, each repeated 3 times, for 54 trials total.

**What participants do:** After each vibration, they select both a colour (same palette as Round 1) and a shape (same slider as Round 2). The selected shape is filled with the chosen colour in real time, giving a combined visual preview. Both responses must be given before continuing.

**What it measures:** Whether intensity-to-colour and pattern-to-shape mappings from Rounds 1 and 2 hold up when both dimensions vary simultaneously, and whether the two mappings operate independently of each other. 

**Dependent variables recorded:** `color_hue`, `color_brightness`, and `shape_value`.

### Counterbalancing

Round order is counterbalanced by participant number:
- **Odd participant IDs:** Colour → Shape → Combined
- **Even participant IDs:** Shape → Colour → Combined

Combined is always the final round.

### Stimuli

**Intensity levels (Round 1 & 3):** 10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%, 100%

**Vibrotactile patterns (Round 2 & 3):**
- `expansion_bouba1`
- `circular_bouba2`
- `inward_bouba3`
- `diagonal_spiky3`
- `corner_spiky1`
- `star_spiky1`

Patterns are created in [bHaptics Designer](https://designer.bhaptics.com) and deployed to the local bHaptics Player.

**Colours:** 11 brightness levels × 10 hues (blue, brown, green, pink, purple, yellow, red, aqua, darkblue, orange) + greyscale. Row order is reshuffled on every trial.

**Shapes:** 20 SVG shapes on a continuous slider from angular (kiki-like) to rounded (bouba-like).

---

## Data Output

A CSV file is created automatically when the session starts and is written to after every trial. It is saved in the working directory as:

```
experiment_data_<participant_id>_<timestamp>.csv
```

### CSV Columns

| Column | Description |
|--------|-------------|
| `participant_id` | Coded participant identifier |
| `age` | Participant age |
| `gender` | Participant gender |
| `round` | `color`, `shape`, or `combined` |
| `trial` | Trial number within the round |
| `pattern_name` | bHaptics event name |
| `pattern_intensity` | Intensity (0.0–1.0) |
| `color_hue` | Selected colour hue (Rounds 1 and 3) |
| `color_brightness` | Brightness index 0–10 (Rounds 1 and 3) |
| `shape_value` | Slider position 1–20 (Rounds 2 and 3) |
| `timestamp` | Unix timestamp of response |

Post-experiment questionnaire responses are appended as a separate section at the end of the same CSV file.

An optional JSON export (full session backup) is available from the completion screen.

---

## Testing Without Hardware

If `bhaptics_python` is not installed or the vest is not connected, the program runs in simulation mode. Vibration calls are logged to the console and the timing proceeds normally. This allows testing the full UI flow without hardware.

The `tests/` folder contains standalone scripts for testing individual components.

---

## Notes

- Press **S** during any screen to skip the current round or practice block (testing only).
- The break timer can also be skipped with **S**.
- Trial sequences are generated at startup so the randomization is fixed for the full session.
- Practice data is discarded and never written to CSV.
- bHaptics credentials (`APP_ID`, `API_KEY`) are stored in `utils/haptics.py`.
