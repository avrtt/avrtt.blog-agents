# agents/vector_search/cli.py
"""
CLI tool for vector search operations
"""
import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Vector Search CLI")
    parser.add_argument("command", choices=["search", "stats", "add"], help="Command to execute")
    parser.add_argument("--query", "-q", help="Search query")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Number of results to return")
    parser.add_argument("--type", "-t", choices=["posts", "sources"], default="sources", help="Type to search")
    
    args = parser.parse_args()
    
    try:
        from .lancedb_client import vector_client
        
        if args.command == "search":
            if not args.query:
                print("Error: --query is required for search command")
                sys.exit(1)
            
            if args.type == "posts":
                results = vector_client.search_posts(args.query, args.limit)
            else:
                results = vector_client.search_sources(args.query, args.limit)
            
            print(f"\n🔍 Search results for: '{args.query}'")
            print(f"Found {len(results)} results\n")
            
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['title']}")
                print(f"   URL: {result['url']}")
                print(f"   Score: {result['score']:.4f}")
                print(f"   Content: {result['content'][:200]}...")
                print()
        
        elif args.command == "stats":
            stats = vector_client.get_stats()
            print("\n📊 Vector Database Statistics")
            print(f"Posts: {stats['posts']}")
            print(f"Sources: {stats['sources']}")
            print()
        
        elif args.command == "add":
            print("Add command not implemented yet")
            print("Use the research agent to automatically add sources")
        
    except ImportError:
        print("Error: Vector search dependencies not installed")
        print("Install with: pip install lancedb sentence-transformers")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
