"""
Haptics Pattern Library

This module stores all vibrotactile patterns used in the experiment.
Each pattern includes the event name and intensity levels.

BLOCK RANDOMIZATION:
All rounds use block randomization where each unique pattern/intensity 
is presented once before any repetitions occur.
"""

from dataclasses import dataclass
from typing import List
import random


@dataclass
class HapticPattern:
    """Represents a single haptic pattern with specific parameters"""
    event_name: str
    intensity: float      # 0.1 to 1.0
    duration: float = 1.0 # Duration multiplier (always 1.0)
    trial_number: int = 0
    
    def __str__(self):
        return f"Trial {self.trial_number}: {self.event_name} at {self.intensity*100:.0f}%"


class HapticsLibrary:
    """Library of all haptic patterns for the experiment"""
    
    def __init__(self):
        # Pattern names from bHaptics deployment
        self.COLOR_PATTERN = "color"
        self.PRACTICE_PATTERN_COLOR = "practice_4"
        self.PRACTICE_PATTERNS_SHAPE = ["practice_1", "practice_3"]
        self.PRACTICE_PATTERNS_COMBINED = ["practice_1", "practice_3"]
        self.SHAPE_PATTERNS = [
            "expansion_bouba1",
            "circular_bouba2", 
            "inward_bouba3",
            "diagonal_spiky3",
            "corner_spiky1",
            "star_spiky1"
        ]
    
    def create_practice_trials_color(self) -> List[HapticPattern]:
        """
        Create 4 practice trials for color round.
        Uses 'practice_4' pattern at intensities: 1.0, 0.2, 0.6, 0.4
        
        Returns:
            List of 4 HapticPattern objects in specified order
        """
        intensities = [1.0, 0.2, 0.6, 0.4]
        patterns = []
        
        for i, intensity in enumerate(intensities, 1):
            patterns.append(HapticPattern(
                event_name=self.PRACTICE_PATTERN_COLOR,
                intensity=intensity,
                duration=1.0,
                trial_number=i
            ))
        
        return patterns
    
    def create_practice_trials_shape(self) -> List[HapticPattern]:
        """
        Create 4 practice trials for shape round.
        Uses patterns: practice_1, practice_3, practice_1, practice_3
        All at 0.6 (60%) intensity
        
        Returns:
            List of 4 HapticPattern objects in specified order
        """
        pattern_sequence = [
            "practice_1",
            "practice_3",
            "practice_1",
            "practice_3"
        ]
        patterns = []
        
        for i, pattern_name in enumerate(pattern_sequence, 1):
            patterns.append(HapticPattern(
                event_name=pattern_name,
                intensity=0.6,
                duration=1.0,
                trial_number=i
            ))
        
        return patterns
    
    def create_practice_trials_combined(self) -> List[HapticPattern]:
        """
        Create 4 practice trials for combined round.
        Uses patterns: practice_1, practice_3, practice_1, practice_3
        At varying intensities: 1.0, 0.2, 0.6, 0.2
        
        Returns:
            List of 4 HapticPattern objects in specified order
        """
        pattern_sequence = [
            "practice_1",
            "practice_3",
            "practice_1",
            "practice_3"
        ]
        intensities = [1.0, 0.2, 0.6, 0.2]
        patterns = []
        
        for i, (pattern_name, intensity) in enumerate(zip(pattern_sequence, intensities), 1):
            patterns.append(HapticPattern(
                event_name=pattern_name,
                intensity=intensity,
                duration=1.0,
                trial_number=i
            ))
        
        return patterns
    
    def create_color_round(self) -> List[HapticPattern]:
        """
        Create the complete color round with block randomization.
        10 intensity levels × 3 repetitions = 30 trials
        
        Block randomization: All 10 intensities appear once before any repeat.
        - Block 1: 10 intensities (shuffled)
        - Block 2: 10 intensities (shuffled independently)
        - Block 3: 10 intensities (shuffled independently)
        """
        all_patterns = []
        
        # Create 3 blocks
        for block in range(3):
            block_patterns = []
            
            # Create one trial for each intensity level
            for intensity_percent in range(10, 101, 10):  # 10%, 20%, ..., 100%
                intensity = intensity_percent / 100.0
                block_patterns.append(HapticPattern(
                    event_name=self.COLOR_PATTERN,
                    intensity=intensity,
                    duration=1.0
                ))
            
            # Shuffle within this block
            random.shuffle(block_patterns)
            
            # Add this block to the full list
            all_patterns.extend(block_patterns)
        
        # Assign trial numbers after all blocks are created
        for i, pattern in enumerate(all_patterns, 1):
            pattern.trial_number = i
        
        return all_patterns
    
    def create_shape_round(self) -> List[HapticPattern]:
        """
        Create the complete shape round with block randomization.
        6 spatiotemporal patterns × 3 repetitions = 18 trials
        All at 60% intensity (constant)
        
        Block randomization: All 6 patterns appear once before any repeat.
        - Block 1: 6 patterns (shuffled)
        - Block 2: 6 patterns (shuffled independently)
        - Block 3: 6 patterns (shuffled independently)
        """
        all_patterns = []
        
        # Create 3 blocks
        for block in range(3):
            block_patterns = []
            
            # Create one trial for each shape pattern
            for event_name in self.SHAPE_PATTERNS:
                block_patterns.append(HapticPattern(
                    event_name=event_name,
                    intensity=0.6,  # Always 60%
                    duration=1.0
                ))
            
            # Shuffle within this block
            random.shuffle(block_patterns)
            
            # Add this block to the full list
            all_patterns.extend(block_patterns)
        
        # Assign trial numbers after all blocks are created
        for i, pattern in enumerate(all_patterns, 1):
            pattern.trial_number = i
        
        return all_patterns
    
    def create_combined_round(self) -> List[HapticPattern]:
    
        all_patterns = []
        
        # Three intensity levels: Low (20%), Medium (60%), High (100%)
        intensities = [0.2, 0.6, 1.0]
        
        # Create 3 repetitions (blocks)
        for repetition in range(3):
            block_patterns = []
            
            # Create all 18 unique combinations for this repetition
            for intensity in intensities:
                for event_name in self.SHAPE_PATTERNS:
                    block_patterns.append(HapticPattern(
                        event_name=event_name,
                        intensity=intensity,
                        duration=1.0
                    ))
            
            # Shuffle within this block (randomize the 18 combinations)
            random.shuffle(block_patterns)
            
            # Add this block to the full list
            all_patterns.extend(block_patterns)
        
        # Assign trial numbers after all blocks are created
        for i, pattern in enumerate(all_patterns, 1):
            pattern.trial_number = i
        
        return all_patterns
    
    def get_summary(self) -> dict:
        """Get a summary of all patterns in the library"""
        return {
            "practice_pattern_color": self.PRACTICE_PATTERN_COLOR,
            "practice_patterns_shape": self.PRACTICE_PATTERNS_SHAPE,
            "practice_patterns_combined": self.PRACTICE_PATTERNS_COMBINED,
            "practice_trials_color": 4,
            "practice_trials_shape": 4,
            "practice_trials_combined": 4,
            "color_pattern": self.COLOR_PATTERN,
            "shape_patterns": self.SHAPE_PATTERNS,
            "color_round_trials": 30,
            "shape_round_trials": 18,
            "combined_round_trials": 54,
            "total_trials": 102,
            "randomization": "Block randomization (all unique patterns once per block)"
        }


# Example usage functions
def print_pattern_list(patterns: List[HapticPattern], title: str = "Patterns"):
    print("="*60)
    print(title)
    print("="*60)
    print(f"Total trials: {len(patterns)}")
    print()
    
    # Show all if <= 20, otherwise first 20
    display_count = min(20, len(patterns))
    print(f"{'All' if len(patterns) <= 20 else 'First 20'} trials:")
    for pattern in patterns[:display_count]:
        print(f"  {pattern}")
    
    if len(patterns) > 20:
        print("  ...")
    
    print()
    
    # Show intensity distribution
    intensity_counts = {}
    for pattern in patterns:
        pct = int(pattern.intensity * 100)
        intensity_counts[pct] = intensity_counts.get(pct, 0) + 1
    
    print("Intensity distribution:")
    for intensity in sorted(intensity_counts.keys()):
        count = intensity_counts[intensity]
        print(f"  {intensity:3d}%: {count} trials")
    
    # Show pattern distribution (if multiple patterns)
    pattern_counts = {}
    for pattern in patterns:
        pattern_counts[pattern.event_name] = pattern_counts.get(pattern.event_name, 0) + 1
    
    if len(pattern_counts) > 1:
        print("\nPattern distribution:")
        for pattern_name in sorted(pattern_counts.keys()):
            count = pattern_counts[pattern_name]
            print(f"  {pattern_name}: {count} trials")
    
    print()


def verify_block_randomization(patterns: List[HapticPattern], block_size: int, title: str):
    """
    Verify that patterns follow block randomization structure.
    Checks that all unique patterns appear once per block.
    """
    print("="*60)
    print(f"BLOCK RANDOMIZATION VERIFICATION: {title}")
    print("="*60)
    
    num_blocks = len(patterns) // block_size
    
    for block_num in range(num_blocks):
        start_idx = block_num * block_size
        end_idx = start_idx + block_size
        block_patterns = patterns[start_idx:end_idx]
        
        # Get unique patterns in this block
        unique_in_block = set()
        for p in block_patterns:
            # Create unique identifier (pattern + intensity)
            unique_id = f"{p.event_name}_{int(p.intensity*100)}"
            unique_in_block.add(unique_id)
        
        print(f"\nBlock {block_num + 1} (trials {start_idx + 1}-{end_idx}):")
        print(f"  Unique combinations: {len(unique_in_block)}")
        print(f"  Expected: {block_size}")
        print(f"  ✓ Valid" if len(unique_in_block) == block_size else f"  ✗ Invalid!")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    # Test the library
    library = HapticsLibrary()
    
    print("\n" + "="*60)
    print("HAPTICS PATTERN LIBRARY - BLOCK RANDOMIZATION")
    print("="*60)
    print()
    
    # Show summary
    summary = library.get_summary()
    print("Library Summary:")
    print(f"  Randomization: {summary['randomization']}")
    print(f"  Color practice pattern: {summary['practice_pattern_color']}")
    print(f"  Shape practice patterns: {summary['practice_patterns_shape']}")
    print(f"  Combined practice patterns: {summary['practice_patterns_combined']}")
    print(f"  Practice trials (color): {summary['practice_trials_color']}")
    print(f"  Practice trials (shape): {summary['practice_trials_shape']}")
    print(f"  Practice trials (combined): {summary['practice_trials_combined']}")
    print(f"  Color pattern: {summary['color_pattern']}")
    print(f"  Shape patterns: {len(summary['shape_patterns'])} patterns")
    print(f"  Total trials: {summary['total_trials']}")
    print()
    
    # Test practice trials
    color_practice = library.create_practice_trials_color()
    print_pattern_list(color_practice, "COLOR PRACTICE TRIALS (4 trials)")
    
    shape_practice = library.create_practice_trials_shape()
    print_pattern_list(shape_practice, "SHAPE PRACTICE TRIALS (4 trials)")
    
    combined_practice = library.create_practice_trials_combined()
    print_pattern_list(combined_practice, "COMBINED PRACTICE TRIALS (4 trials)")
    
    # Test color round generation with verification
    print("\n" + "="*60)
    print("COLOR ROUND - BLOCK RANDOMIZATION TEST")
    print("="*60)
    color_patterns = library.create_color_round()
    print_pattern_list(color_patterns, "COLOR ROUND (30 trials)")
    verify_block_randomization(color_patterns, 10, "Color Round")
    
    # Test shape round generation with verification
    print("\n" + "="*60)
    print("SHAPE ROUND - BLOCK RANDOMIZATION TEST")
    print("="*60)
    shape_patterns = library.create_shape_round()
    print_pattern_list(shape_patterns, "SHAPE ROUND (18 trials)")
    verify_block_randomization(shape_patterns, 6, "Shape Round")
    
    # Test combined round generation with verification
    print("\n" + "="*60)
    print("COMBINED ROUND - BLOCK RANDOMIZATION TEST")
    print("="*60)
    combined_patterns = library.create_combined_round()
    print_pattern_list(combined_patterns, "COMBINED ROUND (54 trials)")
    verify_block_randomization(combined_patterns, 18, "Combined Round")