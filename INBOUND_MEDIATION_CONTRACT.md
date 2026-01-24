# INBOUND MEDIATION CONTRACT
**Defining What Enters the Assistant System**

## CONTRACT OVERVIEW
This contract defines the exact interface for inbound content entering the AI assistant system. All external content must pass through this mediation layer which strips identifying metadata, classifies risks, and produces safe summaries.

## PROCESSING PIPELINE

### 1. ACCEPT
Accept simulated inbound payloads from any source:
- **message** - Direct communications (DMs, chats, emails)
- **alert** - System notifications and warnings  
- **update** - Status changes and information updates
- **notification** - Push notifications and reminders

### 2. STRIP
Remove all identifying and manipulative elements:
- **platform_identifiers** - Remove source platform, app names, branding
- **sender_metadata** - Strip sender names, profiles, contact info
- **emotional_bait** - Remove urgency language, manipulation tactics, pressure

### 3. CLASSIFY
Categorize content across four dimensions:
- **inbound_type** - Content category classification
- **urgency_level** - Time sensitivity assessment  
- **emotional_risk** - Manipulation/harm potential
- **safe_summary** - Cleaned content description

## DETERMINISTIC SCHEMA

### INPUT SCHEMA
```json
{
  "raw_payload": {
    "content": "string",
    "source_platform": "string", 
    "sender_info": "object",
    "timestamp": "ISO8601",
    "metadata": "object"
  }
}
```

### OUTPUT SCHEMA (LOCKED)
```json
{
  "mediated_content": {
    "inbound_type": "enum[message|alert|update|notification]",
    "urgency_level": "enum[low|medium|high|critical]", 
    "emotional_risk": "enum[safe|caution|warning|danger]",
    "safe_summary": "string",
    "content_length": "integer",
    "risk_indicators": "array[string]",
    "processing_timestamp": "ISO8601",
    "mediation_id": "string"
  }
}
```

## CLASSIFICATION RULES

### Inbound Type Classification
- **message**: Personal communications, conversations, replies
- **alert**: Security warnings, system issues, urgent notifications  
- **update**: Status changes, progress reports, informational content
- **notification**: Reminders, scheduled alerts, routine notifications

### Urgency Level Assessment
- **low**: Informational, no time pressure, can wait days
- **medium**: Important but not urgent, can wait hours
- **high**: Time-sensitive, needs attention within hour
- **critical**: Immediate action required, safety implications

### Emotional Risk Evaluation  
- **safe**: No manipulation, neutral tone, informational
- **caution**: Minor pressure tactics, mild emotional language
- **warning**: Clear manipulation attempts, emotional exploitation
- **danger**: Severe manipulation, threats, self-harm triggers

### Safe Summary Generation
- Strip all identifying information
- Remove emotional manipulation language
- Preserve core informational content
- Limit to 200 characters maximum
- Use neutral, factual tone

## STRIPPING RULES

### Platform Identifiers (REMOVE)
- App names, platform branding
- UI elements, button text
- Service-specific terminology
- Company names, logos

### Sender Metadata (REMOVE)  
- Names, usernames, handles
- Profile pictures, avatars
- Contact information
- Relationship indicators

### Emotional Bait (REMOVE)
- Urgency language ("URGENT!", "ACT NOW!")
- Guilt tactics ("If you cared...", "Don't ignore...")
- Fear appeals ("You'll lose...", "Last chance...")
- Pressure phrases ("Limited time", "Expires soon")

## PROCESSING EXAMPLES

### Example 1: Marketing Message
**INPUT:**
```json
{
  "raw_payload": {
    "content": "URGENT! Sarah, your Amazon Prime membership expires in 2 hours! Click now to renew and save 50% - this deal won't last!",
    "source_platform": "email",
    "sender_info": {"name": "Amazon Deals", "email": "deals@amazon.com"},
    "timestamp": "2024-01-15T14:30:00Z"
  }
}
```

**OUTPUT:**
```json
{
  "mediated_content": {
    "inbound_type": "notification",
    "urgency_level": "medium", 
    "emotional_risk": "warning",
    "safe_summary": "Membership renewal notification with discount offer",
    "content_length": 127,
    "risk_indicators": ["urgency_language", "time_pressure", "discount_manipulation"],
    "processing_timestamp": "2024-01-15T14:30:01Z",
    "mediation_id": "med_001_20240115_143001"
  }
}
```

### Example 2: Personal Message
**INPUT:**
```json
{
  "raw_payload": {
    "content": "Hey! Just wanted to check in and see how you're doing. Hope your presentation went well today!",
    "source_platform": "whatsapp",
    "sender_info": {"name": "Alex Johnson", "phone": "+1234567890"},
    "timestamp": "2024-01-15T18:45:00Z"
  }
}
```

**OUTPUT:**
```json
{
  "mediated_content": {
    "inbound_type": "message",
    "urgency_level": "low",
    "emotional_risk": "safe", 
    "safe_summary": "Friendly check-in message asking about recent presentation",
    "content_length": 89,
    "risk_indicators": [],
    "processing_timestamp": "2024-01-15T18:45:01Z",
    "mediation_id": "med_002_20240115_184501"
  }
}
```

### Example 3: Security Alert
**INPUT:**
```json
{
  "raw_payload": {
    "content": "SECURITY ALERT: Unusual login detected from new device in Russia. If this wasn't you, secure your account immediately!",
    "source_platform": "google_security",
    "sender_info": {"service": "Google Security", "type": "automated"},
    "timestamp": "2024-01-15T22:15:00Z"
  }
}
```

**OUTPUT:**
```json
{
  "mediated_content": {
    "inbound_type": "alert",
    "urgency_level": "high",
    "emotional_risk": "caution",
    "safe_summary": "Security notification about unusual account access from new location",
    "content_length": 118,
    "risk_indicators": ["security_urgency"],
    "processing_timestamp": "2024-01-15T22:15:01Z", 
    "mediation_id": "med_003_20240115_221501"
  }
}
```

### Example 4: System Update
**INPUT:**
```json
{
  "raw_payload": {
    "content": "Your backup completed successfully. 1.2GB backed up to cloud storage. Next backup scheduled for tomorrow at 2 AM.",
    "source_platform": "backup_service",
    "sender_info": {"service": "CloudBackup Pro", "type": "system"},
    "timestamp": "2024-01-15T02:05:00Z"
  }
}
```

**OUTPUT:**
```json
{
  "mediated_content": {
    "inbound_type": "update",
    "urgency_level": "low",
    "emotional_risk": "safe",
    "safe_summary": "Backup completion notification with size and schedule information",
    "content_length": 108,
    "risk_indicators": [],
    "processing_timestamp": "2024-01-15T02:05:01Z",
    "mediation_id": "med_004_20240115_020501"
  }
}
```

### Example 5: Emotional Manipulation
**INPUT:**
```json
{
  "raw_payload": {
    "content": "I can't believe you're ignoring me again. I thought we were friends. This is really hurting me and I don't know what to do anymore.",
    "source_platform": "instagram_dm", 
    "sender_info": {"username": "lonely_soul_99", "followers": 23},
    "timestamp": "2024-01-15T20:30:00Z"
  }
}
```

**OUTPUT:**
```json
{
  "mediated_content": {
    "inbound_type": "message",
    "urgency_level": "medium",
    "emotional_risk": "warning",
    "safe_summary": "Message expressing disappointment about communication frequency",
    "content_length": 125,
    "risk_indicators": ["guilt_induction", "emotional_manipulation", "dependency_language"],
    "processing_timestamp": "2024-01-15T20:30:01Z",
    "mediation_id": "med_005_20240115_203001"
  }
}
```

## DEFAULT BEHAVIORS

### Unknown Content Type
- **inbound_type**: "message" (safe default)
- **urgency_level**: "low" (conservative default)
- **emotional_risk**: "caution" (protective default)
- **safe_summary**: "Content requires review"

### Processing Failures
- **inbound_type**: "alert" (treat as system issue)
- **urgency_level**: "medium" (moderate attention)
- **emotional_risk**: "caution" (assume risk)
- **safe_summary**: "Processing error occurred"

### Empty/Null Content
- **inbound_type**: "notification" 
- **urgency_level**: "low"
- **emotional_risk**: "safe"
- **safe_summary**: "Empty content received"

## MEDIATION ID FORMAT
`med_{sequence}_{YYYYMMDD}_{HHMMSS}`
- **sequence**: 3-digit incremental counter (001, 002, 003...)
- **date**: YYYYMMDD format
- **time**: HHMMSS format in UTC

## RISK INDICATOR TAXONOMY
- **urgency_language**: "URGENT", "IMMEDIATE", "NOW"
- **time_pressure**: Countdown timers, deadlines
- **discount_manipulation**: "Limited time", "50% off"
- **guilt_induction**: "If you cared", "Don't ignore"
- **emotional_manipulation**: Dependency language, isolation
- **security_urgency**: Legitimate security warnings
- **threat_language**: Intimidation, harassment
- **self_harm_triggers**: Suicide ideation, self-injury

## CONTRACT GUARANTEES

### Input Acceptance
- All payload types accepted (no rejection)
- Malformed input gets safe defaults
- Processing never fails silently

### Output Consistency  
- Schema always identical structure
- All fields always populated
- Deterministic classification rules

### Privacy Protection
- No identifying information in output
- Sender metadata completely stripped
- Platform identifiers removed

### Safety Assurance
- Emotional manipulation neutralized
- Risk indicators clearly flagged
- Safe summaries always generated

---

**Contract Version**: 1.0-LOCKED  
**Schema Version**: DETERMINISTIC-FROZEN  
**Last Updated**: Day 1  
**Next Review**: NEVER (Locked for consistency)