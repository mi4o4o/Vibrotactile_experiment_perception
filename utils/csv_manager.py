"""
CSV Data Manager - Handles automatic saving of trial data
Saves after each trial to prevent data loss
"""

import csv
import os
from datetime import datetime
from typing import Optional


class CSVDataManager:
    """Manages CSV file creation and automatic trial-by-trial saving"""
    
    def __init__(self, participant_id: str, age: int, gender: str):
        """
        Initialize CSV file for this participant.
        Creates the file immediately with headers and demographics.
        
        Args:
            participant_id: Unique participant identifier
            age: Participant's age
            gender: Participant's gender
        """
        self.participant_id = participant_id
        self.age = age
        self.gender = gender
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"experiment_data_{participant_id}_{timestamp}.csv"
        self.filepath = os.path.join(os.getcwd(), self.filename)
        
        # Create the CSV file with headers
        self._create_csv_file()
        
        print(f"CSV file created: {self.filename}")
    
    def _create_csv_file(self):
        """Create CSV file with headers"""
        with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header row
            writer.writerow([
                'participant_id',
                'age',
                'gender',
                'round',
                'trial',
                'pattern_name',
                'pattern_intensity',
                'color_hue',
                'color_brightness',
                'shape_value',
                'timestamp'
            ])
    
    def save_trial(self, 
                   round_name: str,
                   trial_number: int,
                   pattern_name: str,
                   pattern_intensity: float,
                   color_hue: Optional[str] = None,
                   color_brightness: Optional[int] = None,
                   shape_value: Optional[int] = None,
                   timestamp: float = None):
        """
        Save a single trial immediately to CSV.
        Appends to the existing file.
        
        Args:
            round_name: "color", "shape", or "combined"
            trial_number: Trial number within this round
            pattern_name: Name of vibrotactile pattern
            pattern_intensity: Intensity value (0.0-1.0)
            color_hue: Color hue selected (or None)
            color_brightness: Brightness index 0-10 (or None)
            shape_value: Shape slider value 1-20 (or None)
            timestamp:  timestamp of response
        """
        with open(self.filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            writer.writerow([
                self.participant_id,
                self.age,
                self.gender,
                round_name,
                trial_number,
                pattern_name,
                pattern_intensity,
                color_hue if color_hue else '',
                color_brightness if color_brightness is not None else '',
                shape_value if shape_value is not None else '',
                timestamp if timestamp else ''
            ])
        
        print(f"Saved: {round_name} trial {trial_number}")
    
    def add_post_experiment_questionnaire(self, responses: dict):
        """
        Append post-experiment questionnaire to a separate section at end of CSV.
        
        Args:
            responses: Dictionary with questionnaire responses
        """
        with open(self.filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Add blank row as separator
            writer.writerow([])
            
            # Add questionnaire header
            writer.writerow(['POST-EXPERIMENT QUESTIONNAIRE'])
            writer.writerow([])
            
            # Write responses
            writer.writerow(['Question', 'Response'])
            writer.writerow([
                'Difficulty Rating',
                responses.get('difficulty_rating', 'Not answered')
            ])
            writer.writerow([
                'Difficulty Additional Comments',
                responses.get('difficulty_additional', 'None')
            ])
            writer.writerow([
                'Easier Trials Description',
                responses.get('easier_trials', 'None')
            ])
            writer.writerow([
                'Additional Comments',
                responses.get('additional_comments', 'None')
            ])
        
        print(f"Post-experiment questionnaire saved")
    
    def get_filepath(self) -> str:
        """Return the full path to the CSV file"""
        return self.filepath