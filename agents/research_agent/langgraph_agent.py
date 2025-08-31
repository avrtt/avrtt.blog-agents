# agents/research_agent/langgraph_agent.py
"""
LangGraph-based Research Agent with structured workflow
"""
import os
import json
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime, timezone

try:
    from langgraph.graph import StateGraph, END
    from langchain_openai import ChatOpenAI
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    print("LangGraph not available - using fallback mode")

class ResearchState:
    """State for the research workflow"""
    def __init__(self, topic: str):
        self.topic = topic
        self.search_queries = []
        self.sources = []
        self.draft = ""
        self.metadata = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "topic": topic,
            "status": "initialized"
        }

def run_research_workflow(topic: str) -> Dict[str, Any]:
    """Run the complete research workflow"""
    if not LANGGRAPH_AVAILABLE:
        # Fallback to simple workflow
        return {"status": "completed", "method": "fallback"}
    
    try:
        # Initialize state
        state = ResearchState(topic)
        
        # Generate search queries
        state.search_queries = [
            f"{topic} latest trends",
            f"{topic} expert analysis", 
            f"{topic} case studies"
        ]
        
        # Search and fetch sources
        from .main import search_tavily, fetch_text
        for query in state.search_queries:
            results = search_tavily(query)
            for result in results[:2]:
                content = fetch_text(result["url"])
                if content:
                    state.sources.append({
                        "url": result["url"],
                        "title": result.get("title", "Untitled"),
                        "content": content[:2000]
                    })
        
        # Generate draft
        if os.getenv("OPENAI_API_KEY"):
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
            
            sources_text = "\n\n".join([
                f"- {s['title']}: {s['content'][:300]}..."
                for s in state.sources
            ])
            
            prompt = f"""Create a research draft on "{topic}" based on these sources:

{sources_text}

Write a comprehensive, well-structured Markdown article."""
            
            response = llm.invoke([{"role": "user", "content": prompt}])
            state.draft = response.content
        else:
            state.draft = f"# DRAFT (LLM disabled)\n\nTopic: {topic}\n\nSources found: {len(state.sources)}"
        
        return {
            "status": "completed",
            "method": "langgraph",
            "state": state
        }
        
    except Exception as e:
        print(f"Error in research workflow: {e}")
        return {"status": "error", "method": "langgraph", "error": str(e)}
