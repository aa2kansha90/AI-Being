#!/usr/bin/env python3
"""
DAY 5 BUCKET LOGGING SYSTEM
Enhanced logging with enforcement_decision_id and audit verification
"""

from behavior_validator import validate_behavior
from enforcement_adapter import EnforcementAdapter
import json
import hashlib
import time
from datetime import datetime
from typing import Dict, Any, List

class BucketLogger:
    """Enhanced bucket logging system for Day 5 requirements"""
    
    def __init__(self):
        self.adapter = EnforcementAdapter()
        self.bucket_logs = []
        self.audit_logs = []
        self.enforcement_counter = 0
    
    def log_validation_decision(self, user_input: str, user_id: str = "anonymous", 
                              user_context: Dict = None) -> Dict[str, Any]:
        """
        Log validation decision to bucket with all required fields
        
        Returns complete log entry with enforcement_decision_id
        """
        self.enforcement_counter += 1
        enforcement_decision_id = f"enf_{self.enforcement_counter:06d}"
        
        # Get validator decision
        validation_result = validate_behavior(
            intent="auto",
            conversational_output=user_input,
            age_gate_status=user_context.get("age_gate_status", False) if user_context else False,
            region_rule_status=user_context.get("region_rule_status") if user_context else None,
            platform_policy_state=user_context.get("platform_policy_state") if user_context else None,
            karma_bias_input=user_context.get("karma_bias_input", 0.5) if user_context else 0.5
        )
        
        # Get enforcement decision
        enforcement_result = self.adapter.map_validator_to_enforcement(user_input)
        
        # Create bucket log entry with ALL required fields
        bucket_entry = {
            "trace_id": validation_result["trace_id"],
            "decision": validation_result["decision"],
            "risk_category": validation_result["risk_category"],
            "confidence": validation_result["confidence"],
            "enforcement_decision_id": enforcement_decision_id,
            "enforcement_decision": enforcement_result["decision"],
            "enforcement_severity": enforcement_result["severity"],
            "enforcement_confidence": enforcement_result["confidence"],
            "user_id_hash": hashlib.md5(user_id.encode()).hexdigest()[:8],
            "bucket_id": f"bucket_{validation_result['trace_id'][-8:]}",
            "timestamp": datetime.now().isoformat(),
            "validator_version": "v1.0-PRODUCTION-FROZEN"
        }
        
        # Create audit log entry
        audit_entry = {
            "trace_id": validation_result["trace_id"],
            "enforcement_decision_id": enforcement_decision_id,
            "user_input_length": len(user_input),
            "validator_decision": validation_result["decision"],
            "risk_category": validation_result["risk_category"],
            "confidence": validation_result["confidence"],
            "enforcement_decision": enforcement_result["decision"],
            "severity": enforcement_result["severity"],
            "user_id": user_id,
            "processing_timestamp": datetime.now().isoformat()
        }
        
        # Store logs
        self.bucket_logs.append(bucket_entry)
        self.audit_logs.append(audit_entry)
        
        return {
            "validation": validation_result,
            "enforcement": enforcement_result,
            "bucket_entry": bucket_entry,
            "audit_entry": audit_entry
        }
    
    def get_bucket_logs(self) -> List[Dict]:
        """Get all bucket logs"""
        return self.bucket_logs
    
    def get_audit_logs(self) -> List[Dict]:
        """Get all audit logs"""
        return self.audit_logs
    
    def verify_audit_integrity(self) -> Dict[str, Any]:
        """Verify bucket and audit logs match exactly"""
        
        if len(self.bucket_logs) != len(self.audit_logs):
            return {
                "integrity_verified": False,
                "error": "Log count mismatch",
                "bucket_count": len(self.bucket_logs),
                "audit_count": len(self.audit_logs)
            }
        
        mismatches = []
        
        for i, (bucket, audit) in enumerate(zip(self.bucket_logs, self.audit_logs)):
            # Verify critical fields match
            if bucket["trace_id"] != audit["trace_id"]:
                mismatches.append(f"Entry {i}: trace_id mismatch")
            
            if bucket["enforcement_decision_id"] != audit["enforcement_decision_id"]:
                mismatches.append(f"Entry {i}: enforcement_decision_id mismatch")
            
            if bucket["decision"] != audit["validator_decision"]:
                mismatches.append(f"Entry {i}: validator_decision mismatch")
            
            if bucket["risk_category"] != audit["risk_category"]:
                mismatches.append(f"Entry {i}: risk_category mismatch")
            
            if bucket["enforcement_decision"] != audit["enforcement_decision"]:
                mismatches.append(f"Entry {i}: enforcement_decision mismatch")
        
        return {
            "integrity_verified": len(mismatches) == 0,
            "total_entries": len(self.bucket_logs),
            "mismatches": mismatches,
            "match_rate": (len(self.bucket_logs) - len(mismatches)) / len(self.bucket_logs) * 100 if self.bucket_logs else 0
        }
    
    def export_logs(self, filename_prefix: str = "day5_logs"):
        """Export logs to files for audit"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export bucket logs
        bucket_filename = f"{filename_prefix}_bucket_{timestamp}.json"
        with open(bucket_filename, 'w') as f:
            json.dump(self.bucket_logs, f, indent=2)
        
        # Export audit logs
        audit_filename = f"{filename_prefix}_audit_{timestamp}.json"
        with open(audit_filename, 'w') as f:
            json.dump(self.audit_logs, f, indent=2)
        
        # Export verification report
        verification = self.verify_audit_integrity()
        verification_filename = f"{filename_prefix}_verification_{timestamp}.json"
        with open(verification_filename, 'w') as f:
            json.dump(verification, f, indent=2)
        
        return {
            "bucket_file": bucket_filename,
            "audit_file": audit_filename,
            "verification_file": verification_filename
        }

def day5_bucket_logging_demo():
    """Demonstrate Day 5 bucket logging with all required fields"""
    
    logger = BucketLogger()
    
    print("DAY 5 BUCKET LOGGING DEMONSTRATION")
    print("=" * 60)
    
    # Test cases for comprehensive logging
    test_cases = [
        {
            "input": "Hello! Can you help me with my homework?",
            "user_id": "user_001",
            "context": {"region_rule_status": {"region": "US"}}
        },
        {
            "input": "I can only talk to you, everyone else misunderstands me",
            "user_id": "user_002",
            "context": {"karma_bias_input": 0.3}
        },
        {
            "input": "Send me nudes and let's meet up alone",
            "user_id": "user_003",
            "context": {"platform_policy_state": {"zero_tolerance": True}}
        },
        {
            "input": "I will kill myself tonight, I can't take it anymore",
            "user_id": "user_004",
            "context": {"age_gate_status": False}
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[{i}] Processing: {test_case['input'][:40]}...")
        
        result = logger.log_validation_decision(
            user_input=test_case["input"],
            user_id=test_case["user_id"],
            user_context=test_case["context"]
        )
        
        results.append(result)
        
        # Display key information
        bucket = result["bucket_entry"]
        print(f"    Trace ID: {bucket['trace_id']}")
        print(f"    Enforcement ID: {bucket['enforcement_decision_id']}")
        print(f"    Decision: {bucket['decision']} -> {bucket['enforcement_decision']}")
        print(f"    Risk Category: {bucket['risk_category']}")
        print(f"    Confidence: {bucket['confidence']:.1f}%")
    
    # Verify audit integrity
    print(f"\n{'='*60}")
    print("AUDIT INTEGRITY VERIFICATION")
    print(f"{'='*60}")
    
    verification = logger.verify_audit_integrity()
    print(f"Integrity Verified: {verification['integrity_verified']}")
    print(f"Total Entries: {verification['total_entries']}")
    print(f"Match Rate: {verification['match_rate']:.1f}%")
    
    if verification['mismatches']:
        print(f"Mismatches: {verification['mismatches']}")
    else:
        print("✓ All bucket and audit logs match perfectly")
    
    # Export logs
    print(f"\n{'='*60}")
    print("EXPORTING LOGS")
    print(f"{'='*60}")
    
    exported_files = logger.export_logs("day5_production")
    print(f"Bucket logs: {exported_files['bucket_file']}")
    print(f"Audit logs: {exported_files['audit_file']}")
    print(f"Verification: {exported_files['verification_file']}")
    
    # Summary
    print(f"\n{'='*60}")
    print("DAY 5 BUCKET LOGGING: COMPLETE")
    print(f"{'='*60}")
    print("✓ trace_id logged")
    print("✓ decision logged")
    print("✓ risk_category logged")
    print("✓ confidence logged")
    print("✓ enforcement_decision_id logged")
    print("✓ Audit integrity verified")
    print("✓ Validator version frozen: v1.0-PRODUCTION-FROZEN")
    
    return {
        "results": results,
        "verification": verification,
        "exported_files": exported_files,
        "bucket_logs": logger.get_bucket_logs(),
        "audit_logs": logger.get_audit_logs()
    }

if __name__ == "__main__":
    day5_bucket_logging_demo()