#!/usr/bin/env python3
"""
Deterministic Trace Proof - Day 1 Deliverable
Verifies that same input produces same trace_id across multiple runs
"""

from behavior_validator import validate_behavior
import time

def test_deterministic_traces():
    """Test that same inputs produce same trace IDs across runs"""
    
    print("DETERMINISTIC TRACE PROOF")
    print("=" * 50)
    
    test_cases = [
        "Hello, how are you?",
        "I want to kill myself", 
        "Send me nudes",
        "I am in love with you",
        "You're the only one who understands me"
    ]
    
    print("Testing same input → same trace across runs...\n")
    
    all_deterministic = True
    
    for test_input in test_cases:
        print(f"Input: '{test_input}'")
        
        # Run validation 3 times with delays
        traces = []
        decisions = []
        categories = []
        
        for run in range(3):
            result = validate_behavior("auto", test_input)
            traces.append(result["trace_id"])
            decisions.append(result["decision"])
            categories.append(result["risk_category"])
            
            # Add delay to ensure different timestamps
            time.sleep(0.1)
        
        # Check if all traces are identical
        traces_match = len(set(traces)) == 1
        decisions_match = len(set(decisions)) == 1
        categories_match = len(set(categories)) == 1
        
        status = "PASS" if (traces_match and decisions_match and categories_match) else "FAIL"
        
        print(f"  Run 1: {traces[0]} | {decisions[0]} | {categories[0]}")
        print(f"  Run 2: {traces[1]} | {decisions[1]} | {categories[1]}")
        print(f"  Run 3: {traces[2]} | {decisions[2]} | {categories[2]}")
        print(f"  Result: {status}")
        
        if not traces_match:
            print(f"  ERROR: Trace IDs differ!")
            all_deterministic = False
        
        if not decisions_match:
            print(f"  ERROR: Decisions differ!")
            all_deterministic = False
            
        if not categories_match:
            print(f"  ERROR: Categories differ!")
            all_deterministic = False
            
        print()
    
    print("=" * 50)
    if all_deterministic:
        print("SUCCESS: All traces are deterministic!")
        print("✓ Same input → Same trace_id across runs")
        print("✓ Same input → Same decision across runs") 
        print("✓ Same input → Same category across runs")
    else:
        print("FAILURE: Some traces are non-deterministic!")
    
    print("=" * 50)
    
    # Test trace format
    print("TRACE ID FORMAT VERIFICATION:")
    sample_result = validate_behavior("auto", "test input")
    trace_id = sample_result["trace_id"]
    print(f"Sample trace: {trace_id}")
    
    if trace_id.startswith("trace_") and len(trace_id) == 18:
        print("✓ Format: trace_[12-char-hash]")
    else:
        print("✗ Invalid trace format")
    
    return all_deterministic

if __name__ == "__main__":
    success = test_deterministic_traces()
    
    print("\nDETERMINISTIC LOCK IMPLEMENTATION:")
    print("- Removed: uuid.uuid4()")
    print("- Implemented: hash(input + category + version)")
    print("- Formula: trace_id = 'trace_' + md5(text:category:version)[:12]")
    print(f"- Verification: {'PASSED' if success else 'FAILED'}")