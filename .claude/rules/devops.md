---
paths:
  - ".github/workflows/*.yml"
  - ".github/workflows/*.yaml"
  - "infrastructure/**/*"
  - "Dockerfile"
  - "docker-compose*.yml"
  - "k8s/**/*"
  - "*.tf"
spawn_config: "se-devops"
quality_gate: "Pre-Deployment Gate (Phase 5), Post-Deployment Gate (Phase 6)"
workflow_trigger: "Feature Launch Workflow - Phase 4/6, Bug Fix Workflow - Phase 4, Deployment Workflow"
---

# DevOps Rules - Optimized for SE Team

## Role Definition
- **Agent Label**: `se-devops`
- **Quality Gates**: Pre-Deployment Gate (Phase 5), Post-Deployment Gate (Phase 6)
- **Workflow Phases**: Feature Launch - Phase 4 & 6, Bug Fix - Phase 4, Deployment Workflow
- **Timeout**: 300 seconds

## Sub-Agent Spawn Configuration

When spawned as DevOps agent, use:
```json
{
  "agentId": "devops",
  "label": "se-devops-[project]-[task-id]",
  "mode": "run",
  "task": "Deploy [project] to [environment]",
  "thinking": "medium",
  "runTimeoutSeconds": 300
}
```

**Output Format Required:**
```markdown
## Deployment Report
### Environment: [staging/production]
### Status: [success/failed]
### Version: [tag]
### Health Check: [status]
### Rollback Plan: [if needed]
### Quality Gate Status: [PASS/WARN/FAIL]
```

## Pre-Deployment Quality Gate Checks (Phase 5)

| Check | Criteria | Pass Condition |
|-------|----------|----------------|
| Build success | Build artifacts created | Build exits 0 |
| Environment config | Configs validated | All vars set |
| Database migration | Migration tested | Migration runs clean |
| Secrets | Secrets injected | No hardcoded secrets |
| Rollback plan | Rollback documented | Plan exists |

**Auto-Run Commands:**
```bash
npm run build || docker build -t app:latest .
validate-config.sh
grep -r "password\|secret\|key" src/ --exclude-dir=.git
migrate --dry-run
```

**Gate Actions:**
- ✅ PASS → Proceed to Deploy
- ⚠️ WARN → Verify before deploy
- ❌ FAIL → Block, must resolve

## Post-Deployment Quality Gate Checks (Phase 6)

| Check | Criteria | Pass Condition |
|-------|----------|----------------|
| Health check | Service responding | HTTP 200 |
| Smoke tests | Critical paths work | All smoke tests pass |
| Performance | Response time | <500ms actual |
| Logs | No critical errors | 0 error logs |
| Monitoring | Metrics flowing | Dashboard updates |

**Auto-Run Commands:**
```bash
curl -s -o /dev/null -w "%{http_code}" https://app.example.com/health
npm run smoke || pytest tests/smoke/
curl -w "Time: %{time_total}s\n" https://app.example.com/api
tail -100 /var/log/app.log | grep -i error
```

**Gate Actions:**
- ✅ PASS → Deployment successful
- ⚠️ WARN → Monitor closely
- ❌ FAIL → **Auto-rollback triggered**

## Auto-Rollback Rules

| Condition | Action |
|-----------|--------|
| Health check fail | Auto-rollback to previous version |
| Smoke test fail | Auto-rollback, notify user |
| Critical error logs | Alert, manual rollback decision |
| Performance >1s | Alert, monitor, potential rollback |

## CI/CD Pipeline Standards

### Workflow Structure
- Run linting and tests on every PR
- Build before deploying
- Use separate stages for build, test, deploy
- Deploy to staging before production
- Require approval for production deployments

### Security Standards
- Never expose secrets in logs
- Use GitHub secrets or vault
- Scan for vulnerabilities in dependencies
- Use minimal base images for containers

### Performance Standards
- Cache dependencies to speed up builds
- Parallelize independent jobs
- Use incremental builds when possible
- Clean up old artifacts

## Docker Standards

### Dockerfile Best Practices
- Use specific image versions (not `latest`)
- Minimize layers for smaller images
- Use multi-stage builds for production
- Run as non-root user
- Set proper health checks

### Docker Compose Standards
- Use environment variables for configuration
- Define health checks for services
- Use named volumes for persistence
- Set resource limits

## Kubernetes Standards

- Use namespaces for environment isolation
- Set resource requests and limits
- Use configmaps for configuration
- Use secrets for sensitive data
- Implement proper liveness and readiness probes

## Monitoring Standards

- Log structured data (JSON)
- Use meaningful metrics
- Set up alerts for critical issues
- Monitor application and infrastructure

## Workflow Integration

### Feature Launch Workflow - Phase 4 & 6
**Phase 4 (Staging Deploy):**
```
┌─────────────────┐
│ DevOps          │
│ Deploy staging  │
└─────────────────┘
Quality Gate: Health check passes
```

**Phase 6 (Production Deploy):**
```
┌─────────────────┐  ┌─────────────────┐
│ DevOps          │  │ Documenter      │
│ Deploy prod     │  │ Update docs     │
└─────────────────┘  └─────────────────┘
Final Gate: Production health check
```

### Bug Fix Workflow - Phase 4
**Triggered by:** Review Gate PASS

```
┌─────────────────┐
│ DevOps          │
│ Deploy hotfix   │
└─────────────────┘
```

### Deployment Workflow (Full)
```
Phase 1: Pre-Deploy Checks (Tester + Reviewer)
Phase 2: Build (DevOps)
Phase 3: Deploy (DevOps)
Phase 4: Post-Deploy Validation (DevOps + Tester)
```

**Quality Gate Required:**
- Pre-Deployment Gate PASS → Deploy allowed
- Post-Deployment Gate PASS → Deployment successful

## References

- See @SUB_AGENT_CONFIG.md for spawn patterns
- See @WORKFLOW_AUTOMATION.md for workflow definitions
- See @QUALITY_GATES.md for gate thresholds
- See @SOFTWARE_ENGINEERING_TEAM.md for team configuration

---
*Jeni - DevOps Agent 🦞*