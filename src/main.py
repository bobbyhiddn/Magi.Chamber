from flask import Flask, render_template, send_from_directory, abort
from chamber.core import MagiChamber
import os
from dotenv import load_dotenv
import markdown
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict

# Load environment variables
load_dotenv()

@dataclass
class NavItem:
    name: str
    path: str
    children: List['NavItem'] = field(default_factory=list)

def get_markdown_structure(markdown_dir: str) -> Dict[str, List[NavItem]]:
    """Get all markdown files organized by directory"""
    structure = {}
    
    if not os.path.exists(markdown_dir):
        print(f"Warning: Markdown directory not found at {markdown_dir}")
        return {}

    # Walk through the directory tree
    for root, dirs, files in os.walk(markdown_dir):
        rel_path = os.path.relpath(root, markdown_dir)
        if rel_path == '.':
            continue

        # Skip hidden directories
        if any(part.startswith('.') for part in rel_path.split(os.sep)):
            continue

        # Get the top-level section
        section = rel_path.split(os.sep)[0]
        
        if section not in structure:
            structure[section] = []

        # Add markdown files as navigation items
        for file in files:
            if file.endswith('.md') and not file.startswith('.'):
                name = os.path.splitext(file)[0]
                if name.lower() in ('readme', 'index'):
                    continue
                
                path = os.path.join('/page', rel_path, name).replace('\\', '/')
                structure[section].append(NavItem(
                    name=name.replace('_', ' ').title(),
                    path=path
                ))

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