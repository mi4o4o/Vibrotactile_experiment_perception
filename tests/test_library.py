"""
Test script for the Haptics Library
Uses the library to generate and play patterns
"""

import bhaptics_python
import asyncio
from haptics_library import HapticsLibrary, print_pattern_list


async def test_library():
    """Test the haptics library with actual playback"""
    
    # Initialize bHaptics
    app_id = "68b6faf1e9ad507c08e597dd"
    api_key = "PeiruH2uM6hDUG1HLgu8"
    
    print("Initializing bHaptics...")
    result = await bhaptics_python.registry_and_initialize(app_id, api_key, "redround")
    
    if not result:
        print("Failed to initialize")
        return
    
    print("✓ Initialized\n")
    
    # Create library instance
    library = HapticsLibrary()
    
    # Show menu

    print("HAPTICS LIBRARY TEST")

    print()
    print("Choose what to test:")
    print("  1 - Color round (30 trials: 10 intensities × 3 reps)")
    print("  2 - Shape round (18 trials: 6 patterns × 3 reps)")
    print("  3 - Combined round (54 trials: 3 intensities × 6 patterns × 3 reps)")
    print("  4 - Just show pattern lists (no playback)")
    print("  q - Quit")
    print()
    
    choice = input("Enter choice: ").strip()
    
    if choice == '1':
        # Test color round
        patterns = library.create_color_round()
        print_pattern_list(patterns, "COLOR ROUND")
        
        play = input("\nPlay all trials? (y/n): ").strip().lower()
        if play == 'y':
            await play_patterns(patterns)
    
    elif choice == '2':
        # Test shape round
        patterns = library.create_shape_round()
        print_pattern_list(patterns, "SHAPE ROUND")
        
        play = input("\nPlay all trials? (y/n): ").strip().lower()
        if play == 'y':
            await play_patterns(patterns)
    
    elif choice == '3':
        # Test combined round
        patterns = library.create_combined_round()
        print_pattern_list(patterns, "COMBINED ROUND")
        
        play = input("\nPlay all trials? (y/n): ").strip().lower()
        if play == 'y':
            await play_patterns(patterns)
    
    elif choice == '4':
        # Just show all pattern lists
        print()
        print_pattern_list(library.create_color_round(), "COLOR ROUND")
        print_pattern_list(library.create_shape_round(), "SHAPE ROUND")
        print_pattern_list(library.create_combined_round(), "COMBINED ROUND")
    
    elif choice == 'q':
        print("Exiting...")
    
    else:
        print("Invalid choice")
    
    await bhaptics_python.close()


async def play_patterns(patterns):
    """Play a list of patterns"""
    print()
    print("Playing patterns...")
    print("(2 seconds per trial, 0.5s gap)")
    print()
    
    for pattern in patterns:
        print(f"{pattern}... ", end="", flush=True)
        
        # Play with play_param to control intensity
        request_id = await bhaptics_python.play_param(
            pattern.event_name,
            pattern.intensity,
            1.0, 0.0, 0.0
        )
        
        if request_id >= 0:
            print("✓")
            await asyncio.sleep(2.0)
            await bhaptics_python.stop_by_request_id(request_id)
            await asyncio.sleep(0.5)
        else:
            print("error")
    
    print()

    print("All trials complete!")



if __name__ == "__main__":
    asyncio.run(test_library())