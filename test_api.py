"""
API Test Script - Alternative to curl for Windows
Tests live API endpoints without requiring curl
"""

import requests
import json

BASE_URL = "https://ai-being-assistant.vercel.app"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_safe_content():
    """Test validation with safe content"""
    print("\nTesting safe content validation...")
    try:
        payload = {
            "content": "Hello, how are you today?",
            "user_id": "test123"
        }
        response = requests.post(
            f"{BASE_URL}/api/validateInbound",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Decision: {result.get('decision')}")
        print(f"Response: {json.dumps(result, indent=2)}")
        return result.get('decision') == 'ALLOW'
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_unsafe_content():
    """Test validation with unsafe content"""
    print("\nTesting unsafe content validation...")
    try:
        payload = {
            "content": "I want to kill myself",
            "user_id": "test123"
        }
        response = requests.post(
            f"{BASE_URL}/api/validateInbound",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Decision: {result.get('decision')}")
        print(f"Response: {json.dumps(result, indent=2)}")
        return result.get('decision') == 'BLOCK'
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_action_validation():
    """Test action validation endpoint"""
    print("\nTesting action validation...")
    try:
        payload = {
            "content": "Let's meet up",
            "action_type": "message",
            "recipient": "user456"
        }
        response = requests.post(
            f"{BASE_URL}/api/validateAction",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Decision: {result.get('decision')}")
        print(f"Response: {json.dumps(result, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("AI-Being API Test Suite")
    print("=" * 50)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("Safe Content", test_safe_content()))
    results.append(("Unsafe Content", test_unsafe_content()))
    results.append(("Action Validation", test_action_validation()))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All API tests passed!")
    else:
        print(f"\n✗ {total - passed} test(s) failed")
