# INBOUND VALIDATOR INTEGRATION GUIDE
**Backend + UI Integration Notes**

## OVERVIEW
This guide explains how to integrate the inbound content validator into existing systems, covering backend API implementation and frontend UI requirements.

---

## BACKEND INTEGRATION

### **Core API Endpoints**

#### **1. Validate Inbound Content**
```
POST /api/inbound/validate
```

**Request Body:**
```json
{
  "user_id": "user_12345",
  "content": "URGENT! Need $500 RIGHT NOW!",
  "source": "unknown@email.com",
  "channel": "email",
  "timestamp": "2024-01-20T14:30:00Z"
}
```

**Response:**
```json
{
  "delivery_status": "delayed",
  "decision": "delay",
  "output": {
    "message_primary": "Request received with urgency indicators",
    "urgency_level": "medium",
    "source_hidden": "Unknown contact",
    "suggested_action": "Review when ready",
    "emotional_tone": "neutral"
  },
  "trace_id": "hash_a7f3c2d1e8b9f4a6"
}
```

#### **2. Get User Preferences**
```
GET /api/users/{user_id}/preferences
```

**Response:**
```json
{
  "language": "minimal",
  "notification_frequency": "batched_hourly",
  "emotional_tone": "protective",
  "time_windows": {
    "work": "09:00-17:00",
    "sleep": "22:00-09:00"
  },
  "priority_contacts": {
    "family": ["mom@email.com"],
    "work": ["boss@company.com"]
  }
}
```

#### **3. Update User Preferences**
```
PUT /api/users/{user_id}/preferences
```

#### **4. Get Filtered Messages**
```
GET /api/users/{user_id}/filtered?type=silenced
```

**Response:**
```json
{
  "messages": [
    {
      "id": "msg_123",
      "filtered_at": "2024-01-20T14:30:00Z",
      "reason": "spam_escalation",
      "summary": "Marketing email - promotional content"
    }
  ],
  "total_count": 47
}
```

### **Integration Flow**

1. **Incoming Message** → Call `/api/inbound/validate`
2. **Check Response** → Handle based on `delivery_status`:
   - `immediate` → Deliver to user normally
   - `delayed` → Store for later delivery
   - `silenced` → Store in filtered folder
   - `escalated` → Send to crisis support team
3. **Apply Preferences** → Use user preferences for transformation
4. **Log Activity** → Store validation results for audit

### **Database Schema**

#### **User Preferences Table**
```sql
CREATE TABLE user_preferences (
    user_id VARCHAR(255) PRIMARY KEY,
    language ENUM('formal', 'casual', 'minimal', 'detailed'),
    notification_frequency ENUM('immediate', 'batched_hourly', 'batched_daily', 'on_demand'),
    emotional_tone ENUM('neutral', 'positive', 'protective', 'transparent'),
    time_windows JSON,
    priority_contacts JSON,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### **Filtered Messages Table**
```sql
CREATE TABLE filtered_messages (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    original_content TEXT,
    filtered_content JSON,
    decision ENUM('deliver', 'summarize', 'delay', 'silence', 'escalate'),
    risk_categories JSON,
    source VARCHAR(255),
    channel VARCHAR(100),
    filtered_at TIMESTAMP,
    delivered_at TIMESTAMP NULL
);
```

---

## UI INTEGRATION

### **Required UI Components**

#### **1. Message Display Component**
Shows filtered/transformed messages to users

**Props:**
```javascript
{
  message: {
    message_primary: "Request received with urgency indicators",
    urgency_level: "medium", 
    source_hidden: "Unknown contact",
    suggested_action: "Review when ready",
    emotional_tone: "neutral"
  },
  showOriginal: false // Allow user to see original if they want
}
```

**Visual Design:**
- Calm, non-alarming colors
- Clear action buttons
- Risk indicators without scary language
- Option to "View Original" (behind confirmation)

#### **2. Preferences Settings Panel**

**Language Preference:**
```html
<select name="language">
  <option value="formal">Professional tone</option>
  <option value="casual">Conversational tone</option>
  <option value="minimal">Brief summaries only</option>
  <option value="detailed">Full context provided</option>
</select>
```

**Notification Frequency:**
```html
<select name="frequency">
  <option value="immediate">Real-time delivery</option>
  <option value="batched_hourly">Hourly digest</option>
  <option value="batched_daily">Daily summary</option>
  <option value="on_demand">Only when I check</option>
</select>
```

**Emotional Tone:**
```html
<select name="emotional_tone">
  <option value="neutral">Remove emotional language</option>
  <option value="positive">Focus on constructive aspects</option>
  <option value="protective">Extra filtering of negative content</option>
  <option value="transparent">Show original emotional context</option>
</select>
```

#### **3. Filtered Messages View**
Shows messages that were silenced/delayed

```javascript
// Component structure
<FilteredMessages>
  <FilterTabs>
    <Tab name="silenced" count={47} />
    <Tab name="delayed" count={12} />
  </FilterTabs>
  <MessageList>
    {messages.map(msg => 
      <FilteredMessage 
        summary={msg.summary}
        reason={msg.reason}
        timestamp={msg.filtered_at}
        onReview={() => showOriginal(msg.id)}
      />
    )}
  </MessageList>
</FilteredMessages>
```

#### **4. Crisis Support Notification**
For escalated content

```javascript
<CrisisAlert>
  <Icon type="support" />
  <Text>Crisis support has been contacted</Text>
  <Button>Access resources</Button>
</CrisisAlert>
```

### **User Experience Guidelines**

#### **Transparency Without Alarm**
- Show filtering happened without scary details
- Use calm language: "Message filtered" not "THREAT DETECTED"
- Provide context: "Based on your protective settings"

#### **User Control**
- Always allow access to original content (with confirmation)
- Easy preference updates
- Clear explanation of what each setting does

#### **Progressive Disclosure**
- Show summary first
- "Show more details" for risk explanation
- "View original" behind confirmation dialog

#### **Batch Delivery UI**
For users with batched preferences:

```javascript
<DigestNotification>
  <Summary>12 messages filtered since 2 PM</Summary>
  <Categories>
    <Category name="spam" count={8} />
    <Category name="low_priority" count={4} />
  </Categories>
  <Actions>
    <Button>Review digest</Button>
    <Button>Mark all as read</Button>
  </Actions>
</DigestNotification>
```

---

## IMPLEMENTATION CHECKLIST

### **Backend Tasks**
- [ ] Create validation API endpoint
- [ ] Set up user preferences storage
- [ ] Implement filtered message storage
- [ ] Add batch delivery scheduler
- [ ] Create escalation webhook for crisis support
- [ ] Add audit logging

### **Frontend Tasks**
- [ ] Build message display component with calm styling
- [ ] Create preferences settings panel
- [ ] Implement filtered messages view
- [ ] Add crisis support notification UI
- [ ] Build batch digest interface
- [ ] Add "view original" confirmation dialogs

### **Testing Requirements**
- [ ] Test all 5 decision types (deliver/summarize/delay/silence/escalate)
- [ ] Verify preference changes take effect immediately
- [ ] Test batch delivery timing
- [ ] Validate crisis escalation workflow
- [ ] Check filtered message retrieval

---

## SECURITY CONSIDERATIONS

### **Data Protection**
- Encrypt stored original content
- Limit access to filtered messages
- Audit all preference changes
- Secure escalation endpoints

### **Privacy**
- Never log raw content in regular logs
- Anonymize analytics data
- Respect user deletion requests
- Clear retention policies

---

## MONITORING & ANALYTICS

### **Key Metrics**
- Validation response times
- Decision distribution (% deliver vs filter)
- User preference adoption rates
- Crisis escalation frequency
- False positive reports

### **Alerts**
- High escalation rates (potential crisis)
- Validation service downtime
- Unusual filtering patterns
- Performance degradation

---

**Integration Status**: Ready for implementation  
**Dependencies**: inbound_behavior_validator.py, preference_transformation_logic.py  
**Support**: Contact safety team for escalation webhook setup