---
name: skills-load
description: Lazy load only needed skills for token efficiency. Use after /classify to load specific skills.
---

# Skills Loader Skill

Loads skills on-demand to minimize token usage. Skills are loaded only when needed instead of loading all at session start.

## Skill Tiers

### Hot Skills (Always Loaded)
- `autoglm-browser-agent` - Browser automation
- `autoglm-websearch` - Web search

**Cost**: ~5,000 tokens (pre-loaded)

### Warm Skills (LRU Cached)
- `github` - GitHub CLI
- `cursor-agent` - Cursor coding
- `vercel-deploy` - Deployment

**Cache**: 5 skills, 5-minute TTL

### Cold Skills (Load on Demand)
- `academic-deep-research`
- `us-stock-analysis`
- `weather`
- All other skills

**Load**: Only when requested

## Usage

### Load Specific Skills

```
/skills-load <skill1> <skill2> <skill3>
```

### Examples

```
# Load coding skills
/skills-load cursor-agent github

# Load research skills  
/skills-load autoglm-websearch academic-deep-research

# Load deployment skills
/skills-load cursor-agent github vercel-deploy
```

## Skill Token Estimates

| Skill | Tokens | Tier |
|-------|--------|------|
| browser-agent | 3,000 | hot |
| websearch | 2,000 | hot |
| github | 2,500 | warm |
| cursor-agent | 3,500 | warm |
| vercel-deploy | 2,000 | warm |
| image-recognition | 2,500 | warm |
| academic-research | 4,000 | cold |
| stock-analysis | 3,000 | cold |

## Workflow

```
User: /skills-load cursor-agent github
      │
      ▼
┌─────────────────┐
│ Check Cache     │ → Already loaded?
└─────────────────┘
      │
      ├─ HIT → Return cached
      │
      └─ MISS → Load from file
            │
            ▼
      ┌─────────────────┐
      │ Add to Cache    │ → Warm skills cached
      └─────────────────┘
            │
            ▼
      ┌─────────────────┐
      │ Update Context  │ → Skills now available
      └─────────────────┘
            │
            ▼
        Ready to use
```

## Output Format

```
📊 Skills Loaded

Skills: cursor-agent, github
Tier: warm
Cache: LRU (5 min TTL)

Token Cost: 6,000 tokens
Load Time: ~300ms

Status: ✅ Ready to use
```

## Pre-fetch Patterns

Based on classification:

| Intent | Pre-load Skills |
|--------|-----------------|
| code_task | cursor-agent, github |
| research_task | websearch, browser-agent |
| complex_task | cursor-agent, github, vercel-deploy |

## Integration with Python Optimizer

```bash
# Get skill recommendations
python optimization/skills/router.py --intent code_task
```

## Cache Stats

Check cache performance:

```
/skills-load --stats

Cache Stats:
- Size: 3 skills
- Hits: 15
- Misses: 5
- Hit Rate: 75%
```

## Recommendations

- Use `/classify` first to get skill recommendations
- Only load skills you'll actually use
- Run `/compact` after completing task to free memory

---

*Created by Jeni - Algorithm Optimization System*