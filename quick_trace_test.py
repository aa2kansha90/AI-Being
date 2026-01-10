#!/usr/bin/env python3
"""Quick test of deterministic traces"""

try:
    from behavior_validator import validate_behavior
    
    # Test same input multiple times
    test_input = "Hello world"
    
    print("Testing deterministic traces...")
    
    results = []
    for i in range(3):
        result = validate_behavior("auto", test_input)
        results.append(result["trace_id"])
        print(f"Run {i+1}: {result['trace_id']}")
    
    if len(set(results)) == 1:
        print("SUCCESS: All trace IDs are identical!")
    else:
        print("FAILURE: Trace IDs differ!")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()