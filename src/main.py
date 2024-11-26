from flask import Flask, render_template, send_from_directory, abort
from chamber.core import MagiChamber
import os
from dotenv import load_dotenv
import markdown  # Import the markdown library

# Load environment variables
load_dotenv()

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

        # Convert markdown to HTML
        html_content = markdown.markdown(
                md_content, 
                extensions=['fenced_code', 'codehilite', 'toc']
            )


        return render_template('markdown_page.html', content=html_content, title=page_name.replace('_', ' ').title())

    return chamber.app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8888))
    app.run(host='0.0.0.0', port=port)
