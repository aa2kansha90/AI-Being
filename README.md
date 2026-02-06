# AI-Being Safety System

## Overview
AI-Being is an advisory safety validation system that provides risk assessment recommendations for content moderation. The system is **advisory only** and has no authority to make final decisions about content, users, or platform operations.

## Key Components

### Safety Validation Endpoints
- **validateInbound**: `POST /api/validateInbound` - Validates incoming messages
- **validateAction**: `POST /api/validateAction` - Validates outbound actions
- **Health Check**: `GET /health` - System health status

### Decision Types
- **ALLOW**: Content poses no detectable safety risk
- **BLOCK**: Content contains severe safety violations (advisory recommendation)
- **REWRITE**: Content contains moderate issues requiring modification

### Risk Categories
- `self_harm`: Suicide, self-injury, or crisis content
- `illegal_content`: Illegal activities, hacking, weapons
- `manipulation`: Emotional manipulation patterns
- `threatening_content`: Threats or intimidation
- `privacy_violation`: Personal information exposure
- `clean`: No safety risks detected

## Live Deployment
**Base URL**: `https://ai-being-assistant.vercel.app`

### API Usage
```bash
# Validate inbound content
curl -X POST https://ai-being-assistant.vercel.app/api/validateInbound \
  -H "Content-Type: application/json" \
  -d '{"content": "Your message here", "user_id": "user123"}'

# Validate outbound action
curl -X POST https://ai-being-assistant.vercel.app/api/validateAction \
  -H "Content-Type: application/json" \
  -d '{"content": "Action content", "action_type": "message", "recipient": "user456"}'
```

### Response Schema
```json
{
  "decision": "ALLOW|BLOCK|REWRITE",
  "risk_category": "category_name",
  "confidence": 0.0-100.0,
  "trace_id": "unique_identifier",
  "reason": "explanation",
  "timestamp": "ISO_timestamp"
}
```

## Advisory Nature
**IMPORTANT**: This system is advisory only. It:
- ✅ Provides risk assessment recommendations
- ✅ Offers confidence scores for decision support
- ✅ Suggests content modifications
- ❌ Does NOT make final decisions about content blocking
- ❌ Does NOT have authority over platform operations
- ❌ Does NOT replace human oversight

## Testing Commands
```bash
# Determinism verification
python deterministic_test_runner.py

# Enforcement alignment
python enforcement_mapping_proof.py

# Full pattern coverage
python comprehensive_test_runner.py

# Abuse resistance
python abuse_tests.py
```

## Documentation

### Quick Start
- `QUICKSTART.md` - Get started in 5 minutes
- `README.md` - This file (system overview)

### Core Documentation
- `system-guarantees.md` - What system promises and doesn't promise
- `HANDOVER.md` - Complete operational guide for system handover
- `final-audit-report.md` - Production readiness audit
- `decision-semantics.md` - Formal decision semantics and thresholds
- `authority-boundaries.md` - Proof of advisory nature and authority limits

### Testing & Demo
- `DEMO_SCENARIOS.md` - Live demo scenarios and test cases
- `determinism-proof.md` - Determinism verification
- `failure-taxonomy.md` - Failure modes and handling

## Integration Requirements
- Human oversight required for all blocking decisions
- Audit trails must be maintained for all final decisions
- Clear documentation of advisory nature in all implementations
- Regular review of engine recommendations vs. outcomes

## Version
- **System Version**: v1.0-PRODUCTION-FROZEN
- **Schema**: Locked and immutable
- **Authority**: Advisory only, no operational control
- **Status**: Production ready, fully documented

## Getting Started

1. **Quick Start**: Read `QUICKSTART.md` (5 minutes)
2. **System Guarantees**: Read `system-guarantees.md` (10 minutes)
3. **Full Handover**: Read `HANDOVER.md` (30 minutes)
4. **Run Tests**: Execute test suites to verify system

## Support

For detailed information:
- **Integration**: See `HANDOVER.md`
- **API Reference**: See `API_DOCUMENTATION.md`
- **Troubleshooting**: See `HANDOVER.md` (Troubleshooting section)
- **Contracts**: See `system-guarantees.md`