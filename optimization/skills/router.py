#!/usr/bin/env python3
"""
Skill Router - Phase 3: Lazy Skill Loading
Loads skills only when needed, with caching for frequently used skills.

Author: Jeni (AGI Agent)
Created: 2026-04-15
"""

import json
import time
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum
from collections import OrderedDict
import os


class SkillTier(Enum):
    HOT = "hot"      # Always loaded
    WARM = "warm"    # LRU cached
    COLD = "cold"    # Load on demand


@dataclass
class SkillInfo:
    name: str
    tier: SkillTier
    priority: int
    domains: List[str]
    token_estimate: int
    load_time_ms: int
    use_frequency: str
    depends_on: List[str]
    description: str
    keywords: List[str]


class SkillRegistry:
    """Registry of all available skills with metadata."""
    
    def __init__(self, index_path: str = None):
        if index_path is None:
            index_path = os.path.join(
                os.path.dirname(__file__),
                "skill_index.json"
            )
        
        self.skills: Dict[str, SkillInfo] = {}
        self.domain_mapping: Dict[str, List[str]] = {}
        self.preload_patterns: Dict[str, Dict[str, List[str]]] = {}
        self._load_index(index_path)
    
    def _load_index(self, path: str):
        """Load skill index from JSON file."""
        with open(path, 'r') as f:
            data = json.load(f)
        
        # Load skills
        for name, info in data.get("skills", {}).items():
            self.skills[name] = SkillInfo(
                name=name,
                tier=SkillTier(info.get("tier", "cold")),
                priority=info.get("priority", 5),
                domains=info.get("domains", []),
                token_estimate=info.get("token_estimate", 2000),
                load_time_ms=info.get("load_time_estimate_ms", 200),
                use_frequency=info.get("use_frequency", "low"),
                depends_on=info.get("depends_on", []),
                description=info.get("description", ""),
                keywords=info.get("keywords", [])
            )
        
        # Load domain mapping
        self.domain_mapping = data.get("domain_skill_mapping", {})
        
        # Load preload patterns
        self.preload_patterns = data.get("preload_patterns", {})
    
    def get_skill(self, name: str) -> Optional[SkillInfo]:
        """Get skill info by name."""
        return self.skills.get(name)
    
    def get_skills_by_domain(self, domain: str) -> List[str]:
        """Get skills for a specific domain."""
        return self.domain_mapping.get(domain, [])
    
    def get_skills_by_keywords(self, text: str) -> List[str]:
        """Find skills matching keywords in text."""
        text_lower = text.lower()
        matched_skills = []
        
        for name, skill in self.skills.items():
            for keyword in skill.keywords:
                if keyword.lower() in text_lower:
                    matched_skills.append(name)
                    break
        
        return matched_skills
    
    def get_hot_skills(self) -> List[str]:
        """Get all hot-tier skill names."""
        return [name for name, skill in self.skills.items() 
                if skill.tier == SkillTier.HOT]
    
    def get_warm_skills(self) -> List[str]:
        """Get all warm-tier skill names."""
        return [name for name, skill in self.skills.items() 
                if skill.tier == SkillTier.WARM]
    
    def get_preload_for_intent(self, intent: str) -> List[str]:
        """Get skills to preload for an intent."""
        return self.preload_patterns.get("after_classification", {}).get(intent, [])
    
    def estimate_token_cost(self, skill_names: List[str]) -> int:
        """Estimate total tokens for loading skills."""
        total = 0
        for name in skill_names:
            skill = self.skills.get(name)
            if skill:
                total += skill.token_estimate
        return total


class SkillCache:
    """LRU cache for warm-tier skills."""
    
    def __init__(self, max_size: int = 5, ttl_seconds: int = 300):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: OrderedDict = OrderedDict()  # name -> (content, timestamp)
        self.hit_count = 0
        self.miss_count = 0
    
    def get(self, skill_name: str) -> Optional[str]:
        """Get skill from cache if available and not expired."""
        if skill_name in self.cache:
            content, timestamp = self.cache[skill_name]
            
            # Check TTL
            if time.time() - timestamp < self.ttl_seconds:
                # Move to end (most recently used)
                self.cache.move_to_end(skill_name)
                self.hit_count += 1
                return content
            else:
                # Expired, remove
                del self.cache[skill_name]
        
        self.miss_count += 1
        return None
    
    def put(self, skill_name: str, content: str):
        """Add skill to cache."""
        # Remove oldest if at capacity
        while len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)
        
        self.cache[skill_name] = (content, time.time())
    
    def clear(self):
        """Clear the cache."""
        self.cache.clear()
        self.hit_count = 0
        self.miss_count = 0
    
    def get_stats(self) -> Dict:
        """Get cache statistics."""
        total = self.hit_count + self.miss_count
        hit_rate = self.hit_count / total if total > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hit_count,
            "misses": self.miss_count,
            "hit_rate": round(hit_rate, 2),
            "ttl_seconds": self.ttl_seconds
        }


class SkillRouter:
    """Main skill router for lazy loading with caching."""
    
    def __init__(self, registry: SkillRegistry = None):
        self.registry = registry or SkillRegistry()
        self.cache = SkillCache()
        self.hot_skills_loaded: Set[str] = set()
        self._load_hot_skills()
    
    def _load_hot_skills(self):
        """Pre-load hot-tier skills on initialization."""
        hot_skills = self.registry.get_hot_skills()
        for skill_name in hot_skills:
            self.hot_skills_loaded.add(skill_name)
            # In production, would actually load SKILL.md content
    
    def get_skills_for_request(
        self,
        intent: str,
        domain: str,
        request_text: str,
        budget_tokens: int
    ) -> Dict:
        """Determine which skills to load for a request."""
        
        # Start with hot skills (always loaded)
        skills_to_use = list(self.hot_skills_loaded)
        tokens_used = self.registry.estimate_token_cost(skills_to_use)
        
        # Add intent-based preload
        preload = self.registry.get_preload_for_intent(intent)
        for skill_name in preload:
            if skill_name not in skills_to_use:
                skill = self.registry.get_skill(skill_name)
                if skill and tokens_used + skill.token_estimate <= budget_tokens:
                    skills_to_use.append(skill_name)
                    tokens_used += skill.token_estimate
        
        # Add domain-based skills
        domain_skills = self.registry.get_skills_by_domain(domain)
        for skill_name in domain_skills:
            if skill_name not in skills_to_use:
                skill = self.registry.get_skill(skill_name)
                if skill and tokens_used + skill.token_estimate <= budget_tokens:
                    skills_to_use.append(skill_name)
                    tokens_used += skill.token_estimate
        
        # Add keyword-matched skills
        keyword_skills = self.registry.get_skills_by_keywords(request_text)
        for skill_name in keyword_skills[:3]:  # Limit to top 3 keyword matches
            if skill_name not in skills_to_use:
                skill = self.registry.get_skill(skill_name)
                if skill and tokens_used + skill.token_estimate <= budget_tokens:
                    skills_to_use.append(skill_name)
                    tokens_used += skill.token_estimate
        
        return {
            "skills": skills_to_use,
            "tokens_estimated": tokens_used,
            "budget_remaining": budget_tokens - tokens_used,
            "load_order": self._get_load_order(skills_to_use)
        }
    
    def _get_load_order(self, skill_names: List[str]) -> List[str]:
        """Determine optimal load order based on priority and tier."""
        skills_with_priority = []
        for name in skill_names:
            skill = self.registry.get_skill(name)
            if skill:
                # Hot skills first, then by priority
                order_key = (0 if skill.tier == SkillTier.HOT else 1, skill.priority)
                skills_with_priority.append((order_key, name))
        
        # Sort by order key
        skills_with_priority.sort(key=lambda x: x[0])
        
        return [name for _, name in skills_with_priority]
    
    def load_skill(self, skill_name: str) -> Dict:
        """Load a skill (with caching for warm-tier)."""
        skill = self.registry.get_skill(skill_name)
        
        if not skill:
            return {
                "success": False,
                "error": f"Skill '{skill_name}' not found"
            }
        
        # Hot skills - already loaded
        if skill.tier == SkillTier.HOT:
            return {
                "success": True,
                "source": "hot_cache",
                "tokens": skill.token_estimate,
                "load_time_ms": 0
            }
        
        # Warm skills - check LRU cache
        if skill.tier == SkillTier.WARM:
            cached = self.cache.get(skill_name)
            if cached:
                return {
                    "success": True,
                    "source": "lru_cache",
                    "tokens": skill.token_estimate,
                    "load_time_ms": 0
                }
        
        # Need to load from file (cold or cache miss)
        # In production, would read SKILL.md
        load_time = skill.load_time_ms
        
        # Add to cache if warm
        if skill.tier == SkillTier.WARM:
            # Would cache actual content here
            self.cache.put(skill_name, f"skill_content_placeholder")
        
        return {
            "success": True,
            "source": "file_load",
            "tokens": skill.token_estimate,
            "load_time_ms": load_time,
            "tier": skill.tier.value
        }
    
    def get_stats(self) -> Dict:
        """Get router statistics."""
        return {
            "hot_skills_loaded": list(self.hot_skills_loaded),
            "cache_stats": self.cache.get_stats(),
            "total_skills": len(self.registry.skills),
            "domains": list(self.registry.domain_mapping.keys())
        }


# Convenience functions
def get_skills_for_task(intent: str, domain: str, text: str, budget: int = 15000) -> Dict:
    """Quick function to get skills for a task."""
    router = SkillRouter()
    return router.get_skills_for_request(intent, domain, text, budget)


def test_skill_router():
    """Test the skill router."""
    router = SkillRouter()
    
    test_cases = [
        {
            "intent": "code_task",
            "domain": "software_engineering",
            "text": "Fix the bug in the authentication module",
            "budget": 15000
        },
        {
            "intent": "research_task",
            "domain": "research",
            "text": "Search for latest AI developments",
            "budget": 25000
        },
        {
            "intent": "simple_query",
            "domain": "general",
            "text": "What time is it?",
            "budget": 5000
        }
    ]
    
    print("=" * 60)
    print("SKILL ROUTER TEST RESULTS")
    print("=" * 60)
    
    for case in test_cases:
        result = router.get_skills_for_request(
            case["intent"],
            case["domain"],
            case["text"],
            case["budget"]
        )
        print(f"\nCase: {case['intent']} / {case['domain']}")
        print(f"Text: {case['text']}")
        print(f"Result: {json.dumps(result, indent=2)}")
    
    print("\n" + "=" * 60)
    print("ROUTER STATS:")
    print(json.dumps(router.get_stats(), indent=2))
    print("=" * 60)


if __name__ == "__main__":
    test_skill_router()