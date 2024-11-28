from flask import Flask, render_template, send_from_directory, abort
from chamber.core import MagiChamber
import os
from dotenv import load_dotenv
import markdown  # Import the markdown library
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

def get_markdown_structure() -> Dict[str, List[NavItem]]:
    """Get all markdown files organized by directory"""
    markdown_dir = app.config['MARKDOWN_PAGES_DIR']
    structure = {}
    hierarchy = {}
    
    for path in Path(markdown_dir).rglob('*.md'):
        rel_path = path.relative_to(markdown_dir)
        parts = rel_path.parts
        
        section = parts[0] if len(parts) > 1 else 'main'
        
        if section not in hierarchy:
            hierarchy[section] = {}
            
        current_dict = hierarchy[section]
        for part in parts[1:-1]:
            if part not in current_dict:
                current_dict[part] = {}
            current_dict = current_dict[part]
            
        filename = path.stem
        current_dict[filename] = str(rel_path.with_suffix('')).replace('\\', '/')
    
    def dict_to_nav_items(d: dict) -> List[NavItem]:
        items = []
        for name, path_or_dict in sorted(d.items()):
            if isinstance(path_or_dict, str):
                items.append(NavItem(
                    name=name.replace('_', ' '),
                    path=path_or_dict,
                    children=[]
                ))
            else:
                children = dict_to_nav_items(path_or_dict)
                if children:
                    items.append(NavItem(
                        name=name.replace('_', ' '),
                        path=name,
                        children=children
                    ))
        return items
    
    for section, content in hierarchy.items():
        structure[section] = dict_to_nav_items(content)
    
    return structure

@app.context_processor
def inject_nav_structure():
    """Make nav_structure available to all templates"""
    return {'nav_structure': get_markdown_structure()}

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8888))
    app.run(host='0.0.0.0', port=port)
