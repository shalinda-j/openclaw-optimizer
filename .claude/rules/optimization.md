---
description: Token optimization rules for Claude Code context management
globs: ["**/*"]
---

# Context Optimization Rules

Apply these rules to optimize token usage in every session.

## Memory Rules

### CLAUDE.md Limits
- **Target**: < 200 lines per CLAUDE.md file
- **Import**: Use `@path` for large content, don't inline
- **Comments**: Use `<!-- comment -->` for maintainer notes (stripped from context)

### Rule Organization
- Use `.claude/rules/*.md` for file-specific instructions
- Scope rules with `globs: ["src/**/*.ts"]`
- Don't duplicate instructions across files

### Auto Memory
- Enable auto memory for session learnings
- Limit to 200 lines
- Review weekly for relevance

## Skill Rules

### Tier System
- **Hot skills**: Always loaded (browser-agent, websearch)
- **Warm skills**: LRU cached 5 min (github, cursor-agent)
- **Cold skills**: Load on demand only

### Loading Strategy
- Use `/classify` before loading skills
- Only load skills needed for current task
- Run `/compact` after task completion

### Cache Management
- Clear cache between unrelated tasks
- Pre-fetch common patterns on startup
- Monitor hit rate with `/skills-load --stats`

## Budget Rules

### Budget Tiers
- simple_query: 5,000 tokens
- code_task: 15,000 tokens
- research_task: 25,000 tokens
- complex_task: 40,000 tokens

### Enforcement
- Run `/budget` before starting task
- Alert if > 70% budget used
- Must `/compact` if > 90%

### Cost Tracking
- Track cost per request
- Daily limit: $10
- Monthly limit: $150

## Workflow Rules

### Session Start
```
1. Run /optimize to check context
2. Run /budget to set limits
3. Classify requests with /classify
4. Load only needed skills
```

### During Task
```
1. Monitor token usage
2. Use /compact if needed
3. Avoid loading unnecessary files
```

### Session End
```
1. Run /compact to free context
2. Run /token-report for metrics
3. Archive conversation if completed
```

## Token Efficiency Rules

### File Reading
- Read only needed files
- Use `offset` and `limit` for large files
- Don't read entire codebase

### Tool Usage
- Minimize tool call overhead
- Batch related operations
- Use streaming for large outputs

### Response Generation
- Keep responses concise
- Use bullet lists over paragraphs
- Avoid redundant explanations

## Prohibited Actions

- ❌ Loading all skills at session start
- ❌ Reading entire CLAUDE.md + all rules every message
- ❌ Importing large files without need
- ❌ Keeping completed conversations in context

## Recommended Actions

- ✅ Use `/classify` to route requests
- ✅ Use `/skills-load` for lazy loading
- ✅ Use `/compact` to free tokens
- ✅ Use `/budget` to enforce limits
- ✅ Run `/context-audit` weekly

## Integration Points

| Rule | Skill | Action |
|------|-------|--------|
| Memory limits | /optimize | Check CLAUDE.md size |
| Skill loading | /skills-load | Load on demand |
| Budget enforcement | /budget | Track usage |
| Context audit | /context-audit | Weekly maintenance |
| Savings tracking | /token-report | End of session |

---

*Created by Jeni - Algorithm Optimization System*