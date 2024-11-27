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
    children: Dict[str, List['Page']]  # For subfolders
    is_folder: bool = False

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

def get_markdown_structure() -> Dict[str, Page]:
    """Get all markdown files organized by directory with nested structure"""
    markdown_dir = app.config['MARKDOWN_PAGES_DIR']
    structure = {}
    
    # Helper function to get or create a folder in the structure
    def get_or_create_folder(folder_path: str, parent_dict: Dict[str, Page]) -> Page:
        folder_name = folder_path.split('/')[-1] or 'main'
        if folder_name not in parent_dict:
            parent_dict[folder_name] = Page(
                name=folder_name.replace('_', ' '),
                path=folder_path,
                children={},
                is_folder=True
            )
        return parent_dict[folder_name]

    for path in Path(markdown_dir).rglob('*.md'):
        # Get relative path from markdown dir
        rel_path = path.relative_to(markdown_dir)
        parts = list(rel_path.parts)
        
        # Handle files in root directory
        if len(parts) == 1:
            if 'main' not in structure:
                structure['main'] = Page(
                    name='Main',
                    path='',
                    children={},
                    is_folder=True
                )
            structure['main'].children[path.stem] = Page(
                name=path.stem.replace('_', ' '),
                path=path.stem,
                children={},
            )
            continue

        # Handle files in subdirectories
        current_dict = structure
        current_path = []
        
        # Process all folder levels except the last part (filename)
        for part in parts[:-1]:
            current_path.append(part)
            folder = get_or_create_folder('/'.join(current_path), current_dict)
            current_dict = folder.children

        # Add the file to the last folder
        file_name = parts[-1].replace('.md', '')
        current_dict[file_name] = Page(
            name=file_name.replace('_', ' '),
            path='/'.join(parts[:-1] + [file_name]),
            children={},
        )

    return structure

@app.context_processor
def inject_nav_structure():
    """Make nav_structure available to all templates"""
    return {'nav_structure': get_markdown_structure()}

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8888))
    app.run(host='0.0.0.0', port=port)
