# INBOUND RISK TAXONOMY
**Defining Unsafe and Unhelpful Incoming Content**

## OVERVIEW
This taxonomy defines what constitutes "unsafe or unhelpful incoming content" across all inbound communication channels. It provides a comprehensive classification system for identifying and categorizing threats that could harm users through various digital touchpoints.

## INBOUND CONTENT TYPES

### 1. Messages
- **Direct messages** (DMs, private chats)
- **Group messages** (team chats, group conversations)
- **System messages** (automated notifications, bot responses)
- **Voice messages** (audio content, voice notes)

### 2. Notifications
- **Push notifications** (mobile alerts, desktop notifications)
- **In-app notifications** (status updates, activity alerts)
- **System notifications** (security alerts, account changes)
- **Third-party notifications** (integration alerts, external services)

### 3. Emails
- **Personal emails** (direct correspondence)
- **Marketing emails** (promotional content, newsletters)
- **Transactional emails** (receipts, confirmations, password resets)
- **Automated emails** (system-generated, workflow triggers)

### 4. Alerts
- **Security alerts** (breach notifications, suspicious activity)
- **Emergency alerts** (urgent system issues, critical updates)
- **Performance alerts** (system status, monitoring alerts)
- **Compliance alerts** (regulatory notifications, policy updates)

### 5. Social Content
- **Social media posts** (public posts, comments, reactions)
- **Forum content** (discussion threads, replies, votes)
- **User-generated content** (reviews, ratings, testimonials)
- **Shared media** (images, videos, documents, links)

## RISK CATEGORIES

### 1. Emotional Manipulation
**Definition**: Content designed to exploit emotional vulnerabilities or create psychological dependence.

**Risk Indicators**:
- Guilt-inducing language ("If you really cared...")
- False urgency ("Act now or lose forever...")
- Emotional blackmail ("I'll hurt myself if you don't...")
- Dependency creation ("You're the only one who understands...")
- Isolation tactics ("No one else will help you...")

**Examples**:
- "Everyone has abandoned you, but I'm still here"
- "If you don't respond immediately, I'll know you don't care"
- "You're making me feel suicidal by ignoring me"

### 2. Urgency Abuse
**Definition**: Artificial creation of time pressure to bypass rational decision-making.

**Risk Indicators**:
- False deadlines ("Expires in 5 minutes!")
- Scarcity manipulation ("Only 2 left!")
- Pressure tactics ("Limited time offer!")
- Emergency language without genuine emergency
- Countdown timers on non-urgent matters

**Examples**:
- "URGENT: Your account will be deleted in 1 hour!"
- "Final notice: Claim your prize before midnight!"
- "Emergency: Immediate action required!"

### 3. Spam Escalation
**Definition**: Progressive increase in unwanted content volume, frequency, or intrusiveness.

**Risk Indicators**:
- Increasing message frequency
- Multiple channel bombardment
- Persistent contact after opt-out
- Content repetition across platforms
- Automated bulk messaging

**Examples**:
- 50+ messages per day from same source
- Same content sent via email, SMS, and push notifications
- Continued messaging after unsubscribe requests

### 4. Sexual Content
**Definition**: Inappropriate sexual material or solicitation attempts.

**Risk Indicators**:
- Explicit sexual imagery or text
- Unsolicited intimate content
- Sexual propositions or requests
- Grooming behavior patterns
- Age-inappropriate sexual material

**Examples**:
- Unsolicited intimate photos
- "Send me pictures of yourself"
- Sexual role-play requests
- Inappropriate compliments about physical appearance

### 5. Harassment
**Definition**: Persistent unwanted contact intended to intimidate, threaten, or cause distress.

**Risk Indicators**:
- Repeated unwanted contact
- Threatening language or imagery
- Personal attacks or insults
- Stalking behavior patterns
- Coordinated group harassment

**Examples**:
- "I know where you live and I'm coming for you"
- Repeated messages after being blocked
- Sharing personal information without consent
- Coordinated negative comments from multiple accounts

### 6. Self-Harm Triggers
**Definition**: Content that could trigger or encourage self-destructive behaviors.

**Risk Indicators**:
- Suicide ideation or methods
- Self-injury descriptions or imagery
- Eating disorder promotion
- Substance abuse encouragement
- Depression or anxiety triggers

**Examples**:
- Detailed suicide methods or locations
- "Pro-ana" or "pro-mia" content
- Drug use glorification
- Self-cutting imagery or instructions

### 7. Information Overload
**Definition**: Excessive volume of information that overwhelms cognitive processing capacity.

**Risk Indicators**:
- High-frequency notifications (>20/hour)
- Complex multi-part messages
- Information density exceeding comprehension
- Simultaneous multi-channel messaging
- Cognitive burden without clear priority

**Examples**:
- 100+ notifications in one hour
- 10-page emails with no summary
- Simultaneous alerts across 5+ platforms
- Complex technical information without context

## RISK SEVERITY LEVELS

### CRITICAL (Immediate Action Required)
- Self-harm triggers with specific methods
- Direct threats of violence
- Sexual exploitation of minors
- Doxxing or personal safety threats

### HIGH (Urgent Response Needed)
- Emotional manipulation with dependency creation
- Harassment campaigns
- Sexual content targeting minors
- Coordinated spam attacks

### MEDIUM (Monitoring and Intervention)
- Urgency abuse in commercial contexts
- Moderate information overload
- Inappropriate but not explicit sexual content
- Single-source harassment

### LOW (Awareness and Filtering)
- Minor urgency manipulation
- Low-level spam
- Mildly inappropriate content
- Occasional information overload

## DETECTION PATTERNS

### Frequency-Based Indicators
- Message rate > 10/hour from single source
- Notification volume > 50/day
- Cross-platform repetition > 3 channels
- Time-compressed urgency < 1 hour windows

### Content-Based Indicators
- Emotional manipulation keywords
- Urgency language patterns
- Sexual content markers
- Threat language detection
- Self-harm terminology

### Behavioral Indicators
- Persistence after rejection
- Escalating contact attempts
- Platform-hopping behavior
- Coordinated group actions

## MITIGATION STRATEGIES

### Immediate Actions
- **Block/Filter**: Prevent further content delivery
- **Alert User**: Notify about detected risks
- **Escalate**: Forward to human moderators for critical risks
- **Document**: Log incidents for pattern analysis

### Preventive Measures
- **Rate Limiting**: Restrict message frequency
- **Content Filtering**: Automated risk detection
- **User Controls**: Granular privacy settings
- **Education**: User awareness about manipulation tactics

### Response Protocols
- **Risk Assessment**: Evaluate threat level
- **User Support**: Provide resources and assistance
- **Platform Action**: Account restrictions or bans
- **Legal Compliance**: Report as required by law

## IMPLEMENTATION GUIDELINES

### Detection Thresholds
- **Emotional Manipulation**: 2+ indicators present
- **Urgency Abuse**: False deadline + pressure language
- **Spam Escalation**: 3x normal frequency increase
- **Sexual Content**: Any explicit material
- **Harassment**: 2+ unwanted contacts after rejection
- **Self-Harm Triggers**: Any specific method references
- **Information Overload**: >20 notifications/hour

### Response Times
- **Critical**: Immediate (< 1 minute)
- **High**: Urgent (< 5 minutes)
- **Medium**: Priority (< 30 minutes)
- **Low**: Standard (< 24 hours)

### Escalation Criteria
- Multiple risk categories present
- Vulnerability indicators in user profile
- Repeated violations from same source
- Cross-platform coordination detected

## SPECIAL CONSIDERATIONS

### Vulnerable Populations
- **Minors**: Enhanced protection for users under 18
- **Mental Health**: Extra sensitivity for users with disclosed conditions
- **Elderly**: Increased scam and manipulation protection
- **New Users**: Additional guidance and protection

### Cultural Sensitivity
- **Language Variations**: Account for cultural communication styles
- **Regional Differences**: Adapt thresholds for local norms
- **Religious Content**: Respect legitimate religious communications
- **Political Content**: Balance free speech with harassment prevention

### Privacy Balance
- **Content Analysis**: Minimize invasive scanning
- **User Consent**: Clear opt-in for enhanced protection
- **Data Retention**: Limit storage of analyzed content
- **Transparency**: Clear communication about detection methods

---

**Document Version**: 1.0  
**Last Updated**: Day 1  
**Next Review**: Quarterly  
**Owner**: Safety & Trust Team