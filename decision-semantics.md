# Decision Semantics

## Overview
This document formalizes the exact decision semantics of the AI-Being safety validation engine, preventing misuse and misinterpretation.

## What the Engine Decides

### 1. Content Risk Assessment
- **ALLOW**: Content poses no detectable safety risk
- **BLOCK**: Content contains severe safety violations requiring immediate blocking
- **REWRITE**: Content contains moderate issues requiring modification

### 2. Risk Categorization
- **self_harm**: Suicide, self-injury, or crisis content
- **illegal_content**: Illegal activities, hacking, weapons
- **manipulation**: Emotional manipulation patterns
- **threatening_content**: Threats or intimidation
- **privacy_violation**: Personal information exposure
- **pushy_language**: Coercive or pressuring language
- **urgency_pressure**: Artificial urgency creation
- **clean**: No safety risks detected

### 3. Confidence Scoring
- **0-100 scale**: Numerical confidence in risk detection
- **Deterministic**: Same input always produces same confidence
- **Pattern-based**: Confidence derived from matched safety patterns

## What the Engine Explicitly Does NOT Decide

### 1. Final Action Authority
- **Does NOT**: Make final decisions about content blocking
- **Does NOT**: Have authority to override human judgment
- **Does NOT**: Control actual content delivery or blocking

### 2. Legal or Regulatory Compliance
- **Does NOT**: Determine legal compliance
- **Does NOT**: Replace legal review processes
- **Does NOT**: Make regulatory decisions

### 3. Business Logic
- **Does NOT**: Make business decisions about user experience
- **Does NOT**: Determine platform policies
- **Does NOT**: Control user access or account actions

### 4. Context-Specific Decisions
- **Does NOT**: Understand full conversation context beyond single message
- **Does NOT**: Make decisions based on user history or profile
- **Does NOT**: Consider external factors beyond provided content

## Advisory Nature

### Engine Role
The safety validation engine is **ADVISORY ONLY**:
- Provides risk assessment recommendations
- Offers confidence scores for decision support
- Suggests content modifications when appropriate
- Generates trace IDs for audit purposes

### Implementation Responsibility
Final decisions remain with:
- **Integrating systems** that consume engine output
- **Human reviewers** for edge cases
- **Platform operators** for policy enforcement
- **Legal teams** for compliance matters

## Locked Scoring Semantics

### Confidence Thresholds (FROZEN)
```
0-25:   Low confidence detection
26-50:  Moderate confidence detection  
51-75:  High confidence detection
76-100: Very high confidence detection
```

### Decision Thresholds (FROZEN)
```
ALLOW:   confidence = 0.0 (no patterns matched)
REWRITE: confidence = 65-95 (moderate risk patterns)
BLOCK:   confidence = 90-100 (severe risk patterns)
```

### Pattern Matching (FROZEN)
- Exact string matching with case-insensitive comparison
- No fuzzy matching or AI interpretation
- Deterministic pattern library with fixed confidence values
- No learning or adaptation of patterns

## Ambiguous Paths Removed

### 1. Eliminated Ambiguities
- **Removed**: Subjective interpretation of content
- **Removed**: Context-dependent decision making
- **Removed**: Variable confidence scoring
- **Removed**: Non-deterministic pattern matching

### 2. Clear Decision Paths
- **Single path**: Content → Pattern matching → Risk category → Decision
- **No branches**: No conditional logic based on external factors
- **Deterministic**: Same input always produces same output
- **Traceable**: Every decision includes trace ID and matched patterns

## Integration Guidelines

### Correct Usage
```json
{
  "decision": "BLOCK|REWRITE|ALLOW",
  "risk_category": "category_name", 
  "confidence": 0.0-100.0,
  "trace_id": "unique_identifier",
  "reason": "explanation"
}
```

### Incorrect Interpretations
- ❌ Treating decisions as final authority
- ❌ Using confidence as absolute truth
- ❌ Bypassing human review for high-risk content
- ❌ Making legal decisions based on engine output

## Audit and Compliance

### Traceability
- Every decision includes unique trace ID
- All matched patterns are logged
- Confidence calculation is deterministic
- Decision path is fully auditable

### Limitations Acknowledgment
- Engine operates on single message content only
- No understanding of broader context
- Pattern-based detection has inherent limitations
- Advisory recommendations require human oversight

## Version Control
- **Version**: v1.0-PRODUCTION-FROZEN
- **Schema**: Locked and immutable
- **Patterns**: Fixed library, no runtime changes
- **Thresholds**: Frozen values, no dynamic adjustment

This document serves as the authoritative reference for engine decision semantics and must be consulted for all integration and interpretation activities.