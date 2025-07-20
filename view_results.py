#!/usr/bin/env python3
"""
Pretty viewer for workflow results
"""
import json
from pathlib import Path
from app.person import PersonProfile
from app.state import StateModel
from app.workflow import create_workflow
import os 
import dspy


def setup_dspy():
    api_key = os.getenv("OPENAI_API_KEY")

    lm = dspy.OpenAI(model='gpt-3.5-turbo', api_key=api_key)
    dspy.configure(lm=lm)

setup_dspy()
def create_test_state():
    """Create a basic state model for testing."""
    # Person Profile

    profile = PersonProfile(
        user_type="student",
        experience_level="beginner",
        has_technical_background=True,
        skill_domains=["programming"],
        learning_preference="hands-on",
        hours_per_week=12
    )


    # Create statemodel
    state = StateModel(
        user_id="nati",
        session_id="test_session",
        person_profile=profile,
        project_goal="AI-Powered Eco-Tourism Route Recommendation Engine",
        interests= ["web development", "AI"],
        technical_skills= ["HTML", "CSS", "JavaScript"],
        end_goal = "Create a system that suggests eco-tourism routes based on preferences, environmental impact, and real-time conditions."
    )

    return state


def format_as_html(result_dict):
    """Generate comprehensive HTML report from state."""
    # Helper function to safely get timeline info
    timeline_info = result_dict.get('timeline', {})
    if isinstance(timeline_info, dict) and 'estimated_hours' not in timeline_info:
        # Extract from project_overview if available
        duration_weeks = result_dict.get('project_overview', {}).get('duration', '0 weeks').replace(' weeks', '')
        total_hours = sum([m.get('estimated_hours', 0) for m in result_dict.get('milestones', [])])
        hours_per_week = getattr(result_dict.get('person_profile'), 'hours_per_week', 10) if result_dict.get('person_profile') else 10
    else:
        total_hours = timeline_info.get('estimated_hours', 'Unknown')
        hours_per_week = timeline_info.get('weekly_commitment', 'Unknown')
        duration_weeks = timeline_info.get('timeline_weeks', 'Unknown')
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Project Planning Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; line-height: 1.6; background: #f8f9fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
        .header h1 {{ margin: 0; font-size: 2.5em; }}
        .header .subtitle {{ opacity: 0.9; margin-top: 10px; font-size: 1.1em; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #666; font-size: 0.9em; text-transform: uppercase; letter-spacing: 1px; }}
        .section {{ margin: 30px 0; }}
        .section h2 {{ color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
        .milestone {{ background: #e3f2fd; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #2196f3; }}
        .milestone-header {{ font-weight: bold; font-size: 1.1em; color: #1976d2; }}
        .milestone-meta {{ color: #666; font-size: 0.9em; margin-top: 8px; }}
        .resource {{ background: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 6px; border-left: 4px solid #4caf50; }}
        .quick-win {{ background: #fff3e0; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 4px solid #ff9800; }}
        .deliverable {{ background: #f3e5f5; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 4px solid #9c27b0; }}
        .checkpoint {{ background: #e1f5fe; padding: 15px; margin: 10px 0; border-radius: 6px; border-left: 4px solid #00bcd4; }}
        .risk-item {{ background: #ffebee; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 4px solid #f44336; }}
        .success-metric {{ background: #e8f5e8; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 4px solid #4caf50; }}
        .pivot-opportunity {{ background: #fff8e1; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 4px solid #ffc107; }}
        .learning-step {{ background: #e3f2fd; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 4px solid #2196f3; }}
        .two-column {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
        .error {{ color: #d32f2f; background: #ffebee; padding: 15px; border-radius: 5px; }}
        .success {{ color: #388e3c; background: #e8f5e8; padding: 15px; border-radius: 5px; }}
        .warning {{ color: #f57c00; background: #fff3e0; padding: 15px; border-radius: 5px; }}
        ul {{ padding-left: 0; list-style: none; }}
        li {{ margin: 8px 0; }}
        .timeline-week {{ background: #f5f5f5; padding: 10px; margin: 5px 0; border-radius: 4px; border-left: 3px solid #667eea; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 {result_dict.get('project_goal', 'Project Planning Report')}</h1>
            <div class="subtitle">Comprehensive AI-Generated Project Analysis</div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{result_dict.get('complexity_level', 'Unknown')}</div>
                <div class="stat-label">Complexity Level</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(result_dict.get('milestones', []))}</div>
                <div class="stat-label">Milestones</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_hours}</div>
                <div class="stat-label">Total Hours</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{hours_per_week}</div>
                <div class="stat-label">Hours/Week</div>
            </div>
        </div>

        <div class="section">
            <h2>📋 Executive Summary</h2>
            <p style="font-size: 1.1em; line-height: 1.8;">{result_dict.get('executive_summary', 'No summary available')}</p>
        </div>

        <div class="two-column">
            <div>
                <div class="section">
                    <h2>🎯 Project Milestones</h2>
                    {''.join([f'''
                    <div class="milestone">
                        <div class="milestone-header">{m.get("title", "Milestone")}</div>
                        <div>{m.get("description", "No description")}</div>
                        <div class="milestone-meta">📅 Week {m.get("week", "TBD")} • ⏱️ {m.get("estimated_hours", 0)} hours</div>
                    </div>
                    ''' for m in result_dict.get('milestones', [])[:8]])}
                </div>

                <div class="section">
                    <h2>🏆 Quick Wins</h2>
                    {''.join([f'<div class="quick-win">⚡ {win}</div>' for win in result_dict.get('quick_wins', [])])}
                </div>

                <div class="section">
                    <h2>📦 Project Deliverables</h2>
                    {''.join([f'<div class="deliverable">📄 {deliverable}</div>' for deliverable in result_dict.get('project_deliverables', [])])}
                </div>
            </div>

            <div>
                <div class="section">
                    <h2>📚 Learning Roadmap</h2>
                    {''.join([f'<div class="learning-step">📖 {step}</div>' for step in result_dict.get('learning_path', [])])}
                </div>

                <div class="section">
                    <h2>🔧 Recommended Resources</h2>
                    {''.join([f'<div class="resource">🛠️ {resource}</div>' for resource in result_dict.get('recommended_resources', [])])}
                </div>

                <div class="section">
                    <h2>📋 Completion Checklist</h2>
                    {''.join([f'<div class="deliverable">✅ {item}</div>' for item in result_dict.get('completion_prep', [])])}
                </div>
            </div>
        </div>

        <div class="section">
            <h2>📅 Project Timeline</h2>
            {''.join([f'<div class="timeline-week">📆 {item}</div>' for item in result_dict.get('timeline_summary', [])])}
        </div>

        <div class="section">
            <h2>🔄 Pivot Opportunities</h2>
            <p style="font-style: italic; color: #666;">Strategic points where you can adjust direction if needed:</p>
            {''.join([f'<div class="pivot-opportunity">🔄 {pivot}</div>' for pivot in result_dict.get('pivot_opportunities', [])])}
        </div>

        <div class="section">
            <h2>✅ Success Metrics</h2>
            {''.join([f'<div class="success-metric">🎯 {metric}</div>' for metric in result_dict.get('success_metrics', [])])}
        </div>

        <div class="section">
            <h2>📋 Review Checkpoints</h2>
            {''.join([f'''
            <div class="checkpoint">
                <strong>Week {checkpoint.get("week", "TBD")}</strong><br>
                <strong>Goal:</strong> {checkpoint.get("goal", "Review progress")}<br>
                <strong>Criteria:</strong> {checkpoint.get("criteria", "Assess completion")}
            </div>
            ''' for checkpoint in result_dict.get('checkpoints', [])])}
        </div>

        <div class="section">
            <h2>🎒 Portfolio Items</h2>
            <p style="font-style: italic; color: #666;">Deliverables perfect for showcasing your skills:</p>
            {''.join([f'<div class="deliverable">🏆 {item}</div>' for item in result_dict.get('portfolio_items', [])])}
        </div>

        <div class="section">
            <h2>⚠️ Risk Assessment</h2>
            {''.join([f'<div class="risk-item">⚠️ {risk}</div>' for risk in result_dict.get('risk_assessment', [])])}
        </div>

        <div class="section">
            <h2>📊 Skills & Background Analysis</h2>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px;">
                <p><strong>Skills Gap Analysis:</strong> {result_dict.get('skill_gaps', 'Not assessed')}</p>
                <p><strong>Background Assessment:</strong> {result_dict.get('background_assessment', 'Not available')}</p>
                <p><strong>Learning Curve:</strong> {result_dict.get('conversation_context', {}).get('learning_curve_assessment', 'Not assessed')}</p>
                <p><strong>Skill Alignment:</strong> {result_dict.get('conversation_context', {}).get('skill_alignment_score', 'Not assessed')}</p>
            </div>
        </div>

        <div class="section">
            <h2>👥 Project Structure</h2>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px;">
                <p><strong>Team Project:</strong> {'Yes' if result_dict.get('has_team') else 'No (Solo Project)'}</p>
                <p><strong>Team Size:</strong> {result_dict.get('team_size', 1)} member(s)</p>
                <p><strong>User Profile:</strong> {getattr(result_dict.get('person_profile'), 'user_type', 'Unknown') if result_dict.get('person_profile') else 'Unknown'} ({getattr(result_dict.get('person_profile'), 'experience_level', 'Unknown') if result_dict.get('person_profile') else 'Unknown'})</p>
            </div>
        </div>

        <div class="section">
            <h2>🔧 System Status</h2>
            {f'<div class="error">⚠️ Timeline Generation Issue: {result_dict.get("timeline", {}).get("error", "Unknown error")}</div>' if isinstance(result_dict.get("timeline"), dict) and result_dict.get("timeline", {}).get("error") else '<div class="success">✅ All systems operational</div>'}
            
            {f'<div class="warning"><strong>Scheduling Notes:</strong><br>{"<br>".join([conflict.get("description", "Unknown conflict") for conflict in result_dict.get("calendar_conflicts", [])])}</div>' if result_dict.get('calendar_conflicts') else ''}
        </div>

        <div style="margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 8px; text-align: center; color: #666;">
            <p>📊 Generated by Advanced AI Project Planning System</p>
            <p>This comprehensive analysis provides strategic insights for successful project completion</p>
        </div>
    </div>
</body>
</html>
"""
    return html

def format_as_json(result_dict):
    """Generate clean JSON from state."""
    # Create a clean summary dict
    summary = {
        "project_info": {
            "goal": result_dict.get('project_goal'),
            "type": result_dict.get('project_type'),
            "complexity": result_dict.get('complexity_level'),
            "user_type": getattr(result_dict.get('person_profile'), 'user_type', None) if result_dict.get('person_profile') else None,
            "experience": getattr(result_dict.get('person_profile'), 'experience_level', None) if result_dict.get('person_profile') else None
        },
        "executive_summary": result_dict.get('executive_summary'),
        "milestones": result_dict.get('milestones', [])[:5],  # First 5 milestones
        "learning_path": result_dict.get('learning_path', []),
        "recommended_resources": result_dict.get('recommended_resources', []),
        "timeline_summary": result_dict.get('timeline_summary', []),
        "success_metrics": result_dict.get('success_metrics', []),
        "quick_wins": result_dict.get('quick_wins', []),
        "skills_assessment": {
            "gaps": result_dict.get('skill_gaps'),
            "background": result_dict.get('background_assessment'),
            "alignment_score": result_dict.get('conversation_context', {}).get("skill_alignment_score"),
            "learning_curve": result_dict.get('conversation_context', {}).get("learning_curve_assessment")
        },
        "team_info": {
            "has_team": result_dict.get('has_team'),
            "team_size": result_dict.get('team_size'),
            "team_members": result_dict.get('team_members', [])
        },
        "errors_and_warnings": {
            "timeline_error": result_dict.get('timeline', {}).get("error") if isinstance(result_dict.get('timeline'), dict) else None,
            "calendar_conflicts": result_dict.get('calendar_conflicts', []),
            "general_errors": result_dict.get('errors', []),
            "warnings": result_dict.get('warnings', [])
        }
    }
    return json.dumps(summary, indent=2, default=str)

def main():
    print("🚀 Running workflow and generating formatted output...")
    
    # Create and run workflow
    state = create_test_state()
    workflow = create_workflow()
    
    # Run workflow
    result = workflow.invoke(state)
    
    # Generate HTML report
    html_content = format_as_html(result)
    html_file = Path("project_report.html")
    html_file.write_text(html_content)
    print(f"📄 HTML report saved to: {html_file.absolute()}")
    
    # Generate JSON summary  
    json_content = format_as_json(result)
    json_file = Path("project_summary.json")
    json_file.write_text(json_content)
    print(f"📊 JSON summary saved to: {json_file.absolute()}")
    
    print("\n✅ Files generated successfully!")
    print(f"   • Open {html_file.name} in your browser to view the formatted report")
    print(f"   • Open {json_file.name} to see the structured data")

if __name__ == "__main__":
    main()