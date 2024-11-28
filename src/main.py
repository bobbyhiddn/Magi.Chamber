from flask import Flask, render_template, send_from_directory, abort
from chamber.core import MagiChamber
import os
from dotenv import load_dotenv
import markdown
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()

@dataclass
class NavItem:
    name: str
    path: str
    children: List['NavItem'] = field(default_factory=list)

def create_nav_tree(root_dir: str, current_dir: str) -> List[NavItem]:
    """Recursively create navigation tree for a directory"""
    items = []
    
    try:
        for entry in os.scandir(current_dir):
            # Skip hidden files and directories
            if entry.name.startswith('.'):
                continue
                
            # Get path relative to root markdown directory for URLs
            rel_path = os.path.relpath(entry.path, root_dir)
            
            if entry.is_dir():
                # Process directory
                children = create_nav_tree(root_dir, entry.path)
                if children:  # Only add directories that have markdown files
                    items.append(NavItem(
                        name=entry.name.replace('_', ' ').title(),
                        path=rel_path,
                        children=children
                    ))
            elif entry.is_file() and entry.name.endswith('.md'):
                # Process markdown file
                name = os.path.splitext(entry.name)[0]
                if name.lower() not in ('readme', 'index'):
                    items.append(NavItem(
                        name=name.replace('_', ' ').title(),
                        path=f"/page/{rel_path[:-3]}",  # Remove .md extension
                        children=[]
                    ))
                    
    except Exception as e:
        print(f"Error creating nav tree for {current_dir}: {e}")
        
    return sorted(items, key=lambda x: x.name)

def get_markdown_structure(markdown_dir: str) -> Dict[str, List[NavItem]]:
    """Get all markdown files organized by directory"""
    structure = {}
    
    if not os.path.exists(markdown_dir):
        print(f"Warning: Markdown directory not found at {markdown_dir}")
        return {}

    # Get top-level directories
    try:
        for entry in os.scandir(markdown_dir):
            if entry.is_dir() and not entry.name.startswith('.'):
                nav_items = create_nav_tree(markdown_dir, entry.path)
                if nav_items:
                    structure[entry.name] = nav_items
                    
    except Exception as e:
        print(f"Error getting markdown structure: {e}")

    return structure

def create_app():
    """Initialize and configure the Magi.Chamber server"""
    chamber = MagiChamber()
    chamber.setup_routes()
    
    # Get the absolute path to the src directory
    src_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Basic configuration with corrected markdown pages path
    markdown_dir = os.path.join(src_dir, 'modules', 'pages')
    
    chamber.app.config.update(
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max-size
        JSON_SORT_KEYS=False,
        SECRET_KEY=os.getenv('FLASK_SECRET_KEY'),
        MARKDOWN_PAGES_DIR=markdown_dir
    )

    # Debug print to verify the path
    print(f"Markdown Pages Directory: {markdown_dir}")

    # Add route for serving markdown pages
    @chamber.app.route('/page/<path:page_name>')
    def render_markdown_page(page_name):
        """Render a markdown page as HTML."""
        markdown_dir = chamber.app.config['MARKDOWN_PAGES_DIR']
        
        # Try different possible paths for the markdown file
        possible_paths = [
            os.path.join(markdown_dir, f"{page_name}.md"),
            os.path.join(markdown_dir, page_name, "index.md"),
            os.path.join(markdown_dir, f"{page_name}/README.md")
        ]

        md_file = None
        for path in possible_paths:
            if os.path.exists(path):
                md_file = path
                break

        if not md_file:
            print(f"404: No markdown file found at paths: {possible_paths}")
            abort(404)

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()

            # Convert markdown to HTML with additional extensions
            html_content = markdown.markdown(
                md_content, 
                extensions=[
                    'fenced_code',
                    'codehilite',
                    'tables',
                    'nl2br',
                    'toc'
                ],
                extension_configs={
                    'codehilite': {
                        'css_class': 'highlight',
                        'guess_lang': True,
                        'use_pygments': True,
                        'noclasses': False
                    }
                }
            )

            # Get the title from the page name
            title = page_name.split('/')[-1].replace('_', ' ').title()
            
            return render_template(
                'markdown_page.html',
                content=html_content,
                title=title,
                nav_structure=get_markdown_structure(markdown_dir)
            )
        except Exception as e:
            print(f"Error rendering markdown page: {e}")
            abort(500)

    @chamber.app.context_processor
    def inject_nav_structure():
        """Make nav_structure available to all templates"""
        return {
            'nav_structure': get_markdown_structure(markdown_dir),
            'title': 'Magi Chamber'
        }

    return chamber.app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8888))
    app.run(host='0.0.0.0', port=port)