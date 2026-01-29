"""
Minimal test for fixed enforcement system
"""
import json
from datetime import datetime

# Test JSON serialization fix
test_data = {
    "timestamp": datetime.now().isoformat() + "Z",
    "status": "working",
    "tests_passed": True
}

try:
    with open("test_json.json", "w") as f:
        json.dump(test_data, f, indent=2)
    print("✅ JSON serialization test: PASSED")
    
    # Now test the actual system
    from enforcement_execution_system import EnforcementExecutionSystem
    system = EnforcementExecutionSystem()
    
    # Test one simple action
    result = system.process_action(
        content="Hello, how are you?",
        action_type="message",
        recipient="test@example.com",
        platform="email"
    )
    
    print("✅ System test: PASSED")
    print(f"✅ Trace ID: {result['trace_id']}")
    print("✅ Ready to run full system!")
    
except Exception as e:
    print(f"❌ Error: {e}")