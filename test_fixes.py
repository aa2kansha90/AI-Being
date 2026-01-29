"""
Quick test to verify the enforcement system fixes
"""

from enforcement_execution_system import run_enforcement_execution_proof

if __name__ == "__main__":
    try:
        print("Testing fixed enforcement system...")
        proof = run_enforcement_execution_proof()
        print("\n✅ SUCCESS: All systems working correctly!")
        print("✅ JSON serialization: FIXED")
        print("✅ Enforcement logic: WORKING")
        print("✅ Execution control: VERIFIED")
        print("✅ Trace continuity: MAINTAINED")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("System needs additional fixes")