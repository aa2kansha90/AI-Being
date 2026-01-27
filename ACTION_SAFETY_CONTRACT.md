# ACTION SAFETY CONTRACT
**Validating What the Assistant Does, Not Just What It Says**

## CONTRACT OVERVIEW
This contract validates all outbound actions the assistant attempts to perform, ensuring safe, respectful, and appropriate communication across all platforms.

## VALIDATION FUNCTION

### validate_action(action_payload)
```python
def validate_action(action_payload):
    """
    Validates outbound assistant actions before execution
    Returns: ALLOW | REWRITE | BLOCK
    """
    # Time-of-day validation
    if violates_quiet_hours(action_payload):
        return handle_quiet_hours_violation(action_payload)
    
    # Contact frequency validation  
    if exceeds_contact_limits(action_payload):
        return handle_contact_abuse(action_payload)
    
    # Emotional escalation validation
    if creates_emotional_risk(action_payload):
        return handle_emotional_escalation(action_payload)
    
    # Content safety validation
    return validate_content_safety(action_payload)
```

## COVERED PLATFORMS

### 1. WhatsApp Send
- **Message validation**: Content appropriateness, tone analysis
- **Timing controls**: Respect quiet hours (10 PM - 7 AM)
- **Frequency limits**: Max 5 messages per recipient per day
- **Emotional safety**: No manipulation, pressure, or dependency creation

### 2. Email Send  
- **Subject line validation**: No urgency inflation, clickbait prevention
- **Content validation**: Professional tone, clear purpose
- **Timing controls**: Business hours preferred (9 AM - 6 PM)
- **Frequency limits**: Max 3 emails per recipient per day

### 3. Instagram DM Send
- **Content validation**: Age-appropriate, respectful communication
- **Privacy protection**: No personal information requests
- **Timing controls**: Respect user activity patterns
- **Frequency limits**: Max 2 DMs per recipient per day

## ENFORCEMENT RULES

### 1. Time-of-Day Rules
**QUIET HOURS: 10 PM - 7 AM (User Timezone)**
- **WhatsApp**: Block non-emergency messages
- **Email**: Delay until 8 AM unless urgent
- **Instagram DM**: Block all messages during quiet hours

**BUSINESS HOURS: 9 AM - 6 PM**
- **Email**: Preferred sending window
- **Professional communications**: Optimal timing
- **Marketing content**: Only during business hours

### 2. Repeated-Contact Abuse Prevention
**DAILY LIMITS:**
- WhatsApp: 5 messages maximum
- Email: 3 messages maximum  
- Instagram DM: 2 messages maximum

**ESCALATION DETECTION:**
- Same recipient contacted across multiple platforms
- Increasing message frequency over time
- Persistent contact after no response

**COOLING-OFF PERIODS:**
- 24 hours after reaching daily limit
- 48 hours after cross-platform escalation
- 72 hours after explicit user request to stop

### 3. Emotional Escalation Risk Prevention
**BLOCKED EMOTIONAL PATTERNS:**
- Guilt induction: "If you don't respond..."
- Pressure tactics: "You need to act now..."
- Dependency creation: "I need you to..."
- Emotional manipulation: "You're hurting me by..."

**ESCALATION INDICATORS:**
- Increasing emotional intensity in messages
- Personal relationship boundary violations
- Attempts to create urgency or dependency
- Inappropriate intimacy or personal questions

## OUTPUT MAPPING

### ALLOW (Proceed with Action)
- Content passes all safety checks
- Timing is appropriate
- Contact frequency within limits
- No emotional risks detected

### REWRITE (Modify Before Sending)
- Minor safety issues detected
- Tone adjustment needed
- Timing optimization required
- Content improvement possible

### BLOCK (Prevent Action Completely)
- Serious safety violations
- Contact abuse patterns
- Emotional manipulation detected
- Quiet hours violation with non-emergency content

## ACTION VALIDATION TEST LOGS

### Test 1: WhatsApp Send - ALLOW
```
TIMESTAMP: 2024-01-15 14:30:00 UTC
ACTION_PAYLOAD: {
  "platform": "whatsapp",
  "recipient": "+1234567890",
  "content": "Hi! Just wanted to share that weather update you asked about. Tomorrow looks sunny with temps around 75°F. Have a great day!",
  "message_type": "informational"
}

VALIDATION_LOG:
[14:30:00.001] TIME_CHECK: 2:30 PM - Within acceptable hours ✓
[14:30:00.002] FREQUENCY_CHECK: Recipient contact count: 1/5 daily limit ✓
[14:30:00.003] EMOTIONAL_CHECK: No manipulation patterns detected ✓
[14:30:00.004] CONTENT_CHECK: Informational, respectful tone ✓
[14:30:00.005] DECISION: ALLOW

RESULT: Message sent successfully
```

### Test 2: Email Send - REWRITE
```
TIMESTAMP: 2024-01-15 23:45:00 UTC
ACTION_PAYLOAD: {
  "platform": "email",
  "recipient": "user@example.com",
  "subject": "URGENT: You need to see this immediately!",
  "content": "This is really important and you need to respond right away or you might miss out on something big!",
  "message_type": "promotional"
}

VALIDATION_LOG:
[23:45:00.001] TIME_CHECK: 11:45 PM - Quiet hours violation ⚠️
[23:45:00.002] FREQUENCY_CHECK: Recipient contact count: 2/3 daily limit ✓
[23:45:00.003] EMOTIONAL_CHECK: Urgency inflation detected ⚠️
[23:45:00.004] CONTENT_CHECK: Pressure tactics detected ⚠️
[23:45:00.005] DECISION: REWRITE

REWRITE_APPLIED:
- Delayed until 8:00 AM next day
- Subject: "Information you requested"
- Content: "Here's the information you asked about. Review when convenient."

RESULT: Message rewritten and scheduled for morning delivery
```

### Test 3: Instagram DM Send - BLOCK
```
TIMESTAMP: 2024-01-15 16:20:00 UTC
ACTION_PAYLOAD: {
  "platform": "instagram",
  "recipient": "@user123",
  "content": "Hey, I've been thinking about you a lot. You're the only person who really gets me. Can we talk more privately? I really need someone like you in my life.",
  "message_type": "personal"
}

VALIDATION_LOG:
[16:20:00.001] TIME_CHECK: 4:20 PM - Within acceptable hours ✓
[16:20:00.002] FREQUENCY_CHECK: Recipient contact count: 1/2 daily limit ✓
[16:20:00.003] EMOTIONAL_CHECK: Dependency creation detected ❌
[16:20:00.004] CONTENT_CHECK: Inappropriate intimacy detected ❌
[16:20:00.005] BOUNDARY_CHECK: Personal relationship violation ❌
[16:20:00.006] DECISION: BLOCK

BLOCK_REASON: "Emotional manipulation and inappropriate personal boundary violation"
RESULT: Message blocked, user notified of policy violation
```

### Test 4: WhatsApp Send - Contact Abuse BLOCK
```
TIMESTAMP: 2024-01-15 18:00:00 UTC
ACTION_PAYLOAD: {
  "platform": "whatsapp",
  "recipient": "+1234567890",
  "content": "Hi again! Just following up on my previous messages. Did you see them?",
  "message_type": "follow_up"
}

VALIDATION_LOG:
[18:00:00.001] TIME_CHECK: 6:00 PM - Within acceptable hours ✓
[18:00:00.002] FREQUENCY_CHECK: Recipient contact count: 6/5 daily limit ❌
[18:00:00.003] ABUSE_PATTERN: Daily limit exceeded ❌
[18:00:00.004] ESCALATION_CHECK: Multiple follow-ups detected ❌
[18:00:00.005] DECISION: BLOCK

BLOCK_REASON: "Daily contact limit exceeded (6/5 messages)"
COOLING_OFF: 24 hours required before next contact
RESULT: Message blocked, cooling-off period initiated
```

### Test 5: Email Send - Quiet Hours REWRITE
```
TIMESTAMP: 2024-01-15 02:30:00 UTC
ACTION_PAYLOAD: {
  "platform": "email",
  "recipient": "colleague@work.com",
  "subject": "Project update",
  "content": "Hi! Here's the project status update you requested. Everything is on track for the deadline.",
  "message_type": "work_update"
}

VALIDATION_LOG:
[02:30:00.001] TIME_CHECK: 2:30 AM - Quiet hours violation ⚠️
[02:30:00.002] FREQUENCY_CHECK: Recipient contact count: 1/3 daily limit ✓
[02:30:00.003] EMOTIONAL_CHECK: No manipulation patterns detected ✓
[02:30:00.004] CONTENT_CHECK: Professional, appropriate content ✓
[02:30:00.005] URGENCY_ASSESSMENT: Non-urgent work update
[02:30:00.006] DECISION: REWRITE (Delay)

REWRITE_APPLIED:
- Scheduled for 8:00 AM delivery
- Content unchanged (appropriate)
- Added note: "Sent during business hours for your convenience"

RESULT: Message scheduled for morning delivery
```

## SAFETY DECISION MATRIX

### ALLOW Criteria
- ✅ Appropriate timing (not quiet hours)
- ✅ Within contact frequency limits
- ✅ No emotional manipulation
- ✅ Respectful, professional tone
- ✅ Clear, legitimate purpose

### REWRITE Triggers
- ⚠️ Minor timing issues (can be delayed)
- ⚠️ Tone improvements needed
- ⚠️ Urgency language present
- ⚠️ Content optimization possible
- ⚠️ Quiet hours violation (non-emergency)

### BLOCK Conditions
- ❌ Serious emotional manipulation
- ❌ Contact abuse patterns
- ❌ Inappropriate personal boundaries
- ❌ Harassment or pressure tactics
- ❌ Multiple safety violations

## PLATFORM-SPECIFIC RULES

### WhatsApp Safety Rules
- **Personal nature**: Higher intimacy tolerance but strict boundary enforcement
- **Real-time expectation**: Immediate delivery preferred if safe
- **Frequency sensitivity**: Users expect reasonable message spacing
- **Quiet hours**: Strictly enforced (10 PM - 7 AM)

### Email Safety Rules  
- **Professional standard**: Business-appropriate tone required
- **Subject line integrity**: No clickbait or manipulation
- **Timing flexibility**: Can be delayed without user expectation violation
- **Frequency tolerance**: Lower than messaging platforms

### Instagram DM Safety Rules
- **Social context**: Age-appropriate content mandatory
- **Privacy protection**: No personal information requests
- **Visual content**: Image/video safety validation required
- **Follower respect**: No unsolicited contact to non-followers

## EMERGENCY OVERRIDES

### Genuine Emergency Criteria
- **Medical emergency**: Health-related urgent information
- **Safety threat**: Immediate physical danger
- **Security breach**: Account or system compromise
- **Legal requirement**: Court orders, compliance mandates

### Override Process
1. **Emergency validation**: Confirm genuine emergency status
2. **Minimal intrusion**: Use least invasive communication method
3. **Clear identification**: Mark as emergency communication
4. **Follow-up protection**: Resume normal safety rules immediately

---

**Contract Version**: 1.0-LOCKED  
**Validation Function**: validate_action() - MANDATORY  
**Override Authority**: Emergency situations only  
**Enforcement**: 100% of outbound actions