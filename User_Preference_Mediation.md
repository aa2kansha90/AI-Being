# USER PREFERENCE MEDIATION
**Day 2: Respecting User Mental Space and Preferences**

## OVERVIEW
This system mediates between inbound content and user delivery preferences, ensuring content is transformed to match user's mental state, communication style, and availability preferences while maintaining safety protections.

## PREFERENCE CATEGORIES

### 1. Language Preferences
**Purpose**: Control communication tone and complexity

**Options**:
- **formal**: Professional, structured language
- **casual**: Relaxed, conversational tone  
- **minimal**: Bullet points, essential info only
- **detailed**: Full context and explanations

**Impact**:
- Transforms message summaries to match preferred style
- Adjusts explanation depth for filtered content
- Maintains consistent voice across all communications

### 2. Notification Frequency
**Purpose**: Control information flow rate

**Options**:
- **immediate**: Real-time delivery (0 delay)
- **batched_hourly**: Digest every hour
- **batched_daily**: Single daily summary at preferred time
- **on_demand**: Only when user explicitly checks

**Impact**:
- Groups non-urgent messages into batches
- Delays delivery based on user schedule
- Critical content always bypasses frequency limits

### 3. Emotional Tone Management
**Purpose**: Protect mental state from emotional manipulation

**Options**:
- **neutral**: Strip emotional language, factual only
- **positive**: Emphasize constructive aspects
- **protective**: Extra filtering of negative content
- **transparent**: Show original emotional context

**Impact**:
- Rewrites emotionally charged content in preferred tone
- Filters manipulation attempts more aggressively
- Provides emotional context warnings when needed

### 4. Time Windows
**Purpose**: Respect work/life boundaries

**Settings**:
- **work_hours**: 9:00-17:00 (configurable)
- **personal_hours**: 17:00-22:00 (configurable)
- **sleep_hours**: 22:00-09:00 (configurable)
- **emergency_override**: Always allow critical content

**Impact**:
- Delays non-urgent content outside preferred windows
- Adjusts urgency thresholds based on time context
- Respects do-not-disturb periods

### 5. Priority Contacts
**Purpose**: Ensure important people always reach user

**Categories**:
- **family**: Immediate family members
- **work**: Direct manager, key colleagues
- **emergency**: Medical, legal, security contacts
- **trusted**: Close friends, verified contacts

**Impact**:
- Priority contacts bypass most filtering
- Reduced transformation for trusted sources
- Enhanced verification for claimed priority contacts

## TRANSFORMATION LOGIC

### Content Rewriting Rules

#### **Formal Language Mode**
```
Original: "Hey! Super urgent - need those docs ASAP!!!"
Transformed: "Request received for document delivery with indicated urgency."
```

#### **Minimal Language Mode**  
```
Original: "I hope you're having a great day! I wanted to reach out about..."
Transformed: "• Work request: Project timeline discussion"
```

#### **Neutral Emotional Tone**
```
Original: "I'm devastated you haven't responded! This is crushing me!"
Transformed: "Follow-up message received regarding previous communication."
```

#### **Protective Emotional Tone**
```
Original: "Everyone thinks you're terrible but I still care about you"
Transformed: "Message contains concerning language - review when ready."
```

### Batching Logic

#### **Hourly Batching**
- Collect non-urgent messages for 60 minutes
- Generate single digest with priority ordering
- Include summary count and source diversity

#### **Daily Batching**
- Aggregate all non-critical content for 24 hours
- Categorize by source type (work, personal, commercial)
- Provide actionable summary with key decisions needed

### Time Window Enforcement

#### **Outside Work Hours**
- Work messages → delay until work_hours start
- Urgent work → reduce to "medium" priority
- Personal messages → deliver normally

#### **During Sleep Hours**
- All non-emergency → delay until wake time
- Emergency contacts → immediate delivery
- Critical safety → override all settings

## PREFERENCE INTEGRATION

### User Profile Structure
```json
{
  "user_id": "user_12345",
  "preferences": {
    "language": "minimal",
    "notification_frequency": "batched_hourly", 
    "emotional_tone": "protective",
    "time_windows": {
      "work": "09:00-17:00",
      "personal": "17:00-22:00", 
      "sleep": "22:00-09:00"
    },
    "priority_contacts": {
      "family": ["mom@email.com", "+1-555-0123"],
      "work": ["boss@company.com", "team@company.com"],
      "emergency": ["911", "doctor@clinic.com"]
    }
  }
}
```

### Transformation Pipeline
1. **Safety Check**: Apply risk taxonomy regardless of preferences
2. **Source Verification**: Check against priority contact lists
3. **Time Context**: Evaluate current time window
4. **Content Transform**: Apply language and tone preferences
5. **Delivery Schedule**: Apply frequency and batching rules
6. **Final Output**: Generate preference-aware delivery

## PREFERENCE OVERRIDE CONDITIONS

### Safety Overrides
- **Self-harm content**: Always escalate regardless of preferences
- **Threats**: Immediate delivery to ensure user safety
- **Emergency contacts**: Bypass all filtering and delays

### Critical Business Overrides  
- **System outages**: Override sleep hours for IT staff
- **Security breaches**: Immediate delivery regardless of batching
- **Legal deadlines**: Override emotional tone filtering

### User Control Overrides
- **Manual check**: User can always access full unfiltered content
- **Preference updates**: Take effect immediately for new content
- **Emergency mode**: Temporary bypass of all mediation

## SAMPLE TRANSFORMATIONS

### Scenario 1: Spam During Sleep Hours
**Input**: Marketing email at 2:00 AM
**Preferences**: sleep_hours=22:00-09:00, frequency=batched_daily
**Output**: Delayed until 9:00 AM, included in daily digest

### Scenario 2: Emotional Manipulation from Unknown Contact
**Input**: "You're breaking my heart by ignoring me!"
**Preferences**: emotional_tone=protective, language=minimal
**Output**: "• Message from unknown contact - emotional content detected"

### Scenario 3: Work Emergency from Priority Contact
**Input**: Boss sends "Server down! Need you NOW!" at 11:00 PM
**Preferences**: sleep_hours=22:00-09:00, priority_contacts includes boss
**Output**: Immediate delivery with context: "Priority work contact - server issue"

### Scenario 4: Family Message During Work
**Input**: Mom sends "Call me when you can, nothing urgent"
**Preferences**: work_hours=09:00-17:00, family in priority_contacts
**Output**: Immediate delivery but marked as personal: "Family message - non-urgent"

## IMPLEMENTATION GUIDELINES

### Preference Learning
- **Usage Patterns**: Adapt to user behavior over time
- **Feedback Integration**: Learn from user corrections
- **Context Awareness**: Adjust based on calendar and location

### Privacy Protection
- **Local Processing**: Preferences stored locally when possible
- **Minimal Data**: Only store essential preference indicators
- **User Control**: Full preference export and deletion options

### Performance Optimization
- **Caching**: Cache transformed content for similar messages
- **Batch Processing**: Group transformations for efficiency
- **Lazy Loading**: Only transform content when user requests it

---

**Document Version**: 1.0  
**Last Updated**: Day 2  
**Integration**: Works with inbound_behavior_validator.py  
**Dependencies**: User preference storage system