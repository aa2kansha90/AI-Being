"""
INTEGRATION TEST SUITE - FAILURE SCENARIO TESTING
Tests all possible failure modes to ensure no silent failures
"""

import json
import time
from datetime import datetime
from hardened_validator import HardenedValidator, ValidationError, SystemState

class IntegrationTestSuite:
    def __init__(self):
        self.validator = HardenedValidator()
        self.test_results = []
        self.failure_scenarios = []
    
    def run_all_tests(self):
        """Run comprehensive test suite covering all failure modes"""
        print("🧪 INTEGRATION TEST SUITE - FAILURE SCENARIOS")
        print("=" * 60)
        
        # Test categories
        test_categories = [
            ("Input Validation Tests", self._test_input_validation),
            ("Hard Guard Tests", self._test_hard_guards),
            ("System Failure Tests", self._test_system_failures),
            ("Malformed Payload Tests", self._test_malformed_payloads),
            ("Edge Case Tests", self._test_edge_cases),
            ("Performance Stress Tests", self._test_performance_stress),
            ("Emergency Fallback Tests", self._test_emergency_fallbacks)
        ]
        
        total_tests = 0
        passed_tests = 0
        
        for category_name, test_function in test_categories:
            print(f"\n📋 {category_name}")
            print("-" * 40)
            
            category_results = test_function()
            category_passed = sum(1 for result in category_results if result["passed"])
            category_total = len(category_results)
            
            print(f"Results: {category_passed}/{category_total} passed")
            
            total_tests += category_total
            passed_tests += category_passed
            self.test_results.extend(category_results)
        
        # Final summary
        print(f"\n🎯 OVERALL RESULTS")
        print("=" * 30)
        print(f"Total tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Check for silent failures
        silent_failures = [r for r in self.test_results if not r["passed"] and "silent" in r.get("failure_type", "")]
        if silent_failures:
            print(f"🚨 CRITICAL: {len(silent_failures)} silent failures detected!")
            for failure in silent_failures:
                print(f"  - {failure['test_name']}: {failure['error']}")
        else:
            print("✅ NO SILENT FAILURES DETECTED")
        
        return self.test_results
    
    def _test_input_validation(self):
        """Test input validation with various invalid inputs"""
        tests = []
        
        # Missing required fields
        tests.append(self._run_test(
            "Missing content field",
            {"action_type": "whatsapp_send", "recipient": "test", "user_id": "user1"},
            "outbound",
            expected_decision="deny"
        ))
        
        # Empty content
        tests.append(self._run_test(
            "Empty content",
            {"content": "", "action_type": "email_send", "recipient": "test", "user_id": "user1"},
            "outbound",
            expected_decision="deny"
        ))
        
        # Invalid content type
        tests.append(self._run_test(
            "Non-string content",
            {"content": 123, "action_type": "sms_send", "recipient": "test", "user_id": "user1"},
            "outbound",
            expected_decision="deny"
        ))
        
        # Oversized content
        tests.append(self._run_test(
            "Oversized content",
            {"content": "x" * 15000, "action_type": "email_send", "recipient": "test", "user_id": "user1"},
            "outbound",
            expected_decision="deny"
        ))
        
        return tests
    
    def _test_hard_guards(self):
        """Test hard guards that should never be bypassed"""
        tests = []
        
        # Suicide content (must always escalate for inbound)
        tests.append(self._run_test(
            "Suicide content detection",
            {"content": "I want to kill myself", "source": "crisis", "user_id": "user1"},
            "inbound",
            expected_decision="escalate"
        ))
        
        # Threat content (must always block)
        tests.append(self._run_test(
            "Threat content detection",
            {"content": "I will kill you", "action_type": "whatsapp_send", "recipient": "victim", "user_id": "user1"},
            "outbound",
            expected_decision="hard_deny"
        ))
        
        # Financial scam (must always block)
        tests.append(self._run_test(
            "Financial scam detection",
            {"content": "Send money via cashapp emergency", "source": "scammer", "user_id": "user1"},
            "inbound",
            expected_decision="silence"
        ))
        
        # Variations of suicide keywords
        suicide_variations = [
            "end it all tonight",
            "want to die",
            "going to suicide",
            "kill myself now"
        ]
        
        for variation in suicide_variations:
            tests.append(self._run_test(
                f"Suicide variation: {variation[:20]}...",
                {"content": variation, "source": "crisis", "user_id": "user1"},
                "inbound",
                expected_decision="escalate"
            ))
        
        return tests
    
    def _test_system_failures(self):
        """Test system failure scenarios"""
        tests = []
        
        # Simulate content analysis failure by corrupting validator state
        original_analyze = self.validator._analyze_content_safe
        
        def failing_analyze(content):
            raise Exception("Simulated analysis failure")
        
        # Test with broken analysis
        self.validator._analyze_content_safe = failing_analyze
        
        tests.append(self._run_test(
            "Content analysis failure",
            {"content": "test message", "action_type": "email_send", "recipient": "test", "user_id": "user1"},
            "outbound",
            expected_decision="hard_deny",  # Should fallback to safe decision
            expect_error=True
        ))
        
        # Restore original function
        self.validator._analyze_content_safe = original_analyze
        
        # Test emergency mode activation
        self.validator.failure_count = 5  # Force emergency mode
        
        tests.append(self._run_test(
            "Emergency mode behavior",
            {"content": "normal message", "action_type": "whatsapp_send", "recipient": "test", "user_id": "user1"},
            "outbound",
            expected_decision="hard_deny"  # Should be extra conservative
        ))
        
        # Reset validator state
        self.validator.failure_count = 0
        self.validator.system_state = SystemState.HEALTHY
        
        return tests
    
    def _test_malformed_payloads(self):
        """Test various malformed payload scenarios"""
        tests = []
        
        # Non-dictionary payload
        tests.append(self._run_test(
            "Non-dict payload",
            "this is not a dictionary",
            "outbound",
            expected_decision="deny",
            expect_error=True
        ))
        
        # None payload
        tests.append(self._run_test(
            "None payload",
            None,
            "inbound",
            expected_decision="deny",
            expect_error=True
        ))
        
        # Payload with null values
        tests.append(self._run_test(
            "Null values in payload",
            {"content": None, "source": "test", "user_id": "user1"},
            "inbound",
            expected_decision="deny",
            expect_error=True
        ))
        
        # Payload with wrong direction
        tests.append(self._run_test(
            "Wrong direction field",
            {"direction": "inbound", "content": "test", "action_type": "email", "recipient": "test", "user_id": "user1"},
            "outbound",
            expected_decision="deny",
            expect_error=True
        ))
        
        return tests
    
    def _test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        tests = []
        
        # Empty string content (different from missing)
        tests.append(self._run_test(
            "Empty string content",
            {"content": "", "source": "test", "user_id": "user1"},
            "inbound",
            expected_decision="deny",
            expect_error=True
        ))
        
        # Unicode content
        tests.append(self._run_test(
            "Unicode content",
            {"content": "Hello 🌍 世界", "source": "test", "user_id": "user1"},
            "inbound",
            expected_decision="deliver"
        ))
        
        # Very long but valid content
        tests.append(self._run_test(
            "Maximum length content",
            {"content": "x" * 9999, "source": "test", "user_id": "user1"},
            "inbound",
            expected_decision="deliver"
        ))
        
        # Special characters
        tests.append(self._run_test(
            "Special characters",
            {"content": "!@#$%^&*()_+-=[]{}|;:,.<>?", "source": "test", "user_id": "user1"},
            "inbound",
            expected_decision="deliver"
        ))
        
        return tests
    
    def _test_performance_stress(self):
        """Test performance under stress conditions"""
        tests = []
        
        # Rapid successive calls
        start_time = time.time()
        rapid_results = []
        
        for i in range(10):
            try:
                result = self.validator.validate_inbound({
                    "content": f"test message {i}",
                    "source": f"source{i}",
                    "user_id": "stress_test"
                })
                rapid_results.append(result.decision)
            except Exception as e:
                rapid_results.append(f"error: {e}")
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 10
        
        tests.append({
            "test_name": "Rapid successive calls",
            "passed": all(isinstance(r, str) and r != "error" for r in rapid_results),
            "details": f"Average time per call: {avg_time:.3f}s",
            "results": rapid_results
        })
        
        # Large content processing
        large_content = "This is a test message. " * 200  # ~5000 characters
        
        tests.append(self._run_test(
            "Large content processing",
            {"content": large_content, "source": "test", "user_id": "user1"},
            "inbound",
            expected_decision="deliver"
        ))
        
        return tests
    
    def _test_emergency_fallbacks(self):
        """Test emergency fallback mechanisms"""
        tests = []
        
        # Force multiple failures to trigger emergency mode
        for i in range(4):
            self.validator.failure_count += 1
        
        # Test that emergency mode is more conservative
        tests.append(self._run_test(
            "Emergency mode - medium risk content",
            {"content": "urgent message", "action_type": "whatsapp_send", "recipient": "test", "user_id": "user1"},
            "outbound",
            expected_decision="hard_deny"  # Should be blocked in emergency mode
        ))
        
        # Reset for next test
        self.validator.failure_count = 0
        self.validator.system_state = SystemState.HEALTHY
        
        return tests
    
    def _run_test(self, test_name, payload, direction, expected_decision=None, expect_error=False):
        """Run individual test and return result"""
        try:
            if direction == "outbound":
                result = self.validator.validate_action(payload)
            else:
                result = self.validator.validate_inbound(payload)
            
            # Check if we got a valid result
            if not hasattr(result, 'decision') or not hasattr(result, 'trace_id'):
                return {
                    "test_name": test_name,
                    "passed": False,
                    "error": "Invalid result structure - missing required fields",
                    "failure_type": "silent_failure"
                }
            
            # Check decision if expected
            decision_correct = True
            if expected_decision:
                decision_correct = result.decision == expected_decision
            
            # Check if error was expected
            error_handling_correct = True
            if expect_error:
                error_handling_correct = (
                    result.error_details is not None or 
                    result.system_state == SystemState.EMERGENCY.value or
                    result.decision in ["deny", "hard_deny", "escalate"]
                )
            
            passed = decision_correct and error_handling_correct
            
            test_result = {
                "test_name": test_name,
                "passed": passed,
                "actual_decision": result.decision,
                "expected_decision": expected_decision,
                "system_state": result.system_state,
                "trace_id": result.trace_id,
                "has_safe_output": result.safe_output is not None
            }
            
            if not passed:
                test_result["failure_reason"] = f"Expected {expected_decision}, got {result.decision}"
            
            print(f"  {'✅' if passed else '❌'} {test_name}: {result.decision}")
            
            return test_result
            
        except Exception as e:
            # Any unhandled exception is a failure
            error_result = {
                "test_name": test_name,
                "passed": False,
                "error": str(e),
                "failure_type": "exception_failure"
            }
            
            print(f"  ❌ {test_name}: EXCEPTION - {str(e)}")
            return error_result

if __name__ == "__main__":
    test_suite = IntegrationTestSuite()
    results = test_suite.run_all_tests()
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"integration_test_results_{timestamp}.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📝 Detailed results saved to integration_test_results_{timestamp}.json")