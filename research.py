import argparse
import os
from datetime import datetime
from pathlib import Path
from crew import ResearchCrew

def create_output_dir():
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def save_report(content, topic, output_format="markdown"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in topic)
    safe_topic = safe_topic.replace(' ', '_').lower()[:50]
    
    output_dir = create_output_dir()
    
    if output_format in ["markdown", "both"]:
        md_path = output_dir / f"{safe_topic}_{timestamp}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\nMarkdown report saved to: {md_path}")
    
    if output_format in ["pdf", "both"]:
        print("\nPDF export feature coming soon...")
    
    return content

def main():
    parser = argparse.ArgumentParser(description="AI Research Assistant - Multi-Agent Research System")
    parser.add_argument("topic", help="Research topic or question")
    parser.add_argument("--format", choices=["markdown", "pdf", "both"], 
                       default="markdown", help="Output format")
    parser.add_argument("--depth", choices=["basic", "moderate", "comprehensive"],
                       default="moderate", help="Research depth")
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"AI Research Assistant")
    print(f"{'='*60}")
    print(f"Topic: {args.topic}")
    print(f"Depth: {args.depth}")
    print(f"Format: {args.format}")
    print(f"{'='*60}\n")
    
    print("Initializing research crew...")
    crew = ResearchCrew()
    
    print("Starting research process...\n")
    result = crew.run(args.topic)
    
    print("\n" + "="*60)
    print("Research Complete!")
    print("="*60 + "\n")
    
    save_report(result, args.topic, args.format)
    
    print("\n" + "="*60)
    print("Process Summary:")
    print("- Research Agent: Gathered information")
    print("- Analyst Agent: Synthesized findings")
    print("- Writer Agent: Created report")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
