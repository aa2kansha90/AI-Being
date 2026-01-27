# INBOUND SAFETY FLOW
**Nothing Unsafe Reaches the User**

## FLOW OVERVIEW
This safety flow validates all inbound content before user delivery, classifying risk levels and applying appropriate mediation to ensure user safety and emotional well-being.

## VALIDATION FUNCTION

### validate_inbound(message_payload)
```python
def validate_inbound(message_payload):
    """
    Validates inbound messages before user delivery
    Returns: Safe | Sensitive | Escalating | Suppress
    """
    # Content risk assessment
    risk_level = assess_content_risk(message_payload)
    
    # User preference mediation
    user_settings = get_user_preferences(message_payload.recipient)
    
    # Quiet hours enforcement
    if violates_quiet_hours(message_payload, user_settings):
        return handle_quiet_hours(message_payload)
    
    # Emotional load control
    emotional_load = assess_emotional_impact(message_payload)
    
    # Apply classification and mediation
    return classify_and_mediate(risk_level, emotional_load, user_settings)
```

## CLASSIFICATION SYSTEM

### SAFE
- **Definition**: Content poses no emotional or safety risks
- **Characteristics**: Informational, neutral tone, appropriate timing
- **Action**: Deliver immediately without modification
- **Examples**: Weather updates, calendar reminders, factual information

### SENSITIVE  
- **Definition**: Content requires careful handling but isn't harmful
- **Characteristics**: Personal topics, emotional content, important decisions
- **Action**: Apply user preference filters, timing controls
- **Examples**: Medical results, relationship discussions, financial information

### ESCALATING
- **Definition**: Content shows concerning patterns or emotional manipulation
- **Characteristics**: Increasing pressure, emotional dependency, manipulation tactics
- **Action**: Generate safe summary, provide resources if needed
- **Examples**: Guilt-inducing messages, pressure tactics, dependency creation

### SUPPRESS
- **Definition**: Content is harmful and should not reach user
- **Characteristics**: Harassment, threats, severe manipulation, spam
- **Action**: Block completely, log for pattern analysis
- **Examples**: Threats, explicit manipulation, harassment campaigns

## MEDIATION CONTROLS

### 1. User Preference Mediation
**PREFERENCE CATEGORIES:**
- **Emotional Sensitivity**: High/Medium/Low filtering
- **Contact Frequency**: Strict/Moderate/Relaxed limits
- **Content Types**: Block/Filter/Allow specific categories
- **Timing Preferences**: Custom quiet hours, priority contacts

**MEDIATION ACTIONS:**
- Filter content based on sensitivity settings
- Apply custom contact frequency limits
- Respect content type preferences
- Honor timing and priority settings

### 2. Quiet Hours Enforcement
**DEFAULT QUIET HOURS: 10 PM - 7 AM**
- **Safe content**: Delayed until morning
- **Sensitive content**: Delayed with priority queuing
- **Escalating content**: Immediate safe summary only
- **Suppress content**: Blocked regardless of timing

**EMERGENCY EXCEPTIONS:**
- Medical emergencies: Immediate delivery
- Safety threats: Immediate alert with resources
- Family emergencies: Based on user emergency contacts
- System security: Immediate notification

### 3. Emotional Load Control
**LOAD ASSESSMENT:**
- **Daily emotional quota**: Track cumulative emotional impact
- **Stress indicators**: Monitor user emotional state
- **Recovery periods**: Enforce emotional rest periods
- **Support resources**: Provide help when needed

**LOAD MANAGEMENT:**
- Batch emotional content for manageable delivery
- Space out sensitive messages
- Provide emotional support resources
- Respect user emotional capacity

## INBOUND DEMO LOGS

### Demo 1: SAFE Classification
```
TIMESTAMP: 2024-01-15 14:30:00 UTC
MESSAGE_PAYLOAD: {
  "sender": "weather_service",
  "content": "Tomorrow's forecast: Sunny, 75°F high, 60°F low. Perfect day for outdoor activities!",
  "platform": "notification",
  "message_type": "informational"
}

VALIDATION_LOG:
[14:30:00.001] RISK_ASSESSMENT: Content analysis initiated
[14:30:00.002] EMOTIONAL_SCAN: No emotional triggers detected ✓
[14:30:00.003] MANIPULATION_SCAN: No manipulation patterns ✓
[14:30:00.004] TIMING_CHECK: 2:30 PM - Normal hours ✓
[14:30:00.005] USER_PREFERENCES: Weather notifications enabled ✓
[14:30:00.006] EMOTIONAL_LOAD: Current load: 2/10 (low) ✓
[14:30:00.007] CLASSIFICATION: SAFE

RESULT: Delivered immediately without modification
USER_SEES: "Tomorrow's forecast: Sunny, 75°F high, 60°F low. Perfect day for outdoor activities!"
```

### Demo 2: SENSITIVE Classification
```
TIMESTAMP: 2024-01-15 16:45:00 UTC
MESSAGE_PAYLOAD: {
  "sender": "healthcare_provider",
  "content": "Your test results are available. Please call our office to discuss the findings with your doctor at your earliest convenience.",
  "platform": "email",
  "message_type": "medical"
}

VALIDATION_LOG:
[16:45:00.001] RISK_ASSESSMENT: Medical content detected
[16:45:00.002] SENSITIVITY_SCAN: Health-related information ⚠️
[16:45:00.003] EMOTIONAL_IMPACT: Potential anxiety trigger ⚠️
[16:45:00.004] TIMING_CHECK: 4:45 PM - Appropriate hours ✓
[16:45:00.005] USER_PREFERENCES: Medical notifications priority enabled ✓
[16:45:00.006] EMOTIONAL_LOAD: Current load: 6/10 (moderate) ⚠️
[16:45:00.007] CLASSIFICATION: SENSITIVE

MEDIATION_APPLIED:
- Added calming context: "Routine follow-up communication"
- Provided support resources: "Healthcare support available if needed"
- Timing: Delivered during user's preferred medical communication hours

RESULT: Delivered with supportive context
USER_SEES: "Healthcare Update: Test results available for review. Routine follow-up communication from your healthcare provider. Healthcare support resources available if needed."
```

### Demo 3: ESCALATING Classification
```
TIMESTAMP: 2024-01-15 21:30:00 UTC
MESSAGE_PAYLOAD: {
  "sender": "unknown_contact",
  "content": "I've been thinking about you all day. You're the only person who understands me. I don't know what I'd do without you. Please don't ignore me like everyone else does. I really need to talk to you tonight.",
  "platform": "social_media",
  "message_type": "personal"
}

VALIDATION_LOG:
[21:30:00.001] RISK_ASSESSMENT: Emotional manipulation detected
[21:30:00.002] DEPENDENCY_SCAN: "only person", "don't know what I'd do" ❌
[21:30:00.003] GUILT_SCAN: "don't ignore me like everyone else" ❌
[21:30:00.004] URGENCY_SCAN: "need to talk tonight" ⚠️
[21:30:00.005] TIMING_CHECK: 9:30 PM - Near quiet hours ⚠️
[21:30:00.006] EMOTIONAL_LOAD: Current load: 7/10 (high) ❌
[21:30:00.007] CLASSIFICATION: ESCALATING

MEDIATION_APPLIED:
- Generated safe summary removing manipulation
- Provided mental health resources
- Delayed delivery until morning
- Flagged sender for pattern monitoring

RESULT: Safe summary delivered next morning with resources
USER_SEES: "Personal Message Summary: Someone reached out expressing need for communication support. Mental health resources available: Crisis Text Line (741741), National Suicide Prevention Lifeline (988)."
```

### Demo 4: SUPPRESS Classification
```
TIMESTAMP: 2024-01-15 19:15:00 UTC
MESSAGE_PAYLOAD: {
  "sender": "aggressive_contact",
  "content": "You can't keep ignoring me! I know where you work and I'm going to show up there if you don't respond. You think you're better than me but you're not. I'll make sure everyone knows what kind of person you really are.",
  "platform": "messaging",
  "message_type": "threatening"
}

VALIDATION_LOG:
[19:15:00.001] RISK_ASSESSMENT: Threat analysis initiated
[19:15:00.002] THREAT_SCAN: "I know where you work", "show up there" ❌
[19:15:00.003] HARASSMENT_SCAN: Intimidation patterns detected ❌
[19:15:00.004] ESCALATION_SCAN: Threatening behavior ❌
[19:15:00.005] SAFETY_ASSESSMENT: Physical safety concern ❌
[19:15:00.006] CLASSIFICATION: SUPPRESS

SUPPRESSION_ACTIONS:
- Message completely blocked from user
- Sender flagged for harassment
- Safety resources prepared
- Incident logged for potential law enforcement
- User notified of blocked threatening content (optional)

RESULT: Message suppressed, safety measures activated
USER_SEES: [Optional notification] "A message containing threats was blocked for your safety. Support resources are available if needed."
```

### Demo 5: Quiet Hours Override
```
TIMESTAMP: 2024-01-15 23:45:00 UTC
MESSAGE_PAYLOAD: {
  "sender": "emergency_contact",
  "content": "Emergency: Dad had a heart attack and is being rushed to City Hospital. Please call me as soon as you get this.",
  "platform": "sms",
  "message_type": "emergency"
}

VALIDATION_LOG:
[23:45:00.001] RISK_ASSESSMENT: Emergency content detected
[23:45:00.002] EMERGENCY_SCAN: "heart attack", "rushed to hospital" ⚠️
[23:45:00.003] SENDER_VERIFICATION: Emergency contact verified ✓
[23:45:00.004] TIMING_CHECK: 11:45 PM - Quiet hours ⚠️
[23:45:00.005] EMERGENCY_OVERRIDE: Medical emergency confirmed ✓
[23:45:00.006] CLASSIFICATION: SAFE (Emergency Override)

EMERGENCY_HANDLING:
- Immediate delivery despite quiet hours
- Added emergency context and resources
- Activated emergency support protocols
- Provided crisis support information

RESULT: Immediate delivery with emergency support
USER_SEES: "🚨 Emergency Alert: Dad had a heart attack and is being rushed to City Hospital. Please call [contact] as soon as you get this. Emergency support resources: 911, Hospital Info Line: [number]"
```

## SAFE SUMMARY GENERATION

### Summary Principles
- **Preserve essential information** while removing harmful elements
- **Neutral tone** without emotional manipulation
- **Clear context** about why mediation occurred
- **Resource provision** when appropriate
- **User control** over viewing original content

### Summary Templates

**EMOTIONAL MANIPULATION → NEUTRAL REQUEST**
- Original: "If you don't respond, I'll know you don't care about me"
- Summary: "Message requesting communication response"

**URGENCY INFLATION → APPROPRIATE TIMING**
- Original: "URGENT! Act now or lose everything!"
- Summary: "Time-sensitive information available for review"

**DEPENDENCY CREATION → INDEPENDENT CHOICE**
- Original: "You're the only one who can help me"
- Summary: "Request for assistance received"

**THREAT/HARASSMENT → SAFETY NOTICE**
- Original: "I'm going to make your life miserable"
- Summary: "Concerning message blocked for your safety"

## USER PREFERENCE CONTROLS

### Sensitivity Settings
- **High**: Maximum filtering, extensive safe summaries
- **Medium**: Balanced approach, moderate filtering
- **Low**: Minimal filtering, user handles most content

### Contact Management
- **Trusted Contacts**: Reduced filtering, priority delivery
- **Unknown Contacts**: Enhanced filtering, delayed delivery
- **Blocked Contacts**: Complete suppression

### Content Categories
- **Personal Messages**: Custom sensitivity settings
- **Marketing**: Block/Filter/Allow with frequency limits
- **News/Information**: Emotional content filtering
- **Emergency**: Always allow with verification

### Timing Preferences
- **Custom Quiet Hours**: User-defined rest periods
- **Priority Contacts**: Emergency override permissions
- **Batch Delivery**: Group non-urgent messages
- **Immediate Delivery**: Real-time for trusted sources

## EMOTIONAL LOAD MONITORING

### Load Calculation
```
Daily Emotional Load = Σ(message_emotional_weight × user_sensitivity_factor)

Thresholds:
- 0-3: Low load (normal processing)
- 4-6: Moderate load (careful timing)
- 7-8: High load (batch delivery, extra support)
- 9-10: Critical load (emergency mode, minimal delivery)
```

### Load Management Actions
- **Low Load**: Normal message processing
- **Moderate Load**: Space out emotional content
- **High Load**: Batch emotional messages, provide support
- **Critical Load**: Emergency mode, essential messages only

---

**Flow Version**: 1.0-LOCKED  
**Validation Function**: validate_inbound() - MANDATORY  
**Classification**: Safe|Sensitive|Escalating|Suppress  
**User Protection**: 100% of inbound content validated