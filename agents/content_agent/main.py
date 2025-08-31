# agents/content_agent/main.py
"""
Content Agent - Template for post creation/editing
Run: python -m agents.content_agent.main "outline_file.md"
"""
import os
import sys
import json
from pathlib import Path

def create_outline(topic):
    """Create an outline from a topic"""
    if not os.getenv("OPENAI_API_KEY"):
        return f"""# Outline: {topic}

## Introduction
- Hook and context
- Main thesis

## Main Points
1. [Point 1]
2. [Point 2] 
3. [Point 3]

## Conclusion
- Summary
- Call to action

---
*Generated in dry-run mode*"""
    
    try:
        from langchain_openai import ChatOpenAI
        from .prompts import OUTLINE_GENERATION_PROMPT
        
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        prompt = OUTLINE_GENERATION_PROMPT.format(topic=topic)
        
        response = llm.invoke([{"role": "user", "content": prompt}])
        return response.content
    except Exception as e:
        print(f"Error generating outline: {e}")
        return f"# Outline for: {topic}"

def expand_draft(outline, sources=None):
    """Expand outline into full draft"""
    if not os.getenv("OPENAI_API_KEY"):
        return f"""# DRAFT: {outline.split()[1] if outline.startswith('#') else 'Untitled'}

{outline}

## Full Content Would Be Generated Here

This is a placeholder draft. Set OPENAI_API_KEY to enable full content generation.

---
*Generated in dry-run mode*"""
    
    try:
        from langchain_openai import ChatOpenAI
        from .prompts import DRAFT_EXPANSION_PROMPT
        
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        
        additional_context = ""
        if sources:
            additional_context = f"\n## Sources:\n{sources}"
        
        prompt = DRAFT_EXPANSION_PROMPT.format(
            outline=outline,
            additional_context=additional_context
        )
        
        response = llm.invoke([{"role": "user", "content": prompt}])
        return response.content
    except Exception as e:
        print(f"Error expanding draft: {e}")
        return outline

def self_critique(draft):
    """Self-critique the draft"""
    if not os.getenv("OPENAI_API_KEY"):
        return """## Self-Critique

- [ ] Structure is clear and logical
- [ ] Content is engaging and informative  
- [ ] SEO elements are present
- [ ] Grammar and style are polished

---
*Generated in dry-run mode*"""
    
    try:
        from langchain_openai import ChatOpenAI
        from .prompts import SELF_CRITIQUE_PROMPT
        
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        prompt = SELF_CRITIQUE_PROMPT.format(content=draft[:3000])  # Limit content length
        
        response = llm.invoke([{"role": "user", "content": prompt}])
        return response.content
    except Exception as e:
        print(f"Error generating critique: {e}")
        return "Self-critique would be generated here"

def seo_checklist(draft):
    """Generate SEO checklist"""
    if not os.getenv("OPENAI_API_KEY"):
        return """## SEO Checklist

- [ ] Title is compelling (50-60 chars)
- [ ] Meta description is descriptive (150-160 chars)
- [ ] Headings use proper hierarchy (H1, H2, H3)
- [ ] Keywords are naturally integrated
- [ ] Internal/external links are present
- [ ] Images have alt text (if applicable)
- [ ] Content length is appropriate (1000+ words)
- [ ] URL structure is clean

---
*Generated in dry-run mode*"""
    
    try:
        from langchain_openai import ChatOpenAI
        from .prompts import SEO_CHECKLIST_PROMPT
        
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        prompt = SEO_CHECKLIST_PROMPT.format(content=draft[:3000])  # Limit content length
        
        response = llm.invoke([{"role": "user", "content": prompt}])
        return response.content
    except Exception as e:
        print(f"Error generating SEO checklist: {e}")
        return "SEO checklist would be generated here"

def generate_social_snippets(draft):
    """Generate social media snippets"""
    if not os.getenv("OPENAI_API_KEY"):
        return {
            "telegram": f"📝 New blog post: {draft.split()[1] if draft.startswith('#') else 'Check out our latest post!'}",
            "facebook": f"New blog post: {draft.split()[1] if draft.startswith('#') else 'Check out our latest post!'}",
            "twitter": f"New blog post: {draft.split()[1] if draft.startswith('#') else 'Check out our latest post!'} #blog #tech"
        }
    
    try:
        from langchain_openai import ChatOpenAI
        from .prompts import SOCIAL_MEDIA_PROMPT
        import json
        
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        prompt = SOCIAL_MEDIA_PROMPT.format(content=draft[:2000])  # Limit content length
        
        response = llm.invoke([{"role": "user", "content": prompt}])
        
        # Try to parse JSON response
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "telegram": response.content[:300],
                "facebook": response.content[:280],
                "twitter": response.content[:280]
            }
    except Exception as e:
        print(f"Error generating social snippets: {e}")
        return {
            "telegram": "Social media snippet generation failed",
            "facebook": "Social media snippet generation failed",
            "twitter": "Social media snippet generation failed"
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m agents.content_agent.main <outline_file>")
        sys.exit(1)
    
    outline_file = sys.argv[1]
    
    if not os.path.exists(outline_file):
        # Create outline from topic
        topic = outline_file
        outline = create_outline(topic)
        print(f"Created outline for: {topic}")
    else:
        # Read existing outline
        with open(outline_file, 'r') as f:
            outline = f.read()
        print(f"Read outline from: {outline_file}")
    
    # Expand to draft
    draft = expand_draft(outline)
    
    # Generate critique, SEO checklist, and social snippets
    critique = self_critique(draft)
    seo = seo_checklist(draft)
    social = generate_social_snippets(draft)
    
    # Save outputs
    output_dir = Path("out")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M")
    
    (output_dir / f"draft-{timestamp}.md").write_text(draft, encoding="utf-8")
    (output_dir / f"critique-{timestamp}.md").write_text(critique, encoding="utf-8")
    (output_dir / f"seo-{timestamp}.md").write_text(seo, encoding="utf-8")
    (output_dir / f"social-{timestamp}.json").write_text(
        json.dumps(social, ensure_ascii=False, indent=2), 
        encoding="utf-8"
    )
    
    print(f"✅ Generated draft, critique, SEO checklist, and social snippets in out/")

if __name__ == "__main__":
    import datetime
    from pathlib import Path
    main()
