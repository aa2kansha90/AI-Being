# INBOUND DECISION ENUM DOCUMENTATION

## Overview
The Inbound Decision Enum defines how inbound content should be handled after validation. Unlike outbound content that focuses on generation control, inbound decisions focus on delivery and user protection.

## Decision Types

### DELIVER
**Purpose**: Safe content that should be delivered normally to the user.
**Action**: Present content to user without modification.
**Use Cases**:
- Normal conversations
- Legitimate notifications
- Safe informational content
- Routine system messages

**Example**:
```python
InboundDecision.DELIVER
# Content: "Hello! Hope you're having a great day."
# Action: Show message normally
```

### SUMMARIZE
**Purpose**: Content that might overwhelm the user but isn't harmful.
**Action**: Provide condensed version to reduce cognitive load.
**Use Cases**:
- Very long messages (>500 characters)
- Information-dense content
- Multi-paragraph emails
- Complex technical notifications

**Example**:
```python
InboundDecision.SUMMARIZE
# Content: "This is a very long message with lots of details..."
# Action: Show "Message from John: Project update with timeline details... [View Full]"
```

### DELAY
**Purpose**: Suspicious timing or urgency manipulation detected.
**Action**: Hold content for specified duration before delivery.
**Use Cases**:
- False urgency ("Expires in 5 minutes!")
- Pressure tactics ("Act now!")
- Scarcity manipulation ("Only 2 left!")
- Suspected scam timing

**Example**:
```python
InboundDecision.DELAY
# Content: "URGENT: Limited time offer expires in 5 minutes!"
# Action: Delay delivery by 30 minutes, then show with warning
```

### SILENCE
**Purpose**: Harmful content that should be blocked without notifying sender.
**Action**: Block delivery, don't send read receipts or bounce messages.
**Use Cases**:
- Personal harassment
- Emotional manipulation
- Repeated unwanted contact
- Mild threats or insults

**Example**:
```python
InboundDecision.SILENCE
# Content: "You're such a stupid idiot, nobody likes you."
# Action: Block message, no notification to sender, log incident
```

### ESCALATE
**Purpose**: Critical threats requiring immediate human intervention.
**Action**: Block content and alert security/moderation team.
**Use Cases**:
- Direct threats of violence
- Panic-inducing phishing attempts
- Severe harassment
- Emergency manipulation

**Example**:
```python
InboundDecision.ESCALATE
# Content: "I know where you live and I'm coming for you."
# Action: Block message, alert security team, potentially contact authorities
```

## Decision Flow Logic

```
Inbound Content
    ↓
[1] Check for Critical Threats
    ↓ (if found)
    ESCALATE
    
[2] Check for Harassment/Manipulation
    ↓ (if found)
    SILENCE
    
[3] Check for Frequency-based Harassment
    ↓ (if found)
    SILENCE
    
[4] Check for Urgency Manipulation
    ↓ (if found)
    DELAY
    
[5] Check for Information Overload
    ↓ (if found)
    SUMMARIZE
    
[6] Default Safe Content
    ↓
    DELIVER
```

## Implementation Details

### Confidence Thresholds
- **ESCALATE**: >85% confidence required
- **SILENCE**: >70% confidence required
- **DELAY**: >70% confidence required
- **SUMMARIZE**: >60% confidence required
- **DELIVER**: Default for <60% confidence

### Timing Considerations
- **DELIVER**: Immediate delivery
- **SUMMARIZE**: Immediate delivery with summary
- **DELAY**: Configurable delay (5 minutes to 1 hour)
- **SILENCE**: No delivery, silent block
- **ESCALATE**: Immediate block + alert

### User Experience Impact

#### DELIVER
- ✅ Normal user experience
- ✅ No delays or modifications
- ✅ Full content visibility

#### SUMMARIZE
- ⚠️ Condensed view initially
- ✅ Option to view full content
- ✅ Reduced cognitive load

#### DELAY
- ⚠️ Delayed notification
- ⚠️ May include warning label
- ✅ Protection from urgency manipulation

#### SILENCE
- ❌ Content not delivered
- ✅ No harassment notification
- ✅ Sender unaware of block

#### ESCALATE
- ❌ Content blocked completely
- ⚠️ May notify user of threat
- ✅ Human review triggered

## Integration with Existing System

### Relationship to Outbound Decisions
- **Outbound**: `allow`, `soft_rewrite`, `hard_deny`
- **Inbound**: `deliver`, `summarize`, `delay`, `silence`, `escalate`
- **Direction Flag**: `direction="inbound"` distinguishes processing path

### Shared Components
- Risk categories (extended for inbound)
- Confidence scoring system
- Trace ID generation
- Pattern matching engine

### New Components
- Delay duration calculation
- Summary generation
- Frequency analysis
- Sender reputation tracking

## Error Handling

### Fallback Behavior
```python
# If validation fails
default_decision = InboundDecision.SILENCE  # Fail-safe approach
```

### Exception Cases
- **Unknown sender**: Apply stricter thresholds
- **System messages**: Bypass most filtering
- **Emergency contacts**: Prioritize delivery
- **Blocked senders**: Automatic SILENCE

## Monitoring and Metrics

### Key Metrics
- **Delivery Rate**: % of content delivered normally
- **Summary Rate**: % of content summarized
- **Delay Rate**: % of content delayed
- **Block Rate**: % of content silenced
- **Escalation Rate**: % of content escalated

### Alert Thresholds
- **High Escalation Rate**: >5% may indicate attack
- **High Delay Rate**: >20% may indicate false positives
- **Low Delivery Rate**: <70% may indicate over-filtering

## Testing and Validation

### Test Categories
1. **Safe Content**: Should result in DELIVER
2. **Long Content**: Should result in SUMMARIZE
3. **Urgent Scams**: Should result in DELAY
4. **Harassment**: Should result in SILENCE
5. **Threats**: Should result in ESCALATE

### Validation Criteria
- ✅ Correct decision for content type
- ✅ Appropriate confidence scores
- ✅ Proper delay durations
- ✅ Accurate summary generation
- ✅ Deterministic trace IDs

---

**Document Version**: 1.0  
**Last Updated**: Day 1 - Inbound Extension  
**Related Files**: `inbound_behavior_validator.py`  
**Owner**: Safety & Trust Team