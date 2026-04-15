#!/usr/bin/env python3
"""
Request Router - Phase 1: Classification Engine
Routes requests to appropriate execution paths based on intent classification.

Author: Jeni (AGI Agent)
Created: 2026-04-15
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class IntentType(Enum):
    SIMPLE_QUERY = "simple_query"
    CODE_TASK = "code_task"
    RESEARCH_TASK = "research_task"
    COMPLEX_TASK = "complex_task"


class DomainType(Enum):
    SOFTWARE_ENGINEERING = "software_engineering"
    BUSINESS_OPERATIONS = "business_operations"
    RESEARCH = "research"
    COMMUNICATION = "communication"
    AUTOMATION = "automation"
    GENERAL = "general"


class PriorityLevel(Enum):
    URGENT = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


@dataclass
class ClassificationResult:
    intent: IntentType
    domain: DomainType
    priority: PriorityLevel
    skills: List[str]
    needs_memory: bool
    budget_tokens: int
    confidence: float


class IntentClassifier:
    """Classifies user requests into intent types."""
    
    # Keyword patterns for each intent
    INTENT_PATTERNS = {
        IntentType.CODE_TASK: [
            r'\b(code|coding|program|function|class|module|component)\b',
            r'\b(bug|fix|debug|error|exception|crash)\b',
            r'\b(refactor|optimize|improve|rewrite)\b',
            r'\b(test|tests|testing|unit test|integration)\b',
            r'\b(create|build|implement|develop|write)\b.*\b(file|component|feature|module)\b',
            r'\b(review|PR|pull request|commit)\b',
            r'\b(API|endpoint|route|controller)\b',
            r'\b(git|github|branch|merge)\b',
        ],
        IntentType.RESEARCH_TASK: [
            r'\b(research|investigate|explore|study)\b',
            r'\b(search|find|lookup|query)\b.*\b(information|data|details)\b',
            r'\b(analyze|analysis|compare|comparison)\b',
            r'\b(report|summary|overview|brief)\b',
            r'\b(best practices|latest|current|trends)\b',
            r'\b(deep dive|thorough|comprehensive)\b',
            r'\b(market|industry|competitive)\b.*\b(analysis|research)\b',
        ],
        IntentType.COMPLEX_TASK: [
            r'\b(plan|design|architecture|system)\b',
            r'\b(implement|deploy|launch|release)\b.*\b(complete|full|end-to-end)\b',
            r'\b(workflow|pipeline|automation|pipeline)\b',
            r'\b(multi-step|multiple|several)\b.*\b(actions|tasks|steps)\b',
            r'\b(project|solution|system)\b.*\b(create|build|develop)\b',
            r'\b(end-to-end|complete|full)\b.*\b(solution|implementation)\b',
        ],
    }
    
    def classify(self, request: str) -> Tuple[IntentType, float]:
        """Classify request into intent type with confidence score."""
        request_lower = request.lower()
        
        # Check each intent pattern
        scores = {}
        for intent, patterns in self.INTENT_PATTERNS.items():
            matches = 0
            for pattern in patterns:
                if re.search(pattern, request_lower):
                    matches += 1
            scores[intent] = matches / len(patterns) if matches > 0 else 0
        
        # Find best match
        best_intent = max(scores, key=scores.get)
        confidence = scores[best_intent]
        
        # Default to simple_query if no strong match
        if confidence < 0.1:
            return IntentType.SIMPLE_QUERY, 0.5
        
        return best_intent, confidence


class DomainDetector:
    """Detects the domain/context of a request."""
    
    DOMAIN_PATTERNS = {
        DomainType.SOFTWARE_ENGINEERING: [
            r'\b(code|coding|programming|development)\b',
            r'\b(git|github|PR|commit|branch|merge)\b',
            r'\b(API|endpoint|server|backend|frontend)\b',
            r'\b(test|testing|debug|debugging)\b',
            r'\b(deploy|deployment|CI|CD|pipeline)\b',
            r'\b(refactor|optimize|architecture)\b',
        ],
        DomainType.BUSINESS_OPERATIONS: [
            r'\b(Work360|work360)\b',
            r'\b(client|customer|sales|marketing)\b',
            r'\b(business|company|organization)\b',
            r'\b(invoice|proposal|quote|contract)\b',
            r'\b(meeting|appointment|schedule)\b',
            r'\b(Shalinda|Uththama)\b',
        ],
        DomainType.RESEARCH: [
            r'\b(research|investigate|study|explore)\b',
            r'\b(search|find|analyze|analysis)\b',
            r'\b(report|summary|overview)\b',
            r'\b(compare|comparison|evaluate)\b',
            r'\b(market|industry|trends)\b',
        ],
        DomainType.COMMUNICATION: [
            r'\b(email|message|send|notify)\b',
            r'\b(WhatsApp|Telegram|Discord|Signal)\b',
            r'\b(social|media|post|tweet)\b',
            r'\b(communicate|reply|respond)\b',
        ],
        DomainType.AUTOMATION: [
            r'\b(automate|automation|scheduled|schedule)\b',
            r'\b(cron|heartbeat|routine|workflow)\b',
            r'\b(recurring|periodic|regular)\b',
            r'\b(background|daemon|service)\b',
        ],
    }
    
    def detect(self, request: str) -> Tuple[DomainType, float]:
        """Detect domain from request with confidence."""
        request_lower = request.lower()
        
        scores = {}
        for domain, patterns in self.DOMAIN_PATTERNS.items():
            matches = 0
            for pattern in patterns:
                if re.search(pattern, request_lower):
                    matches += 1
            scores[domain] = matches / len(patterns) if matches > 0 else 0
        
        best_domain = max(scores, key=scores.get)
        confidence = scores[best_domain]
        
        if confidence < 0.05:
            return DomainType.GENERAL, 0.5
        
        return best_domain, confidence


class PriorityScorer:
    """Scores the priority level of a request."""
    
    PRIORITY_PATTERNS = {
        PriorityLevel.URGENT: [
            r'\b(urgent|critical|emergency|ASAP|immediately)\b',
            r'\b(down|broken|crashed|failed|error)\b.*\b(system|gateway|service)\b',
            r'\b(security|breach|attack|vulnerability)\b',
        ],
        PriorityLevel.HIGH: [
            r'\b(important|priority|client|customer)\b',
            r'\b(bug|issue|problem|error)\b',
            r'\b(need|require|must|should)\b.*\b(now|soon|today)\b',
        ],
        PriorityLevel.LOW: [
            r'\b(later|eventually|when possible|sometime)\b',
            r'\b(optional|nice to have|minor|small)\b',
            r'\b(cleanup|organize|tidy)\b',
        ],
    }
    
    def score(self, request: str) -> Tuple[PriorityLevel, float]:
        """Score priority level from request."""
        request_lower = request.lower()
        
        scores = {}
        for priority, patterns in self.PRIORITY_PATTERNS.items():
            matches = 0
            for pattern in patterns:
                if re.search(pattern, request_lower):
                    matches += 1
            scores[priority] = matches
        
        # Check for urgent first
        if scores.get(PriorityLevel.URGENT, 0) > 0:
            return PriorityLevel.URGENT, 0.9
        
        # Check for high
        if scores.get(PriorityLevel.HIGH, 0) > 0:
            return PriorityLevel.HIGH, 0.7
        
        # Check for low
        if scores.get(PriorityLevel.LOW, 0) > 0:
            return PriorityLevel.LOW, 0.6
        
        # Default to medium
        return PriorityLevel.MEDIUM, 0.5


class RequestRouter:
    """Main router that orchestrates classification and routing."""
    
    # Budget allocations per intent
    BUDGET_MAP = {
        IntentType.SIMPLE_QUERY: 5000,
        IntentType.CODE_TASK: 15000,
        IntentType.RESEARCH_TASK: 25000,
        IntentType.COMPLEX_TASK: 40000,
    }
    
    # Skills needed per intent
    SKILLS_MAP = {
        IntentType.SIMPLE_QUERY: [],
        IntentType.CODE_TASK: ["cursor-agent", "github"],
        IntentType.RESEARCH_TASK: ["autoglm-websearch", "autoglm-browser-agent"],
        IntentType.COMPLEX_TASK: ["cursor-agent", "github", "vercel-deploy"],
    }
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.domain_detector = DomainDetector()
        self.priority_scorer = PriorityScorer()
    
    def route(self, request: str) -> ClassificationResult:
        """Route a request and return classification result."""
        
        # Classify intent
        intent, intent_conf = self.intent_classifier.classify(request)
        
        # Detect domain
        domain, domain_conf = self.domain_detector.detect(request)
        
        # Score priority
        priority, priority_conf = self.priority_scorer.score(request)
        
        # Determine skills needed
        skills = self.SKILLS_MAP.get(intent, [])
        
        # Determine if memory needed
        needs_memory = intent != IntentType.SIMPLE_QUERY or domain != DomainType.GENERAL
        
        # Get budget
        budget = self.BUDGET_MAP.get(intent, 15000)
        
        # Calculate overall confidence
        confidence = (intent_conf + domain_conf + priority_conf) / 3
        
        return ClassificationResult(
            intent=intent,
            domain=domain,
            priority=priority,
            skills=skills,
            needs_memory=needs_memory,
            budget_tokens=budget,
            confidence=confidence
        )
    
    def route_to_json(self, request: str) -> Dict:
        """Route request and return JSON result."""
        result = self.route(request)
        return {
            "intent": result.intent.value,
            "domain": result.domain.value,
            "priority": result.priority.value,
            "priority_name": result.priority.name.lower(),
            "skills": result.skills,
            "needs_memory": result.needs_memory,
            "budget_tokens": result.budget_tokens,
            "confidence": round(result.confidence, 2)
        }
    
    def get_execution_path(self, result: ClassificationResult) -> Dict:
        """Get execution path details based on classification."""
        return {
            "path": result.intent.value,
            "budget": {
                "total": result.budget_tokens,
                "system": 2000,
                "memory": 5000 if result.needs_memory else 1000,
                "skills": sum([3000 for _ in result.skills]),
                "response": result.budget_tokens - 2000 - (5000 if result.needs_memory else 1000) - sum([3000 for _ in result.skills])
            },
            "model_tier": "small" if result.intent == IntentType.SIMPLE_QUERY else "medium",
            "cache_key": self._generate_cache_key(result),
            "preload_skills": result.skills[:2] if result.skills else [],  # Preload top 2 skills
        }
    
    def _generate_cache_key(self, result: ClassificationResult) -> str:
        """Generate a cache key for this classification."""
        return f"{result.intent.value}:{result.domain.value}:{result.priority.value}"


# Convenience function for quick routing
def classify_request(request: str) -> Dict:
    """Quick classification function."""
    router = RequestRouter()
    return router.route_to_json(request)


# Test function
def test_router():
    """Test the router with sample requests."""
    router = RequestRouter()
    
    test_requests = [
        "What time is it?",
        "Fix the bug in the authentication module",
        "Research the latest AI developments",
        "Build a complete user authentication system",
        "Send an email to the client",
        "Check gateway status",
        "Create a new React component for the dashboard",
    ]
    
    print("=" * 60)
    print("REQUEST ROUTER TEST RESULTS")
    print("=" * 60)
    
    for request in test_requests:
        result = router.route_to_json(request)
        print(f"\nRequest: {request}")
        print(f"Result: {json.dumps(result, indent=2)}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_router()