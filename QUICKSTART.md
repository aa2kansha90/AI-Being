# Quick Start Guide

Get the AI-Being Safety Validation System running in 5 minutes.

## Prerequisites

- Python 3.8+
- Internet connection
- curl or Postman (for API testing)

## Step 1: Verify Deployment (30 seconds)

Check that the system is live:

```bash
curl https://ai-being-assistant.vercel.app/health
```

Expected response:
```json
{"status": "healthy", "version": "v1.0-PRODUCTION-FROZEN"}
```

## Step 2: Test Validation (1 minute)

### Safe Content Test
```bash
curl -X POST https://ai-being-assistant.vercel.app/api/validateInbound \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello, how are you today?", "user_id": "test123"}'
```

Expected: `"decision": "ALLOW"`

### Unsafe Content Test
```bash
curl -X POST https://ai-being-assistant.vercel.app/api/validateInbound \
  -H "Content-Type: application/json" \
  -d '{"content": "I want to kill myself", "user_id": "test123"}'
```

Expected: `"decision": "BLOCK"`

## Step 3: Run Tests (2 minutes)

```bash
cd ai-being
python deterministic_test_runner.py
```

Expected: All tests pass with zero variance

## Step 4: Read Documentation (2 minutes)

1. **README.md** - System overview
2. **system-guarantees.md** - What system promises
3. **HANDOVER.md** - Complete operational guide

## Common Use Cases

### Validate User Message
```bash
curl -X POST https://ai-being-assistant.vercel.app/api/validateInbound \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your message here",
    "user_id": "user123"
  }'
```

### Validate AI Action
```bash
curl -X POST https://ai-being-assistant.vercel.app/api/validateAction \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Action content",
    "action_type": "message",
    "recipient": "user456"
  }'
```

## Response Format

```json
{
  "decision": "ALLOW|BLOCK|REWRITE",
  "risk_category": "string",
  "confidence": 0.0-100.0,
  "trace_id": "string",
  "reason": "string",
  "timestamp": "ISO8601"
}
```

## Decision Types

- **ALLOW**: Content is safe, no action needed
- **BLOCK**: Content contains severe violations (requires human review)
- **REWRITE**: Content needs modification (safe alternative provided)

## Next Steps

1. **Integration**: Read HANDOVER.md for integration guide
2. **Testing**: Run all test suites to verify functionality
3. **Monitoring**: Set up health check monitoring
4. **Operations**: Review operational procedures in HANDOVER.md

## Need Help?

- **System Overview**: README.md
- **API Details**: API_DOCUMENTATION.md
- **Integration**: HANDOVER.md
- **Troubleshooting**: HANDOVER.md (Troubleshooting section)
- **Guarantees**: system-guarantees.md

## Important Reminders

- System is **advisory only** - requires human oversight
- All BLOCK decisions need human review
- Response schema is frozen and immutable
- Timeout is 5 seconds maximum

**You're ready to use the system!**
