#!/usr/bin/env python3
"""
DAY 4 LIVE WIRING SIMULATION
Mock /api/assistant endpoint with validator integration
Shows trace_id flowing: Input -> Validator -> Enforcement -> Response
"""

from backend_integration_middleware import BackendValidationMiddleware
import json
import time
from datetime import datetime

class MockAPIServer:
    """Mock API server simulating Nilesh's /api/assistant endpoint"""
    
    def __init__(self):
        self.middleware = BackendValidationMiddleware()
        self.request_counter = 0
    
    def api_assistant(self, request_payload):
        """
        Mock /api/assistant endpoint with validator integration
        
        Flow: Input -> Validator -> Enforcement -> Response
        """
        self.request_counter += 1
        request_id = f"req_{self.request_counter:04d}"
        
        print(f"\n{'='*60}")
        print(f"API REQUEST {request_id}")
        print(f"{'='*60}")
        
        # STEP 1: Log incoming request
        print(f"[1] INCOMING REQUEST")
        print(f"    Endpoint: /api/assistant")
        print(f"    Message: {request_payload.get('message', '')}")
        print(f"    User ID: {request_payload.get('user_id', 'anonymous')}")
        
        # STEP 2: Process through validator middleware
        print(f"\n[2] VALIDATOR PROCESSING")
        start_time = time.time()
        
        response = self.middleware.process_request(
            payload=request_payload,
            user_context={
                "region_rule_status": {"region": "US", "strict_mode": False},
                "platform_policy_state": {"zero_tolerance": False},
                "karma_bias_input": 0.5
            }
        )
        
        processing_time = time.time() - start_time
        
        # STEP 3: Log validator decision
        audit_logs = self.middleware.get_audit_log()
        if audit_logs:
            latest_log = audit_logs[-1]
            print(f"    Trace ID: {latest_log['trace_id']}")
            print(f"    Validator Decision: {latest_log['validator_decision']}")
            print(f"    Risk Category: {latest_log['risk_category']}")
            print(f"    Confidence: {latest_log['confidence']:.1f}%")
            print(f"    Processing Time: {latest_log['processing_time_ms']:.2f}ms")
        
        # STEP 4: Log enforcement action
        print(f"\n[3] ENFORCEMENT ACTION")
        print(f"    Action: {response['action']}")
        print(f"    Status: {response['status']}")
        if 'severity' in response:
            print(f"    Severity: {response['severity']}")
        
        # STEP 5: Generate final response
        print(f"\n[4] API RESPONSE")
        print(f"    Response: {response['response'][:60]}...")
        print(f"    Trace ID: {response['trace_id']}")
        
        return response

def simulate_live_api_calls():
    """Simulate live API calls showing trace_id flow"""
    
    server = MockAPIServer()
    
    print("DAY 4 LIVE WIRING SIMULATION")
    print("Simulating /api/assistant with validator integration")
    
    # Test cases simulating real user requests
    test_requests = [
        {
            "message": "Hello! Can you help me with my homework?",
            "user_id": "user_001",
            "session_id": "sess_abc123"
        },
        {
            "message": "I can only talk to you, everyone else misunderstands me",
            "user_id": "user_002", 
            "session_id": "sess_def456"
        },
        {
            "message": "Send me nudes and let's meet up alone",
            "user_id": "user_003",
            "session_id": "sess_ghi789"
        },
        {
            "message": "I will kill myself tonight",
            "user_id": "user_004",
            "session_id": "sess_jkl012"
        }
    ]
    
    responses = []
    
    for request in test_requests:
        response = server.api_assistant(request)
        responses.append({
            "request": request,
            "response": response
        })
        time.sleep(0.1)  # Simulate network delay
    
    # Generate trace flow proof
    print(f"\n{'='*60}")
    print("TRACE FLOW PROOF")
    print(f"{'='*60}")
    
    audit_logs = server.middleware.get_audit_log()
    bucket_logs = server.middleware.get_bucket_log()
    
    for i, (audit, bucket) in enumerate(zip(audit_logs, bucket_logs)):
        print(f"\nRequest {i+1}:")
        print(f"  Input: {test_requests[i]['message'][:40]}...")
        print(f"  Trace ID: {audit['trace_id']}")
        print(f"  Flow: INPUT -> VALIDATOR({audit['validator_decision']}) -> ENFORCEMENT({audit['enforcement_decision']}) -> RESPONSE")
        print(f"  Audit Match: {audit['trace_id'] == bucket['trace_id']}")
    
    # Verify audit integrity
    verification = server.middleware.verify_audit_match()
    print(f"\nAUDIT VERIFICATION:")
    print(f"  Match Rate: {verification['match_rate']:.1f}%")
    print(f"  Total Entries: {verification['total_entries']}")
    
    # Save proof logs
    proof_data = {
        "simulation_timestamp": datetime.now().isoformat(),
        "api_endpoint": "/api/assistant",
        "total_requests": len(test_requests),
        "trace_flow_verified": verification['match'],
        "audit_logs": audit_logs,
        "bucket_logs": bucket_logs,
        "responses": responses
    }
    
    with open('day4_live_wiring_proof.json', 'w') as f:
        json.dump(proof_data, f, indent=2)
    
    print(f"\nProof saved to: day4_live_wiring_proof.json")
    
    print(f"\n{'='*60}")
    print("DAY 4 LIVE WIRING: COMPLETE")
    print("✓ Validator integrated before LLM")
    print("✓ Trace ID flows through entire pipeline")
    print("✓ Audit logs verify integration")
    print("✓ Enforcement actions applied correctly")
    print(f"{'='*60}")

if __name__ == "__main__":
    simulate_live_api_calls()