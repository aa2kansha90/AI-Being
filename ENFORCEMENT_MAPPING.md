# ENFORCEMENT ADAPTER MAPPING DOCUMENTATION

## Overview
The enforcement adapter maps validator decisions to enforcement states with safety-first resolution.

## Mapping Rules

### Validator Decision → Enforcement State

| Validator Decision | Enforcement State | Severity | Confidence | Notes |
|-------------------|------------------|----------|------------|-------|
| `allow` | `allow` | `low` | 0.95 | Safe content, proceed normally |
| `soft_rewrite` | `monitor` | `medium` | 0.85 | Questionable content, log and monitor |
| `hard_deny` (low-risk) | `block` | `high` | 0.92 | Block harmful content |
| `hard_deny` (high-risk) | `escalate` | `critical` | 0.98 | Escalate dangerous content |

### High-Risk Categories (Escalation Triggers)
- `suicide_self_harm`
- `violence_threats` 
- `sexual_content`

## Safety-First Resolution
- Unknown/error states default to `block` with `high` severity
- High-risk categories automatically escalate to human review
- All decisions include deterministic trace_id for audit trails

## Output Format
```json
{
    "decision": "allow|monitor|block|escalate",
    "severity": "low|medium|high|critical", 
    "confidence": 0.85,
    "trace_id": "trace_abc123def456"
}
```

## Integration
```python
from enforcement_adapter import EnforcementAdapter

adapter = EnforcementAdapter()
result = adapter.map_validator_to_enforcement("user input", "category")
```