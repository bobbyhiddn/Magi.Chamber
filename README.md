# Magi.Chamber

A mystical repository for MAGI CLI spells, serving as the astral plane where spells reside until pondered by magi.

It serves as both a spell repository and a devlog for the MAGI CLI project at this site:

- [Magi.Chamber.fly.dev](https://magi-chamber.fly.dev)

## Setup

1. Create your .env file:
```bash
# Generate a secure key
python flask_keygen.py > .env
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