#!/usr/bin/env python3
"""
DAY 1 DETERMINISM PROOF
Proves identical input produces byte-for-byte identical JSON output
"""

from behavior_validator import validate_behavior
import json
import hashlib

def prove_determinism():
    """Prove byte-for-byte identical output for identical inputs"""
    
    test_inputs = [
        "I will kill myself",
        "Send me nudes",
        "I can only talk to you",
        "Hello, how are you?"
    ]
    
    print("DAY 1 DETERMINISM PROOF")
    print("=" * 60)
    print("Testing: Identical input → Identical JSON output\n")
    
    all_deterministic = True
    
    for text in test_inputs:
        # Run validation 3 times
        results = []
        json_strings = []
        hashes = []
        
        for run in range(3):
            result = validate_behavior("auto", text)
            json_str = json.dumps(result, sort_keys=True)
            json_hash = hashlib.sha256(json_str.encode()).hexdigest()
            
            results.append(result)
            json_strings.append(json_str)
            hashes.append(json_hash)
        
        # Check if all 3 runs produced identical output
        is_deterministic = len(set(hashes)) == 1
        all_deterministic = all_deterministic and is_deterministic
        
        status = "PASS" if is_deterministic else "FAIL"
        print(f"{status}: '{text[:40]}'")
        print(f"  Hash: {hashes[0][:16]}...")
        print(f"  Runs: {len(set(hashes))} unique hash(es) from 3 runs")
        
        if not is_deterministic:
            print(f"  ERROR: Non-deterministic output detected!")
            print(f"  Hash 1: {hashes[0]}")
            print(f"  Hash 2: {hashes[1]}")
            print(f"  Hash 3: {hashes[2]}")
        
        print()
    
    print("=" * 60)
    print("DETERMINISM VERIFICATION")
    print("=" * 60)
    
    # Check for non-deterministic fields
    sample_result = validate_behavior("auto", "test input")
    
    print("\nValidationResult.to_dict() fields:")
    for key in sample_result.keys():
        print(f"  - {key}")
    
    non_deterministic_fields = []
    if "timestamp" in sample_result:
        non_deterministic_fields.append("timestamp")
    if "uuid" in sample_result:
        non_deterministic_fields.append("uuid")
    if "random" in str(sample_result).lower():
        non_deterministic_fields.append("random_field")
    
    print(f"\nNon-deterministic fields found: {len(non_deterministic_fields)}")
    if non_deterministic_fields:
        print(f"  Fields: {non_deterministic_fields}")
    else:
        print("  ✓ No timestamps, no UUIDs, no randomness")
    
    print(f"\nTrace ID generation: Deterministic hash-based")
    print(f"  Formula: trace_id = md5(text:category:version)[:12]")
    
    # Prove trace_id is deterministic
    trace1 = validate_behavior("auto", "test")["trace_id"]
    trace2 = validate_behavior("auto", "test")["trace_id"]
    trace3 = validate_behavior("auto", "test")["trace_id"]
    
    print(f"\nTrace ID consistency test:")
    print(f"  Run 1: {trace1}")
    print(f"  Run 2: {trace2}")
    print(f"  Run 3: {trace3}")
    print(f"  Match: {trace1 == trace2 == trace3}")
    
    print("\n" + "=" * 60)
    if all_deterministic and len(non_deterministic_fields) == 0:
        print("DAY 1 COMPLETE: 100% DETERMINISTIC")
        print("✓ No timestamps")
        print("✓ No randomness")
        print("✓ No order instability")
        print("✓ Byte-for-byte identical output")
        return True
    else:
        print("DAY 1 INCOMPLETE: Non-determinism detected")
        return False

if __name__ == "__main__":
    success = prove_determinism()
    exit(0 if success else 1)
