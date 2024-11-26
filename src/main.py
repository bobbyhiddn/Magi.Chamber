from flask import Flask, render_template, send_from_directory, abort
from chamber.core import MagiChamber
import os
from dotenv import load_dotenv
import markdown  # Import the markdown library
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict

# Load environment variables
load_dotenv()

@dataclass
class Page:
    name: str
    path: str

def create_app():
    """Initialize and configure the Magi.Chamber server"""
    chamber = MagiChamber()
    chamber.setup_routes()
    
    # Basic configuration
# In main.py
    chamber.app.config.update(
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max-size
        JSON_SORT_KEYS=False,
        SECRET_KEY=os.getenv('FLASK_SECRET_KEY'),
        # Update this line to point to the correct directory
        MARKDOWN_PAGES_DIR=os.path.join(os.path.dirname(__file__), 'chamber', 'pages')
    )

    # Add route for serving markdown pages
    @chamber.app.route('/page/<path:page_name>')
    def render_markdown_page(page_name):
        """Render a markdown page as HTML."""
        markdown_dir = chamber.app.config['MARKDOWN_PAGES_DIR']
        md_file = os.path.join(markdown_dir, f"{page_name}.md")
        
        if not os.path.exists(md_file):
            abort(404)

        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert markdown to HTML with syntax highlighting
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

        return render_template('markdown_page.html', content=html_content, title=page_name.replace('_', ' ').title())

    return chamber.app

app = create_app()

def get_markdown_structure() -> Dict[str, List[Page]]:
    """Get all markdown files organized by directory"""
    markdown_dir = app.config['MARKDOWN_PAGES_DIR']
    structure = {}
    
    for path in Path(markdown_dir).rglob('*.md'):
        # Get relative path from markdown dir
        rel_path = path.relative_to(markdown_dir)
        # Get section (folder name or 'main' for root files)
        section = rel_path.parent.name if rel_path.parent.name else 'main'
        # Get page name without .md extension
        page_name = path.stem
        # Get full path for URL without .md extension
        page_path = str(rel_path.with_suffix('')).replace('\\', '/')
        
        if section not in structure:
            structure[section] = []
        
        structure[section].append(Page(
            name=page_name.replace('_', ' '),
            path=page_path
        ))
    
    return structure

@app.context_processor
def inject_nav_structure():
    """Make nav_structure available to all templates"""
    return {'nav_structure': get_markdown_structure()}

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8888))
    app.run(host='0.0.0.0', port=port)
