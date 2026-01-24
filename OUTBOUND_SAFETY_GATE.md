# OUTBOUND SAFETY GATE
**Controlling What Leaves the Assistant System**

## GATE OVERVIEW
This safety gate validates all outbound content from Sankalp before delivery, ensuring non-manipulative, respectful communication that maintains user trust and dignity.

## VALIDATION PIPELINE

### 1. RECEIVE DRAFTS
Accept outbound drafts from Sankalp in three categories:
- **messages** - Direct communications to users
- **notifications** - System alerts and updates  
- **replies** - Responses to user queries

### 2. SAFETY VALIDATION
Enforce three critical standards:
- **non-manipulative language** - No emotional exploitation
- **no urgency inflation** - Appropriate time pressure only
- **no system phrasing** - Human-like, natural communication

### 3. PRODUCE SAFE PAYLOADS
Generate final outbound-safe content ready for delivery

## LOCKED INTERFACE SCHEMA

### INPUT FROM SANKALP
```json
{
  "draft_payload": {
    "content_type": "enum[message|notification|reply]",
    "draft_text": "string",
    "intended_recipient": "string",
    "urgency_level": "enum[low|medium|high|critical]",
    "context": "string",
    "timestamp": "ISO8601",
    "draft_id": "string"
  }
}
```

### OUTPUT TO RAJ ENFORCEMENT
```json
{
  "approved_payload": {
    "content_type": "enum[message|notification|reply]",
    "approved_text": "string",
    "safety_status": "enum[approved|modified|rejected]",
    "urgency_level": "enum[low|medium|high|critical]",
    "delivery_timing": "enum[immediate|delayed|scheduled]",
    "safety_flags": "array[string]",
    "approval_timestamp": "ISO8601",
    "approval_id": "string"
  }
}
```

## SAFETY ENFORCEMENT RULES

### 1. NON-MANIPULATIVE LANGUAGE
**BLOCKED PATTERNS:**
- Guilt induction: "If you don't...", "You're letting me down"
- Emotional blackmail: "I'll be hurt if...", "You don't care about..."
- Dependency creation: "Only you can...", "I need you to..."
- Fear tactics: "You'll lose...", "Something bad will happen"

**REQUIRED TRANSFORMATIONS:**
- Convert guilt → neutral request
- Replace fear → factual information
- Remove dependency → user choice
- Eliminate pressure → respectful suggestion

### 2. NO URGENCY INFLATION
**BLOCKED ESCALATIONS:**
- False deadlines on non-urgent matters
- Artificial scarcity ("Only 2 left!")
- Panic language ("URGENT!", "EMERGENCY!")
- Time pressure without justification

**APPROPRIATE URGENCY:**
- Genuine security issues → high
- System maintenance → medium  
- General information → low
- Marketing content → low (never high)

### 3. NO SYSTEM PHRASING
**BLOCKED LANGUAGE:**
- "As an AI assistant..."
- "I am programmed to..."
- "System notification:"
- "Error code 404..."
- "Please contact administrator..."

**REQUIRED STYLE:**
- Natural, conversational tone
- Human-like communication
- Personal but professional
- Clear, direct language

## VALIDATION PROOFS

### Proof 1: Message Safety Validation
**SANKALP DRAFT:**
```json
{
  "draft_payload": {
    "content_type": "message",
    "draft_text": "You MUST respond immediately or you'll miss this incredible opportunity! Don't let me down - I'm counting on you!",
    "intended_recipient": "user_123",
    "urgency_level": "high",
    "context": "promotional_message",
    "timestamp": "2024-01-15T14:30:00Z",
    "draft_id": "draft_001"
  }
}
```

**RAJ ENFORCEMENT OUTPUT:**
```json
{
  "approved_payload": {
    "content_type": "message",
    "approved_text": "There's an opportunity available that might interest you. Feel free to review when convenient.",
    "safety_status": "modified",
    "urgency_level": "low",
    "delivery_timing": "immediate",
    "safety_flags": ["urgency_inflation", "manipulative_language", "pressure_tactics"],
    "approval_timestamp": "2024-01-15T14:30:01Z",
    "approval_id": "appr_001_20240115_143001"
  }
}
```

### Proof 2: Notification Safety Validation
**SANKALP DRAFT:**
```json
{
  "draft_payload": {
    "content_type": "notification",
    "draft_text": "SYSTEM ALERT: As an AI assistant, I am programmed to inform you that your account requires immediate attention or data loss may occur!",
    "intended_recipient": "user_456",
    "urgency_level": "critical",
    "context": "account_maintenance",
    "timestamp": "2024-01-15T16:45:00Z",
    "draft_id": "draft_002"
  }
}
```

**RAJ ENFORCEMENT OUTPUT:**
```json
{
  "approved_payload": {
    "content_type": "notification",
    "approved_text": "Your account has a maintenance update available. Please review at your convenience to ensure continued service.",
    "safety_status": "modified",
    "urgency_level": "medium",
    "delivery_timing": "immediate",
    "safety_flags": ["system_phrasing", "urgency_inflation", "fear_tactics"],
    "approval_timestamp": "2024-01-15T16:45:01Z",
    "approval_id": "appr_002_20240115_164501"
  }
}
```

### Proof 3: Reply Safety Validation
**SANKALP DRAFT:**
```json
{
  "draft_payload": {
    "content_type": "reply",
    "draft_text": "I understand you're frustrated, but you need to calm down and follow my instructions exactly or things will get worse for you.",
    "intended_recipient": "user_789",
    "urgency_level": "medium",
    "context": "support_response",
    "timestamp": "2024-01-15T18:20:00Z",
    "draft_id": "draft_003"
  }
}
```

**RAJ ENFORCEMENT OUTPUT:**
```json
{
  "approved_payload": {
    "content_type": "reply",
    "approved_text": "I understand this situation is frustrating. Here are some steps that might help resolve the issue. Let me know if you'd like to try a different approach.",
    "safety_status": "modified",
    "urgency_level": "low",
    "delivery_timing": "immediate",
    "safety_flags": ["condescending_tone", "threat_implication", "controlling_language"],
    "approval_timestamp": "2024-01-15T18:20:01Z",
    "approval_id": "appr_003_20240115_182001"
  }
}
```

### Proof 4: Clean Content Approval
**SANKALP DRAFT:**
```json
{
  "draft_payload": {
    "content_type": "message",
    "draft_text": "Thanks for your question about the weather forecast. Tomorrow looks sunny with temperatures around 75°F. Have a great day!",
    "intended_recipient": "user_101",
    "urgency_level": "low",
    "context": "information_response",
    "timestamp": "2024-01-15T12:15:00Z",
    "draft_id": "draft_004"
  }
}
```

**RAJ ENFORCEMENT OUTPUT:**
```json
{
  "approved_payload": {
    "content_type": "message",
    "approved_text": "Thanks for your question about the weather forecast. Tomorrow looks sunny with temperatures around 75°F. Have a great day!",
    "safety_status": "approved",
    "urgency_level": "low",
    "delivery_timing": "immediate",
    "safety_flags": [],
    "approval_timestamp": "2024-01-15T12:15:01Z",
    "approval_id": "appr_004_20240115_121501"
  }
}
```

### Proof 5: Rejected Content
**SANKALP DRAFT:**
```json
{
  "draft_payload": {
    "content_type": "message",
    "draft_text": "If you don't buy this now, you'll regret it forever! Everyone who ignores this offer ends up miserable. Don't be like them - you're better than that, right?",
    "intended_recipient": "user_202",
    "urgency_level": "critical",
    "context": "sales_message",
    "timestamp": "2024-01-15T20:30:00Z",
    "draft_id": "draft_005"
  }
}
```

**RAJ ENFORCEMENT OUTPUT:**
```json
{
  "approved_payload": {
    "content_type": "message",
    "approved_text": "",
    "safety_status": "rejected",
    "urgency_level": "low",
    "delivery_timing": "blocked",
    "safety_flags": ["severe_manipulation", "fear_tactics", "guilt_induction", "false_urgency"],
    "approval_timestamp": "2024-01-15T20:30:01Z",
    "approval_id": "appr_005_20240115_203001"
  }
}
```

## SAFETY FLAG TAXONOMY

### Manipulation Flags
- **guilt_induction**: Attempts to create guilt or shame
- **emotional_blackmail**: Conditional emotional threats
- **dependency_creation**: "Only you can help" messaging
- **fear_tactics**: Threats of negative consequences

### Urgency Flags  
- **urgency_inflation**: Artificial time pressure
- **false_deadlines**: Fake expiration times
- **panic_language**: "URGENT!", "EMERGENCY!" without cause
- **scarcity_manipulation**: "Limited time", "Only X left"

### System Flags
- **system_phrasing**: "As an AI", "I am programmed"
- **technical_jargon**: Error codes, admin language
- **robotic_tone**: Unnatural, mechanical language
- **corporate_speak**: Formal, impersonal communication

### Tone Flags
- **condescending_tone**: Talking down to user
- **controlling_language**: Demanding compliance
- **threat_implication**: Subtle threats or warnings
- **pressure_tactics**: Pushing for immediate action

## APPROVAL DECISION MATRIX

### APPROVED (No Changes)
- Natural, respectful language
- Appropriate urgency level
- No manipulation detected
- Human-like communication style

### MODIFIED (Safety Corrections)
- Manipulative language → neutral phrasing
- Inflated urgency → appropriate level
- System phrasing → natural language
- Pressure tactics → respectful suggestions

### REJECTED (Blocked Delivery)
- Severe manipulation attempts
- Multiple safety violations
- Harmful or threatening content
- Irreparable safety issues

## DELIVERY TIMING CONTROLS

### IMMEDIATE
- Clean, approved content
- Genuine urgent matters
- User-requested information
- Time-sensitive but appropriate

### DELAYED  
- Modified content needing review
- Non-urgent notifications
- Batch-appropriate messages
- Quiet hours consideration

### SCHEDULED
- Marketing content (business hours only)
- Routine updates (morning delivery)
- Non-critical notifications
- User preference alignment

### BLOCKED
- Rejected content
- Safety violations
- Manipulation attempts
- Harmful messaging

## RAJ ENFORCEMENT INTERFACE

### Authentication
- Secure API endpoint
- Sankalp authorization required
- Rate limiting: 1000 requests/hour
- Audit logging enabled

### Response Guarantees
- Maximum 100ms processing time
- Always returns valid JSON
- Never fails silently
- Comprehensive safety flags

### Monitoring
- All transactions logged
- Safety flag analytics
- Rejection rate tracking
- Performance metrics

---

**Gate Version**: 1.0-LOCKED  
**Interface**: RAJ-ENFORCEMENT-READY  
**Authority**: FINAL APPROVAL GATE  
**Override**: NONE (Safety paramount)