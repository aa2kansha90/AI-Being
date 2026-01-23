# UNIFIED INPUT/OUTPUT SCHEMA
**Standardized Interface Specification**

## OVERVIEW
This document defines the canonical input and output formats for the unified bidirectional safety validator, ensuring consistent interfaces across all system components.

---

## INPUT SCHEMAS

### **Outbound Action Payload**
```json
{
  "direction": "outbound",
  "action_type": "whatsapp_send|email_send|instagram_dm_send|sms_send",
  "user_id": "string",
  "recipient": "string",
  "content": "string",
  "metadata": {
    "timestamp": "ISO_8601_string",
    "channel_context": "object",
    "user_preferences": "object"
  }
}
```

**Required Fields:**
- `direction` - Must be "outbound"
- `action_type` - Specific communication channel
- `user_id` - Unique user identifier
- `recipient` - Target contact (email, phone, username)
- `content` - Message text to be validated

**Optional Fields:**
- `metadata.timestamp` - When action was initiated
- `metadata.channel_context` - Platform-specific data
- `metadata.user_preferences` - User configuration overrides

### **Inbound Message Payload**
```json
{
  "direction": "inbound",
  "content": "string",
  "source": "string",
  "user_id": "string",
  "channel": "whatsapp|email|instagram|sms|notification|alert",
  "metadata": {
    "timestamp": "ISO_8601_string",
    "message_id": "string",
    "thread_context": "object"
  }
}
```

**Required Fields:**
- `direction` - Must be "inbound"
- `content` - Message text to be filtered
- `source` - Sender identifier (email, phone, username)
- `user_id` - Recipient user identifier
- `channel` - Communication platform

**Optional Fields:**
- `metadata.timestamp` - When message was received
- `metadata.message_id` - Platform message identifier
- `metadata.thread_context` - Conversation history

---

## OUTPUT SCHEMAS

### **Validation Response (Universal)**
```json
{
  "trace_id": "string",
  "direction": "inbound|outbound",
  "decision": "allow|soft_rewrite|hard_deny|deliver|summarize|delay|silence|escalate",
  "risk_categories": ["string"],
  "severity": "low|medium|high|critical",
  "enforcement_reason": "string|null",
  "processing_time_ms": "number",
  "timestamp": "ISO_8601_string"
}
```

### **Outbound Response (Additional Fields)**
```json
{
  "original_content": "string|null",
  "safe_rewrite": "string|null",
  "block_reason": "string|null",
  "retry_allowed": "boolean",
  "suggested_alternatives": ["string"]
}
```

### **Inbound Response (Additional Fields)**
```json
{
  "safe_output": {
    "message_primary": "string",
    "urgency_level": "low|medium|high|critical",
    "source_hidden": "string",
    "suggested_action": "string",
    "emotional_tone": "neutral|protective|supportive|transparent"
  },
  "original_blocked": "boolean",
  "escalation_triggered": "boolean",
  "filtered_reason": "string|null"
}
```

---

## COMPLETE RESPONSE EXAMPLES

### **Outbound - Allowed**
```json
{
  "trace_id": "a7f3c2d1e8b9f4a6",
  "direction": "outbound",
  "decision": "allow",
  "risk_categories": [],
  "severity": "low",
  "enforcement_reason": null,
  "processing_time_ms": 45,
  "timestamp": "2024-01-22T10:30:00Z",
  "original_content": "Hi Sarah, can we meet for coffee tomorrow?",
  "safe_rewrite": null,
  "block_reason": null,
  "retry_allowed": true,
  "suggested_alternatives": []
}
```

### **Outbound - Blocked with Rewrite**
```json
{
  "trace_id": "b8e4d3f2a9c5e7b1",
  "direction": "outbound",
  "decision": "soft_rewrite",
  "risk_categories": ["emotional_manipulation"],
  "severity": "medium",
  "enforcement_reason": null,
  "processing_time_ms": 78,
  "timestamp": "2024-01-22T10:31:00Z",
  "original_content": "If you don't respond I'll know you don't care about me",
  "safe_rewrite": "I'd appreciate your help when you have a chance",
  "block_reason": null,
  "retry_allowed": true,
  "suggested_alternatives": [
    "I'm hoping to hear from you soon",
    "Let me know when you're available to chat"
  ]
}
```

### **Outbound - Hard Denied**
```json
{
  "trace_id": "c9f5e4a3b7d6f8c2",
  "direction": "outbound",
  "decision": "hard_deny",
  "risk_categories": ["aggressive_language", "harassment"],
  "severity": "high",
  "enforcement_reason": null,
  "processing_time_ms": 62,
  "timestamp": "2024-01-22T10:32:00Z",
  "original_content": null,
  "safe_rewrite": "Take a moment to cool down before sending this message",
  "block_reason": "Content contains aggressive language that could harm relationships",
  "retry_allowed": false,
  "suggested_alternatives": [
    "I'm feeling frustrated about this situation",
    "Can we discuss this when we're both calm?"
  ]
}
```

### **Inbound - Delivered**
```json
{
  "trace_id": "d1a6f7b4c8e9d5f3",
  "direction": "inbound",
  "decision": "deliver",
  "risk_categories": [],
  "severity": "low",
  "enforcement_reason": null,
  "processing_time_ms": 32,
  "timestamp": "2024-01-22T10:33:00Z",
  "safe_output": {
    "message_primary": "Hi honey, dinner is ready when you get home. Love you!",
    "urgency_level": "low",
    "source_hidden": "Family contact",
    "suggested_action": "No action required",
    "emotional_tone": "neutral"
  },
  "original_blocked": false,
  "escalation_triggered": false,
  "filtered_reason": null
}
```

### **Inbound - Crisis Escalated**
```json
{
  "trace_id": "e2b7g8c5d9f0e6g4",
  "direction": "inbound",
  "decision": "escalate",
  "risk_categories": ["self_harm_triggers"],
  "severity": "critical",
  "enforcement_reason": "crisis_content_detected",
  "processing_time_ms": 156,
  "timestamp": "2024-01-22T10:34:00Z",
  "safe_output": {
    "message_primary": "Crisis support has been contacted",
    "urgency_level": "high",
    "source_hidden": "Support team notified",
    "suggested_action": "Professional support activated",
    "emotional_tone": "supportive"
  },
  "original_blocked": true,
  "escalation_triggered": true,
  "filtered_reason": "Content contains self-harm indicators requiring immediate professional intervention"
}
```

### **Inbound - Summarized**
```json
{
  "trace_id": "f3c8h9d6e0g1f7h5",
  "direction": "inbound",
  "decision": "summarize",
  "risk_categories": ["financial_scam", "urgency_abuse"],
  "severity": "high",
  "enforcement_reason": null,
  "processing_time_ms": 89,
  "timestamp": "2024-01-22T10:35:00Z",
  "safe_output": {
    "message_primary": "Message contains concerning content - review when ready",
    "urgency_level": "low",
    "source_hidden": "Unknown contact",
    "suggested_action": "Review for safety concerns",
    "emotional_tone": "protective"
  },
  "original_blocked": true,
  "escalation_triggered": false,
  "filtered_reason": "Financial scam attempt with false urgency detected"
}
```

---

## ERROR RESPONSE SCHEMA

### **Validation Error**
```json
{
  "error": true,
  "error_code": "INVALID_INPUT|PROCESSING_ERROR|SYSTEM_UNAVAILABLE",
  "error_message": "string",
  "trace_id": "string",
  "timestamp": "ISO_8601_string",
  "retry_after_seconds": "number|null",
  "fallback_action": "allow|deny|delay"
}
```

### **Error Examples**

**Invalid Input:**
```json
{
  "error": true,
  "error_code": "INVALID_INPUT",
  "error_message": "Missing required field: direction",
  "trace_id": "error_g4d9i0e7f1h2i8j6",
  "timestamp": "2024-01-22T10:36:00Z",
  "retry_after_seconds": null,
  "fallback_action": "deny"
}
```

**System Error:**
```json
{
  "error": true,
  "error_code": "PROCESSING_ERROR",
  "error_message": "Risk analysis service temporarily unavailable",
  "trace_id": "error_h5e0j1f8g2i3j9k7",
  "timestamp": "2024-01-22T10:37:00Z",
  "retry_after_seconds": 30,
  "fallback_action": "delay"
}
```

---

## FIELD DEFINITIONS

### **Decision Types**
- **allow** - Content approved for sending/delivery
- **soft_rewrite** - Content modified to safer version
- **hard_deny** - Content completely blocked
- **deliver** - Inbound content shown to user normally
- **summarize** - Inbound content shown as safe summary
- **delay** - Inbound content held for later delivery
- **silence** - Inbound content hidden in filtered folder
- **escalate** - Crisis content forwarded to professional support

### **Risk Categories**
- **emotional_manipulation** - Guilt, blackmail, dependency creation
- **urgency_abuse** - False deadlines, pressure tactics
- **harassment** - Threats, personal attacks, stalking behavior
- **financial_scam** - Money requests, payment fraud attempts
- **self_harm_triggers** - Suicide ideation, self-injury content
- **spam_escalation** - High frequency, repetitive messaging
- **information_overload** - Excessive volume, cognitive burden
- **aggressive_language** - Hostile, threatening communication

### **Severity Levels**
- **low** - Minor concerns, monitoring recommended
- **medium** - Moderate risk, intervention suggested
- **high** - Significant risk, blocking/filtering required
- **critical** - Immediate danger, escalation mandatory

### **Enforcement Reasons**
- **quiet_hours_violation** - Message sent during sleep hours
- **repeated_contact_abuse** - Excessive messaging frequency
- **emotional_escalation** - Increasing aggression detected
- **crisis_content_detected** - Self-harm or suicide content
- **spam_pattern_detected** - Automated bulk messaging

---

**Schema Version**: 1.0-FROZEN  
**Compatibility**: All system components must implement this exact format  
**Breaking Changes**: Require major version increment and migration plan