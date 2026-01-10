#!/usr/bin/env python3
"""
Analyze test matrix structure
"""

import json

def analyze_test_matrix():
    with open('edge_test_matrix.json', 'r', encoding='utf-8') as f:
        matrix = json.load(f)
    
    test_categories = matrix["edge_test_matrix"]["test_categories"]
    
    print("TEST MATRIX ANALYSIS")
    print("=" * 40)
    
    total_tests = 0
    for category_name, category_data in test_categories.items():
        tests = category_data.get("tests", [])
        test_count = len(tests)
        total_tests += test_count
        
        print(f"{category_name}: {test_count} tests")
        for test in tests:
            print(f"  - {test['test_id']}: {test['content'][:30]}...")
    
    print("=" * 40)
    print(f"Total tests found: {total_tests}")
    
    metadata = matrix["edge_test_matrix"]["metadata"]
    expected_total = metadata.get("total_test_cases", 0)
    print(f"Expected total: {expected_total}")
    
    if total_tests != expected_total:
        print(f"MISMATCH: Found {total_tests} but expected {expected_total}")
    else:
        print("Test count matches metadata")

if __name__ == "__main__":
    analyze_test_matrix()