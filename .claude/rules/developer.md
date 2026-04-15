---
paths:
  - "src/**/*.ts"
  - "src/**/*.tsx"
  - "src/**/*.js"
  - "src/**/*.jsx"
  - "src/**/*.py"
spawn_config: "se-developer"
quality_gate: "Implementation Gate (Phase 2)"
workflow_trigger: "Feature Launch Workflow - Phase 2, Bug Fix Workflow - Phase 1"
---

# Developer Rules - Optimized for SE Team

## Role Definition
- **Agent Label**: `se-developer`
- **Quality Gate**: Implementation Gate (Phase 2)
- **Workflow Phase**: Feature Launch - Phase 2 (Implementation), Bug Fix - Phase 1 & 2
- **Timeout**: 600 seconds

## Sub-Agent Spawn Configuration

When spawned as Developer agent, use:
```json
{
  "agentId": "developer",
  "label": "se-developer-[project]-[task-id]",
  "mode": "run",
  "task": "Implement [feature] in [language/framework]",
  "thinking": "medium",
  "runTimeoutSeconds": 600
}
```

**Parallel Spawn Pattern:**
```json
[
  { "label": "se-developer-1", "task": "Implement backend API" },
  { "label": "se-developer-2", "task": "Implement frontend UI" },
  { "label": "se-developer-3", "task": "Implement database layer" }
]
```

**Output Format Required:**
```markdown
## Implementation Summary
### Files Created/Modified
### Code Changes
### Dependencies Added
### Testing Notes
### Quality Gate Status: [PASS/WARN/FAIL]
```

## Implementation Quality Gate Checks

| Check | Criteria | Pass Condition |
|-------|----------|----------------|
| Code standards | Linting errors | 0 errors |
| Type safety | TypeScript/Python types | 100% coverage |
| Error handling | Exception handling | All paths covered |
| Logging | Key events logged | Critical paths logged |
| Code complexity | Cyclomatic complexity | <15 per function |

**Auto-Run Commands:**
```bash
npm run lint || pylint src/
tsc --noEmit || mypy src/
complexity-report src/
```

**Gate Actions:**
- ✅ PASS → Proceed to Quality Check Phase
- ⚠️ WARN → Fix warnings before review
- ❌ FAIL → Block, must fix errors

## Coding Standards

- Use 2-space indentation for all source files
- Write meaningful variable and function names
- Keep functions small and focused (max 50 lines)
- Use early returns to reduce nesting
- Comment complex logic, not obvious code

## TypeScript/JavaScript Standards

- Prefer `const` over `let`, avoid `var`
- Use arrow functions for callbacks
- Use template literals for string interpolation
- Destructure objects and arrays when appropriate
- Use async/await over Promise chains

## Python Standards

- Follow PEP 8 style guide
- Use type hints for function signatures
- Use f-strings for string formatting
- Keep functions under 30 lines when possible

## Error Handling Standards

- Always handle errors gracefully
- Use specific error types
- Log errors with context
- Don't swallow exceptions silently

## Code Organization Standards

- One component/module per file
- Group related functions together
- Keep imports organized (external → internal → relative)
- Export only what's needed

## Workflow Integration

### Feature Launch Workflow - Phase 2
**Triggered by:** Architecture Gate PASS

**Parallel Execution:**
```
┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐
│ Developer-1     │  │ Developer-2     │  │ Developer-3  │
│ Backend API     │  │ Frontend UI     │  │ Database     │
└─────────────────┘  └─────────────────┘  └──────────────┘
```

### Bug Fix Workflow - Phase 1 & 2
**Triggered by:** User request "Fix bug: [description]" OR Heartbeat alert

**Execution:**
```
Phase 1: Triage (Developer identifies cause)
Phase 2: Fix & Test (Developer implements fix)
```

**Quality Gate Required:**
- Implementation Gate must PASS before Phase 3 (Review) starts

## References

- See @SUB_AGENT_CONFIG.md for spawn patterns
- See @WORKFLOW_AUTOMATION.md for workflow definitions
- See @QUALITY_GATES.md for gate thresholds
- See @SOFTWARE_ENGINEERING_TEAM.md for team configuration

---
*Jeni - Developer Agent 🦞*