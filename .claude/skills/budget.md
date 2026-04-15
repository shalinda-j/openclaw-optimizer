---
name: budget
description: Check token budget status and enforce limits. Use to track token usage and prevent overruns.
---

# Token Budget Skill

Monitors and enforces token budget limits for efficient context management.

## Budget Tiers

| Tier | Total | System | Memory | Skills | Response |
|------|-------|--------|--------|--------|----------|
| simple | 5,000 | 1,000 | 1,000 | 0 | 3,000 |
| code | 15,000 | 2,000 | 3,000 | 5,000 | 5,000 |
| research | 25,000 | 2,000 | 5,000 | 8,000 | 10,000 |
| complex | 40,000 | 3,000 | 8,000 | 12,000 | 17,000 |

## Budget Enforcement

### Current Session Budget

```
┌─────────────────────────────────────────┐
│        TOKEN Budget Status              │
├─────────────────────────────────────────┤
│                                         │
│  Tier: [current_tier]                   │
│  Budget: X tokens                       │
│                                         │
│  ─────────────────────────────────────  │
│  Allocation:                            │
│  ├─ System:    X tokens (X%)            │
│  ├─ Memory:    X tokens (X%)            │
│  ├─ Skills:    X tokens (X%)            │
│  └─ Response:  X tokens (X%)            │
│                                         │
│  ─────────────────────────────────────  │
│  Used:     X tokens                     │
│  Remaining: X tokens                    │
│  Status:   [OK/WARNING/OVER]            │
│                                         │
└─────────────────────────────────────────┘
```

## Alert Thresholds

| Status | Threshold | Action |
|--------|-----------|--------|
| OK | < 70% budget | Continue |
| WARNING | 70-90% budget | Consider /compact |
| OVER | > 90% budget | Must /compact or truncate |

## Overflow Handling

When budget exceeded:

1. **Compress** - Use `/compact` to summarize
2. **Truncate** - Remove oldest content
3. **Chunk** - Split into smaller pieces
4. **Reject** - Ask user to simplify request

## Cost Tracking

| Metric | Value |
|--------|-------|
| Price/1K input | $0.003 |
| Price/1K output | $0.015 |
| Current cost | $X.XX |

### Daily/Monthly Budgets

| Limit | Warning | Critical |
|-------|---------|----------|
| Daily | $8.00 | $12.00 |
| Monthly | $100 | $150 |

## Usage

```
User: /budget
      │
      ▼
┌─────────────────┐
│  Get Current    │
│  Tier           │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  Calculate      │
│  Usage          │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  Check Status   │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  Recommendations│
└─────────────────┘
```

## Recommendations

Based on status:

- **OK**: No action needed
- **WARNING**: Consider `/compact` or reduce memory
- **OVER**: Must compress or split request

## Integration

Works with:
- `/classify` - Set budget based on intent
- `/optimize` - Context audit
- `/compact` - Free up tokens

---

*Created by Jeni - Algorithm Optimization System*