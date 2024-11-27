# Magi.Chamber

A Flask-based repository service for MAGI CLI spells, providing both an API for spell distribution and documentation hosting. The chamber serves as both a spell repository and documentation hub, accessible at:

- [magi-chamber.fly.dev](https://magi-chamber.fly.dev)

## Architecture

The system consists of three main components:

1. **Chamber** - The Flask web application that serves spells and documentation
2. **Grimoire** - Git submodule containing the spell collection ([Magi.Spells](https://github.com/bobbyhiddn/Magi.Spells))
3. **Library** - Git submodule containing documentation ([Magi.Library](https://github.com/bobbyhiddn/Magi.Library))

## Setup

1. Create environment variables:
```bash
# Generate a Flask secret key
python utils/flask_keygen.py > .env

# Add required environment variables
FLASK_SECRET_KEY="<generated-key>"
CHAMBER_API_KEY="<github-pat>"
WEBHOOK_SECRET="<webhook-secret>"
```

2. Local development:
```bash
# Start the chamber
docker-compose up --build
```

3. Deployment:
```bash
# First time setup
fly launch

# Deploy
./fly_deploy.sh
```

## API Endpoints

- `GET /health` - Chamber status check
- `GET /spells` - List all available spells
- `GET /spells/<spell_name>` - Retrieve a specific spell
- `GET /manifest` - Get spell manifest for syncing

## Development

The chamber follows the Flask to Fly.io framework for development and deployment. Key components:

- `src/chamber/core.py` - Main server logic
- `src/main.py` - Application entry point
- `Dockerfile` & `docker-compose.yml` - Container configuration
- `fly_deploy.sh` - Deployment script

## Structure

```
magi-chamber/
├── src/
│   ├── chamber/           # Core server code
│   ├── grimoire/         # Spell storage
│   ├── archives/         # Version history
│   └── main.py          # Entry point
├── Dockerfile
├── docker-compose.yml
└── fly_deploy.sh
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Add your spells to the grimoire
4. Commit your changes
5. Push to the branch
6. Create a Pull Request