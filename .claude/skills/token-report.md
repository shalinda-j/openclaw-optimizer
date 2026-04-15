---
name: token-report
description: Generate token savings report with cost analysis. Use at session end to track efficiency.
---

# Token Report Skill

Generates comprehensive token savings report with cost analysis and optimization metrics.

## Report Structure

### Session Summary

```
╔══════════════════════════════════════════════════════════════╗
║              TOKEN EFFICIENCY REPORT                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Session Duration: X minutes                                 ║
║  Requests Processed: X                                       ║
║                                                              ║
║  ────────────────────────────────────────────────────────── ║
║                                                              ║
║  TOKEN USAGE                                                 ║
║  ────────────────────────────────────────────────────────── ║
║                                                              ║
║  Baseline (unoptimized):     80,000 tokens/request           ║
║  Optimized (actual):         X tokens/request                ║
║                                                              ║
║  Tokens Saved:               X tokens                        ║
║  Savings Percentage:         X%                              ║
║                                                              ║
║  ────────────────────────────────────────────────────────── ║
║                                                              ║
║  COST ANALYSIS                                               ║
║  ────────────────────────────────────────────────────────── ║
║                                                              ║
║  Baseline Cost:              $X.XX                           ║
║  Actual Cost:                $X.XX                           ║
║  Cost Saved:                 $X.XX                           ║
║                                                              ║
║  ────────────────────────────────────────────────────────── ║
║                                                              ║
║  CLASSIFICATION DISTRIBUTION                                 ║
║  ────────────────────────────────────────────────────────── ║
║                                                              ║
║  simple_query:   X requests (X%)                            ║
║  code_task:      X requests (X%)                            ║
║  research_task:  X requests (X%)                            ║
║  complex_task:   X requests (X%)                            ║
║                                                              ║
║  ────────────────────────────────────────────────────────── ║
║                                                              ║
║  SKILL LOAD STATS                                            ║
║  ────────────────────────────────────────────────────────── ║
║                                                              ║
║  Cache Hits:     X (X%)                                      ║
║  Cache Misses:   X (X%)                                      ║
║  Avg Load Time:  X ms                                        ║
║                                                              ║
║  ────────────────────────────────────────────────────────── ║
║                                                              ║
║  PROJECTION                                                  ║
║  ────────────────────────────────────────────────────────── ║
║                                                              ║
║  Daily Savings (100 req):    $X.XX                           ║
║  Monthly Savings:            $X.XX                           ║
║  Annual Savings:             $X.XX                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Metrics Tracked

### Token Metrics

| Metric | Description |
|--------|-------------|
| Total requests | Number of requests processed |
| Avg tokens/request | Average token usage per request |
| Total tokens saved | Cumulative savings vs baseline |
| Savings % | Percentage reduction vs 80K baseline |

### Cost Metrics

| Metric | Description |
|--------|-------------|
| Baseline cost | Cost at 80K tokens/request |
| Actual cost | Cost with optimization |
| Cost saved | Money saved per session |
| Projected savings | Daily/monthly/yearly projections |

### Classification Metrics

| Intent | Count | Percentage |
|--------|-------|------------|
| simple_query | - | - |
| code_task | - | - |
| research_task | - | - |
| complex_task | - | - |

### Skill Metrics

| Metric | Description |
|--------|-------------|
| Cache hit rate | LRU cache efficiency |
| Load time | Avg skill load time |
| Skills loaded | Skills loaded this session |

## Cost Calculation

### Pricing

| Type | Price/1K tokens |
|------|-----------------|
| Input | $0.003 |
| Output | $0.015 |

### Formula

```
Cost = (input_tokens/1000 × $0.003) + (output_tokens/1000 × $0.015)

Assume 70% input, 30% output split.
```

### Baseline vs Optimized

| Scenario | Tokens | Cost |
|----------|--------|------|
| Baseline | 80,000 | $0.50 |
| Optimized simple | 5,000 | $0.03 |
| Optimized code | 15,000 | $0.10 |
| Optimized research | 25,000 | $0.17 |
| Optimized complex | 40,000 | $0.26 |

## Usage

### Session End Report

```
> /token-report

[Generate report for current session]
```

### Weekly Report

```
> /token-report --weekly

[Aggregate reports for past 7 days]
```

### Monthly Report

```
> /token-report --monthly

[Aggregate reports for past 30 days]
```

## Integration with Python Optimizer

```bash
# Generate report from optimizer
python optimization/optimizer.py --report
```

## Saving Reports

Reports are saved to:

```
.claude/reports/
├── daily/
│   ├── 2026-04-15.json
│   └── 2026-04-16.json
└── weekly/
    └── week-16-2026.json
```

## Dashboard Integration

For real-time monitoring, see Phase 6 implementation:

```
optimization/monitoring/
├── dashboard.py
├── collector.py
└── alerts.py
```

## Recommendations

Based on report:

1. **High simple_query ratio**: Good! Low cost per request
2. **High complex_task ratio**: Consider splitting tasks
3. **Low cache hit rate**: Clear cache, warm patterns
4. **Cost exceeding budget**: Reduce task complexity

## Targets

| Metric | Target | Alert if |
|--------|--------|----------|
| Avg tokens/request | < 20,000 | > 30,000 |
| Savings % | > 70% | < 50% |
| Cache hit rate | > 60% | < 40% |
| Daily cost | < $5 | > $10 |

---

*Created by Jeni - Algorithm Optimization System*