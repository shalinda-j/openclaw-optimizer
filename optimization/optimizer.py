#!/usr/bin/env python3
"""
Algorithm Optimizer - Main Integration Module
Integrates classification, budgeting, and skill loading for token-efficient execution.

Author: Jeni (AGI Agent)
Created: 2026-04-15
Version: 1.0.0
"""

import json
import time
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# Import components
import sys
sys.path.insert(0, os.path.dirname(__file__))

from classifier.router import RequestRouter, ClassificationResult, IntentType, DomainType
from skills.router import SkillRouter, SkillRegistry
# Budget tiers loaded from JSON directly


@dataclass
class OptimizationResult:
    """Result of optimization analysis for a request."""
    classification: Dict
    skills: Dict
    budget: Dict
    execution_path: Dict
    estimated_tokens: int
    estimated_cost_usd: float
    cache_recommendation: str
    timestamp: str


class AlgorithmOptimizer:
    """
    Main optimizer that integrates all components for efficient request handling.
    
    Workflow:
    1. Classify request (intent, domain, priority)
    2. Determine budget allocation
    3. Select skills to load
    4. Recommend execution path
    5. Estimate costs
    """
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.dirname(__file__)
        
        # Initialize components
        self.request_router = RequestRouter()
        self.skill_registry = SkillRegistry()
        self.skill_router = SkillRouter(self.skill_registry)
        self.budget_tiers = self._load_budget_config()
        
        # Stats tracking
        self.stats = {
            "total_requests": 0,
            "tokens_saved": 0,
            "cost_saved_usd": 0,
            "classifications": {},
            "cache_hits": 0,
            "avg_tokens_per_request": 0
        }
    
    def _load_budget_config(self) -> Dict:
        """Load budget configuration."""
        budget_path = os.path.join(self.config_path, "budget", "tiers.json")
        try:
            with open(budget_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Default budget config
            return {
                "tiers": {
                    "simple": {"total_budget": 5000},
                    "code": {"total_budget": 15000},
                    "research": {"total_budget": 25000},
                    "complex": {"total_budget": 40000}
                },
                "cost_tracking": {
                    "price_per_1k_tokens": {"input": 0.003, "output": 0.015}
                }
            }
    
    def optimize(self, request: str) -> OptimizationResult:
        """
        Optimize a request for efficient execution.
        
        Args:
            request: The user request text
            
        Returns:
            OptimizationResult with all analysis details
        """
        start_time = time.time()
        
        # Step 1: Classify request
        classification = self.request_router.route_to_json(request)
        
        # Step 2: Get budget allocation
        intent = classification["intent"]
        budget_info = self._get_budget_allocation(intent)
        
        # Step 3: Select skills
        skills_info = self.skill_router.get_skills_for_request(
            intent,
            classification["domain"],
            request,
            budget_info["total"]
        )
        
        # Step 4: Calculate execution path
        execution_path = self._calculate_execution_path(
            classification,
            skills_info,
            budget_info
        )
        
        # Step 5: Estimate costs
        total_tokens = budget_info["total"]
        cost_estimate = self._estimate_cost(total_tokens)
        
        # Step 6: Cache recommendation
        cache_rec = self._get_cache_recommendation(classification)
        
        # Update stats
        self._update_stats(classification, total_tokens)
        
        result = OptimizationResult(
            classification=classification,
            skills=skills_info,
            budget=budget_info,
            execution_path=execution_path,
            estimated_tokens=total_tokens,
            estimated_cost_usd=cost_estimate,
            cache_recommendation=cache_rec,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return result
    
    def _get_budget_allocation(self, intent: str) -> Dict:
        """Get budget allocation for an intent."""
        tier_name = {
            "simple_query": "simple",
            "code_task": "code",
            "research_task": "research",
            "complex_task": "complex"
        }.get(intent, "simple")
        
        tier_config = self.budget_tiers.get("tiers", {}).get(tier_name, {})
        
        return {
            "tier": tier_name,
            "total": tier_config.get("total_budget", 15000),
            "allocation": tier_config.get("allocation", {}),
            "model": tier_config.get("model", "medium")
        }
    
    def _calculate_execution_path(
        self,
        classification: Dict,
        skills: Dict,
        budget: Dict
    ) -> Dict:
        """Calculate the execution path details."""
        
        # Determine memory loading strategy
        memory_strategy = "selective" if classification["needs_memory"] else "minimal"
        
        # Determine skill loading strategy
        skill_strategy = "lazy" if len(skills["skills"]) > 3 else "direct"
        
        # Calculate actual allocations
        system_tokens = budget["allocation"].get("system_prompt", 2000)
        memory_tokens = budget["allocation"].get("memory_context", 3000)
        skill_tokens = skills["tokens_estimated"]
        response_tokens = budget["total"] - system_tokens - memory_tokens - skill_tokens
        
        return {
            "memory_strategy": memory_strategy,
            "skill_strategy": skill_strategy,
            "allocation": {
                "system": system_tokens,
                "memory": memory_tokens,
                "skills": skill_tokens,
                "response": max(response_tokens, 2000)  # Ensure minimum response buffer
            },
            "model_tier": budget["model"],
            "preload_skills": skills["load_order"][:2],
            "parallel_execution": len(skills["skills"]) > 1
        }
    
    def _estimate_cost(self, tokens: int) -> float:
        """Estimate cost in USD for token usage."""
        pricing = self.budget_tiers.get("cost_tracking", {}).get("price_per_1k_tokens", {})
        input_price = pricing.get("input", 0.003)
        output_price = pricing.get("output", 0.015)
        
        # Assume 70% input, 30% output
        input_tokens = tokens * 0.7
        output_tokens = tokens * 0.3
        
        cost = (input_tokens / 1000 * input_price) + (output_tokens / 1000 * output_price)
        return round(cost, 4)
    
    def _get_cache_recommendation(self, classification: Dict) -> str:
        """Recommend caching strategy."""
        intent = classification["intent"]
        domain = classification["domain"]
        
        if intent == "simple_query" and domain == "general":
            return "cache_l1"  # Hot cache for simple queries
        elif intent in ["research_task"]:
            return "cache_l2"  # Warm cache for research
        elif classification["confidence"] > 0.8:
            return "cache_l3"  # Cold cache for high-confidence patterns
        else:
            return "no_cache"  # Don't cache uncertain/complex requests
    
    def _update_stats(self, classification: Dict, tokens_used: int):
        """Update statistics."""
        self.stats["total_requests"] += 1
        
        # Track classifications
        intent = classification["intent"]
        self.stats["classifications"][intent] = \
            self.stats["classifications"].get(intent, 0) + 1
        
        # Calculate savings (compared to 80K baseline)
        baseline_tokens = 80000
        saved = baseline_tokens - tokens_used
        self.stats["tokens_saved"] += saved
        
        # Cost saved
        baseline_cost = self._estimate_cost(baseline_tokens)
        actual_cost = self._estimate_cost(tokens_used)
        self.stats["cost_saved_usd"] += (baseline_cost - actual_cost)
        
        # Average tokens
        total = self.stats["total_requests"]
        current_avg = self.stats["avg_tokens_per_request"]
        self.stats["avg_tokens_per_request"] = \
            ((current_avg * (total - 1)) + tokens_used) / total
    
    def get_stats(self) -> Dict:
        """Get optimizer statistics."""
        return {
            **self.stats,
            "skill_router_stats": self.skill_router.get_stats(),
            "baseline_tokens": 80000,
            "current_avg_tokens": round(self.stats["avg_tokens_per_request"], 0),
            "savings_percent": round(
                (self.stats["tokens_saved"] / (self.stats["total_requests"] * 80000)) * 100
                if self.stats["total_requests"] > 0 else 0, 1
            )
        }
    
    def get_summary_report(self) -> str:
        """Generate a summary report."""
        stats = self.get_stats()
        
        report = f"""
+================================================================+
|           ALGORITHM OPTIMIZER - SUMMARY REPORT                  |
+================================================================+
|                                                                |
|  Total Requests Processed: {stats['total_requests']}                              |
|                                                                |
|  ------------------------------------------------------------- |
|  TOKEN USAGE                                                   |
|  ------------------------------------------------------------- |
|  Baseline (before):     80,000 tokens/request                  |
|  Optimized (after):     {stats['current_avg_tokens']:,.0f} tokens/request                  |
|  Total Tokens Saved:    {stats['tokens_saved']:,.0f} tokens                      |
|  Savings Percentage:    {stats['savings_percent']}%                               |
|                                                                |
|  ------------------------------------------------------------- |
|  COST SAVINGS                                                  |
|  ------------------------------------------------------------- |
|  Total Cost Saved:      ${stats['cost_saved_usd']:,.2f}                          |
|  Avg Cost/Request:      ${stats['cost_saved_usd']/stats['total_requests']:.4f} (saved)           |
|                                                                |
|  ------------------------------------------------------------- |
|  CLASSIFICATION DISTRIBUTION                                   |
|  ------------------------------------------------------------- |
"""
        
        for intent, count in stats['classifications'].items():
            pct = (count / stats['total_requests'] * 100) if stats['total_requests'] > 0 else 0
            report += f"|  {intent}: {count} requests ({pct:.1f}%)              |\n"
        
        report += """|                                                                |
+================================================================+
"""
        
        return report
    
    def to_json(self, result: OptimizationResult) -> Dict:
        """Convert result to JSON."""
        return asdict(result)


# Convenience function
def optimize_request(request: str) -> Dict:
    """Quick optimization function."""
    optimizer = AlgorithmOptimizer()
    result = optimizer.optimize(request)
    return optimizer.to_json(result)


def test_optimizer():
    """Test the optimizer."""
    optimizer = AlgorithmOptimizer()
    
    test_requests = [
        "What time is it?",
        "Fix the bug in the authentication module",
        "Research the latest AI developments and create a report",
        "Build a complete user authentication system with tests and deploy it",
        "Send an email to the client",
        "Check gateway status",
    ]
    
    print("=" * 70)
    print("ALGORITHM OPTIMIZER TEST RESULTS")
    print("=" * 70)
    
    for request in test_requests:
        result = optimizer.optimize(request)
        print("\n" + "-" * 70)
        print(f"REQUEST: {request}")
        print("-" * 70)
        
        print(f"\n[Classification]")
        print(f"   Intent:    {result.classification['intent']}")
        print(f"   Domain:    {result.classification['domain']}")
        print(f"   Priority:  {result.classification['priority_name']}")
        print(f"   Confidence: {result.classification['confidence']:.2f}")
        
        print(f"\n[Skills to Load]")
        print(f"   Skills: {result.skills['skills']}")
        print(f"   Tokens: {result.skills['tokens_estimated']}")
        
        print(f"\n[Budget Allocation]")
        print(f"   Tier:   {result.budget['tier']}")
        print(f"   Total:  {result.budget['total']} tokens")
        print(f"   Model:  {result.budget['model']}")
        
        print(f"\n[Estimates]")
        print(f"   Tokens: {result.estimated_tokens}")
        print(f"   Cost:   ${result.estimated_cost_usd:.4f}")
        print(f"   Cache:  {result.cache_recommendation}")
        
        # Compare to baseline
        baseline = 80000
        saved = baseline - result.estimated_tokens
        print(f"\n[Savings vs Baseline (80K)]")
        print(f"   Tokens Saved: {saved:,}")
        print(f"   Reduction:    {(saved/baseline*100):.1f}%")
    
    print("\n" + "=" * 70)
    print(optimizer.get_summary_report())
    print("=" * 70)


if __name__ == "__main__":
    test_optimizer()