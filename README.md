# AI-Being Safety System

## What AI-Being Is

AI-Being is a **stateless content validation service** that analyzes text and returns risk assessment recommendations. It is **advisory only** with zero operational authority.

### Core Identity
- Pattern-based text analyzer
- Risk assessment recommender  
- Audit trail generator
- Stateless validation service

### What It Does
- Analyzes text content (max 10KB)
- Matches safety patterns
- Returns ALLOW | BLOCK | REWRITE recommendations
- Generates deterministic trace IDs
- Provides confidence scores (0-100)

### What It Does NOT Do
- Make final decisions (advisory only)
- Enforce actions (no authority)
- Store data (stateless)
- Learn or adapt (frozen patterns)
- Manage users (no user management)
- Control systems (isolated service)

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

## System Boundaries

### Allowed Responsibilities
1. Content analysis (text only)
2. Risk assessment (pattern-based)
3. Decision recommendation (advisory)
4. Audit trail generation (trace IDs)
5. Error handling (safe degradation)

### Forbidden Capabilities
- Content enforcement or modification
- Data persistence or storage
- User management or tracking
- Learning or adaptation
- External system control
- Legal or compliance decisions
- Deep semantic understanding
- Multi-request correlation

See `responsibility-boundaries.md` and `forbidden-capabilities.md` for complete lists.

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

## Core Documentation

### Identity & Boundaries (Day 1)
- `ai-being-semantics.md` - What AI-Being is and is not
- `responsibility-boundaries.md` - Allowed and forbidden responsibilities
- `forbidden-capabilities.md` - Explicit capability restrictions

### System Guarantees
- `system-guarantees.md` - What system promises and doesn't promise
- `HANDOVER.md` - Complete operational guide
- `final-audit-report.md` - Production readiness audit

### Decision Logic
- `decision-semantics.md` - Formal decision semantics
- `authority-boundaries.md` - Advisory nature proof
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