# Docker - OrangeShield

## Prérequis

- Docker Engine 20.10+
- Docker Compose 2.0+

## Démarrage rapide

### Production
```bash
docker-compose -f docker/docker-compose.yml up -d
```

### Développement (avec hot-reload)
```bash
docker-compose -f docker/docker-compose.dev.yml up -d
```

### Build manuel
```bash
docker build -f docker/Dockerfile -t orangep:latest .
docker run -d -p 5000:5000 orangep:latest
```

## Variables d'environnement

| Variable | Défaut | Description |
|----------|--------|-------------|
| `PORT` | `5000` | Port du serveur |
| `HOST` | `0.0.0.0` | Adresse d'écoute |
| `FLASK_DEBUG` | `False` | Mode debug |

## Commandes utiles

```bash
# Voir les logs
docker-compose -f docker/docker-compose.yml logs -f

# Arrêter
docker-compose -f docker/docker-compose.yml down

# Rebuild
docker-compose -f docker/docker-compose.yml build --no-cache
```
