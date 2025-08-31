# agents/dev_agent/main.py
"""
Dev Agent - GitHub API integration for issue/PR handling
Run: python -m agents.dev_agent.main
"""
import os
import sys
import json
from pathlib import Path

def setup_github_client():
    """Setup GitHub client with token"""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not set - running in dry-run mode")
        return None
    
    try:
        from github import Github
        return Github(token)
    except ImportError:
        print("PyGithub not installed - running in dry-run mode")
        return None

def analyze_issue(issue_data):
    """Analyze GitHub issue and provide suggestions"""
    if not os.getenv("OPENAI_API_KEY"):
        return {
            "labels": ["enhancement", "help-wanted"],
            "checklist": [
                "Reproduce the issue",
                "Check if it's a duplicate", 
                "Add relevant labels",
                "Assign appropriate milestone"
            ],
            "suggestions": "This appears to be a feature request. Consider adding more context about use cases."
        }
    
    # TODO: Implement LLM analysis
    return {"labels": [], "checklist": [], "suggestions": ""}

def suggest_fixes(issue_data):
    """Suggest code fixes for issues"""
    if not os.getenv("OPENAI_API_KEY"):
        return {
            "auto_fixable": False,
            "suggestions": "Manual review required",
            "code_changes": []
        }
    
    # TODO: Implement LLM fix suggestions
    return {"auto_fixable": False, "suggestions": "", "code_changes": []}

def run_linter(file_path):
    """Run linter on file"""
    try:
        import subprocess
        result = subprocess.run(["flake8", file_path], capture_output=True, text=True)
        return result.stdout, result.stderr
    except FileNotFoundError:
        return "", "flake8 not installed"

def main():
    print("Dev Agent - GitHub integration")
    print("Available functions:")
    print("1. analyze_issue() - Analyze GitHub issues")
    print("2. suggest_fixes() - Suggest code fixes") 
    print("3. run_linter() - Run linting")
    print("\nRunning in dry-run mode. Set GITHUB_TOKEN and OPENAI_API_KEY for full functionality.")

if __name__ == "__main__":
    main()
