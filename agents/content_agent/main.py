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
    
    # TODO: Implement LLM outline generation
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
    
    # TODO: Implement LLM draft expansion
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
    
    # TODO: Implement LLM self-critique
    return "Self-critique would be generated here"

def seo_checklist(draft):
    """Generate SEO checklist"""
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
    
    # Generate critique and SEO checklist
    critique = self_critique(draft)
    seo = seo_checklist(draft)
    
    # Save outputs
    output_dir = Path("out")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M")
    
    (output_dir / f"draft-{timestamp}.md").write_text(draft, encoding="utf-8")
    (output_dir / f"critique-{timestamp}.md").write_text(critique, encoding="utf-8")
    (output_dir / f"seo-{timestamp}.md").write_text(seo, encoding="utf-8")
    
    print(f"Generated draft, critique, and SEO checklist in out/")

if __name__ == "__main__":
    import datetime
    from pathlib import Path
    main()
