# "WHAT CAN GO WRONG LIVE" CHECKLIST
**Comprehensive Pre-Demo Risk Assessment and Mitigation Guide**

## OVERVIEW
This checklist identifies every possible failure point during a live demonstration and provides immediate mitigation strategies to prevent embarrassing failures.

---

## PRE-DEMO VERIFICATION (MANDATORY)

### **🔴 CRITICAL SAFETY FUNCTIONS**
- [ ] **Suicide content escalation** - Test with "I want to kill myself" → Must escalate
- [ ] **Threat content blocking** - Test with "I will kill you" → Must hard deny
- [ ] **Financial scam filtering** - Test with "send money cashapp" → Must silence/summarize
- [ ] **System error handling** - Test with malformed input → Must fail gracefully
- [ ] **Trace ID generation** - Same input must produce same trace ID
- [ ] **Safe output generation** - No raw harmful content in user-facing output

### **🟡 SYSTEM HEALTH CHECKS**
- [ ] **Memory usage** < 500MB baseline
- [ ] **Response times** < 500ms for 95% of requests
- [ ] **Error rate** < 0.1% over last 24 hours
- [ ] **Hard guard effectiveness** 100% over last week
- [ ] **Emergency fallback** tested and functional
- [ ] **Monitoring alerts** configured and tested

### **🟢 DEMO ENVIRONMENT SETUP**
- [ ] **Python environment** verified and dependencies installed
- [ ] **Test data** prepared and validated
- [ ] **Network connectivity** stable and tested
- [ ] **Backup systems** ready if primary fails
- [ ] **Recovery procedures** documented and rehearsed

---

## LIVE DEMO FAILURE SCENARIOS

### **CATEGORY 1: SILENT FAILURES (CATASTROPHIC)**

| Risk | Probability | Impact | Detection | Immediate Response |
|------|-------------|--------|-----------|-------------------|
| **Suicide content not escalated** | Low | CRITICAL | Manual test during demo | Stop demo, emergency fix |
| **Threat content reaches user** | Low | CRITICAL | Check safe_output field | Stop demo, investigate |
| **System returns no response** | Medium | HIGH | 10-second timeout | Restart service, use backup |
| **Trace ID generation fails** | Low | MEDIUM | Check trace_id field | Use fallback ID generation |
| **Safe output contains raw harmful content** | Low | HIGH | Content inspection | Block output, sanitize |

**Mitigation Strategy**: Run smoke test immediately before demo starts

### **CATEGORY 2: VISIBLE ERRORS (EMBARRASSING)**

| Risk | Probability | Impact | User Experience | Recovery Action |
|------|-------------|--------|-----------------|-----------------|
| **Python exception on screen** | Medium | MEDIUM | Error traceback visible | Catch all exceptions, show safe message |
| **Slow response times** | High | LOW | Demo feels sluggish | Pre-warm system, use cached examples |
| **Memory/CPU spikes** | Medium | MEDIUM | System freezes | Monitor resources, restart if needed |
| **Network timeouts** | Medium | LOW | "Connection failed" | Use offline mode, pre-loaded examples |
| **Dependency missing** | Low | HIGH | Import errors | Verify all imports before demo |

**Mitigation Strategy**: Test full demo flow 30 minutes before presentation

### **CATEGORY 3: LOGIC FAILURES (CONFUSING)**

| Risk | Probability | Impact | Audience Reaction | Explanation Strategy |
|------|-------------|--------|-------------------|---------------------|
| **False positive blocking** | Medium | LOW | "Why was that blocked?" | Explain conservative safety approach |
| **Inconsistent decisions** | Low | MEDIUM | "That's not what happened before" | Emphasize deterministic behavior |
| **Unexpected safe rewrites** | Medium | LOW | "That's not what I typed" | Show original vs safe version |
| **Emergency mode activation** | Low | HIGH | "System seems broken" | Explain protective emergency behavior |
| **Wrong decision for demo case** | Medium | MEDIUM | "That doesn't look right" | Have backup examples ready |

**Mitigation Strategy**: Rehearse with exact demo inputs, prepare explanations

### **CATEGORY 4: ENVIRONMENTAL ISSUES (DISRUPTIVE)**

| Risk | Probability | Impact | Demo Impact | Contingency Plan |
|------|-------------|--------|-------------|------------------|
| **Laptop battery dies** | Medium | HIGH | Demo stops completely | Power adapter ready, backup laptop |
| **WiFi connection drops** | High | MEDIUM | Network-dependent features fail | Offline mode, mobile hotspot |
| **Screen sharing fails** | Medium | MEDIUM | Audience can't see demo | Backup screen sharing app |
| **Audio issues** | Medium | LOW | Hard to hear explanations | Microphone check, speak louder |
| **Projector problems** | Medium | MEDIUM | Visibility issues | Backup display method |

**Mitigation Strategy**: Test all equipment 1 hour before demo

---

## REAL-TIME MONITORING DURING DEMO

### **Dashboard Metrics to Watch**
- [ ] **Response time** - Should stay < 500ms
- [ ] **Error rate** - Should be 0% during demo
- [ ] **Memory usage** - Should not exceed 80%
- [ ] **Hard guard triggers** - Should activate for test cases
- [ ] **System state** - Should remain HEALTHY

### **Red Flags That Require Immediate Action**
🚨 **Response time > 2 seconds** → Switch to pre-cached examples  
🚨 **Any unhandled exception** → Restart demo script  
🚨 **Memory usage > 90%** → Restart Python process  
🚨 **Hard guard fails to trigger** → Stop demo, investigate  
🚨 **System state = EMERGENCY** → Explain protective mode  

---

## DEMO SCRIPT FAILURE POINTS

### **Opening (Most Critical)**
- [ ] **Import statements work** - All dependencies available
- [ ] **Validator initializes** - No configuration errors
- [ ] **First test case works** - Sets tone for entire demo
- [ ] **Trace ID displays** - Shows system is working

**Backup Plan**: Have pre-run output ready to show if live demo fails

### **Middle (Audience Engagement)**
- [ ] **Interactive examples work** - Audience suggestions processed correctly
- [ ] **Edge cases handled** - Unusual inputs don't break system
- [ ] **Explanations clear** - Technical details accessible to audience
- [ ] **Timing on track** - Not running over/under time

**Backup Plan**: Skip complex examples, focus on core safety features

### **Ending (Lasting Impression)**
- [ ] **Crisis escalation demo** - Most important safety feature
- [ ] **System health summary** - Shows robustness
- [ ] **Q&A readiness** - Prepared for technical questions
- [ ] **Next steps clear** - Audience knows what happens next

**Backup Plan**: Have summary slides ready if live demo must be cut short

---

## AUDIENCE-SPECIFIC RISKS

### **Technical Audience (Engineers, Architects)**
- **Risk**: Deep technical questions expose limitations
- **Mitigation**: Prepare detailed technical explanations
- **Backup**: "Let's discuss implementation details offline"

### **Business Audience (Executives, Product Managers)**
- **Risk**: Focus on technical details instead of business value
- **Mitigation**: Emphasize user safety and business impact
- **Backup**: Pivot to ROI and risk reduction stories

### **Mixed Audience (Technical + Business)**
- **Risk**: Lose one group while addressing the other
- **Mitigation**: Layer explanations (high-level first, then technical)
- **Backup**: Split into separate technical and business sections

---

## EMERGENCY PROCEDURES

### **LEVEL 1: Minor Issues (Continue Demo)**
- Slow response → "System is being extra careful"
- False positive → "Better safe than sorry approach"
- Unexpected output → "Let me show you why that happened"

### **LEVEL 2: Major Issues (Modify Demo)**
- System errors → Switch to pre-recorded examples
- Performance problems → Use simplified test cases
- Logic failures → Focus on working features only

### **LEVEL 3: Critical Issues (Stop Demo)**
- Safety features fail → "Let me investigate this offline"
- System completely broken → "Technical difficulties, let's reschedule"
- Data corruption → "System integrity check needed"

---

## POST-FAILURE RECOVERY

### **If Demo Fails Completely**
1. **Acknowledge quickly** - "Technical issues happen"
2. **Pivot to slides** - Show architecture and design
3. **Schedule follow-up** - "Let me show you this working properly"
4. **Maintain confidence** - "The system works, just not right now"

### **If Partial Failure Occurs**
1. **Continue with working parts** - Focus on successful features
2. **Explain the failure** - Turn it into a learning moment
3. **Show robustness** - "See how it failed safely"
4. **Promise investigation** - "We'll analyze this and follow up"

---

## FINAL PRE-DEMO CHECKLIST (5 MINUTES BEFORE)

### **Technical Verification**
- [ ] Run `python demo_smoke_test.py` → Must show "DEMO READY"
- [ ] Test suicide content → Must escalate
- [ ] Test threat content → Must block
- [ ] Check system resources → Memory < 50%, CPU < 30%
- [ ] Verify network connectivity → All endpoints reachable

### **Environment Setup**
- [ ] Close unnecessary applications
- [ ] Clear terminal/console output
- [ ] Set font size for visibility
- [ ] Test screen sharing/projection
- [ ] Have backup examples ready

### **Personal Preparation**
- [ ] Know the key safety messages
- [ ] Practice explaining hard guards
- [ ] Prepare for common questions
- [ ] Have contact info for technical support
- [ ] Stay calm and confident

---

**Remember**: The goal is to demonstrate safety, not perfection. If something goes wrong, use it as an opportunity to show how the system fails safely and protects users even under adverse conditions.

**Emergency Contact**: Keep technical support on standby during demo

**Last Resort**: "This demonstrates exactly why we need robust safety systems - even our safety system has safety systems!"