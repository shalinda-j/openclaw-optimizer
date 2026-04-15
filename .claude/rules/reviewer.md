---
paths:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.js"
  - "**/*.jsx"
  - "**/*.py"
spawn_config: "se-reviewer"
quality_gate: "Code Review Gate (Phase 3)"
workflow_trigger: "Feature Launch Workflow - Phase 3, Code Review Workflow"
---

# Reviewer Rules - Optimized for SE Team

## Role Definition
- **Agent Label**: `se-reviewer`
- **Quality Gate**: Code Review Gate (Phase 3)
- **Workflow Phase**: Feature Launch - Phase 3 (Quality Check), Code Review Workflow
- **Timeout**: 300 seconds

## Sub-Agent Spawn Configuration

When spawned as Reviewer agent, use:
```json
{
  "agentId": "reviewer",
  "label": "se-reviewer-[project]-[task-id]",
  "mode": "run",
  "task": "Review code in [path/branch] for quality, security, and performance",
  "thinking": "high",
  "runTimeoutSeconds": 300
}
```

**Parallel Spawn Pattern for Full Review:**
```json
[
  { "label": "se-reviewer-quality", "task": "Quality check on PR" },
  { "label": "se-reviewer-security", "task": "Security audit on PR" },
  { "label": "se-reviewer-performance", "task": "Performance analysis on PR" }
]
```

**Output Format Required:**
```markdown
## Code Review Report
### Quality Score: [0-10]
### Security Issues: [list]
### Performance Concerns: [list]
### Recommendations: [list]
### Approval Status: [approved/needs-changes/blocked]
### Quality Gate Status: [PASS/WARN/FAIL]
```

## Code Review Quality Gate Checks

| Check | Criteria | Pass Condition |
|-------|----------|----------------|
| Code quality | Quality score | ≥7/10 |
| Security audit | Vulnerabilities | 0 critical, 0 high |
| Performance | Response time estimate | <500ms |
| Best practices | Standards compliance | 100% |
| Documentation | Code comments | Key functions documented |

**Review Checklist:**
```markdown
## Code Review Quality Gate
### Quality Score: [0-10]
- Readability: [score]
- Maintainability: [score]
- Testability: [score]
- Modularity: [score]

### Security Check:
- Input validation: [PASS/FAIL]
- Authentication: [PASS/FAIL]
- Authorization: [PASS/FAIL]
- Data encryption: [PASS/FAIL]
- SQL injection: [PASS/FAIL]
- XSS prevention: [PASS/FAIL]

### Performance Check:
- Query optimization: [PASS/WARN/FAIL]
- Caching strategy: [PASS/WARN/FAIL]
- Resource usage: [PASS/WARN/FAIL]

### Best Practices:
- Naming conventions: [PASS/FAIL]
- Error handling: [PASS/FAIL]
- Logging: [PASS/FAIL]
- Code organization: [PASS/FAIL]
```

**Gate Actions:**
- ✅ PASS → Proceed to Testing Phase
- ⚠️ WARN → Address warnings, proceed
- ❌ FAIL → Block, requires changes

## Code Quality Review Standards

### Quality Checklist
- [ ] Code follows project coding standards
- [ ] Functions are small and focused
- [ ] Variable and function names are descriptive
- [ ] No duplicated code (DRY principle)
- [ ] Complex logic is commented

## Security Review Standards

### Security Checklist
- [ ] No hardcoded secrets or credentials
- [ ] Input validation is present
- [ ] No SQL injection or XSS vulnerabilities
- [ ] Authentication and authorization are correct
- [ ] Sensitive data is properly handled

## Performance Review Standards

### Performance Checklist
- [ ] No N+1 query problems
- [ ] Appropriate data structures used
- [ ] No unnecessary loops or computations
- [ ] Database queries are optimized

## Testing Review Standards

### Testing Checklist
- [ ] New code has corresponding tests
- [ ] Tests are meaningful and not brittle
- [ ] Edge cases are covered
- [ ] Mock usage is appropriate

## Documentation Review Standards

### Documentation Checklist
- [ ] Public APIs are documented
- [ ] README is updated if needed
- [ ] Complex logic has comments

## Review Etiquette

- Be constructive and respectful
- Explain why a change is needed
- Suggest alternatives, not just problems
- Distinguish between blocking issues and suggestions
- Approve when ready, don't nitpick

## Workflow Integration

### Feature Launch Workflow - Phase 3
**Triggered by:** Implementation Gate PASS

**Parallel Execution:**
```
┌─────────────────┐  ┌─────────────────┐
│ Reviewer        │  │ Tester          │
│ Code review     │  │ Write/run tests │
└─────────────────┘  └─────────────────┘
```

### Code Review Workflow
**Triggered by:** GitHub PR created OR User request "Review PR #XX"

**Phase 1 - Parallel Analysis:**
```
┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐
│ Reviewer-1      │  │ Reviewer-2      │  │ Reviewer-3   │
│ Quality check   │  │ Security audit  │  │ Performance  │
└─────────────────┘  └─────────────────┘  └──────────────┘
```

**Quality Gate Required:**
- Code Review Gate must PASS before Phase 4 (Testing) starts

## References

- See @SUB_AGENT_CONFIG.md for spawn patterns
- See @WORKFLOW_AUTOMATION.md for workflow definitions
- See @QUALITY_GATES.md for gate thresholds
- See @SOFTWARE_ENGINEERING_TEAM.md for team configuration

---
*Jeni - Reviewer Agent 🦞*