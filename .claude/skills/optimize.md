---
name: optimize
description: Analyze current context and optimize for token efficiency. Use before starting tasks to minimize token usage.
---

# Context Optimizer Skill

This skill analyzes and optimizes Claude Code's context for maximum token efficiency.

## When to Use

- Before starting a complex task
- When context feels bloated
- After loading multiple files
- Weekly maintenance check

## Optimization Actions

### 1. Memory Audit

Check CLAUDE.md and .claude/rules/ for:
- Redundant instructions (remove duplicates)
- Outdated rules (update or delete)
- Large imports (split into smaller files)
- Hidden comments (use HTML comments for maintainer notes)

**Target**: < 200 lines per CLAUDE.md file

### 2. Skill Audit

Review loaded skills:
- Which skills are currently in context?
- Which are actually needed for current task?
- Can unused skills be unloaded?

**Recommendation**: Use `/skills-load` to load only needed skills

### 3. Token Estimate

Calculate current token usage:
- System prompt: ~2,000 tokens
- Memory files: Count lines × ~10 tokens
- Skills loaded: Each skill ~2,000-4,000 tokens
- Conversation history: Previous messages

**Budget check**: Run `/budget` after estimate

### 4. Optimization Recommendations

Based on analysis, suggest:
- Run `/compact` if context > 50% of window
- Split large CLAUDE.md into rules/
- Remove unused skill imports
- Use lazy loading for skills
- Archive old conversation history

## Workflow

```
User: /optimize
      │
      ▼
┌─────────────────┐
│  Memory Audit   │ → Check CLAUDE.md + rules/
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  Skill Audit    │ → List loaded skills
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  Token Estimate │ → Calculate current usage
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Recommendations │ → Suggest optimizations
└─────────────────┘
      │
      ▼
  Output report
```

## Output Format

```
📊 CONTEXT OPTIMIZATION REPORT

Memory Status:
- CLAUDE.md: X lines (Y tokens)
- Rules: N files (Y tokens)
- Total Memory: Y tokens

Skills Status:
- Loaded: [list]
- Tokens: Y

Total Context: X tokens (Y% of window)

Recommendations:
1. [action]
2. [action]

Potential Savings: X tokens
```

## Integration

This skill works with:
- `/budget` - Token budget check
- `/compact` - Compress context
- `/skills-load` - Lazy load skills
- `/classify` - Route requests efficiently

---

*Created by Jeni - Algorithm Optimization System*