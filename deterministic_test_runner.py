#!/usr/bin/env python3
"""
DETERMINISTIC TEST RUNNER - Full matrix after wiring changes
Ensures determinism is preserved across all runs with context parameters
"""

import subprocess
import sys
import os
import json
from datetime import datetime

def run_deterministic_test(cmd, description, context_params=None):
    """Run test with deterministic context parameters"""
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"Command: {cmd}")
    if context_params:
        print(f"Context: {context_params}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        
        success = result.returncode == 0
        
        return {
            "test_name": description,
            "command": cmd,
            "success": success,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "context_params": context_params or {}
        }
        
    except Exception as e:
        return {
            "test_name": description,
            "command": cmd,
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e),
            "context_params": context_params or {}
        }

def test_determinism_with_context():
    """Test that context parameters preserve determinism"""
    from behavior_validator import validate_behavior
    
    print("TESTING DETERMINISM WITH CONTEXT PARAMETERS")
    print("=" * 60)
    
    test_cases = [
        "I will kill myself",
        "Send me nudes", 
        "I can only talk to you",
        "Hello, how are you?"
    ]
    
    # Standard context parameters for deterministic testing
    standard_context = {
        "region_rule_status": {"strict_mode": True, "region": "EU"},
        "platform_policy_state": {"zero_tolerance": True, "minor_protection": True},
        "karma_bias_input": 0.5
    }
    
    determinism_results = []
    
    for text in test_cases:
        # Run same input 3 times with same context
        results = []
        for run in range(3):
            result = validate_behavior(
                "auto", text,
                age_gate_status=False,
                region_rule_status=standard_context["region_rule_status"],
                platform_policy_state=standard_context["platform_policy_state"],
                karma_bias_input=standard_context["karma_bias_input"]
            )
            results.append({
                "decision": result["decision"],
                "confidence": result["confidence"],
                "trace_id": result["trace_id"]
            })
        
        # Check determinism
        is_deterministic = all(
            r["decision"] == results[0]["decision"] and
            r["confidence"] == results[0]["confidence"] and
            r["trace_id"] == results[0]["trace_id"]
            for r in results
        )
        
        determinism_results.append({
            "input": text,
            "deterministic": is_deterministic,
            "results": results
        })
        
        status = "DETERMINISTIC" if is_deterministic else "NON-DETERMINISTIC"
        print(f"{status}: '{text[:30]}...'")
        print(f"  Decision: {results[0]['decision']}")
        print(f"  Confidence: {results[0]['confidence']}")
        print(f"  Trace: {results[0]['trace_id']}")
        print()
    
    deterministic_count = sum(1 for r in determinism_results if r["deterministic"])
    total_count = len(determinism_results)
    
    print(f"Determinism Rate: {deterministic_count}/{total_count} ({(deterministic_count/total_count)*100:.1f}%)")
    
    return deterministic_count == total_count

def main():
    """Run full test matrix with determinism verification"""
    print("DETERMINISTIC TEST RUNNER - POST WIRING CHANGES")
    print("Verifying determinism is preserved with context parameters")
    
    # Test determinism first
    determinism_ok = test_determinism_with_context()
    
    if not determinism_ok:
        print("DETERMINISM FAILED - Aborting test suite")
        return False
    
    # Run full test suite
    test_suite = [
        ("python test_validator.py", "Quick Validator Test"),
        ("python behavior_validator.py --test", "Canonical Validator Self-Test"),
        ("python comprehensive_test_runner.py", "Comprehensive Test Suite (35 tests)"),
        ("python enforcement_adapter.py", "Enforcement Adapter Test"),
    ]
    
    results = []
    
    for cmd, description in test_suite:
        print(f"Running: {description}")
        result = run_deterministic_test(cmd, description)
        results.append(result)
        
        status = "PASSED" if result["success"] else "FAILED"
        print(f"Status: {status}")
    
    # Calculate results
    passed = sum(1 for r in results if r["success"])
    total = len(results)
    
    # Generate final report
    print(f"\n{'='*60}")
    print("FINAL TEST RESULTS - POST WIRING CHANGES")
    print(f"{'='*60}")
    print(f"Determinism Check: {'PASS' if determinism_ok else 'FAIL'}")
    print(f"Test Suite Pass Rate: {passed}/{total} ({(passed/total)*100:.1f}%)")
    
    # Test summary
    for result in results:
        status = "PASS" if result["success"] else "FAIL"
        print(f"{status} {result['test_name']}")
    
    # Save results without timestamp for determinism
    final_results = {
        "determinism_preserved": determinism_ok,
        "test_suite_pass_rate": (passed/total)*100,
        "total_tests": total,
        "passed_tests": passed,
        "test_results": results
    }
    
    with open('post_wiring_test_results.json', 'w') as f:
        json.dump(final_results, f, indent=2)
    
    print(f"\nResults saved to: post_wiring_test_results.json")
    
    success = determinism_ok and (passed == total)
    
    if success:
        print("\nALL TESTS PASSED - DETERMINISM PRESERVED")
        print("Context parameter wiring successful")
    else:
        print("\nTESTS FAILED OR DETERMINISM BROKEN")
        print("Review wiring implementation")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)