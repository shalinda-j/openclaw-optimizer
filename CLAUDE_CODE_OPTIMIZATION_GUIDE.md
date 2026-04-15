# Claude Code + Algorithm Optimization Integration Guide

## Overview

This guide shows how to apply the token-efficient algorithm optimization system to Claude Code's context management using "/" commands (skills).

---

## 📦 Claude Code Installation

### Option 1: Native Install (Recommended)

```powershell
# Windows PowerShell
irm https://claude.ai/install.ps1 | iex

# Or using WinGet
winget install Anthropic.ClaudeCode
```

### Option 2: npx (Alternative)

```bash
# Using npx (requires Node.js)
npx claude-code

# Or install globally
npm install -g @anthropic/claude-code
```

---

## 🔧 "/" Commands for Context Management

Claude Code uses **slash commands** (skills) for workflows. Here's how to create custom optimization commands:

### Built-in Commands

| Command | Purpose |
|---------|---------|
| `/init` | Generate CLAUDE.md automatically |
| `/compact` | Compress context, free up tokens |
| `/memory` | View/edit auto memory |
| `/cost` | Show token usage and cost |
| `/status` | Session status |

### Custom Optimization Commands

Create these in `.claude/skills/`:

```
.claude/skills/
├── optimize.md          # /optimize - Analyze and optimize context
├── budget.md            # /budget - Token budget check
├── classify.md          # /classify - Classify request type
├── skills-load.md       # /skills-load - Lazy load skills
├── context-audit.md     # /context-audit - Audit context usage
└── token-report.md      # /token-report - Generate savings report
```

---

## 📁 Creating Optimization Skills

### 1. `/optimize` Skill

```markdown
---
name: optimize
description: Analyze current context and optimize for token efficiency
---

# Context Optimizer

Analyze the current context window and optimize:

1. **Memory Check**: Review CLAUDE.md and .claude/rules/ for redundancy
2. **Skill Audit**: Identify unused skills loaded in context
3. **Token Estimate**: Calculate current token usage
4. **Recommendations**: Suggest optimizations

## Actions

- Run `/compact` if context > 50%
- Remove redundant rules
- Suggest splitting large CLAUDE.md files
- Enable lazy skill loading
```

### 2. `/budget` Skill

```markdown
---
name: budget
description: Check token budget and enforce limits
---

# Token Budget Check

Current Budget Status:

| Tier | Limit | Current | Status |
|------|-------|---------|--------|
| System | 2,000 | - | - |
| Memory | 5,000 | - | - |
| Skills | 10,000 | - | - |
| Response | 13,000 | - | - |

## Budget Enforcement

1. If over budget → suggest `/compact`
2. Identify high-token items
3. Recommend selective memory loading
```

### 3. `/classify` Skill

```markdown
---
name: classify
description: Classify request type and route to optimal path
---

# Request Classifier

Classify the next request:

**Intent Types:**
- `simple_query` → 5K budget (quick questions)
- `code_task` → 15K budget (coding, debugging)
- `research_task` → 25K budget (research, analysis)
- `complex_task` → 40K budget (multi-step workflows)

**Actions:**
1. Read user request
2. Classify intent + domain + priority
3. Select budget tier
4. Load only needed skills
5. Set response limit
```

---

## 🗂️ Context Optimization Structure

### Directory Layout

```
.claude/
├── CLAUDE.md              # Project instructions (keep < 200 lines)
├── rules/
│   ├── typescript.md      # TypeScript rules (scoped)
│   ├── react.md           # React rules (scoped)
│   ├── testing.md         # Testing rules (scoped)
│   └── optimization.md    # Optimization rules
├── skills/
│   ├── optimize.md        # /optimize command
│   ├── budget.md          # /budget command
│   ├── classify.md        # /classify command
│   ├── skills-load.md     # /skills-load command
│   ├── context-audit.md   # /context-audit command
│   └── token-report.md    # /token-report command
└── settings.json          # Claude Code settings
```

### settings.json

```json
{
  "permissions": {
    "allow": ["Read", "Edit", "Bash(git *)", "Bash(npm *)"],
    "deny": []
  },
  "contextOptimization": {
    "maxMemoryLines": 200,
    "lazyLoadSkills": true,
    "budgetEnforcement": true,
    "defaultBudget": 15000
  },
  "autoMemory": {
    "enabled": true,
    "maxLines": 200
  }
}
```

---

## 📊 CLAUDE.md Optimization Template

```markdown
# Project Instructions (Optimized)

> Target: < 200 lines for token efficiency

## Build Commands
- Build: `npm run build`
- Test: `npm test`
- Dev: `npm run dev`

## Architecture
- Components: `src/components/`
- API: `src/api/`
- Utils: `src/utils/`

## Coding Standards
- TypeScript strict mode
- 2-space indentation
- Prefer async/await

## Context Optimization Rules
@.claude/rules/optimization.md

## Token Budget
- Simple queries: 5K
- Code tasks: 15K
- Research: 25K
- Complex: 40K

<!-- 
  Hidden notes for maintainers (stripped from context):
  Update this file when adding new patterns.
  Run /optimize weekly to audit context.
-->
```

---

## 🔄 Workflow Integration

### Before Starting a Session

```bash
# 1. Start Claude Code
claude

# 2. Run optimization check
> /optimize

# 3. Check budget status
> /budget

# 4. Initialize if needed
> /init
```

### During a Session

```bash
# Classify request before executing
> /classify "Fix the bug in auth module"

# Result:
# Intent: code_task
# Budget: 15K tokens
# Skills: cursor-agent, github
# Memory: needed

# Load only needed skills
> /skills-load cursor-agent github

# Execute the task
> Fix the bug in auth module
```

### After Completion

```bash
# Compress context
> /compact

# Generate token report
> /token-report

# View savings
> /cost
```

---

## 📈 Expected Savings

| Metric | Before | After | Savings |
|--------|--------|-------|---------|
| Context loaded | Full | Selective | 70% |
| Skills loaded | All | On-demand | 90% |
| Avg tokens | 80K | 15K | 81% |
| Cost/request | $0.50 | $0.10 | 80% |

---

## 🛠️ Implementation Steps

### Step 1: Create Skills Directory

```bash
mkdir .claude
mkdir .claude/rules
mkdir .claude/skills
```

### Step 2: Create CLAUDE.md

```bash
# Generate automatically
claude
> /init

# Or create manually
touch .claude/CLAUDE.md
```

### Step 3: Create Optimization Skills

Create each skill file in `.claude/skills/`:

```bash
# Create optimize skill
cat > .claude/skills/optimize.md << 'EOF'
---
name: optimize
description: Analyze and optimize context for token efficiency
---
# Context Optimizer
[content...]
EOF
```

### Step 4: Configure Settings

```bash
cat > .claude/settings.json << 'EOF'
{
  "contextOptimization": {
    "lazyLoadSkills": true,
    "budgetEnforcement": true
  }
}
EOF
```

### Step 5: Test

```bash
claude
> /optimize
> /budget
> /classify "Test request"
```

---

## 🔗 Integration with Our Optimizer

Link the Python optimizer we created:

### Create Integration Skill

```markdown
---
name: run-optimizer
description: Run Python optimizer for detailed analysis
---

# Algorithm Optimizer Integration

Run the Python optimization module:

```bash
python optimization/optimizer.py --request "<request>"
```

Outputs:
- Classification
- Budget allocation
- Skill recommendations
- Cost estimate
- Savings calculation
```

### Usage

```bash
> /run-optimizer "Fix the bug in authentication"

# Output:
# Intent: code_task
# Budget: 15,000 tokens
# Skills: cursor-agent, github
# Cost: $0.0990
# Savings: 81.2%
```

---

## 📝 Quick Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║           CLAUDE CODE OPTIMIZATION COMMANDS                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                                ║
║  /optimize     - Analyze and optimize context                 ║
║  /budget       - Check token budget status                    ║
║  /classify     - Classify request type                        ║
║  /skills-load  - Lazy load needed skills                      ║
║  /context-audit- Audit context usage                          ║
║  /token-report - Generate savings report                      ║
║  /compact      - Compress context (built-in)                  ║
║  /cost         - Show cost (built-in)                         ║
║                                                                ║
║  WORKFLOW:                                                     ║
║  1. /optimize → Check context                                  ║
║  2. /classify <request> → Route                                ║
║  3. /skills-load <skills> → Load                               ║
║  4. Execute task                                               ║
║  5. /compact → Free context                                    ║
║  6. /token-report → Track savings                              ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🚀 One-Line Setup

```bash
# Quick setup script
claude && \
mkdir -p .claude/rules .claude/skills && \
echo '{"contextOptimization":{"lazyLoadSkills":true}}' > .claude/settings.json && \
claude "/init"
```

---

## 📚 Related Files

- `optimization/optimizer.py` - Main Python optimizer
- `optimization/classifier/router.py` - Classification logic
- `optimization/skills/router.py` - Skill loading logic
- `optimization/budget/tiers.json` - Budget definitions

---

*Created: 2026-04-15*
*Author: Jeni (AGI Agent)*