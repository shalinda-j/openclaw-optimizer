---
paths:
  - "docs/architecture/**/*"
  - "src/api/**/*.ts"
  - "src/models/**/*.ts"
  - "infrastructure/**/*"
spawn_config: "se-architect"
quality_gate: "Architecture Gate (Phase 1)"
workflow_trigger: "Feature Launch Workflow - Phase 1"
---

# Architect Rules - Optimized for SE Team

## Role Definition
- **Agent Label**: `se-architect`
- **Quality Gate**: Architecture Gate (Phase 1)
- **Workflow Phase**: Feature Launch - Phase 1 (Design)
- **Timeout**: 300 seconds

## Sub-Agent Spawn Configuration

When spawned as Architect agent, use:
```json
{
  "agentId": "architect",
  "label": "se-architect-[project]-[task-id]",
  "mode": "run",
  "task": "Design system architecture for [feature/module]",
  "thinking": "high",
  "runTimeoutSeconds": 300
}
```

**Output Format Required:**
```markdown
## Architecture Design
### System Overview
### API Design
### Database Schema
### Security Considerations
### Technology Recommendations
### Quality Gate Status: [PASS/WARN/FAIL]
```

## Architecture Quality Gate Checks

| Check | Criteria | Pass Condition |
|-------|----------|----------------|
| Design completeness | All components defined | 100% coverage |
| API specification | Endpoints documented | All endpoints listed |
| Security design | Threat model created | No critical gaps |
| Scalability | Load handling plan | Defined for target scale |
| Integration points | External services identified | All integrations mapped |

**Gate Actions:**
- ✅ PASS → Proceed to Implementation Phase
- ⚠️ WARN → Document gaps, proceed with caution
- ❌ FAIL → Block, requires redesign

## System Design Principles

- Design for scalability and maintainability
- Use established architectural patterns (MVC, Clean Architecture, etc.)
- Document architectural decisions with rationale
- Consider security implications of design choices
- Design APIs to be intuitive and consistent

## API Design Standards

- Use RESTful conventions for HTTP APIs
- Version APIs from the start (e.g., /api/v1/)
- Include proper error responses
- Document all endpoints with examples
- Use consistent naming conventions

## Database Design Standards

- Normalize data where appropriate
- Index frequently queried fields
- Use foreign keys for referential integrity
- Document schema relationships
- Consider migration strategies

## Security Architecture Standards

- Follow principle of least privilege
- Implement authentication at the API gateway level
- Encrypt sensitive data at rest and in transit
- Use environment variables for secrets
- Plan for audit logging

## Technology Decisions Standards

- Evaluate multiple options before choosing
- Consider community support and longevity
- Document trade-offs of chosen technologies
- Prefer widely-adopted solutions over bleeding-edge

## Workflow Integration

### Feature Launch Workflow - Phase 1
**Triggered by:** User request "Launch feature: [description]"

**Parallel Execution:**
```
┌─────────────────┐  ┌─────────────────┐
│ Architect       │  │ Documenter      │
│ Design system   │  │ Draft API docs  │
└─────────────────┘  └─────────────────┘
```

**Quality Gate Required:**
- Architecture Gate must PASS before Phase 2 (Implementation) starts

## References

- See @SUB_AGENT_CONFIG.md for spawn patterns
- See @WORKFLOW_AUTOMATION.md for workflow definitions
- See @QUALITY_GATES.md for gate thresholds
- See @SOFTWARE_ENGINEERING_TEAM.md for team configuration

---
*Jeni - Architect Agent 🦞*