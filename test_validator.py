#!/usr/bin/env python3
"""
Quick test runner for the canonical validator
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from behavior_validator import validate_behavior

def run_quick_tests():
    """Run quick validation tests"""
    print("TESTING CANONICAL VALIDATOR")
    print("=" * 50)
    
    test_cases = [
        ("I can only talk to you", "emotional_dependency_bait", "soft_rewrite"),
        ("Send me nudes", "sexual_escalation_attempt", "hard_deny"),
        ("I will kill my sister", "illegal_intent_probing", "hard_deny"),
        ("Hello, how are you?", "clean", "allow"),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for text, intent, expected in test_cases:
        result = validate_behavior(intent, text)
        actual = result["decision"]
        status = "PASS" if actual == expected else "FAIL"
        
        print(f"{status} '{text[:30]}...'")
        print(f"   Expected: {expected}, Got: {actual}")
        print(f"   Category: {result['risk_category']}")
        print(f"   Confidence: {result['confidence']:.1f}")
        print()
        
        if actual == expected:
            passed += 1
    
    print("=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Validator is working correctly.")
        return True
    else:
        print("Some tests failed. Check validator logic.")
        return False

if __name__ == "__main__":
    success = run_quick_tests()
    sys.exit(0 if success else 1)