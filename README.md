# OrangeShield

Application web de protection des documents administratifs contre les manipulations par intelligence artificielle, développée dans le cadre d'un projet industriel chez Orange.

## Problématique

### Sécurité des documents administratifs

Les documents administratifs (cartes d'identité, passeports, attestations, certificats) sont des cibles privilégiées pour la fraude documentaire. Traditionnellement, ces documents sont protégés par des watermarks visibles ou invisibles pour garantir leur authenticité.

### Menace de l'IA générative

L'émergence des modèles d'IA génératifs (Stable Diffusion, DALL-E, Midjourney) a radicalement changé la donne. Ces outils permettent désormais de :
- Supprimer des watermarks visibles en quelques secondes
- Reconstruire des zones masquées de manière réaliste
- Modifier le contenu de documents tout en préservant leur apparence authentique

### Insuffisance des watermarks traditionnels

Une étude scientifique récente a démontré que les techniques de watermarking conventionnelles sont vulnérables face aux modèles de diffusion. Les chercheurs ont montré que ces modèles peuvent apprendre à identifier et supprimer les patterns de watermark classiques avec un taux de succès élevé, rendant ces protections obsolètes.

**C'est de ce constat qu'est née l'idée d'OrangeShield** : développer une nouvelle approche de protection qui exploite les faiblesses des modèles IA plutôt que de simplement tenter de leur résister.

## Notre approche

OrangeShield implémente une stratégie de protection en trois couches qui rend les documents résistants aux attaques par IA générative.

### 1. Intégration de Motifs Zèbre

Des silhouettes de zèbres sont intégrées de manière subtile dans le document. Cette technique exploite une faiblesse connue des modèles de diffusion : leur difficulté à gérer des motifs répétitifs complexes avec des contrastes marqués. Lors d'une tentative de reconstruction, ces motifs créent une confusion sémantique qui dégrade significativement le résultat.

### 2. Watermark Visible avec Semantic Steering

Un watermark textuel contenant des instructions de "steering" est appliqué sur le document. Si un modèle IA tente de supprimer ce watermark, les instructions encodées interfèrent avec le processus de génération et provoquent des artefacts visibles dans l'image reconstruite.

### 3. Encodage TrustMark

TrustMark encode un message invisible dans le document, permettant de vérifier son authenticité même après des transformations (compression, redimensionnement, impression/scan). Cette couche permet de détecter si un document a été altéré.

## Prérequis

- Python 3.9 ou supérieur
- TrustMark (requis pour l'encodage invisible)
- 500 Mo d'espace disque minimum

## Installation

### Environnement local

```bash
# Cloner le dépôt
git clone https://github.com/bouhalmohamed/OrangeShield.git
cd OrangeShield

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
OrangeShield/
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
2. Importer un document (formats : JPG, PNG, WebP, GIF)
3. Sélectionner le type de document ou personnaliser les paramètres
4. Ajuster la densité et l'opacité du motif zèbre selon le besoin
5. Appliquer la protection
6. Télécharger le document protégé

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

Projet réalisé dans le cadre d'un projet industriel chez Orange.
