---
name: context-audit
description: Audit current context usage and identify optimization opportunities. Use for weekly maintenance.
---

# Context Audit Skill

Performs comprehensive audit of context usage and identifies optimization opportunities.

## Audit Checklist

### 1. Memory Files Audit

| File | Lines | Tokens | Status |
|------|-------|--------|--------|
| CLAUDE.md | - | - | Check |
| CLAUDE.local.md | - | - | Check |
| .claude/rules/*.md | - | - | Check |
| Auto memory | - | - | Check |

**Issues to check**:
- Duplicate instructions across files
- Outdated rules no longer relevant
- Large imports consuming tokens
- HTML comments not stripped

### 2. Skills Audit

| Tier | Skills | Tokens | Status |
|------|--------|--------|--------|
| Hot | - | - | Pre-loaded |
| Warm | - | - | Cached |
| Cold | - | - | On-demand |

**Issues to check**:
- Unused skills in context
- Skills loaded but not invoked
- Cache misses (low hit rate)

### 3. Conversation Audit

| Item | Count | Tokens | Status |
|------|-------|--------|--------|
| User messages | - | - | - |
| Assistant messages | - | - | - |
| Tool calls | - | - | - |

**Issues to check**:
- Old messages consuming tokens
- Redundant tool results
- Large outputs not summarized

### 4. Import Audit

| Import | Path | Tokens | Needed? |
|--------|------|--------|---------|
| @README | - | - | Check |
| @package.json | - | - | Check |
| Other imports | - | - | Check |

**Issues to check**:
- Imports loading unnecessary content
- Large files imported wholesale
- Missing file-specific imports

## Audit Workflow

```
User: /context-audit
      │
      ▼
┌─────────────────┐
│ Memory Audit    │ → CLAUDE.md + rules
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Skills Audit    │ → Loaded skills
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Conversation    │ → Message history
│ Audit           │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Import Audit    │ → @imports
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Generate Report │
└─────────────────┘
```

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║              CONTEXT AUDIT REPORT                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  MEMORY AUDIT                                                ║
║  ├─ CLAUDE.md:      X lines (Y tokens) ── [OK/OPTIMIZE]     ║
║  ├─ Rules:          N files (Y tokens) ── [OK/OPTIMIZE]     ║
║  └─ Auto Memory:    X lines (Y tokens) ── [OK]              ║
║                                                              ║
║  SKILLS AUDIT                                                ║
║  ├─ Hot:            N skills (Y tokens) ── [OK]             ║
║  ├─ Warm:           N skills (Y tokens) ── [OK/CLEAR CACHE] ║
║  └─ Cold:           N skills (0 tokens)  ── [OK]            ║
║                                                              ║
║  CONVERSATION AUDIT                                          ║
║  ├─ Messages:       X messages (Y tokens)                   ║
║  ├─ Tool Calls:     X calls (Y tokens)                      ║
║  └─ Status:         [OK/COMPACT]                            ║
║                                                              ║
║  IMPORT AUDIT                                                ║
║  ├─ Imports:        N files (Y tokens)                      ║
║  └─ Status:         [OK/REDUCE]                             ║
║                                                              ║
║  ────────────────────────────────────────────────────────── ║
║                                                              ║
║  TOTAL CONTEXT: X tokens                                     ║
║  WINDOW LIMIT: 200,000 tokens                                ║
║  USAGE:        Y%                                            ║
║                                                              ║
║  RECOMMENDATIONS:                                            ║
║  1. [action]                                                 ║
║  2. [action]                                                 ║
║                                                              ║
║  POTENTIAL SAVINGS: X tokens                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Recommendations

Based on audit findings:

### Memory Optimizations
- Remove duplicates from CLAUDE.md
- Split large files into rules/
- Use path-scoped rules for file-specific instructions
- Add HTML comments for maintainer notes

### Skills Optimizations
- Clear cache after task completion
- Use lazy loading for cold skills
- Check skill usage with `/skills-load --stats`

### Conversation Optimizations
- Run `/compact` to summarize old messages
- Archive completed conversations
- Start fresh for new unrelated tasks

### Import Optimizations
- Import only relevant sections
- Use path-scoped imports
- Remove unused imports

## Weekly Maintenance

Run `/context-audit` weekly:

```bash
# Weekly routine
claude
> /context-audit
> /optimize
> /compact
> /token-report
```

## Integration

Works with:
- `/optimize` - Apply recommendations
- `/compact` - Free up tokens
- `/budget` - Budget enforcement
- `/token-report` - Track savings

---

*Created by Jeni - Algorithm Optimization System*