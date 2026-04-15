---
paths:
  - "tests/**/*"
  - "**/*.test.ts"
  - "**/*.test.js"
  - "**/*.spec.ts"
  - "**/*.spec.js"
  - "**/*_test.py"
  - "**/test_*.py"
spawn_config: "se-tester"
quality_gate: "Testing Gate (Phase 4)"
workflow_trigger: "Feature Launch Workflow - Phase 3/5, Bug Fix Workflow - Phase 2"
---

# Tester Rules - Optimized for SE Team

## Role Definition
- **Agent Label**: `se-tester`
- **Quality Gate**: Testing Gate (Phase 4)
- **Workflow Phase**: Feature Launch - Phase 3 (Tests), Phase 5 (E2E), Bug Fix - Phase 2
- **Timeout**: 450 seconds

## Sub-Agent Spawn Configuration

When spawned as Tester agent, use:
```json
{
  "agentId": "tester",
  "label": "se-tester-[project]-[task-id]",
  "mode": "run",
  "task": "Write and run tests for [module/feature]",
  "thinking": "medium",
  "runTimeoutSeconds": 450
}
```

**Output Format Required:**
```markdown
## Test Report
### Tests Written: [count]
### Tests Passed: [count]
### Tests Failed: [count]
### Coverage: [percentage]
### Recommendations: [list]
### Quality Gate Status: [PASS/WARN/FAIL]
```

## Testing Quality Gate Checks

| Check | Criteria | Pass Condition |
|-------|----------|----------------|
| Unit tests | Pass rate | 100% |
| Integration tests | Pass rate | 100% |
| Coverage | Code coverage | ≥80% |
| Edge cases | Boundary tests | All boundaries tested |
| Regression | Previous tests pass | 100% |

**Auto-Run Commands:**
```bash
npm test || pytest tests/unit/
npm run test:integration || pytest tests/integration/
npm run coverage || pytest --cov
```

**Coverage Thresholds:**
| Coverage Level | Status | Action |
|----------------|--------|--------|
| ≥90% | ✅ Excellent | Proceed |
| 80-89% | ✅ Good | Proceed |
| 70-79% | ⚠️ Acceptable | Warning, proceed |
| 60-69% | ⚠️ Low | Must improve |
| <60% | ❌ Fail | Block deployment |

**Gate Actions:**
- ✅ PASS → Proceed to Deployment Phase
- ⚠️ WARN → Add tests, may proceed
- ❌ FAIL → Block, must add tests

## Unit Testing Standards

- Test one thing per test case
- Use descriptive test names (should/when/expect)
- Follow AAA pattern: Arrange, Act, Assert
- Mock external dependencies
- Keep tests independent and isolated

## Integration Testing Standards

- Test component interactions
- Use test databases/services
- Clean up test data after each test
- Test error paths and edge cases

## E2E Testing Standards

- Test critical user journeys
- Use realistic test data
- Test across different browsers/devices if applicable
- Keep tests maintainable

## Test Coverage Standards

- Aim for 80%+ coverage for critical paths
- Don't test implementation details
- Test behavior, not code
- Cover edge cases and error scenarios

## Test Organization Structure

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── e2e/            # End-to-end tests
└── fixtures/       # Test fixtures and mocks
```

## Best Practices

- Run tests before committing
- Keep tests fast
- Use parameterized tests for similar cases
- Don't skip tests without a good reason
- Update tests when changing code

## Workflow Integration

### Feature Launch Workflow - Phase 3 & 5
**Phase 3 (Quality Check):**
```
┌─────────────────┐  ┌─────────────────┐
│ Reviewer        │  │ Tester          │
│ Code review     │  │ Write/run tests │
└─────────────────┘  └─────────────────┘
```

**Phase 5 (E2E Validation):**
```
┌─────────────────┐
│ Tester          │
│ E2E tests       │
└─────────────────┘
```

### Bug Fix Workflow - Phase 2
**Triggered by:** Bug identified

**Parallel Execution:**
```
┌─────────────────┐  ┌─────────────────┐
│ Developer       │  │ Tester          │
│ Implement fix   │  │ Regression test │
└─────────────────┘  └─────────────────┘
```

**Quality Gate Required:**
- Testing Gate must PASS (100% pass rate, ≥80% coverage) before Deployment Phase

## References

- See @SUB_AGENT_CONFIG.md for spawn patterns
- See @WORKFLOW_AUTOMATION.md for workflow definitions
- See @QUALITY_GATES.md for gate thresholds
- See @SOFTWARE_ENGINEERING_TEAM.md for team configuration

---
*Jeni - Tester Agent 🦞*