from flask import Flask, jsonify, send_file, abort
from pathlib import Path
import hashlib
import os
import datetime
import logging
import re

class MagiChamber:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # Pretty print JSON
        
        # Setup logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        
        # Container paths
        self.grimoire = Path("grimoire/spells")
        self.archives = Path("archives")

    def _extract_spell_info(self, spell_path):
        """Extract spell information including proper docstring"""
        with open(spell_path, "r") as scroll:
            content = scroll.read()
            
            # Find the docstring after @click.command()
            matches = re.search(r'@click\.command\([^)]*\)\s*def\s+\w+\([^)]*\):\s*"""(.*?)"""', 
                              content, re.DOTALL)
            
            if matches:
                description = matches.group(1).strip()
            else:
                # Fallback to first docstring in file
                matches = re.search(r'"""(.*?)"""', content, re.DOTALL)
                description = matches.group(1).strip() if matches else "No description provided"
            
            return {
                "name": spell_path.stem,
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
                    spells.append(self._extract_spell_info(spell_path))
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