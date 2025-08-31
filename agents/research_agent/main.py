# agents/research_agent/main.py
"""
Run: python -m agents.research_agent.main "Research topic"
"""
import os
import sys
import json
import datetime
from pathlib import Path

OUT = Path("out")
OUT.mkdir(exist_ok=True)

def search_tavily(query):
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        print("TAVILY_API_KEY not set — dry-run returning example results")
        return [{"title":"Example","url":"https://example.com","snippet":"Example snippet"}]
    import requests
    endpoint = os.getenv("TAVILY_ENDPOINT","https://api.tavily.com/search")
    r = requests.get(endpoint, params={"q": query, "key": key}, timeout=15)
    r.raise_for_status()
    return r.json().get("results", [])[:8]

def fetch_text(url):
    try:
        import requests, trafilatura
        html = requests.get(url, timeout=15).text
        text = trafilatura.extract(html) or ""
        return text[:100000]
    except Exception as e:
        print("fetch error", e)
        return ""

def call_llm_system(prompt):
    if not os.getenv("OPENAI_API_KEY"):
        return "# DRAFT (LLM disabled)\n\n" + prompt[:1000]
    from langchain.llms import OpenAI
    llm = OpenAI(temperature=0.2)
    return llm(prompt)

def main():
    topic = " ".join(sys.argv[1:]) or "Auto-generated topic"
    
    # Try LangGraph workflow first
    try:
        from .langgraph_agent import run_research_workflow
        result = run_research_workflow(topic)
        
        if result["status"] == "completed" and result["method"] == "langgraph":
            state = result["state"]
            
            # Save outputs
            ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M")
            (OUT / f"draft-{ts}.md").write_text(state.draft, encoding="utf-8")
            
            # Save sources
            sources_data = []
            for source in state.sources:
                sources_data.append({
                    "url": source["url"],
                    "title": source["title"],
                    "excerpt": source["content"][:2000]
                })
            
            (OUT / f"sources-{ts}.json").write_text(
                json.dumps(sources_data, ensure_ascii=False, indent=2), 
                encoding="utf-8"
            )
            
            print(f"✅ LangGraph workflow completed. Wrote draft and sources to out/")
            return
    except Exception as e:
        print(f"LangGraph workflow failed: {e}, falling back to simple workflow")
    
    # Fallback to simple workflow
    hits = search_tavily(topic)
    notes = []
    for h in hits[:5]:
        txt = fetch_text(h["url"])
        notes.append({"url": h["url"], "title": h.get("title"), "excerpt": txt[:2000]})
    prompt = f"Topic: {topic}\n\nSources:\n" + "\n\n".join([f"- {n['url']}: {n['excerpt'][:300]}" for n in notes])
    draft = call_llm_system(prompt)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M")
    (OUT / f"draft-{ts}.md").write_text(draft, encoding="utf-8")
    (OUT / f"sources-{ts}.json").write_text(json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✅ Simple workflow completed. Wrote draft and sources to out/")

if __name__ == "__main__":
    main()
