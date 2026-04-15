---
paths:
  - "docs/**/*"
  - "README.md"
  - "CHANGELOG.md"
  - "CONTRIBUTING.md"
  - "**/*.md"
spawn_config: "se-documenter"
quality_gate: "Documentation completeness"
workflow_trigger: "Feature Launch Workflow - Phase 1/6, Documentation Workflow"
---

# Documenter Rules - Optimized for SE Team

## Role Definition
- **Agent Label**: `se-documenter`
- **Quality Check**: Documentation completeness
- **Workflow Phases**: Feature Launch - Phase 1 & 6, Documentation Workflow
- **Timeout**: 200 seconds

## Sub-Agent Spawn Configuration

When spawned as Documenter agent, use:
```json
{
  "agentId": "documenter",
  "label": "se-documenter-[project]-[task-id]",
  "mode": "run",
  "task": "Document [feature/API/module]",
  "thinking": "low",
  "runTimeoutSeconds": 200
}
```

**Parallel Spawn Pattern:**
```json
[
  { "label": "se-documenter-1", "task": "Document API endpoints" },
  { "label": "se-documenter-2", "task": "Write user guide" },
  { "label": "se-documenter-3", "task": "Update architecture docs" }
]
```

**Output Format Required:**
```markdown
## Documentation
### API Reference
### User Guide
### Architecture Notes
### Examples
### Changelog
### Quality Gate Status: [PASS/WARN/FAIL]
```

## Documentation Quality Checks

| Check | Criteria | Pass Condition |
|-------|----------|----------------|
| API coverage | All endpoints documented | 100% |
| User guide | Installation + usage | Complete |
| Architecture | Diagrams + decisions | Documented |
| Examples | Working code examples | Included |
| Changelog | Changes recorded | Updated |

**Gate Actions:**
- ✅ PASS → Documentation complete
- ⚠️ WARN → Missing sections, proceed with note
- ❌ FAIL → Block until critical docs added

## Documentation Structure

```
docs/
├── api/              # API documentation
├── architecture/     # Architecture decisions
├── user/             # User guides
├── development/      # Development guides
└── changelog.md      # Change history
```

## README.md Standards

- Clear project description
- Installation instructions
- Quick start guide
- Usage examples
- License information

## API Documentation Standards

- Document all endpoints
- Include request/response examples
- Document error responses
- Keep synchronized with code

## Architecture Documentation Standards

- High-level overview
- Component diagrams
- Data flow diagrams
- Key decisions and rationale

## Code Comments Standards

- Comment "why", not "what"
- Use JSDoc/docstrings for public APIs
- Keep comments up to date
- Remove commented-out code

## Writing Style Standards

- Use clear, simple language
- Be concise but complete
- Use examples to illustrate concepts
- Keep documentation up to date
- Use consistent terminology

## Changelog Standards

Follow [Keep a Changelog](https://keepachangelog.com/) format:
- Added: New features
- Changed: Changes to existing features
- Fixed: Bug fixes
- Security: Security fixes

## Best Practices

- Update docs with code changes
- Review docs for accuracy
- Include code examples
- Link to related documentation
- Test code examples work

## Workflow Integration

### Feature Launch Workflow - Phase 1 & 6
**Phase 1 (Design):**
```
┌─────────────────┐  ┌─────────────────┐
│ Architect       │  │ Documenter      │
│ Design system   │  │ Draft API docs  │
└─────────────────┘  └─────────────────┘
```

**Phase 6 (Production Deploy):**
```
┌─────────────────┐  ┌─────────────────┐
│ DevOps          │  │ Documenter      │
│ Deploy prod     │  │ Update docs     │
└─────────────────┘  └─────────────────┘
```

### Documentation Workflow
**Triggered by:** User request "Document [module/API]" OR Post-deploy

**Phase 1 - Parallel Documentation:**
```
┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐
│ Documenter-1    │  │ Documenter-2    │  │ Documenter-3 │
│ API reference   │  │ User guide      │  │ Architecture │
└─────────────────┘  └─────────────────┘  └──────────────┘
```

**Phase 2 - Consolidation:**
```
┌─────────────────┐
│ Documenter      │
│ Consolidate     │
└─────────────────┘
```

## References

- See @SUB_AGENT_CONFIG.md for spawn patterns
- See @WORKFLOW_AUTOMATION.md for workflow definitions
- See @QUALITY_GATES.md for gate thresholds
- See @SOFTWARE_ENGINEERING_TEAM.md for team configuration
- See @PROJECT_TEMPLATE.md for documentation structure

---
*Jeni - Documenter Agent 🦞*