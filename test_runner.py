#!/usr/bin/env python3
"""
PROJECT TEST RUNNER - Complete validation suite
Based on pinned context: run python test_runner.py
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"Command: {cmd}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        success = result.returncode == 0
        status = "PASSED" if success else "FAILED"
        print(f"\nSTATUS: {status} (exit code: {result.returncode})")
        
        return success
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

def main():
    """Main test runner"""
    print("AI-BEING PROJECT TEST RUNNER")
    print("Based on pinned context instructions")
    
    tests = [
        ("python test_validator.py", "Quick Validator Test"),
        ("python behavior_validator.py --test", "Canonical Validator Self-Test"),
        ("python comprehensive_test_runner.py", "Comprehensive Test Suite (35 tests)"),
        ("python bucket_integration_test_suite.py", "Bucket Integration Tests"),
        ("python enforcement_adapter.py", "Enforcement Adapter Test"),
    ]
    
    # Check if auto_validation_suite exists (from pinned context)
    if os.path.exists("auto_validation_suite.py"):
        tests.append(("python auto_validation_suite.py", "Auto Validation Suite"))
    
    passed = 0
    total = len(tests)
    
    for cmd, description in tests:
        if run_command(cmd, description):
            passed += 1
    
    print(f"\n{'='*60}")
    print("FINAL RESULTS")
    print(f"{'='*60}")
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("ALL TESTS PASSED! Project is working correctly.")
        print("\nNext steps from pinned context:")
        print("- Run comprehensive tests: python comprehensive_test_runner.py")
        print("- All 35 test cases from edge_test_matrix.json")
        return True
    else:
        print("Some tests failed. Check individual test outputs above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)