#!/usr/bin/env python3
"""Test the canonical validator"""

try:
    from behavior_validator import validate_behavior
    
    print("Import successful")
    
    # Quick test
    result = validate_behavior("clean", "Hello there")
    print(f"Basic test: {result['decision']}")
    
    result = validate_behavior("sexual_escalation_attempt", "Send me nudes")
    print(f"Hard deny test: {result['decision']}")
    
    print("Validator is working correctly!")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()