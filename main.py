import sys
import json
import time
from dataclasses import asdict
from typing import List

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt

from data.demographics import DemographicsData
from data.trial import TrialData

from screens.demographics_screen import DemographicsScreen
from screens.instructions_screen import InstructionsScreen
from screens.round_instruction_screen import (
    RoundInstructionScreen,
    COLOR_ROUND_INSTRUCTIONS,
    SHAPE_ROUND_INSTRUCTIONS,
    COMBINED_ROUND_INSTRUCTIONS
)
from screens.practice_complete_screen import PracticeCompleteScreen
from screens.shape_screen import ShapeRatingScreen
from screens.color_screen import ColorRatingScreen
from screens.combined_screen import CombinedRatingScreen
from screens.completion_screen import CompletionScreen
from screens.playback_screen import PatternPlaybackScreen
from screens.break_screen import BreakScreen
from screens.post_experiment_screen import PostExperimentScreen

from utils.haptics import play_vibration_pattern
from utils.theming import set_light_theme
from utils.csv_manager import CSVDataManager
from haptics_library import HapticsLibrary


class ExperimentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vibrotactile Perception Study")
        self.resize(1000, 700)

        # Generate all trial sequences upfront so the order is fixed before the session starts
        self.haptics_lib = HapticsLibrary()
        self.practice_patterns_color = self.haptics_lib.create_practice_trials_color()
        self.practice_patterns_shape = self.haptics_lib.create_practice_trials_shape()
        self.practice_patterns_combined = self.haptics_lib.create_practice_trials_combined()
        self.color_patterns = self.haptics_lib.create_color_round()
        self.shape_patterns = self.haptics_lib.create_shape_round()
        self.combined_patterns = self.haptics_lib.create_combined_round()

        # Track whether we're in practice mode and which trial we're on
        self.is_practice = False
        self.practice_trial = 1
        self.practice_total_color = len(self.practice_patterns_color)    # 4
        self.practice_total_shape = len(self.practice_patterns_shape)    # 4
        self.practice_total_combined = len(self.practice_patterns_combined)  # 4

        self.phase = "color"
        self.color_total = len(self.color_patterns)      # 30 trials
        self.shape_total = len(self.shape_patterns)      # 18 trials
        self.combined_total = len(self.combined_patterns)  # 54 trials

        self.color_trial = 1
        self.shape_trial = 1
        self.combined_trial = 1

        self.demographics: DemographicsData | None = None
        self.responses: List[TrialData] = []
        self.post_experiment_responses: dict = {}
        self.csv_manager: CSVDataManager | None = None

        # Counterbalancing: odd participants do Color, Shape, Combined, and even participants do Shape, Color, Combined
        self.is_odd_participant = True

        self.current_pattern = None
        self.next_screen = None

        # All screens are loaded into a QStackedWidget and swapped in/out during the session
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.screen_demographics = DemographicsScreen(self.on_demographics_complete)
        self.screen_instructions = InstructionsScreen(self.on_instructions_complete)
        self.screen_color_instructions = RoundInstructionScreen(self.on_color_instructions_complete)
        self.screen_shape_instructions = RoundInstructionScreen(self.on_shape_instructions_complete)
        self.screen_combined_instructions = RoundInstructionScreen(self.on_combined_instructions_complete)
        self.screen_practice_complete = PracticeCompleteScreen(self.on_practice_complete)
        self.screen_playback = PatternPlaybackScreen(
            on_finished=self._playback_finished,
            play_vibration=play_vibration_pattern,
        )
        self.screen_color = ColorRatingScreen(self.on_color_rating_complete)
        self.screen_shape = ShapeRatingScreen(self.on_shape_rating_complete, play_vibration_pattern)
        self.screen_combined = CombinedRatingScreen(self.on_combined_rating_complete)
        self.screen_post_experiment = PostExperimentScreen(self.on_post_experiment_complete)
        self.screen_complete = CompletionScreen(self.save_data, self.restart_experiment)

        self.stack.addWidget(self.screen_demographics)
        self.stack.addWidget(self.screen_instructions)
        self.stack.addWidget(self.screen_color_instructions)
        self.stack.addWidget(self.screen_shape_instructions)
        self.stack.addWidget(self.screen_combined_instructions)
        self.stack.addWidget(self.screen_practice_complete)
        self.stack.addWidget(self.screen_playback)
        self.stack.addWidget(self.screen_color)
        self.stack.addWidget(self.screen_shape)
        self.stack.addWidget(self.screen_combined)
        self.stack.addWidget(self.screen_post_experiment)
        self.stack.addWidget(self.screen_complete)

        self.show_demographics()

    def _get_round_order_string(self):
        if self.is_odd_participant:
            return "Color -> Shape -> Combined"
        else:
            return "Shape -> Color -> Combined"

    def show_demographics(self):
        # Reset all trial counters when starting a new session
        self.phase = "color"
        self.color_trial = 1
        self.shape_trial = 1
        self.combined_trial = 1
        self.is_practice = False
        self.practice_trial = 1
        self.stack.setCurrentWidget(self.screen_demographics)

    def show_instructions(self):
        self.stack.setCurrentWidget(self.screen_instructions)

    def show_playback_then(self, next_screen_name: str):
        """
        Trigger the vibration for the current trial, then automatically advance
        to the rating screen once playback finishes. The correct pattern is looked
        up from the pre-generated sequence based on the current phase and trial number.
        """
        self.next_screen = next_screen_name

        if self.is_practice:
            if self.phase == "color":
                self.current_pattern = self.practice_patterns_color[self.practice_trial - 1]
                self.screen_playback.set_trial_info(self.practice_trial, self.practice_total_color)
            elif self.phase == "shape":
                self.current_pattern = self.practice_patterns_shape[self.practice_trial - 1]
                self.screen_playback.set_trial_info(self.practice_trial, self.practice_total_shape)
            elif self.phase == "combined":
                self.current_pattern = self.practice_patterns_combined[self.practice_trial - 1]
                self.screen_playback.set_trial_info(self.practice_trial, self.practice_total_combined)
        elif self.phase == "color":
            self.current_pattern = self.color_patterns[self.color_trial - 1]
            self.screen_playback.set_trial_info(self.color_trial, self.color_total)
        elif self.phase == "shape":
            self.current_pattern = self.shape_patterns[self.shape_trial - 1]
            self.screen_playback.set_trial_info(self.shape_trial, self.shape_total)
        elif self.phase == "combined":
            self.current_pattern = self.combined_patterns[self.combined_trial - 1]
            self.screen_playback.set_trial_info(self.combined_trial, self.combined_total)

        self.screen_playback.set_pattern(self.current_pattern)
        self.stack.setCurrentWidget(self.screen_playback)
        self.screen_playback.start()

    def _playback_finished(self):
        # Called automatically after the vibration ends, routes to the right rating screen
        if self.next_screen == "color":
            self.show_color()
        elif self.next_screen == "shape":
            self.show_shape()
        elif self.next_screen == "combined":
            self.show_combined()

    def show_color(self):
        if self.is_practice:
            self.screen_color.set_trial_info(self.practice_trial, self.practice_total_color)
        else:
            self.screen_color.set_trial_info(self.color_trial, self.color_total)
        self.stack.setCurrentWidget(self.screen_color)

    def show_shape(self):
        if self.is_practice:
            self.screen_shape.set_trial_info(self.practice_trial, self.practice_total_shape)
        else:
            self.screen_shape.set_trial_info(self.shape_trial, self.shape_total)
        self.stack.setCurrentWidget(self.screen_shape)

    def show_combined(self):
        if self.is_practice:
            self.screen_combined.set_trial_info(self.practice_trial, self.practice_total_combined)
        else:
            self.screen_combined.set_trial_info(self.combined_trial, self.combined_total)
        self.stack.setCurrentWidget(self.screen_combined)

    def show_break_to_second_round(self):
        # The destination after the break depends on which group the participant is in
        if self.is_odd_participant:
            self.screen_break = BreakScreen(self.show_shape_round_instructions)
        else:
            self.screen_break = BreakScreen(self.show_color_round_instructions)
        self.stack.addWidget(self.screen_break)
        self.stack.setCurrentWidget(self.screen_break)

    def show_break_to_combined(self):
        # Combined is always the final round for both groups
        self.screen_break = BreakScreen(self.show_combined_round_instructions)
        self.stack.addWidget(self.screen_break)
        self.stack.setCurrentWidget(self.screen_break)

    def start_shape_trials(self):
        self.phase = "shape"
        self.shape_trial = 1
        self.show_playback_then("shape")

    def start_combined_trials(self):
        self.phase = "combined"
        self.combined_trial = 1
        self.show_playback_then("combined")

    def show_complete(self):
        pid = self.demographics.participant_id if self.demographics else "unknown"
        self.screen_complete.set_summary(pid, len(self.responses))
        if self.csv_manager:
            csv_path = self.csv_manager.get_filepath()
            print(f"\n✓ All data saved to: {csv_path}\n")
        self.stack.setCurrentWidget(self.screen_complete)

    def show_post_experiment(self):
        self.screen_post_experiment.reset()
        self.stack.setCurrentWidget(self.screen_post_experiment)

    def show_practice_complete(self):
        # Update the transition screen text to match whichever round just finished
        if self.phase == "color":
            self.screen_practice_complete.set_round_info("Colour")
        elif self.phase == "shape":
            self.screen_practice_complete.set_round_info("Shape")
        elif self.phase == "combined":
            self.screen_practice_complete.set_round_info("Combined")
        self.stack.setCurrentWidget(self.screen_practice_complete)

    def on_practice_complete(self):
        # Participant clicked "begin main round" - flip off practice mode and start for real
        self.is_practice = False
        if self.phase == "color":
            self.color_trial = 1
            self.show_playback_then("color")
        elif self.phase == "shape":
            self.shape_trial = 1
            self.show_playback_then("shape")
        elif self.phase == "combined":
            self.combined_trial = 1
            self.show_playback_then("combined")

    def on_demographics_complete(self, demo: DemographicsData):
        """
        Called when the participant submits their demographics
        Determines counterbalancing group from the participant ID number,
        creates the CSV file, and moves to the instructions screen.
        """
        self.demographics = demo

        # Derive odd/even group from the numeric part of the participant ID
        pid_str = str(demo.participant_id)
        numeric_id = ''.join(filter(str.isdigit, pid_str))

        if numeric_id:
            participant_number = int(numeric_id)
            self.is_odd_participant = (participant_number % 2 == 1)
            group_reason = f"Standard (ID {participant_number} % 2 = {'odd' if self.is_odd_participant else 'even'})"
        else:
            self.is_odd_participant = True
            group_reason = "No numeric ID found → defaulting to ODD"
            print(f"⚠ Warning: No numeric ID found in '{pid_str}', defaulting to ODD")

        print(f"{'='*60}")
        print(f"Participant ID: {demo.participant_id}")
        print(f"Group: {'ODD' if self.is_odd_participant else 'EVEN'}")
        print(f"Round Order: {self._get_round_order_string()}")
        print(f"{'='*60}\n")

        # Create the CSV file immediately so data is never lost mid-session
        self.csv_manager = CSVDataManager(
            participant_id=demo.participant_id,
            age=demo.age,
            gender=demo.gender
        )

        self.show_instructions()

    def on_instructions_complete(self):
        # Route to the first round based on counterbalancing group
        if self.is_odd_participant:
            self.phase = "color"
            self.show_color_round_instructions()
        else:
            self.phase = "shape"
            self.show_shape_round_instructions()

    def show_color_round_instructions(self):
        # The round number shown to the participant depends on their group order
        round_name = "Round 1: Colour" if self.is_odd_participant else "Round 2: Colour"
        self.screen_color_instructions.set_round_info(round_name, COLOR_ROUND_INSTRUCTIONS)
        self.stack.setCurrentWidget(self.screen_color_instructions)

    def on_color_instructions_complete(self):
        self.is_practice = True
        self.practice_trial = 1
        self.phase = "color"
        self.show_playback_then("color")

    def show_shape_round_instructions(self):
        round_name = "Round 2: Shape" if self.is_odd_participant else "Round 1: Shape"
        self.screen_shape_instructions.set_round_info(round_name, SHAPE_ROUND_INSTRUCTIONS)
        self.stack.setCurrentWidget(self.screen_shape_instructions)

    def on_shape_instructions_complete(self):
        self.is_practice = True
        self.practice_trial = 1
        self.phase = "shape"
        self.show_playback_then("shape")

    def show_combined_round_instructions(self):
        self.screen_combined_instructions.set_round_info(
            "Round 3: Combined",
            COMBINED_ROUND_INSTRUCTIONS
        )
        self.stack.setCurrentWidget(self.screen_combined_instructions)

    def on_combined_instructions_complete(self):
        self.is_practice = True
        self.practice_trial = 1
        self.phase = "combined"
        self.show_playback_then("combined")

    def on_color_rating_complete(self, hue: str, brightness_idx: int):
        """
        Called when the participant selects a colour. If in practice mode the
        response is discarded. Otherwise it's saved to memory and immediately
        written to the CSV file, then the next trial begins.
        """
        timestamp = time.time()

        if self.is_practice:
            print(f"Color practice trial {self.practice_trial} completed (not saved)")
            if self.practice_trial < self.practice_total_color:
                self.practice_trial += 1
                self.show_playback_then("color")
            else:
                self.show_practice_complete()
        else:
            self.responses.append(
                TrialData(
                    phase="color",
                    trial=self.color_trial,
                    pattern_event_name=self.current_pattern.event_name,
                    pattern_intensity=self.current_pattern.intensity,
                    shape_angularity=None,
                    shape_color=f"{hue}_{brightness_idx}",
                    combined_angularity=None,
                    combined_color=None,
                    timestamp=timestamp,
                )
            )

            if self.csv_manager:
                self.csv_manager.save_trial(
                    round_name="color",
                    trial_number=self.color_trial,
                    pattern_name=self.current_pattern.event_name,
                    pattern_intensity=self.current_pattern.intensity,
                    color_hue=hue,
                    color_brightness=brightness_idx,
                    shape_value=None,
                    timestamp=timestamp
                )

            if self.color_trial < self.color_total:
                self.color_trial += 1
                self.show_playback_then("color")
            else:
                if self.is_odd_participant:
                    self.show_break_to_second_round()
                else:
                    self.show_break_to_combined()

    def on_shape_rating_complete(self, angularity: int):
        """
        Called when the participant moves the shape slider and confirms and data is saved immediately to CSV file.
        """
        timestamp = time.time()

        if self.is_practice:
            print(f"Shape practice trial {self.practice_trial} completed (not saved)")
            if self.practice_trial < self.practice_total_shape:
                self.practice_trial += 1
                self.show_playback_then("shape")
            else:
                self.show_practice_complete()
        else:
            self.responses.append(
                TrialData(
                    phase="shape",
                    trial=self.shape_trial,
                    pattern_event_name=self.current_pattern.event_name,
                    pattern_intensity=self.current_pattern.intensity,
                    shape_angularity=angularity,
                    shape_color=None,
                    combined_angularity=None,
                    combined_color=None,
                    timestamp=timestamp,
                )
            )

            if self.csv_manager:
                self.csv_manager.save_trial(
                    round_name="shape",
                    trial_number=self.shape_trial,
                    pattern_name=self.current_pattern.event_name,
                    pattern_intensity=self.current_pattern.intensity,
                    color_hue=None,
                    color_brightness=None,
                    shape_value=angularity,
                    timestamp=timestamp
                )

            if self.shape_trial < self.shape_total:
                self.shape_trial += 1
                self.show_playback_then("shape")
            else:
                if self.is_odd_participant:
                    self.show_break_to_combined()
                else:
                    self.show_break_to_second_round()

    def on_combined_rating_complete(self, angularity: int, hue: str, brightness_idx: int):
        """
        Called when the participant confirms both a colour and shape in the combined round
        Both responses are stored together in a single trial record
        """
        timestamp = time.time()

        if self.is_practice:
            print(f"Combined practice trial {self.practice_trial} completed (not saved)")
            if self.practice_trial < self.practice_total_combined:
                self.practice_trial += 1
                self.show_playback_then("combined")
            else:
                self.show_practice_complete()
        else:
            self.responses.append(
                TrialData(
                    phase="combined",
                    trial=self.combined_trial,
                    pattern_event_name=self.current_pattern.event_name,
                    pattern_intensity=self.current_pattern.intensity,
                    shape_angularity=None,
                    shape_color=None,
                    combined_angularity=angularity,
                    combined_color=f"{hue}_{brightness_idx}",
                    timestamp=timestamp,
                )
            )

            if self.csv_manager:
                self.csv_manager.save_trial(
                    round_name="combined",
                    trial_number=self.combined_trial,
                    pattern_name=self.current_pattern.event_name,
                    pattern_intensity=self.current_pattern.intensity,
                    color_hue=hue,
                    color_brightness=brightness_idx,
                    shape_value=angularity,
                    timestamp=timestamp
                )

            if self.combined_trial < self.combined_total:
                self.combined_trial += 1
                self.show_playback_then("combined")
            else:
                self.show_post_experiment()

    def on_post_experiment_complete(self, responses: dict):
        self.post_experiment_responses = responses
        if self.csv_manager:
            self.csv_manager.add_post_experiment_questionnaire(responses)
        self.show_complete()

    def save_data(self):
        """
        Exports all session data to JSON (and a matching CSV) via a save dialog.
        The CSV is already written trial-by-trial during the session, so this
        JSON export is mainly for a complete structured backup.
        """
        if not self.demographics:
            return

        data = {
            "demographics": asdict(self.demographics),
            "counterbalancing": {
                "is_odd_participant": self.is_odd_participant,
                "round_order": self._get_round_order_string()
            },
            "responses": [asdict(t) for t in self.responses],
            "post_experiment_questionnaire": self.post_experiment_responses,
            "completedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }

        filename = f"experiment-data-{self.demographics.participant_id}-{int(time.time())}.json"
        path, _ = QFileDialog.getSaveFileName(self, "Save data", filename, "JSON files (*.json)")

        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        csv_path = path.replace('.json', '.csv')
        self._export_to_csv(csv_path)

        QMessageBox.information(self, "Saved", f"Data saved to:\n{path}\n{csv_path}")

    def _export_to_csv(self, csv_path: str):
        import csv
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'participant_id', 'age', 'gender', 'counterbalancing_group',
                'phase', 'trial', 'pattern_event_name', 'pattern_intensity',
                'shape_angularity', 'shape_color', 'combined_angularity',
                'combined_color', 'timestamp'
            ])
            for trial in self.responses:
                writer.writerow([
                    self.demographics.participant_id,
                    self.demographics.age,
                    self.demographics.gender,
                    'ODD' if self.is_odd_participant else 'EVEN',
                    trial.phase,
                    trial.trial,
                    trial.pattern_event_name,
                    trial.pattern_intensity,
                    trial.shape_angularity if trial.shape_angularity else '',
                    trial.shape_color if trial.shape_color else '',
                    trial.combined_angularity if trial.combined_angularity else '',
                    trial.combined_color if trial.combined_color else '',
                    trial.timestamp
                ])

    def restart_experiment(self):
        # Clear everything so the next participant starts completely fresh
        self.responses = []
        self.csv_manager = None
        self.show_demographics()

    def keyPressEvent(self, event):
        # Press 'S' during any screen to skip to the end of the current round (used for testing purposes only)
        if event.key() == Qt.Key.Key_S:
            if self.is_practice:
                if self.phase == "color":
                    print(f" SKIP: Color practice (was at trial {self.practice_trial}/{self.practice_total_color})")
                elif self.phase == "shape":
                    print(f" SKIP: Shape practice (was at trial {self.practice_trial}/{self.practice_total_shape})")
                elif self.phase == "combined":
                    print(f" SKIP: Combined practice (was at trial {self.practice_trial}/{self.practice_total_combined})")
                self.show_practice_complete()
            elif self.phase == "color":
                print(f" SKIP: Color round (was at trial {self.color_trial}/{self.color_total})")
                if self.is_odd_participant:
                    self.show_break_to_second_round()
                else:
                    self.show_break_to_combined()
            elif self.phase == "shape":
                print(f" SKIP: Shape round (was at trial {self.shape_trial}/{self.shape_total})")
                if self.is_odd_participant:
                    self.show_break_to_combined()
                else:
                    self.show_break_to_second_round()
            elif self.phase == "combined":
                print(f" SKIP: Combined round (was at trial {self.combined_trial}/{self.combined_total})")
                self.show_post_experiment()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    set_light_theme(app)
    window = ExperimentApp()
    window.show()
    sys.exit(app.exec())