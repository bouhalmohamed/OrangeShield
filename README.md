# OrangeShield

Application web de protection d'images contre les manipulations par intelligence artificielle, développée dans le cadre d'un stage de 6 mois chez Orange.

## Contexte

Avec l'essor des modèles génératifs (Stable Diffusion, DALL-E, Midjourney), la manipulation d'images est devenue triviale. OrangeShield propose une solution de protection multi-couches qui rend les images résistantes aux tentatives de modification par IA.

## Système de Protection

L'application implémente trois niveaux de protection complémentaires :

### 1. Intégration de Motifs Zèbre

Des silhouettes de zèbres sont intégrées de manière subtile dans l'image. Cette technique exploite la difficulté des modèles de diffusion à gérer des motifs répétitifs complexes, créant une confusion sémantique lors des tentatives de reconstruction.

### 2. Watermark Visible avec Semantic Steering

Un watermark textuel est appliqué avec des instructions de "steering" destinées à perturber les modèles IA. Si un modèle tente de supprimer le watermark, les instructions encodées provoquent une dégradation de l'image reconstruite.

### 3. Encodage TrustMark

TrustMark encode un message invisible dans l'image, permettant de vérifier son authenticité. Ce watermark résiste aux transformations courantes (compression, redimensionnement, capture d'écran).

## Prérequis

- Python 3.9 ou supérieur
- TrustMark (requis pour l'encodage invisible)
- 500 Mo d'espace disque minimum

## Installation

### Environnement local

```bash
# Cloner le dépôt
git clone https://github.com/[username]/orangeshield.git
cd orangeshield

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

Accéder à http://localhost:5000

### Docker

```bash
# Mode production
docker-compose -f docker/docker-compose.yml up -d

# Mode développement avec hot-reload
docker-compose -f docker/docker-compose.dev.yml up -d

# Arrêter
docker-compose -f docker/docker-compose.yml down
```

## Architecture

```
orangeshield/
├── app.py                      # Point d'entrée Flask
├── config.py                   # Configuration centralisée
├── requirements.txt            # Dépendances Python
├── zebra.png                   # Image source pour motif zèbre
│
├── controllers/
│   └── watermark_controller.py # Validation et traitement des requêtes
│
├── models/
│   └── image_processor.py      # Manipulation d'images bas niveau
│
├── services/
│   ├── watermark_service.py    # Orchestration des protections
│   ├── zebra_service.py        # Intégration motifs zèbre
│   └── trustmark_service.py    # Encodage TrustMark
│
├── views/
│   ├── routes.py               # Endpoints HTTP
│   ├── templates/              # Templates Jinja2
│   └── static/                 # CSS, JS, images
│
├── utils/
│   ├── constants.py            # Constantes et presets
│   └── file_utils.py           # Utilitaires fichiers
│
├── tests/
│   ├── unit/                   # Tests unitaires
│   └── integration/            # Tests d'intégration
│
└── docker/
    ├── Dockerfile              # Image production
    ├── Dockerfile.dev          # Image développement
    └── docker-compose.yml      # Orchestration
```

## Utilisation

1. Ouvrir l'interface web
2. Glisser-déposer ou sélectionner une image (formats : JPG, PNG, WebP, GIF)
3. Sélectionner un preset de document ou personnaliser les paramètres
4. Ajuster la densité et l'opacité du motif zèbre
5. Appliquer la protection
6. Télécharger l'image protégée

### Presets disponibles

| Preset | Usage |
|--------|-------|
| Default | Protection standard |
| Confidential | Documents sensibles |
| Copyright | Protection droits d'auteur |
| Draft | Versions de travail |
| Internal | Usage interne uniquement |
| Proof | Épreuves et maquettes |
| Custom | Paramètres personnalisés |

## Tests

```bash
# Exécuter tous les tests
pytest

# Avec rapport de couverture
pytest --cov=. --cov-report=html

# Tests unitaires uniquement
pytest tests/unit/

# Tests d'intégration
pytest tests/integration/

# Test spécifique
pytest tests/unit/test_zebra_service.py -v
```

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | Flask 3.0 |
| Traitement image | Pillow, NumPy |
| Watermark invisible | TrustMark |
| Frontend | HTML5, CSS3, JavaScript |
| Containerisation | Docker |

## Auteur

Projet réalisé dans le cadre d'un stage chez Orange.
