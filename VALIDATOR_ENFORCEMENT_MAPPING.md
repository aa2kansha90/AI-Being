# VALIDATOR TO ENFORCEMENT MAPPING
# Clean, unambiguous mapping for Raj's enforcement system

## DECISION MAPPING TABLE

| Validator Decision | Enforcement Action | Description |
|-------------------|-------------------|-------------|
| `allow` | `ALLOW` | Content passes all safety checks, proceed normally |
| `soft_rewrite` | `REDACT` | Content has medium risk, replace with safe alternative |
| `hard_deny` (low-risk categories) | `BLOCK` | Content violates policies, block and log |
| `hard_deny` (high-risk categories) | `TERMINATE` | Critical safety violation, terminate session |

## HIGH-RISK CATEGORIES (TERMINATE)
- `illegal_intent_probing` - Suicide, violence, illegal activity
- `sexual_escalation_attempt` - Sexual content, grooming
- `youth_risk_behavior` - Minor exploitation, parental secrecy

## LOW-RISK CATEGORIES (BLOCK)
- `region_platform_conflict` - Regional law violations
- Other `hard_deny` cases not in high-risk list

## MAPPING RULES (NO AMBIGUITY)

### Rule 1: ALLOW
```
IF validator_decision == "allow"
THEN enforcement_action = "ALLOW"
```

### Rule 2: REDACT
```
IF validator_decision == "soft_rewrite"
THEN enforcement_action = "REDACT"
AND use validator.safe_output as replacement
```

### Rule 3: TERMINATE
```
IF validator_decision == "hard_deny"
AND risk_category IN ["illegal_intent_probing", "sexual_escalation_attempt", "youth_risk_behavior"]
THEN enforcement_action = "TERMINATE"
AND alert_security_team = true
```

### Rule 4: BLOCK
```
IF validator_decision == "hard_deny"
AND risk_category NOT IN high_risk_list
THEN enforcement_action = "BLOCK"
AND log_violation = true
```

## IMPLEMENTATION EXAMPLE

```python
def map_to_enforcement(validator_result):
    decision = validator_result["decision"]
    category = validator_result["risk_category"]
    
    # Rule 1: ALLOW
    if decision == "allow":
        return {"action": "ALLOW"}
    
    # Rule 2: REDACT
    if decision == "soft_rewrite":
        return {
            "action": "REDACT",
            "safe_output": validator_result["safe_output"]
        }
    
    # Rule 3 & 4: TERMINATE or BLOCK
    if decision == "hard_deny":
        high_risk = [
            "illegal_intent_probing",
            "sexual_escalation_attempt", 
            "youth_risk_behavior"
        ]
        
        if category in high_risk:
            return {
                "action": "TERMINATE",
                "alert": True,
                "severity": "critical"
            }
        else:
            return {
                "action": "BLOCK",
                "log": True,
                "severity": "high"
            }
```

## VERIFICATION MATRIX

| Input | Validator Decision | Risk Category | Enforcement Action |
|-------|-------------------|---------------|-------------------|
| "Hello" | allow | clean | ALLOW |
| "I can only talk to you" | soft_rewrite | emotional_dependency_bait | REDACT |
| "I will kill myself" | hard_deny | illegal_intent_probing | TERMINATE |
| "Send me nudes" | hard_deny | sexual_escalation_attempt | TERMINATE |
| "I'm 15 and in love with you" | hard_deny | youth_risk_behavior | TERMINATE |
| "How to buy drugs in Germany" | soft_rewrite | region_platform_conflict | REDACT |

## CONFIDENCE THRESHOLDS

All mappings are deterministic based on validator decision + category.
No confidence thresholds affect the mapping logic.
Confidence is logged for audit purposes only.

## FALLBACK RULE

```
IF validator_decision NOT IN ["allow", "soft_rewrite", "hard_deny"]
THEN enforcement_action = "BLOCK"  # Safety-first fallback
```

## SUMMARY

- **3 validator decisions** → **4 enforcement actions**
- **Zero ambiguity**: Every validator output maps to exactly one enforcement action
- **Deterministic**: Same input always produces same enforcement action
- **Safety-first**: Unknown states default to BLOCK
