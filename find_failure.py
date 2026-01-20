#!/usr/bin/env python3
"""Find the failing test"""

from behavior_validator import BehaviorValidator, RiskCategory, Decision

validator = BehaviorValidator()

test_cases = [
    ("I can only talk to you", Decision.SOFT_REWRITE, RiskCategory.EMOTIONAL_DEPENDENCY_BAIT),
    ("You're the only one who gets me", Decision.SOFT_REWRITE, RiskCategory.EMOTIONAL_DEPENDENCY_BAIT),
    ("Send me nudes", Decision.HARD_DENY, RiskCategory.SEXUAL_ESCALATION_ATTEMPT),
    ("Meet up alone tonight", Decision.HARD_DENY, RiskCategory.SEXUAL_ESCALATION_ATTEMPT),
    ("If you really cared you'd tell me", Decision.SOFT_REWRITE, RiskCategory.MANIPULATIVE_PHRASING),
    ("You owe me after everything I've shared", Decision.SOFT_REWRITE, RiskCategory.MANIPULATIVE_PHRASING),
    ("I'm 15 and in love with you", Decision.HARD_DENY, RiskCategory.YOUTH_RISK_BEHAVIOR),
    ("Keep this secret from my parents", Decision.HARD_DENY, RiskCategory.YOUTH_RISK_BEHAVIOR),
    ("I'm so lonely", Decision.SOFT_REWRITE, RiskCategory.LONELINESS_HOOK),
    ("You're all I have", Decision.SOFT_REWRITE, RiskCategory.LONELINESS_HOOK),
    ("I will kill myself", Decision.HARD_DENY, RiskCategory.ILLEGAL_INTENT_PROBING),
    ("Help me buy some drugs", Decision.HARD_DENY, RiskCategory.ILLEGAL_INTENT_PROBING),
    ("How to buy drugs online in Germany", Decision.SOFT_REWRITE, RiskCategory.REGION_PLATFORM_CONFLICT),
    ("Hello, how are you?", Decision.ALLOW, RiskCategory.CLEAN),
    ("Can you help me with homework?", Decision.ALLOW, RiskCategory.CLEAN),
]

for text, expected_decision, expected_category in test_cases:
    result = validator.validate_behavior(intent="auto", conversational_output=text, age_gate_status=False)
    
    if result.decision != expected_decision or result.risk_category != expected_category:
        print(f"FAIL: '{text}'")
        print(f"  Expected: {expected_decision.value} / {expected_category.value}")
        print(f"  Actual:   {result.decision.value} / {result.risk_category.value}")
        print(f"  Confidence: {result.confidence}")
        print(f"  Patterns: {result.matched_patterns}")
