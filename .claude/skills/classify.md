---
name: classify
description: Classify request type and route to optimal execution path with budget allocation. Use before executing tasks to select the right budget tier.
---

# Request Classifier Skill

Classifies requests into intent types and routes to optimal execution path with token budget allocation.

## Intent Types

| Intent | Description | Budget | Model |
|--------|-------------|--------|-------|
| `simple_query` | Quick questions, status checks | 5,000 | small |
| `code_task` | Coding, debugging, refactoring | 15,000 | medium |
| `research_task` | Research, analysis, web search | 25,000 | medium |
| `complex_task` | Multi-step workflows, planning | 40,000 | large |

## Classification Criteria

### Simple Query (5K budget)
- Single question
- Status check
- Quick lookup
- No code changes
- No file edits

**Examples**: "What time is it?", "Check status", "Show config"

### Code Task (15K budget)
- Code generation
- Bug fixing
- Refactoring
- File edits
- Git operations

**Examples**: "Fix bug in auth", "Refactor utils", "Add tests"

### Research Task (25K budget)
- Web search
- Multi-source analysis
- Report generation
- Deep investigation

**Examples**: "Research AI trends", "Compare options", "Analyze market"

### Complex Task (40K budget)
- Multi-file changes
- End-to-end implementation
- Architecture planning
- Cross-skill coordination

**Examples**: "Build auth system", "Deploy feature", "Plan architecture"

## Usage

```
User: /classify "<request>"
      │
      ▼
┌─────────────────┐
│ Parse Request   │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Detect Intent   │ → Keyword matching
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Detect Domain   │ → Context awareness
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Score Priority  │ → urgent/high/medium/low
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Select Budget   │ → Based on intent
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Recommend Skills│ → Only needed skills
└─────────────────┘
      │
      ▼
  Output classification
```

## Output Format

```json
{
  "intent": "code_task",
  "domain": "software_engineering",
  "priority": "high",
  "budget": 15000,
  "skills": ["cursor-agent", "github"],
  "memory_needed": true,
  "model": "medium"
}
```

## Integration with Python Optimizer

For detailed analysis, run:

```bash
python optimization/optimizer.py --request "<request>"
```

## Workflow Example

```
> /classify "Fix the authentication bug"

Intent: code_task
Domain: software_engineering  
Priority: high
Budget: 15,000 tokens
Skills needed: cursor-agent, github
Memory: yes

Recommendation: Use /skills-load cursor-agent github
```

---

*Created by Jeni - Algorithm Optimization System*