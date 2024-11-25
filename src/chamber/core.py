from flask import Flask, jsonify, send_file, abort, render_template
from pathlib import Path
import hashlib
import os
import datetime
import logging
import re
import ast

class MagiChamber:
    def __init__(self):
        # Ensure the template_folder is set correctly
        self.app = Flask(__name__, template_folder='templates')
        self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # Pretty print JSON
        
        # Setup logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        
        # Container paths
        self.grimoire = Path("grimoire/spells")
        self.archives = Path("archives")

    def _extract_spell_info(self, spell_path):
        """Extract spell information including Click command help text"""
        with open(spell_path, "r", encoding="utf-8") as scroll:
            content = scroll.read()
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                self.logger.error(f"Syntax error when parsing {spell_path}: {e}")
                return None

            command_name = None
            description = "No description found"
            alias = None

            # Iterate over all function definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check if the function has a @click.command() decorator
                    has_click_command = False
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                            if decorator.func.value.id == "click" and decorator.func.attr == "command":
                                has_click_command = True
                                break
                        elif isinstance(decorator, ast.Attribute):
                            if decorator.value.id == "click" and decorator.attr == "command":
                                has_click_command = True
                                break
                    if has_click_command:
                        # Found the command function
                        command_name = node.name
                        # Get the docstring
                        docstring = ast.get_docstring(node)
                        if docstring:
                            description = docstring.strip()
                        break  # Assuming only one command per file

            # Now look for 'alias' assignment at the module level
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "alias":
                            if isinstance(node.value, ast.Str):
                                alias = node.value.s
                            elif isinstance(node.value, ast.Constant):  # For Python 3.8+
                                alias = node.value.value
                            break

            if not command_name:
                self.logger.warning(f"No Click command found in {spell_path}")
                return None

            return {
                "name": spell_path.stem,
                "command": command_name,
                "alias": alias,
                "description": description,
                "hash": hashlib.sha256(spell_path.read_bytes()).hexdigest(),
                "last_modified": datetime.datetime.fromtimestamp(
                    os.path.getmtime(spell_path)
                ).isoformat(),
                "type": "spell"
            }

    def setup_routes(self):
        @self.app.route("/health", methods=["GET"])
        def chamber_health():
            """Simple health check endpoint"""
            return jsonify({
                "status": "operational",
                "timestamp": datetime.datetime.now().isoformat(),
                "version": "0.1.0",
                "spells_available": bool(list(self.grimoire.glob("*.py")))
            })

        @self.app.route("/spells", methods=["GET"])
        def list_spells():
            """Lists all available spells in the chamber"""
            spells = []
            
            if not self.grimoire.exists():
                return jsonify({"spells": [], "error": "Grimoire not found"})
            
            for spell_path in self.grimoire.glob("*.py"):
                try:
                    if spell_path.name == "__init__.py":
                        continue
                    spell_info = self._extract_spell_info(spell_path)
                    if spell_info['command']:  # Only format if we found a command
                        formatted_desc = f"{spell_info['name']}"
                        if spell_info['alias']:
                            formatted_desc += f": '{spell_info['alias']}'"
                        formatted_desc += f" - {spell_info['description']}"
                        spell_info['formatted_description'] = formatted_desc
                    spells.append(spell_info)
                except Exception as e:
                    self.logger.error(f"Error processing spell {spell_path}: {str(e)}", exc_info=True)
                    continue
                    
            return jsonify({
                "spells": sorted(spells, key=lambda x: x['name']),
                "count": len(spells),
                "timestamp": datetime.datetime.now().isoformat()
            })

        @self.app.route("/spells/<spell_name>", methods=["GET"])
        def get_spell(spell_name):
            """Retrieve a specific spell from the chamber"""
            spell_path = self.grimoire / f"{spell_name}.py"
            if not spell_path.exists():
                abort(404, description="Spell not found in chamber")
            return send_file(spell_path)

        @self.app.route("/manifest", methods=["GET"])
        def get_manifest():
            """Get a manifest of all spells and their hashes for syncing"""
            manifest = {
                "version": "0.1.0",
                "last_updated": datetime.datetime.now().isoformat(),
                "grimoire_status": "available" if self.grimoire.exists() else "unavailable",
                "spells": {}
            }
            
            if not self.grimoire.exists():
                return jsonify(manifest)
            
            for spell_path in self.grimoire.glob("*.py"):
                try:
                    if spell_path.name == "__init__.py":
                        continue
                    spell_info = self._extract_spell_info(spell_path)
                    manifest["spells"][spell_path.stem] = {
                        "hash": spell_info["hash"],
                        "modified": spell_info["last_modified"],
                        "description": spell_info["description"]
                    }
                except Exception as e:
                    self.logger.error(f"Error processing spell {spell_path}: {str(e)}")
                    continue
            
            manifest["spell_count"] = len(manifest["spells"])
            return jsonify(manifest)

        @self.app.route("/", methods=["GET"])
        def index():
            """Render the index page."""
            return render_template("index.html")