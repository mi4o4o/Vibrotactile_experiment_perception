# data/trial.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class TrialData:
    phase: str                 # "color", "shape", or "combined"
    trial: int                 # trial index within that phase
    
    # Pattern information
    pattern_event_name: str    # bHaptics pattern name
    pattern_intensity: float   # 0.0 to 1.0
    
    # Response data
    shape_angularity: Optional[int]
    shape_color: Optional[str]
    combined_angularity: Optional[int]
    combined_color: Optional[str]
    
    timestamp: float