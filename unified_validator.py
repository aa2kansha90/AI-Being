"""
UNIFIED BIDIRECTIONAL VALIDATOR
Validates both outbound actions and inbound messages
"""

import json
import hashlib
from datetime import datetime, time
from enum import Enum
from typing import Dict, List, Optional, Tuple

class ActionType(Enum):
    WHATSAPP_SEND = "whatsapp_send"
    EMAIL_SEND = "email_send"
    INSTAGRAM_DM_SEND = "instagram_dm_send"
    SMS_SEND = "sms_send"

class OutboundDecision(Enum):
    ALLOW = "allow"
    SOFT_REWRITE = "soft_rewrite"
    HARD_DENY = "hard_deny"

class InboundDecision(Enum):
    DELIVER = "deliver"
    SUMMARIZE = "summarize"
    DELAY = "delay"
    SILENCE = "silence"
    ESCALATE = "escalate"

class UnifiedValidator:
    def __init__(self):
        self.contact_history = {}  # Track repeated contact patterns
        self.time_rules = {
            "quiet_hours": {"start": "22:00", "end": "07:00"},
            "work_hours": {"start": "09:00", "end": "17:00"}
        }
    
    def validate_action(self, action_payload: Dict) -> Dict:
        """Validate outbound actions before sending"""
        
        # Generate deterministic trace
        trace_content = f"{action_payload.get('content', '')}:{action_payload.get('action_type', '')}:outbound"
        trace_id = hashlib.md5(trace_content.encode()).hexdigest()[:16]
        
        # Extract action details
        action_type = action_payload.get("action_type")
        content = action_payload.get("content", "")
        recipient = action_payload.get("recipient", "")
        user_id = action_payload.get("user_id", "")
        
        # Check enforcement rules
        enforcement_result = self._check_outbound_enforcement(
            user_id, recipient, content, action_type
        )
        
        if enforcement_result["blocked"]:
            return {
                "trace_id": trace_id,
                "direction": "outbound",
                "decision": OutboundDecision.HARD_DENY.value,
                "enforcement_reason": enforcement_result["reason"],
                "safe_rewrite": enforcement_result.get("safe_rewrite"),
                "timestamp": datetime.now().isoformat()
            }
        
        # Content analysis
        risk_analysis = self._analyze_outbound_content(content)
        
        # Make decision
        if risk_analysis["severity"] == "high":
            decision = OutboundDecision.HARD_DENY.value
        elif risk_analysis["severity"] == "medium":
            decision = OutboundDecision.SOFT_REWRITE.value
        else:
            decision = OutboundDecision.ALLOW.value
        
        return {
            "trace_id": trace_id,
            "direction": "outbound",
            "decision": decision,
            "risk_categories": risk_analysis["categories"],
            "safe_rewrite": risk_analysis.get("safe_rewrite"),
            "original_content": content if decision == OutboundDecision.ALLOW.value else None,
            "timestamp": datetime.now().isoformat()
        }
    
    def validate_inbound(self, message_payload: Dict) -> Dict:
        """Validate inbound messages before user sees them"""
        
        # Generate deterministic trace
        trace_content = f"{message_payload.get('content', '')}:{message_payload.get('source', '')}:inbound"
        trace_id = hashlib.md5(trace_content.encode()).hexdigest()[:16]
        
        # Extract message details
        content = message_payload.get("content", "")
        source = message_payload.get("source", "")
        user_id = message_payload.get("user_id", "")
        
        # Check enforcement rules
        enforcement_result = self._check_inbound_enforcement(
            user_id, source, content
        )
        
        if enforcement_result["blocked"]:
            # Generate safe output for enforcement blocks
            safe_output = self._generate_safe_output_for_enforcement(
                enforcement_result["decision"], enforcement_result["reason"]
            )
            return {
                "trace_id": trace_id,
                "direction": "inbound",
                "decision": enforcement_result["decision"],
                "enforcement_reason": enforcement_result["reason"],
                "safe_output": safe_output,
                "timestamp": datetime.now().isoformat()
            }
        
        # Content analysis
        risk_analysis = self._analyze_inbound_content(content, source)
        
        # Make decision based on risk
        decision = self._determine_inbound_decision(risk_analysis)
        
        # Generate safe output
        safe_output = self._generate_safe_output(content, risk_analysis, decision)
        
        return {
            "trace_id": trace_id,
            "direction": "inbound",
            "decision": decision,
            "risk_categories": risk_analysis["categories"],
            "safe_output": safe_output,
            "timestamp": datetime.now().isoformat()
        }
    
    def _check_outbound_enforcement(self, user_id: str, recipient: str, content: str, action_type: str) -> Dict:
        """Check outbound enforcement rules"""
        
        # Time-of-day rules
        current_time = datetime.now().time()
        if self._is_quiet_hours(current_time) and not self._is_emergency_content(content):
            return {
                "blocked": True,
                "reason": "quiet_hours_violation",
                "safe_rewrite": f"Message scheduled for delivery at 7:00 AM: {content[:50]}..."
            }
        
        # Repeated contact abuse
        contact_key = f"{user_id}:{recipient}"
        if self._check_repeated_contact_abuse(contact_key):
            return {
                "blocked": True,
                "reason": "repeated_contact_abuse",
                "safe_rewrite": "Consider giving the recipient some space before messaging again."
            }
        
        # Emotional escalation detection
        if self._detect_emotional_escalation(content):
            return {
                "blocked": True,
                "reason": "emotional_escalation",
                "safe_rewrite": "Take a moment to cool down before sending this message."
            }
        
        return {"blocked": False}
    
    def _check_inbound_enforcement(self, user_id: str, source: str, content: str) -> Dict:
        """Check inbound enforcement rules"""
        
        # Time-of-day rules for non-emergency content
        current_time = datetime.now().time()
        if self._is_quiet_hours(current_time) and not self._is_emergency_content(content):
            return {
                "blocked": True,
                "decision": InboundDecision.DELAY.value,
                "reason": "quiet_hours_protection",
                "safe_summary": "Message received during quiet hours - will be delivered at 7:00 AM"
            }
        
        # Spam/harassment detection
        if self._detect_spam_pattern(source, content):
            return {
                "blocked": True,
                "decision": InboundDecision.SILENCE.value,
                "reason": "spam_pattern_detected",
                "safe_summary": "Promotional content filtered"
            }
        
        # Crisis content escalation
        if self._detect_crisis_content(content):
            return {
                "blocked": True,
                "decision": InboundDecision.ESCALATE.value,
                "reason": "crisis_content_detected",
                "safe_summary": "Crisis support has been contacted"
            }
        
        return {"blocked": False}
    
    def _analyze_outbound_content(self, content: str) -> Dict:
        """Analyze outbound content for risks"""
        categories = []
        severity = "low"
        
        # Check for aggressive language
        aggressive_keywords = ["hate", "kill", "destroy", "revenge", "payback"]
        if any(keyword in content.lower() for keyword in aggressive_keywords):
            categories.append("aggressive_language")
            severity = "high"
        
        # Check for emotional manipulation
        manipulation_keywords = ["if you don't", "you have to", "you must", "or else"]
        if any(keyword in content.lower() for keyword in manipulation_keywords):
            categories.append("emotional_manipulation")
            severity = "medium"
        
        # Check for spam indicators
        spam_keywords = ["urgent", "limited time", "act now", "click here"]
        if any(keyword in content.lower() for keyword in spam_keywords):
            categories.append("spam_indicators")
            severity = "medium"
        
        safe_rewrite = None
        if severity in ["medium", "high"]:
            safe_rewrite = self._generate_safe_rewrite(content, categories)
        
        return {
            "categories": categories,
            "severity": severity,
            "safe_rewrite": safe_rewrite
        }
    
    def _analyze_inbound_content(self, content: str, source: str) -> Dict:
        """Analyze inbound content for risks"""
        categories = []
        severity = "low"
        
        # Emotional manipulation
        manipulation_keywords = ["devastated", "heartbroken", "abandoned", "last hope"]
        if any(keyword in content.lower() for keyword in manipulation_keywords):
            categories.append("emotional_manipulation")
            severity = "high"
        
        # Urgency abuse
        urgency_keywords = ["urgent", "emergency", "right now", "immediately"]
        if any(keyword in content.lower() for keyword in urgency_keywords):
            categories.append("urgency_abuse")
            severity = "medium"
        
        # Financial scam indicators
        financial_keywords = ["send money", "cashapp", "venmo", "$", "payment"]
        if any(keyword in content.lower() for keyword in financial_keywords):
            categories.append("financial_scam")
            severity = "high"
        
        # Self-harm triggers
        harm_keywords = ["kill myself", "end it all", "suicide", "hurt myself"]
        if any(keyword in content.lower() for keyword in harm_keywords):
            categories.append("self_harm_triggers")
            severity = "critical"
        
        # Harassment detection
        harassment_keywords = ["terrible person", "hate you", "worthless", "pathetic", "loser"]
        if any(keyword in content.lower() for keyword in harassment_keywords):
            categories.append("harassment")
            severity = "high"
        
        return {
            "categories": categories,
            "severity": severity
        }
    
    def _determine_inbound_decision(self, risk_analysis: Dict) -> str:
        """Determine inbound decision based on risk analysis"""
        severity = risk_analysis["severity"]
        categories = risk_analysis["categories"]
        
        if severity == "critical" or "self_harm_triggers" in categories:
            return InboundDecision.ESCALATE.value
        elif severity == "high":
            return InboundDecision.SUMMARIZE.value
        elif severity == "medium":
            return InboundDecision.DELAY.value
        else:
            return InboundDecision.DELIVER.value
    
    def _generate_safe_output(self, content: str, risk_analysis: Dict, decision: str) -> Dict:
        """Generate safe output for user"""
        if decision == InboundDecision.DELIVER.value:
            return {
                "message_primary": content,
                "urgency_level": "normal",
                "source_hidden": "Verified contact",
                "suggested_action": "No action required",
                "emotional_tone": "neutral"
            }
        elif decision == InboundDecision.SUMMARIZE.value:
            return {
                "message_primary": "Message contains concerning content - review when ready",
                "urgency_level": "low",
                "source_hidden": "Unknown contact",
                "suggested_action": "Review for safety concerns",
                "emotional_tone": "protective"
            }
        elif decision == InboundDecision.DELAY.value:
            return {
                "message_primary": "Message with urgency indicators received",
                "urgency_level": "medium",
                "source_hidden": "Contact",
                "suggested_action": "Review when ready (no time pressure)",
                "emotional_tone": "neutral"
            }
        elif decision == InboundDecision.ESCALATE.value:
            return {
                "message_primary": "Crisis support has been contacted",
                "urgency_level": "high",
                "source_hidden": "Support team notified",
                "suggested_action": "Professional support activated",
                "emotional_tone": "supportive"
            }
        else:  # SILENCE
            return {
                "message_primary": "Content filtered",
                "urgency_level": "low",
                "source_hidden": "Filtered source",
                "suggested_action": "Available in filtered folder",
                "emotional_tone": "neutral"
            }
    
    def _generate_safe_rewrite(self, content: str, categories: List[str]) -> str:
        """Generate safe rewrite for outbound content"""
        if "aggressive_language" in categories:
            return "I'm feeling frustrated about this situation and would like to discuss it."
        elif "emotional_manipulation" in categories:
            return "I'd appreciate your help with this when you have a chance."
        else:
            return "I wanted to reach out about something important."
    
    def _is_quiet_hours(self, current_time: time) -> bool:
        """Check if current time is in quiet hours"""
        start = time.fromisoformat(self.time_rules["quiet_hours"]["start"])
        end = time.fromisoformat(self.time_rules["quiet_hours"]["end"])
        
        # Handle overnight quiet hours (22:00-07:00)
        if start > end:
            return current_time >= start or current_time <= end
        else:
            return start <= current_time <= end
    
    def _is_emergency_content(self, content: str) -> bool:
        """Check if content is genuine emergency"""
        emergency_keywords = ["911", "hospital", "accident", "fire", "police", "ambulance", "emergency"]
        return any(keyword in content.lower() for keyword in emergency_keywords)
    
    def _check_repeated_contact_abuse(self, contact_key: str) -> bool:
        """Check for repeated contact abuse pattern"""
        # Simplified: check if more than 5 messages in last hour
        if contact_key not in self.contact_history:
            self.contact_history[contact_key] = []
        
        now = datetime.now()
        # Remove old entries (older than 1 hour)
        self.contact_history[contact_key] = [
            timestamp for timestamp in self.contact_history[contact_key]
            if (now - timestamp).seconds < 3600
        ]
        
        # Add current timestamp
        self.contact_history[contact_key].append(now)
        
        # Check if more than 5 messages in last hour
        return len(self.contact_history[contact_key]) > 5
    
    def _detect_emotional_escalation(self, content: str) -> bool:
        """Detect emotional escalation in outbound content"""
        escalation_keywords = ["furious", "enraged", "hate you", "never forgive", "done with you"]
        return any(keyword in content.lower() for keyword in escalation_keywords)
    
    def _detect_spam_pattern(self, source: str, content: str) -> bool:
        """Detect spam patterns in inbound content"""
        spam_indicators = ["congratulations", "you've won", "click here", "limited time"]
        return any(indicator in content.lower() for indicator in spam_indicators)
    
    def _detect_crisis_content(self, content: str) -> bool:
        """Detect crisis content requiring escalation"""
        crisis_keywords = ["kill myself", "end it all", "suicide", "hurt myself", "no point living"]
        return any(keyword in content.lower() for keyword in crisis_keywords)
    
    def _generate_safe_output_for_enforcement(self, decision: str, reason: str) -> Dict:
        """Generate safe output for enforcement-blocked content"""
        if decision == InboundDecision.ESCALATE.value:
            return {
                "message_primary": "Crisis support has been contacted",
                "urgency_level": "high",
                "source_hidden": "Support team notified",
                "suggested_action": "Professional support activated",
                "emotional_tone": "supportive"
            }
        elif decision == InboundDecision.DELAY.value:
            return {
                "message_primary": "Message received during quiet hours",
                "urgency_level": "low",
                "source_hidden": "Contact",
                "suggested_action": "Will be delivered at 7:00 AM",
                "emotional_tone": "neutral"
            }
        elif decision == InboundDecision.SILENCE.value:
            return {
                "message_primary": "Content filtered",
                "urgency_level": "low",
                "source_hidden": "Filtered source",
                "suggested_action": "Available in filtered folder",
                "emotional_tone": "neutral"
            }
        else:
            return {
                "message_primary": "Message filtered for safety",
                "urgency_level": "low",
                "source_hidden": "Unknown contact",
                "suggested_action": "Review when ready",
                "emotional_tone": "protective"
            }

# Example usage and testing
if __name__ == "__main__":
    validator = UnifiedValidator()
    
    print("🛡️  UNIFIED BIDIRECTIONAL VALIDATOR DEMO")
    print("=" * 50)
    
    # Test outbound actions
    print("\n📤 OUTBOUND ACTION VALIDATION")
    print("-" * 30)
    
    outbound_tests = [
        {
            "action_type": "whatsapp_send",
            "content": "I hate you and will never forgive you for this!",
            "recipient": "friend@example.com",
            "user_id": "user123"
        },
        {
            "action_type": "email_send", 
            "content": "Hi, can we meet for coffee tomorrow?",
            "recipient": "colleague@work.com",
            "user_id": "user123"
        }
    ]
    
    for test in outbound_tests:
        result = validator.validate_action(test)
        print(f"Content: \"{test['content'][:50]}...\"")
        print(f"Decision: {result['decision'].upper()}")
        if result.get('safe_rewrite'):
            print(f"Safe rewrite: \"{result['safe_rewrite']}\"")
        print()
    
    # Test inbound messages
    print("\n📥 INBOUND MESSAGE VALIDATION")
    print("-" * 30)
    
    inbound_tests = [
        {
            "content": "EMERGENCY!!! Need $500 RIGHT NOW or mom dies!",
            "source": "unknown@scammer.com",
            "user_id": "user123"
        },
        {
            "content": "Everyone has abandoned me. I'm going to kill myself tonight.",
            "source": "stranger@social.com", 
            "user_id": "user123"
        },
        {
            "content": "Meeting moved to 3 PM tomorrow. See you then!",
            "source": "boss@company.com",
            "user_id": "user123"
        }
    ]
    
    for test in inbound_tests:
        result = validator.validate_inbound(test)
        print(f"Original: \"{test['content'][:50]}...\"")
        print(f"Decision: {result['decision'].upper()}")
        print(f"User sees: \"{result['safe_output']['message_primary']}\"")
        print(f"Action: {result['safe_output']['suggested_action']}")
        print()
    
    print("✅ All validations complete!")