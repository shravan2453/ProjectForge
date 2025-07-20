"""
Mock data and sample responses for testing DSPy modules and nodes.

This file contains realistic sample data that mimics what your DSPy modules
would receive and return, allowing you to test module logic without making
actual LLM API calls.
"""

from typing import Dict, Any, List


# Sample DSPy Module Outputs
CLASSIFIER_RESPONSES = {
    "beginner_web_project": {
        "project_type": "web-app",
        "project_subtype": "static-website", 
        "suitable_for_portfolio": True,
        "complexity_level": "beginner-friendly",
        "complexity_reasoning": "Basic HTML/CSS project perfect for learning fundamentals",
        "skill_alignment_score": "high",
        "learning_curve_assessment": "gentle - building on existing knowledge",
        "recommended_resources": [
            "MDN Web Development Basics",
            "freeCodeCamp HTML/CSS course",
            "CSS Grid and Flexbox guides"
        ],
        "skill_gaps": "CSS layout techniques, responsive design basics",
        "reasoning": "Excellent starter project that matches user's current level"
    },
    
    "intermediate_fullstack": {
        "project_type": "full-stack-web-app",
        "project_subtype": "database-driven-app",
        "suitable_for_portfolio": True, 
        "complexity_level": "intermediate-challenge",
        "complexity_reasoning": "Requires both frontend and backend skills with database integration",
        "skill_alignment_score": "medium-high",
        "learning_curve_assessment": "moderate - several new concepts to integrate",
        "recommended_resources": [
            "React Official Documentation",
            "Node.js and Express tutorials", 
            "PostgreSQL beginner guide",
            "RESTful API design principles"
        ],
        "skill_gaps": "Backend API design, database relationships, authentication",
        "reasoning": "Good step-up project that builds on existing frontend knowledge"
    },
    
    "advanced_system": {
        "project_type": "distributed-system",
        "project_subtype": "microservices-architecture",
        "suitable_for_portfolio": True,
        "complexity_level": "advanced-expert",
        "complexity_reasoning": "Requires deep understanding of system design and multiple technologies",
        "skill_alignment_score": "medium",
        "learning_curve_assessment": "steep - many advanced concepts to master",
        "recommended_resources": [
            "Designing Data-Intensive Applications book",
            "Docker and Kubernetes documentation",
            "System Design Interview guides",
            "Microservices patterns documentation"
        ],
        "skill_gaps": "System architecture, containerization, service orchestration, monitoring",
        "reasoning": "Ambitious project requiring significant learning investment"
    }
}


INTENT_REFINER_RESPONSES = {
    "vague_input": {
        "clarified_intent": "Build a personal portfolio website to showcase programming projects and attract job opportunities",
        "follow_up_questions": [
            "What type of job roles are you targeting?",
            "Do you have existing projects to showcase?",
            "What's your preferred tech stack?",
            "Do you need a blog section?"
        ],
        "suggested_project_types": ["portfolio-website", "static-site", "personal-brand"],
        "generated_ideas": [
            "Interactive portfolio with project demos",
            "Blog-integrated developer portfolio", 
            "Minimalist showcase website",
            "Full-stack portfolio with admin panel"
        ],
        "has_relevant_background": True,
        "background_assessment": "User has programming experience but needs to present it professionally",
        "reasoning": "Refined vague 'website' request into specific portfolio goal"
    },
    
    "specific_input": {
        "clarified_intent": "Create an e-commerce platform for local artisans to sell handmade products online",
        "follow_up_questions": [
            "How many vendors will use the platform initially?",
            "What payment methods do you want to support?", 
            "Do you need inventory management features?",
            "Will you handle shipping or leave that to vendors?"
        ],
        "suggested_project_types": ["marketplace-app", "e-commerce-platform", "multi-vendor-system"],
        "generated_ideas": [
            "Etsy-like marketplace for local crafters",
            "Subscription box service for artisan products",
            "Event-based craft fair platform",
            "Social commerce app for makers"
        ],
        "has_relevant_background": False,
        "background_assessment": "User has general web development skills but lacks e-commerce domain knowledge",
        "reasoning": "Well-defined idea that needs technical scope clarification"
    }
}


MILESTONE_RESPONSES = {
    "web_app_timeline": {
        "estimated_hours": 80,
        "weekly_commitment": "8-12 hours",
        "timeline_weeks": 8,
        "milestones": [
            {
                "week": 1,
                "title": "Project Setup & Planning",
                "tasks": ["Set up development environment", "Create project structure", "Plan database schema"],
                "deliverables": ["GitHub repo", "Project plan document", "Database design"]
            },
            {
                "week": 2-3, 
                "title": "Backend Development",
                "tasks": ["Build REST API", "Implement authentication", "Set up database"],
                "deliverables": ["Working API endpoints", "User authentication system", "Database with seed data"]
            },
            {
                "week": 4-6,
                "title": "Frontend Development", 
                "tasks": ["Create React components", "Implement routing", "Connect to API"],
                "deliverables": ["Responsive UI", "User dashboard", "API integration"]
            },
            {
                "week": 7-8,
                "title": "Testing & Deployment",
                "tasks": ["Write unit tests", "Deploy to cloud", "User testing"],
                "deliverables": ["Test suite", "Live application", "Documentation"]
            }
        ],
        "learning_path": [
            "Review REST API principles",
            "Learn React state management",
            "Understand authentication flows", 
            "Practice deployment procedures"
        ],
        "reasoning": "Realistic 8-week timeline with room for learning and iteration"
    }
}


TIMELINE_RESPONSES = {
    "balanced_schedule": {
        "weekly_schedule": {
            "week1": {"tasks": ["Environment setup", "Git workflow"], "hours": 8},
            "week2": {"tasks": ["Database design", "API planning"], "hours": 10},
            "week3": {"tasks": ["Backend development"], "hours": 12}, 
            "week4": {"tasks": ["Frontend components"], "hours": 10},
            "week5": {"tasks": ["UI integration"], "hours": 12},
            "week6": {"tasks": ["Testing implementation"], "hours": 8},
            "week7": {"tasks": ["Deployment setup"], "hours": 6},
            "week8": {"tasks": ["Final polish", "Documentation"], "hours": 8}
        },
        "milestone_timeline": "" Week 1-2: Foundation\n" Week 3-4: Backend\n" Week 5-6: Frontend\n" Week 7-8: Launch",
        "scheduling_warnings": "Week 3 and 5 require higher time commitment",
        "pacing_recommendations": "Build in buffer time for debugging and learning new concepts"
    }
}


REPORT_RESPONSES = {
    "comprehensive_report": {
        "executive_summary": "8-week full-stack web development project designed to build practical skills while creating a portfolio-worthy application.",
        "project_overview": {
            "scope": "Full-stack e-commerce platform with user authentication and payment processing",
            "target_audience": "Local artisans and craft enthusiasts", 
            "key_features": ["User registration", "Product catalog", "Shopping cart", "Payment integration"],
            "success_metrics": ["Functional application", "Responsive design", "Secure authentication", "Deployed to cloud"]
        },
        "timeline_summary": [
            "Phase 1 (Weeks 1-2): Planning and backend setup",
            "Phase 2 (Weeks 3-5): Core development", 
            "Phase 3 (Weeks 6-8): Integration and deployment"
        ],
        "team_responsibilities": [
            "Solo project - developer responsible for all aspects",
            "Mentor review at milestone completion",
            "Peer feedback during development phases"
        ],
        "learning_roadmap": [
            "Master React component architecture",
            "Understand RESTful API design",
            "Learn authentication and security basics",
            "Practice cloud deployment workflows"
        ],
        "resource_prioritization": {
            "critical": "React documentation, Node.js guides",
            "important": "Database design tutorials, deployment guides", 
            "nice-to-have": "Advanced optimization techniques, testing frameworks"
        },
        "success_metrics": [
            "Fully functional web application",
            "Mobile-responsive design",
            "Secure user authentication",
            "Successful cloud deployment",
            "Clean, documented codebase"
        ],
        "risk_assessment": [
            "Timeline risk: Complex features may take longer than estimated",
            "Technical risk: Authentication implementation challenges",
            "Scope risk: Feature creep during development",
            "Mitigation: Weekly progress reviews and scope management"
        ],
        "project_alignment": [
            "Aligns with full-stack development career goals",
            "Builds practical skills demanded by employers",
            "Creates substantial portfolio piece",
            "Provides end-to-end project experience"
        ]
    }
}


# Sample error responses for testing error handling
ERROR_RESPONSES = {
    "insufficient_info": {
        "error_type": "ValidationError",
        "message": "Insufficient project information provided",
        "required_fields": ["project_goal", "user_type", "technical_skills"],
        "suggestions": ["Please provide more details about your project goals"]
    },
    
    "complexity_mismatch": {
        "error_type": "SkillMismatchError", 
        "message": "Project complexity exceeds current skill level",
        "recommended_action": "Consider starting with a simpler project or additional learning",
        "alternative_projects": ["Static portfolio website", "Simple CRUD application"]
    }
}


# Utility functions for tests
def get_mock_response(module_name: str, scenario: str) -> Dict[str, Any]:
    """Get a mock response for a specific module and scenario."""
    response_map = {
        "classifier": CLASSIFIER_RESPONSES,
        "intent_refiner": INTENT_REFINER_RESPONSES, 
        "milestone_gen": MILESTONE_RESPONSES,
        "timeline": TIMELINE_RESPONSES,
        "report": REPORT_RESPONSES
    }
    
    return response_map.get(module_name, {}).get(scenario, {})


def create_mock_completed_tasks(count: int = 3) -> List[Dict[str, Any]]:
    """Generate mock completed tasks for testing past project analysis."""
    base_tasks = [
        {
            "project_type": "web-app",
            "status": "completed",
            "technologies": ["HTML", "CSS", "JavaScript"],
            "outcome": "Personal portfolio website deployed successfully",
            "duration_weeks": 3,
            "complexity_at_time": "beginner"
        },
        {
            "project_type": "data-analysis", 
            "status": "completed",
            "technologies": ["Python", "Pandas", "Matplotlib"],
            "outcome": "Sales data visualization dashboard created",
            "duration_weeks": 4,
            "complexity_at_time": "intermediate"
        },
        {
            "project_type": "mobile-app",
            "status": "in-progress", 
            "technologies": ["React Native", "Firebase"],
            "outcome": "Learning project - 70% complete",
            "duration_weeks": 6,
            "complexity_at_time": "intermediate"
        }
    ]
    
    return base_tasks[:count]