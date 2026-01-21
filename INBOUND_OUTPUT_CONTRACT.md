# INBOUND OUTPUT CONTRACT
**Safe Delivery Interface for Downstream Layers**

## OVERVIEW
This contract defines the standardized output format for inbound content validation. It ensures downstream layers receive only safe, sanitized information without exposure to raw content or internal system details.

## OUTPUT BLOCK SPECIFICATION

### Single Output Format
All inbound validation results MUST be delivered in this exact format:

```json
{
  "message_primary": "string",
  "urgency_level": "low|medium|high|critical",
  "source_hidden": "boolean",
  "suggested_action": "deliver|summarize|delay|silence|escalate",
  "emotional_tone": "neutral|positive|negative|manipulative|threatening"
}
```

## FIELD DEFINITIONS

### message_primary
**Type**: String (max 200 characters)  
**Purpose**: Safe, sanitized version of the primary message content  
**Rules**:
- NO raw content from original message
- NO personally identifiable information
- NO app/platform branding or names
- NO specific threat details
- Generic, safe summary only

**Examples**:
- ✅ "Meeting reminder from colleague"
- ✅ "Marketing message about product offer"
- ✅ "Message contains inappropriate content"
- ❌ "John Smith says: Meet me at Starbucks on 5th Street"
- ❌ "WhatsApp message from +1234567890"

### urgency_level
**Type**: Enum  
**Values**: `low`, `medium`, `high`, `critical`  
**Purpose**: Indicates time-sensitivity without revealing manipulation tactics

**Mapping**:
- `low`: Normal content, no time pressure
- `medium`: Some urgency but not manipulative
- `high`: Legitimate urgent content
- `critical`: Emergency-level urgency (rare, verified)

### source_hidden
**Type**: Boolean  
**Purpose**: Indicates if source identity should be concealed from user  
**Rules**:
- `true`: Hide sender identity (harassment, threats, spam)
- `false`: Safe to show sender (normal content)

### suggested_action
**Type**: Enum  
**Values**: `deliver`, `summarize`, `delay`, `silence`, `escalate`  
**Purpose**: Recommended handling action for downstream systems

**Action Definitions**:
- `deliver`: Show content normally
- `summarize`: Show condensed version
- `delay`: Hold for specified time
- `silence`: Block without notification
- `escalate`: Block and alert security

### emotional_tone
**Type**: Enum  
**Values**: `neutral`, `positive`, `negative`, `manipulative`, `threatening`  
**Purpose**: Emotional context without revealing specific content

**Tone Definitions**:
- `neutral`: Factual, business-like content
- `positive`: Friendly, supportive content
- `negative`: Sad, disappointed, but not harmful
- `manipulative`: Guilt, pressure, emotional exploitation
- `threatening`: Intimidation, aggression, harm

## PRIVACY PROTECTION RULES

### NO Raw Content Leaks
- Original message text NEVER appears in output
- Specific details NEVER included in message_primary
- Personal information ALWAYS stripped
- Location data NEVER exposed

### NO App Branding Leaks
- Platform names removed ("WhatsApp" → "messaging app")
- Service names removed ("Gmail" → "email service")
- Brand names removed ("Starbucks" → "coffee shop")
- App-specific terminology removed

### NO Internal System Details
- Validation confidence scores hidden
- Pattern match details hidden
- Risk category specifics hidden
- Trace IDs not exposed to downstream

## CONTENT SANITIZATION EXAMPLES

### Original → Sanitized
```
"Hey, meet me at Starbucks on 5th Street at 3pm"
→ "Meeting invitation from contact"

"URGENT: Your Netflix account will be suspended in 1 hour!"
→ "Urgent account notification"

"You're such an idiot, nobody likes you"
→ "Message contains inappropriate content"

"I know where you live and I'm coming for you"
→ "Message flagged for security review"
```

## SAMPLE PAYLOADS

### Example 1: Safe Personal Message
```json
{
  "message_primary": "Friendly message from contact",
  "urgency_level": "low",
  "source_hidden": false,
  "suggested_action": "deliver",
  "emotional_tone": "positive"
}
```

### Example 2: Long Work Email
```json
{
  "message_primary": "Detailed project update from colleague",
  "urgency_level": "medium",
  "source_hidden": false,
  "suggested_action": "summarize",
  "emotional_tone": "neutral"
}
```

### Example 3: Scam Urgency
```json
{
  "message_primary": "Account security notification",
  "urgency_level": "high",
  "source_hidden": true,
  "suggested_action": "delay",
  "emotional_tone": "manipulative"
}
```

### Example 4: Harassment Message
```json
{
  "message_primary": "Message contains inappropriate content",
  "urgency_level": "low",
  "source_hidden": true,
  "suggested_action": "silence",
  "emotional_tone": "negative"
}
```

### Example 5: Direct Threat
```json
{
  "message_primary": "Message flagged for security review",
  "urgency_level": "critical",
  "source_hidden": true,
  "suggested_action": "escalate",
  "emotional_tone": "threatening"
}
```

### Example 6: Marketing Email
```json
{
  "message_primary": "Promotional offer from business",
  "urgency_level": "low",
  "source_hidden": false,
  "suggested_action": "deliver",
  "emotional_tone": "neutral"
}
```

### Example 7: False Emergency
```json
{
  "message_primary": "Emergency alert notification",
  "urgency_level": "critical",
  "source_hidden": true,
  "suggested_action": "escalate",
  "emotional_tone": "manipulative"
}
```

### Example 8: System Notification
```json
{
  "message_primary": "System maintenance notification",
  "urgency_level": "medium",
  "source_hidden": false,
  "suggested_action": "deliver",
  "emotional_tone": "neutral"
}
```

### Example 9: Emotional Manipulation
```json
{
  "message_primary": "Message with emotional pressure",
  "urgency_level": "low",
  "source_hidden": true,
  "suggested_action": "silence",
  "emotional_tone": "manipulative"
}
```

### Example 10: Information Overload
```json
{
  "message_primary": "Lengthy informational message",
  "urgency_level": "low",
  "source_hidden": false,
  "suggested_action": "summarize",
  "emotional_tone": "neutral"
}
```

## IMPLEMENTATION REQUIREMENTS

### Mandatory Fields
ALL five fields MUST be present in every output:
- `message_primary` (never null or empty)
- `urgency_level` (valid enum value)
- `source_hidden` (boolean)
- `suggested_action` (valid enum value)
- `emotional_tone` (valid enum value)

### Validation Rules
```python
def validate_output_contract(output):
    required_fields = [
        "message_primary", "urgency_level", 
        "source_hidden", "suggested_action", "emotional_tone"
    ]
    
    # Check all fields present
    for field in required_fields:
        if field not in output:
            raise ContractViolation(f"Missing field: {field}")
    
    # Validate field types and values
    if not isinstance(output["message_primary"], str):
        raise ContractViolation("message_primary must be string")
    
    if len(output["message_primary"]) > 200:
        raise ContractViolation("message_primary exceeds 200 chars")
    
    if output["urgency_level"] not in ["low", "medium", "high", "critical"]:
        raise ContractViolation("Invalid urgency_level")
    
    if not isinstance(output["source_hidden"], bool):
        raise ContractViolation("source_hidden must be boolean")
    
    if output["suggested_action"] not in ["deliver", "summarize", "delay", "silence", "escalate"]:
        raise ContractViolation("Invalid suggested_action")
    
    if output["emotional_tone"] not in ["neutral", "positive", "negative", "manipulative", "threatening"]:
        raise ContractViolation("Invalid emotional_tone")
```

### Error Handling
If validation fails, return safe fallback:
```json
{
  "message_primary": "Content under review",
  "urgency_level": "low",
  "source_hidden": true,
  "suggested_action": "silence",
  "emotional_tone": "neutral"
}
```

## SECURITY CONSIDERATIONS

### Data Minimization
- Only essential information in output
- No debugging information exposed
- No internal system state revealed
- No raw content preservation

### Privacy Protection
- Sender identity protected when appropriate
- Content details abstracted
- No tracking identifiers exposed
- No metadata leakage

### Fail-Safe Defaults
- Unknown content → `silence`
- Uncertain urgency → `low`
- Suspicious source → `source_hidden: true`
- Unclear tone → `neutral`

## COMPLIANCE REQUIREMENTS

### Downstream Layer Obligations
Systems receiving this output MUST:
- Respect `suggested_action` recommendations
- Honor `source_hidden` flags
- Not attempt to reverse-engineer original content
- Not store raw validation details

### Audit Requirements
- Log all output contract deliveries
- Track suggested_action compliance
- Monitor for contract violations
- Report security escalations

---

**Contract Version**: 1.0  
**Last Updated**: Day 2  
**Compliance**: Mandatory for all downstream systems  
**Owner**: Safety & Trust Team