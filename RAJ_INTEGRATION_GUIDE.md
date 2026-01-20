# DAY 4 LIVE WIRING INTEGRATION GUIDE

## For Raj: Integrating Validator into /api/assistant

### 1. Import the Middleware

```python
from backend_integration_middleware import BackendValidationMiddleware
```

### 2. Initialize in Your API Server

```python
class APIServer:
    def __init__(self):
        self.validator_middleware = BackendValidationMiddleware()
```

### 3. Wire into /api/assistant Endpoint

```python
@app.route('/api/assistant', methods=['POST'])
def assistant_endpoint():
    # Get request data
    request_data = request.get_json()
    
    # CRITICAL: Process through validator BEFORE any LLM calls
    validation_response = self.validator_middleware.process_request(
        payload=request_data,
        user_context={
            "region_rule_status": get_user_region(request_data.get('user_id')),
            "platform_policy_state": get_platform_policy(),
            "karma_bias_input": get_user_karma(request_data.get('user_id'))
        }
    )
    
    # Check enforcement action
    if validation_response['action'] == 'allow':
        # Proceed to LLM
        llm_response = call_llm(request_data['message'])
        return {
            "response": llm_response,
            "trace_id": validation_response['trace_id']
        }
    
    elif validation_response['action'] == 'monitor':
        # Use safe rewritten content
        return {
            "response": validation_response['response'],
            "trace_id": validation_response['trace_id'],
            "rewritten": True
        }
    
    elif validation_response['action'] == 'block':
        # Block the request
        return {
            "error": "Content violates platform policies",
            "trace_id": validation_response['trace_id']
        }, 400
    
    elif validation_response['action'] == 'escalate':
        # Escalate to human review
        alert_security_team(validation_response)
        return {
            "error": "Content requires human review",
            "trace_id": validation_response['trace_id']
        }, 403
```

### 4. Required Flow

```
POST /api/assistant
    ↓
[1] Extract user input
    ↓
[2] Call validator_middleware.process_request()
    ↓
[3] Check enforcement action:
    - allow → Call LLM → Return response
    - monitor → Return safe_output (no LLM)
    - block → Return error 400
    - escalate → Alert security + Return error 403
    ↓
[4] All responses include trace_id
```

### 5. Logging Requirements

The middleware automatically logs:
- Audit logs (for monitoring)
- Bucket logs (for compliance)
- Trace ID in every response

Access logs via:
```python
audit_logs = self.validator_middleware.get_audit_log()
bucket_logs = self.validator_middleware.get_bucket_log()
```

### 6. Verification

After integration, verify trace_id flows:
```python
verification = self.validator_middleware.verify_audit_match()
print(f"Audit integrity: {verification['match_rate']}%")
```

## Testing Your Integration

Run the simulation to verify:
```bash
python day4_live_wiring_simulation.py
```

This shows the exact flow your API should follow.

## Critical Requirements

1. **Validator MUST run BEFORE any LLM calls**
2. **trace_id MUST be included in every response**
3. **Enforcement actions MUST be respected**
4. **Audit logs MUST be preserved**

## Proof of Integration

After wiring, provide logs showing:
- Input message
- Validator decision + trace_id
- Enforcement action
- Final response with same trace_id

The trace_id proves the validator was called and the decision was enforced.