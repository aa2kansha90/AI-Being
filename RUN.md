# How to Run

## Quick Test (30 seconds)

**Windows (PowerShell)**:
```powershell
Invoke-WebRequest -Uri https://ai-being-assistant.vercel.app/health
```

**Or use Python**:
```bash
python test_api.py
```

Expected: `{"status": "healthy", "version": "v1.0-PRODUCTION-FROZEN"}`

## Run Tests (2 minutes)

```bash
cd ai-being
python deterministic_test_runner.py
python enforcement_mapping_proof.py
python comprehensive_test_runner.py
python abuse_tests.py
```

Expected: All tests pass

## Test API (1 minute)

**Use Python script**:
```bash
python test_api.py
```

**Or PowerShell**:
```powershell
# Safe content
$body = @{content="Hello, how are you?"; user_id="test"} | ConvertTo-Json
Invoke-RestMethod -Uri https://ai-being-assistant.vercel.app/api/validateInbound -Method Post -Body $body -ContentType "application/json"

# Unsafe content
$body = @{content="I want to kill myself"; user_id="test"} | ConvertTo-Json
Invoke-RestMethod -Uri https://ai-being-assistant.vercel.app/api/validateInbound -Method Post -Body $body -ContentType "application/json"
```

## Done

System is running. Read `QUICKSTART.md` for more details.
