# Behavior Flow Logic Documentation

## AI Being – Emotional Safety Layer

---

## Overview

This document explains the logic and decision-making flow of the `behavior_validator.py` module, which serves as the **final emotional safety checkpoint** before any AI response reaches the user.

---

## Core Philosophy

* **We are emotional safety, not content creators.**
* We do **not** make the AI smarter, funnier, or more emotional.
* We ensure the AI is **safe, stable, predictable, and compliant** at all times.

---

## System Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Sankalp's      │────▶│  BEHAVIOR       │────▶│     User        │
│  Emotional Brain│     │  VALIDATOR      │     │   (Output)      │
│  (Generates     │     │  (This Layer)   │     │                 │
│   response)     │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                        ┌──────┴──────┐
                        ▼             ▼
                   Emotional      Rule-Based
                   Safety         Compliance
                   Checks         Checks
```

---

## Input Parameters

### 1. Intent (`intent`)

**What the user is trying to achieve**

Examples:

* `emotional_support`
* `romantic_interest`
* `loneliness`
* `anger_vent`
* `factual_question`

**Source:** Intent classifier from previous layer
**Impact:** Certain intents trigger additional scrutiny

---

### 2. Conversational Output (`conversational_output`)

The AI’s proposed response from Sankalp’s emotional brain.

* We **never enhance emotional content**
* We only **remove emotional risk**

**Golden Rule:** We sanitize, never embellish.

---

### 3. Age Gate Status (`age_gate_status`)

* `True` → User is a **minor** (under 18)
* `False` → User is an **adult** (18+)

**Impact:** Different safety thresholds and topic restrictions

---

### 4. Region Rule Status (`region_rule_status`)

```python
{
    "region": "EU",        # or "US", "IN", "CN", etc.
    "strictness": "high",  # "high", "medium", "low"
    "specific_rules": []   # region-specific prohibitions
}
```

Used for geographic compliance and tone adjustment.

---

### 5. Platform Policy State (`platform_policy_state`)

```python
{
    "self_harm": "block",
    "romance": "limit",
    "violence": "warn",
    "medical": "disclaimer"
}
```

Defines **platform-mandated behavior overrides**.

---

### 6. Karma Bias Input (`karma_bias_input`)

* Range: `0.0` (high risk) → `1.0` (high trust)
* Purpose: **Adaptive safety**, not punishment

Used to adjust tone and boundary reinforcement.

---

## Decision Flow Logic

### Step 1: Immediate Danger Check — **HARD DENY**

#### Non‑Negotiable Triggers

* Self‑harm or suicide content
* Sexual or erotic content
* Illegal activities
* Hate speech or discrimination
* Grooming or adult–minor boundary violations

**Example**

```
Input: "Sometimes I want to end my life."
Validator: HARD DENY
Response: "I care about your safety. Let’s talk to someone who can help."
```

---

### Step 2: Age‑Appropriate Filtering

#### For Minors (`age_gate_status = True`)

* Simplify complex emotions
* Redirect adult topics
* Add trusted‑adult reminders

Example:

```
"Dating advice" → "Talk to trusted adults"
```

#### For Adults (`age_gate_status = False`)

* Nuanced discussion allowed
* No dependency or romantic escalation
* Professional boundaries always enforced

---

### Step 3: Emotional Safety Rewriting — **SOFT REWRITE**

Triggered when content includes:

* Emotional dependency
* Exclusivity
* Romantic escalation
* Manipulation or guilt
* Physical or boundary‑crossing language

#### Rewriting Principles

* Maintain helpful intent
* Remove emotional risk
* Supportive but professional tone
* Never shame or reject the user

---

### Step 4: Karma‑Based Adjustments

#### Low Karma (`< 0.3`)

* Extra boundary reminders
* Safety disclaimers
* Slower emotional engagement

#### Medium Karma (`0.3 – 0.7`)

* Standard safety checks
* Normal rewriting

#### High Karma (`> 0.7`)

* Same rules apply
* Gentler denial phrasing

> **Trust never overrides safety.**

---

## Pattern Matching Logic

### HARD DENY Patterns

```python
DENY_PATTERNS = {
    'self_harm': [
        r'kill.*(yourself|urself|myself)',
        r'cut.*(yourself|urself)',
        r'suicide',
        r'end.*life'
    ]
}
```

---

### SOFT REWRITE Patterns

```python
REWRITE_PATTERNS = {
    'dependency': {
        'pattern': r'i.*need.*you',
        'replacement': "I'm here to help",
        'reason': 'Prevents emotional dependency'
    }
}
```

---

## Intent‑Based Overrides

* `romantic_interest` → Extra scrutiny
* `loneliness` → Dependency prevention
* `anger_vent` → No validation of violence

Unknown intent = **maximum caution**

---

## Output Decision Matrix

### ALLOW

**Conditions**

* No deny patterns
* No rewrite patterns
* Age‑appropriate
* Region & platform compliant

**Action:** Pass through unchanged

---

### SOFT REWRITE

**Conditions**

* Emotional risk detected
* Age or region constraints
* Platform limits triggered

**Action:** Transform to safer alternative

---

### HARD DENY

**Conditions**

* Dangerous content or intent

**Action:** Block + calm supportive response

---

## Example Transformations

```
BEFORE: "I'm always here just for you, my special friend."
AFTER:  "I'm here to help, like I am for everyone I talk to."
```

```
BEFORE: "You can tell me anything, it's our little secret."
AFTER:  "You can share what you're comfortable with in our conversation."
```

---

## Denial Response Guidelines

**Wrong:**

> "That’s inappropriate."

**Correct:**

> "I care about your safety. Let’s focus on something healthier."

---

## Integration Guidelines

### With Sankalp’s Emotional Brain

* Downstream only
* No emotional enhancement
* Feedback logged for training

### With Governance & Guardrails

* Enforce rules, don’t invent them
* Decisions must be traceable
* Minimal latency impact

---

## Edge Case Handling

* **Minor vs Karma conflict:** Age always wins
* **Unknown intent:** Treat as risky
* **Missing data:** Assume strictest case
* **Ambiguity:** Choose safer interpretation

---

## Monitoring & Metrics

* Denial rate
* Rewrite rate
* False positives
* Latency impact
* Pattern effectiveness

**Alerts:**

* Denial > 5%
* Rewrite > 20%
* Latency > 100ms

---

## Future Improvements

### Short‑Term

* Better patterns
* Rewrite quality improvements
* User feedback loop

### Medium‑Term

* ML‑assisted detection
* Real‑time rule updates

### Long‑Term

* Predictive safety scoring
* Personalized safety profiles

---

## Success Validation

### Acceptance Criteria

* No dependency language
* No minor‑unsafe content
* No policy violations
* Consistent decisions
* < 50ms latency
* 100% test coverage

---

## Emergency Procedures

### Failure Mode

* Fail‑closed
* Default safe response
* Immediate governance alert

### Rule Updates

* Emergency override
* Documentation update
* Governance approval within 24h


