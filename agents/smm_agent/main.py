# agents/smm_agent/main.py
"""
SMM Agent - Social Media Marketing automation
Run: python -m agents.smm_agent.main "post.md"
"""
import os
import sys
import json
import datetime
from pathlib import Path

def extract_post_metadata(markdown_content):
    """Extract metadata from markdown post"""
    lines = markdown_content.split('\n')
    metadata = {
        'title': '',
        'description': '',
        'tags': [],
        'url': ''
    }
    
    for line in lines:
        if line.startswith('title:'):
            metadata['title'] = line.split(':', 1)[1].strip().strip('"')
        elif line.startswith('description:'):
            metadata['description'] = line.split(':', 1)[1].strip().strip('"')
        elif line.startswith('tags:'):
            tags_str = line.split(':', 1)[1].strip()
            metadata['tags'] = [t.strip() for t in tags_str.strip('[]').split(',')]
    
    return metadata

def generate_social_posts(metadata, content):
    """Generate social media posts"""
    if not os.getenv("OPENAI_API_KEY"):
        return {
            "telegram": f"📝 {metadata.get('title', 'New Post')}\n\n{metadata.get('description', 'Check out our latest post!')[:200]}...\n\nRead more: [URL]",
            "facebook": f"{metadata.get('title', 'New Post')}\n\n{metadata.get('description', 'Check out our latest post!')[:200]}...\n\nRead more: [URL]",
            "twitter": f"{metadata.get('title', 'New Post')}\n\n{metadata.get('description', 'Check out our latest post!')[:200]}...\n\n#blog #tech"
        }
    
    # TODO: Implement LLM social post generation
    return {
        "telegram": "Telegram post would be generated here",
        "facebook": "Facebook post would be generated here", 
        "twitter": "Twitter post would be generated here"
    }

def send_telegram_message(message):
    """Send message to Telegram"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set - skipping Telegram")
        return False
    
    try:
        import requests
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        response = requests.post(url, json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

def send_facebook_post(message):
    """Send post to Facebook Page"""
    token = os.getenv("FB_PAGE_TOKEN")
    
    if not token:
        print("FB_PAGE_TOKEN not set - skipping Facebook")
        return False
    
    # TODO: Implement Facebook API
    print("Facebook posting not implemented yet")
    return False

def send_twitter_tweet(message):
    """Send tweet to Twitter/X"""
    token = os.getenv("X_API_TOKEN")
    
    if not token:
        print("X_API_TOKEN not set - skipping Twitter")
        return False
    
    # TODO: Implement Twitter API
    print("Twitter posting not implemented yet")
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m agents.smm_agent.main <post.md>")
        sys.exit(1)
    
    post_file = sys.argv[1]
    
    if not os.path.exists(post_file):
        print(f"Post file not found: {post_file}")
        sys.exit(1)
    
    # Read post content
    with open(post_file, 'r') as f:
        content = f.read()
    
    # Extract metadata
    metadata = extract_post_metadata(content)
    
    # Generate social posts
    posts = generate_social_posts(metadata, content)
    
    # Send to platforms
    results = {
        "telegram": send_telegram_message(posts["telegram"]),
        "facebook": send_facebook_post(posts["facebook"]),
        "twitter": send_twitter_tweet(posts["twitter"])
    }
    
    # Save outputs
    output_dir = Path("out")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M")
    
    output_data = {
        "metadata": metadata,
        "posts": posts,
        "results": results,
        "timestamp": timestamp
    }
    
    (output_dir / f"smm-{timestamp}.json").write_text(
        json.dumps(output_data, ensure_ascii=False, indent=2), 
        encoding="utf-8"
    )
    
    print("Social media posts generated and sent:")
    for platform, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {platform}")
    
    print(f"Results saved to: out/smm-{timestamp}.json")

if __name__ == "__main__":
    main()
