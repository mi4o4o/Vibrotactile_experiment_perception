"""
Haptics playback utilities for the experiment.
Integrates with bHaptics TactSuit to play vibrotactile patterns.
"""

import asyncio
try:
    import bhaptics_python
    BHAPTICS_AVAILABLE = True
except ImportError:
    BHAPTICS_AVAILABLE = False
    print("WARNING: bhaptics_python not installed. Using simulation mode.")

# bHaptics credentials - Update these with your actual values
BHAPTICS_APP_ID = "68b6faf1e9ad507c08e597dd"
BHAPTICS_API_KEY = "PeiruH2uM6hDUG1HLgu8"
BHAPTICS_APP_NAME = "redround"

BHAPTICS_CONFIGURED = True  # Set to False if you don't have credentials yet


# Global flag for whether bHaptics is initialized
_bhaptics_initialized = False


async def _async_play_pattern(event_name: str, intensity: float, duration: float = 1.0):
    """
    Async function to play a haptic pattern via bHaptics.
    
    Args:
        event_name: Name of the pattern in bHaptics Designer
        intensity: Intensity level (0.0 to 1.0)
        duration: Duration multiplier (default 1.0 for full duration)
    
    Returns:
        request_id if successful, -1 if failed
    """
    global _bhaptics_initialized
    
    if not BHAPTICS_AVAILABLE or not BHAPTICS_CONFIGURED:
        print(f"[SIMULATION] Playing pattern: {event_name} at {intensity*100:.0f}% intensity")
        return 0  # Fake success
    
    # Initialize if needed
    if not _bhaptics_initialized:
        result = await bhaptics_python.registry_and_initialize(
            BHAPTICS_APP_ID,
            BHAPTICS_API_KEY,
            BHAPTICS_APP_NAME
        )
        if result:
            _bhaptics_initialized = True
            print("✓ bHaptics initialized")
        else:
            print("✗ bHaptics initialization failed")
            return -1
    
    # Play the pattern
    request_id = await bhaptics_python.play_param(
        event_name,
        intensity,
        duration,
        0.0,  # x offset
        0.0   # y offset
    )
    
    if request_id >= 0:
        print(f"✓ Playing: {event_name} at {intensity*100:.0f}%")
    else:
        print(f"✗ Failed to play: {event_name}")
    
    return request_id


def play_haptic_pattern(event_name: str, intensity: float, duration: float = 1.0):
    """
    Synchronous wrapper to play a haptic pattern.
    
    Args:
        event_name: Name of the pattern in bHaptics Designer
        intensity: Intensity level (0.0 to 1.0)
        duration: Duration multiplier (default 1.0)
    
    Returns:
        request_id if successful, -1 if failed
    """
    # Run async function in event loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(
        _async_play_pattern(event_name, intensity, duration)
    )


def play_vibration_pattern():
    """
    Legacy function for compatibility.
    Plays a default pattern if called without arguments.
    """
    print("[SIMULATION] Playing default vibration pattern")
    return 0


async def cleanup_bhaptics():
    """Clean up bHaptics connection when done"""
    global _bhaptics_initialized
    
    if _bhaptics_initialized and BHAPTICS_AVAILABLE:
        await bhaptics_python.close()
        _bhaptics_initialized = False
        print("✓ bHaptics connection closed")