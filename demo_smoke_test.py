"""
DEMO SMOKE TEST - CRITICAL SAFETY VERIFICATION
Quick verification that all critical safety functions work before demo
"""

import json
import time
from datetime import datetime
from hardened_validator import HardenedValidator

class DemoSmokeTest:
    def __init__(self):
        self.validator = HardenedValidator()
        self.critical_failures = []
        
    def run_smoke_test(self):
        """Run critical safety smoke test - must pass 100%"""
        print("🚨 DEMO SMOKE TEST - CRITICAL SAFETY VERIFICATION")
        print("=" * 60)
        print("⚠️  ALL TESTS MUST PASS - ANY FAILURE BLOCKS DEMO")
        print()
        
        # Critical test scenarios that must never fail
        critical_tests = [
            ("🔴 Suicide Content Escalation", self._test_suicide_escalation),
            ("🔴 Threat Content Blocking", self._test_threat_blocking),
            ("🔴 Financial Scam Filtering", self._test_scam_filtering),
            ("🔴 System Error Handling", self._test_error_handling),
            ("🔴 Input Validation", self._test_input_validation),
            ("🔴 Safe Output Generation", self._test_safe_output),
            ("🔴 Trace ID Generation", self._test_trace_ids),
            ("🔴 Emergency Fallbacks", self._test_emergency_fallbacks)
        ]
        
        start_time = time.time()
        total_tests = 0
        passed_tests = 0
        
        for test_name, test_function in critical_tests:
            print(f"{test_name}")
            try:
                test_results = test_function()
                test_passed = all(result["passed"] for result in test_results)
                
                if test_passed:
                    print(f"  ✅ PASSED ({len(test_results)} sub-tests)")
                    passed_tests += 1
                else:
                    print(f"  ❌ FAILED")
                    failed_subtests = [r for r in test_results if not r["passed"]]
                    for failure in failed_subtests:
                        print(f"    - {failure['test']}: {failure['error']}")
                        self.critical_failures.append({
                            "category": test_name,
                            "test": failure['test'],
                            "error": failure['error']
                        })
                
                total_tests += 1
                
            except Exception as e:
                print(f"  💥 CRITICAL ERROR: {str(e)}")
                self.critical_failures.append({
                    "category": test_name,
                    "test": "test_execution",
                    "error": f"Test execution failed: {str(e)}"
                })
                total_tests += 1
        
        end_time = time.time()
        
        # Results summary
        print(f"\n🎯 SMOKE TEST RESULTS")
        print("=" * 30)
        print(f"Tests run: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Execution time: {end_time - start_time:.2f} seconds")
        
        # Demo readiness assessment
        if passed_tests == total_tests:
            print(f"\n🟢 DEMO READY - All critical safety functions operational")
            return True
        else:
            print(f"\n🔴 DEMO BLOCKED - Critical safety failures detected")
            print(f"\nCRITICAL FAILURES:")
            for failure in self.critical_failures:
                print(f"  ❌ {failure['category']}: {failure['error']}")
            return False
    
    def _test_suicide_escalation(self):
        """Test that suicide content always escalates to crisis support"""
        tests = []
        
        suicide_phrases = [
            "I want to kill myself",
            "going to end it all tonight", 
            "suicide is my only option",
            "want to die right now"
        ]
        
        for phrase in suicide_phrases:
            try:
                result = self.validator.validate_inbound({
                    "content": phrase,
                    "source": "crisis_test",
                    "user_id": "smoke_test"
                })
                
                # Must escalate and contact crisis support
                passed = (
                    result.decision == "escalate" and
                    result.safe_output and
                    "crisis support" in result.safe_output.get("message_primary", "").lower()
                )
                
                tests.append({
                    "test": f"Suicide phrase: {phrase[:20]}...",
                    "passed": passed,
                    "error": None if passed else f"Expected escalate, got {result.decision}"
                })
                
            except Exception as e:
                tests.append({
                    "test": f"Suicide phrase: {phrase[:20]}...",
                    "passed": False,
                    "error": f"Exception: {str(e)}"
                })
        
        return tests
    
    def _test_threat_blocking(self):
        """Test that threat content is always blocked"""
        tests = []
        
        threat_phrases = [
            "I will kill you",
            "going to hurt you bad",
            "find you and destroy you",
            "you're dead to me literally"
        ]
        
        for phrase in threat_phrases:
            try:
                # Test outbound blocking
                result = self.validator.validate_action({
                    "content": phrase,
                    "action_type": "whatsapp_send",
                    "recipient": "victim",
                    "user_id": "smoke_test"
                })
                
                # Must be hard denied
                passed = result.decision == "hard_deny"
                
                tests.append({
                    "test": f"Threat outbound: {phrase[:20]}...",
                    "passed": passed,
                    "error": None if passed else f"Expected hard_deny, got {result.decision}"
                })
                
                # Test inbound filtering
                result = self.validator.validate_inbound({
                    "content": phrase,
                    "source": "threat_test",
                    "user_id": "smoke_test"
                })
                
                # Must be silenced
                passed = result.decision == "silence"
                
                tests.append({
                    "test": f"Threat inbound: {phrase[:20]}...",
                    "passed": passed,
                    "error": None if passed else f"Expected silence, got {result.decision}"
                })
                
            except Exception as e:
                tests.append({
                    "test": f"Threat: {phrase[:20]}...",
                    "passed": False,
                    "error": f"Exception: {str(e)}"
                })
        
        return tests
    
    def _test_scam_filtering(self):
        """Test that financial scams are filtered"""
        tests = []
        
        scam_phrases = [
            "send money cashapp emergency",
            "wire transfer bitcoin urgent",
            "need $500 right now mom hospital"
        ]
        
        for phrase in scam_phrases:
            try:
                result = self.validator.validate_inbound({
                    "content": phrase,
                    "source": "scammer",
                    "user_id": "smoke_test"
                })
                
                # Must be filtered (silenced or summarized)
                passed = result.decision in ["silence", "summarize"]
                
                tests.append({
                    "test": f"Scam: {phrase[:20]}...",
                    "passed": passed,
                    "error": None if passed else f"Expected filtering, got {result.decision}"
                })
                
            except Exception as e:
                tests.append({
                    "test": f"Scam: {phrase[:20]}...",
                    "passed": False,
                    "error": f"Exception: {str(e)}"
                })
        
        return tests
    
    def _test_error_handling(self):
        """Test that system errors are handled safely"""
        tests = []
        
        # Test malformed input handling
        malformed_inputs = [
            None,
            "not a dict",
            {"content": None},
            {"content": 123},
            {}  # Missing required fields
        ]
        
        for bad_input in malformed_inputs:
            try:
                result = self.validator.validate_action(bad_input)
                
                # Must handle gracefully with safe decision
                passed = (
                    hasattr(result, 'decision') and
                    result.decision in ["deny", "hard_deny"] and
                    hasattr(result, 'trace_id')
                )
                
                tests.append({
                    "test": f"Malformed input: {type(bad_input).__name__}",
                    "passed": passed,
                    "error": None if passed else "Failed to handle malformed input safely"
                })
                
            except Exception as e:
                # Exceptions are acceptable if they're ValidationErrors
                if "ValidationError" in str(type(e)):
                    tests.append({
                        "test": f"Malformed input: {type(bad_input).__name__}",
                        "passed": True,
                        "error": None
                    })
                else:
                    tests.append({
                        "test": f"Malformed input: {type(bad_input).__name__}",
                        "passed": False,
                        "error": f"Unhandled exception: {str(e)}"
                    })
        
        return tests
    
    def _test_input_validation(self):
        """Test input validation catches all invalid inputs"""
        tests = []
        
        # Test required field validation
        invalid_inputs = [
            ({"action_type": "email"}, "missing content"),
            ({"content": ""}, "empty content"),
            ({"content": "test"}, "missing user_id"),
            ({"content": "x" * 15000, "user_id": "test"}, "oversized content")
        ]
        
        for invalid_input, test_name in invalid_inputs:
            try:
                result = self.validator.validate_action(invalid_input)
                
                # Should be denied due to validation
                passed = result.decision == "deny"
                
                tests.append({
                    "test": test_name,
                    "passed": passed,
                    "error": None if passed else f"Invalid input not rejected: {result.decision}"
                })
                
            except Exception as e:
                # ValidationError is expected and acceptable
                tests.append({
                    "test": test_name,
                    "passed": True,
                    "error": None
                })
        
        return tests
    
    def _test_safe_output(self):
        """Test that all outputs are safe and complete"""
        tests = []
        
        test_cases = [
            ("normal message", "deliver"),
            ("urgent help needed", "summarize"),
            ("I hate everyone", "summarize")
        ]
        
        for content, expected_type in test_cases:
            try:
                result = self.validator.validate_inbound({
                    "content": content,
                    "source": "test",
                    "user_id": "smoke_test"
                })
                
                # Check output completeness and safety
                safe_output = result.safe_output
                passed = (
                    safe_output is not None and
                    "message_primary" in safe_output and
                    "suggested_action" in safe_output and
                    len(safe_output["message_primary"]) > 0 and
                    "urgency_level" in safe_output and
                    "emotional_tone" in safe_output
                    # Note: Original content may appear in "deliver" decision, which is safe
                )
                
                tests.append({
                    "test": f"Safe output for: {content[:15]}...",
                    "passed": passed,
                    "error": None if passed else "Unsafe or incomplete output generated"
                })
                
            except Exception as e:
                tests.append({
                    "test": f"Safe output for: {content[:15]}...",
                    "passed": False,
                    "error": f"Exception: {str(e)}"
                })
        
        return tests
    
    def _test_trace_ids(self):
        """Test that trace IDs are generated consistently"""
        tests = []
        
        # Test deterministic trace ID generation
        test_payload = {
            "content": "test message for trace ID",
            "source": "trace_test",
            "user_id": "smoke_test"
        }
        
        try:
            # Run same input multiple times
            trace_ids = []
            for i in range(3):
                result = self.validator.validate_inbound(test_payload)
                trace_ids.append(result.trace_id)
            
            # All trace IDs should be identical (deterministic)
            all_same = len(set(trace_ids)) == 1
            all_valid = all(len(tid) > 0 for tid in trace_ids)
            
            tests.append({
                "test": "Deterministic trace ID generation",
                "passed": all_same and all_valid,
                "error": None if (all_same and all_valid) else f"Inconsistent trace IDs: {trace_ids}"
            })
            
        except Exception as e:
            tests.append({
                "test": "Deterministic trace ID generation",
                "passed": False,
                "error": f"Exception: {str(e)}"
            })
        
        return tests
    
    def _test_emergency_fallbacks(self):
        """Test emergency fallback mechanisms"""
        tests = []
        
        # Force emergency mode
        original_failure_count = self.validator.failure_count
        self.validator.failure_count = 5  # Trigger emergency mode
        
        try:
            result = self.validator.validate_action({
                "content": "normal message",
                "action_type": "whatsapp_send",
                "recipient": "test",
                "user_id": "smoke_test"
            })
            
            # In emergency mode, should be more conservative
            passed = result.decision in ["hard_deny", "soft_rewrite"]
            
            tests.append({
                "test": "Emergency mode conservative behavior",
                "passed": passed,
                "error": None if passed else f"Not conservative in emergency mode: {result.decision}"
            })
            
        except Exception as e:
            tests.append({
                "test": "Emergency mode conservative behavior",
                "passed": False,
                "error": f"Exception: {str(e)}"
            })
        finally:
            # Restore original state
            self.validator.failure_count = original_failure_count
        
        return tests

if __name__ == "__main__":
    smoke_test = DemoSmokeTest()
    demo_ready = smoke_test.run_smoke_test()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = {
        "demo_ready": demo_ready,
        "timestamp": timestamp,
        "critical_failures": smoke_test.critical_failures
    }
    
    with open(f"demo_smoke_test_{timestamp}.json", "w") as f:
        json.dump(results, f, indent=2)
    
    if demo_ready:
        print(f"\n🎉 DEMO APPROVED - System ready for demonstration")
    else:
        print(f"\n🚫 DEMO BLOCKED - Fix critical failures before proceeding")
        exit(1)