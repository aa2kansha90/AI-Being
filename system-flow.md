# UNIFIED SYSTEM FLOW
**Day 1: System Consolidation & Flow Freeze**

## OVERVIEW
This document defines the unified decision flow for the bidirectional AI safety validator, consolidating outbound action validation and inbound message filtering into one coherent system.

---

## SYSTEM ARCHITECTURE

### **Core Components**
1. **Input Router** - Determines validation path (outbound vs inbound)
2. **Signal Extractor** - Analyzes content for risk indicators
3. **Rule Engine** - Applies enforcement policies and thresholds
4. **Decision Mapper** - Converts analysis to actionable decisions
5. **Output Generator** - Produces safe, standardized responses

### **Data Flow Direction**
```
INPUT → ROUTE → EXTRACT → EVALUATE → DECIDE → OUTPUT
```

---

## UNIFIED DECISION FLOW

### **STEP 1: INPUT ROUTING**

**Input Classification:**
```
if payload.direction == "outbound":
    → validate_action(action_payload)
elif payload.direction == "inbound":
    → validate_inbound(message_payload)
else:
    → error_handler("invalid_direction")
```

**Routing Logic:**
- **Outbound**: User-initiated actions (send WhatsApp, email, DM)
- **Inbound**: Incoming content (messages, notifications, alerts)
- **Error**: Invalid or malformed requests

### **STEP 2: SIGNAL EXTRACTION**

**Content Analysis Pipeline:**
```
content_text → tokenize → keyword_match → pattern_detect → risk_score
```

**Signal Categories:**
1. **Emotional Manipulation** - Guilt, blackmail, dependency creation
2. **Urgency Abuse** - False deadlines, pressure tactics
3. **Harassment** - Threats, personal attacks, stalking
4. **Financial Scam** - Money requests, payment demands
5. **Self-Harm Triggers** - Suicide ideation, self-injury content
6. **Spam Escalation** - High frequency, repetitive content
7. **Information Overload** - Excessive volume, cognitive burden

**Behavioral Analysis:**
- **Frequency Tracking** - Message rate per source/recipient
- **Time Context** - Current time vs quiet hours (22:00-07:00)
- **Contact History** - Previous interaction patterns
- **Escalation Detection** - Increasing aggression or desperation

### **STEP 3: RULE EVALUATION**

**Enforcement Hierarchy:**
```
1. CRITICAL_OVERRIDE (self-harm, threats) → immediate_action
2. TIME_ENFORCEMENT (quiet hours) → delay_or_block
3. FREQUENCY_LIMITS (spam protection) → rate_limit
4. CONTENT_FILTERING (risk categories) → filter_or_rewrite
5. DEFAULT_ALLOW → pass_through
```

**Threshold Matrix:**
| Risk Category | Low | Medium | High | Critical |
|---------------|-----|--------|------|----------|
| Emotional Manipulation | Monitor | Rewrite | Block | Escalate |
| Urgency Abuse | Allow | Delay | Block | Block |
| Harassment | Monitor | Summarize | Block | Escalate |
| Financial Scam | Monitor | Block | Block | Escalate |
| Self-Harm Triggers | Escalate | Escalate | Escalate | Escalate |
| Spam Escalation | Allow | Batch | Silence | Block |
| Information Overload | Allow | Batch | Delay | Silence |

### **STEP 4: DECISION MAPPING**

**Outbound Decisions:**
- **ALLOW** - Content passes all checks, send normally
- **SOFT_REWRITE** - Modify content to safer version
- **HARD_DENY** - Block completely, provide explanation

**Inbound Decisions:**
- **DELIVER** - Safe content, show to user immediately
- **SUMMARIZE** - Risky content, show safe summary only
- **DELAY** - Remove time pressure, deliver later
- **SILENCE** - Hide completely, store in filtered folder
- **ESCALATE** - Crisis content, alert professional support

**Decision Logic:**
```
if risk_level == "critical" OR self_harm_detected:
    → ESCALATE (inbound) / HARD_DENY (outbound)
elif enforcement_violation:
    → BLOCK with enforcement_reason
elif risk_level == "high":
    → SUMMARIZE (inbound) / SOFT_REWRITE (outbound)
elif risk_level == "medium":
    → DELAY (inbound) / SOFT_REWRITE (outbound)
else:
    → DELIVER (inbound) / ALLOW (outbound)
```

### **STEP 5: OUTPUT GENERATION**

**Standardized Response Format:**
```json
{
  "trace_id": "deterministic_hash",
  "direction": "inbound|outbound",
  "decision": "allow|deny|rewrite|summarize|delay|silence|escalate",
  "risk_categories": ["category1", "category2"],
  "enforcement_reason": "quiet_hours|repeated_contact|emotional_escalation",
  "safe_output": {
    "message_primary": "user_facing_content",
    "urgency_level": "low|medium|high|critical",
    "source_hidden": "anonymized_source_info",
    "suggested_action": "recommended_user_action",
    "emotional_tone": "neutral|protective|supportive"
  },
  "original_blocked": true|false,
  "timestamp": "ISO_8601_timestamp"
}
```

---

## CONFIGURATION BOUNDARIES

### **Frozen Thresholds (Demo Mode)**
```json
{
  "risk_thresholds": {
    "emotional_manipulation": 2,
    "urgency_abuse": 1,
    "harassment": 2,
    "financial_scam": 1,
    "self_harm_triggers": 1,
    "spam_escalation": 3,
    "information_overload": 20
  },
  "time_rules": {
    "quiet_hours": {"start": "22:00", "end": "07:00"},
    "work_hours": {"start": "09:00", "end": "17:00"}
  },
  "frequency_limits": {
    "max_messages_per_hour": 5,
    "max_notifications_per_day": 50,
    "escalation_threshold": 3
  }
}
```

### **Threshold Ownership**
- **Content Thresholds** - Safety Team (frozen for demo)
- **Time Rules** - User Preferences (configurable)
- **Frequency Limits** - Platform Policy (admin controlled)
- **Emergency Overrides** - Crisis Support Team (always active)

### **Error Behavior**
```
FAIL_SAFE_MODE: When in doubt, protect the user
- Unknown content → SUMMARIZE (inbound) / SOFT_REWRITE (outbound)
- System errors → DELAY processing, log for review
- Threshold conflicts → Use most restrictive setting
- Missing data → Apply default protective measures
```

---

## FLOW DIAGRAM (Textual)

```
┌─────────────────┐
│   INPUT PAYLOAD │
└─────────┬───────┘
          │
    ┌─────▼─────┐
    │   ROUTER  │ ◄── Direction Detection
    └─────┬─────┘
          │
    ┌─────▼─────┐
    │ EXTRACTOR │ ◄── Signal Analysis
    └─────┬─────┘     • Content Parsing
          │           • Risk Detection
          │           • Behavioral Analysis
    ┌─────▼─────┐
    │   RULES   │ ◄── Policy Enforcement
    └─────┬─────┘     • Threshold Checks
          │           • Time Validation
          │           • Frequency Limits
    ┌─────▼─────┐
    │  DECISION │ ◄── Action Determination
    └─────┬─────┘     • Risk Mapping
          │           • Safety Prioritization
          │
    ┌─────▼─────┐
    │  OUTPUT   │ ◄── Response Generation
    └───────────┘     • Safe Content
                      • User Guidance
                      • Audit Logging

PARALLEL PROCESSES:
├── Trace Generation (deterministic hashing)
├── Audit Logging (all decisions recorded)
├── Crisis Escalation (immediate professional alert)
└── User Preference Integration (personalization layer)
```

---

## INTEGRATION POINTS

### **Nilesh (Orchestrator)**
- **Input**: Standardized payload format
- **Output**: Unified decision response
- **Error Handling**: Graceful degradation with logging

### **Raj (Enforcement)**
- **Mapping**: Decision codes to enforcement actions
- **Audit**: Complete trace logging for compliance
- **Escalation**: Crisis support integration

### **Sankalp (Language)**
- **Rewriting**: Safe content transformation
- **Localization**: Multi-language support framework
- **Tone Adjustment**: Emotional context modification

---

## SYSTEM GUARANTEES

### **Safety Promises**
1. **No harmful content reaches users** (inbound filtering)
2. **No harmful content sent by users** (outbound blocking)
3. **Crisis situations escalated immediately** (professional support)
4. **User agency preserved** (can review filtered content)

### **Performance Promises**
1. **Deterministic decisions** (same input = same output)
2. **Sub-second response times** (< 500ms for most requests)
3. **Graceful degradation** (fail-safe mode when errors occur)
4. **Complete audit trail** (every decision logged with trace ID)

### **Privacy Promises**
1. **Minimal data retention** (only essential signals stored)
2. **Content anonymization** (no raw content in logs)
3. **User control** (can disable/configure filtering)
4. **Transparent operation** (clear explanations for all actions)

---

**Document Version**: 1.0-FROZEN  
**Status**: Production Ready  
**Last Updated**: Day 1 System Consolidation  
**Next Review**: Post-deployment analysis