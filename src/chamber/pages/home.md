# Welcome to the Magi Chamber

*A mystical nexus where arcane knowledge takes form*

## About the Chamber

The Magi Chamber serves as an ethereal repository of magical command-line spells, a sanctum where digital incantations are stored and shared among practitioners of the terminal arts. Here, spells are carefully curated, preserved, and made available to those who seek to enhance their command-line prowess.

## Our Purpose

- **Spell Repository**: We maintain a collection of powerful command-line spells, each crafted to automate and enhance your daily tasks
- **Knowledge Exchange**: A gathering place for magi to share their craft and discover new magical techniques
- **Arcane Synchronization**: Through our mystical APIs, we ensure your local grimoire stays in harmony with our central chamber

## Available Services

### For Apprentice Magi
- Browse our collection of beginner-friendly spells
- Learn the basics of spell crafting
- Understand the principles of command-line magic

### For Advanced Practitioners
- Access powerful automation spells
- Contribute your own magical creations
- Synchronize with remote spell repositories

## Getting Started

To begin your journey:

1. Install the Magi CLI tool:
```bash
pip install magi_cli_pypi
```

2. Clone your local sanctum:
```bash
git clone https://github.com/bobbyhiddn/Magi.CLI ~/.sanctum
```

3. Initialize your environment:
```bash
cast initialize
```

## System Architecture

### Directory Structure

Your local sanctum (~/.sanctum) contains several mystical directories:

- `.tome/` - Your personal grimoire of spell macros
- `.orb/` - A crystalline cache of downloaded spells
- `.runes/` - Mystical GUI elements for visual spell casting
- `.aether/` - Records of your conversations with the ethereal AI
- `.graveyard/` - Recovery zone for banished files

### Spell Management

The Chamber employs a zero-trust distribution system:

1. **Verification** - All spells are cryptographically verified
2. **Dependencies** - Explicit approval required for new dependencies
3. **Caching** - Local spell storage in your .orb directory
4. **Updates** - Automatic version checking via manifest hashes

### Security Measures

- HMAC verification for all webhook communications
- Manifest hash validation for spell integrity
- Dependency declaration and approval system
- Secure API communication protocols

## Advanced Usage

### Self-Hosting

You can host your own Chamber instance:

```bash
docker pull ghcr.io/bobbyhiddn/magi.chamber:latest
docker run -p 5000:5000 magi.chamber
```

### Development

Contributing to the Chamber:

1. Fork the repository
2. Set up local development environment:
```bash
git clone https://github.com/yourusername/Magi.Chamber
cd Magi.Chamber
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. Start local server:
```bash
flask run
```

## API Documentation

The Chamber exposes these mystical endpoints:

- `GET /health` - Check server vitality
- `GET /spells` - View available spells
- `GET /manifest` - Retrieve spell versions
- `GET /spells/<name>` - Fetch specific spell
- `POST /webhook` - Handle spell updates

For detailed API documentation, visit `/docs` on your Chamber instance.