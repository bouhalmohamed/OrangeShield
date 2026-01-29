# OrangeShield - Protection d'Images contre l'IA

Application web Flask qui protège les images avec un double watermark (visible + invisible TrustMark) pour résister aux manipulations par les modèles IA.

## Structure du Projet

Le projet suit une architecture MVC :

```
orange/
├── app.py                 # Point d'entrée
├── config.py              # Configuration
├── controllers/           # Gestion des requêtes
├── models/                # Traitement d'images
├── services/              # Logique métier (watermark)
├── views/                 # Routes Flask et interface
│   ├── templates/
│   └── static/
├── utils/                 # Utilitaires
├── tests/                 # Tests unitaires et d'intégration
└── docker/                # Configuration Docker
```

## Installation

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. (Optionnel) Installer TrustMark pour le watermark invisible :
```bash
pip install trustmark
```

3. Lancer l'application :
```bash
python app.py
```

4. Accéder à `http://localhost:5000`

## Utilisation avec Docker

```bash
# Lancer en production
docker-compose -f docker/docker-compose.yml up -d

# Lancer en développement (hot-reload)
docker-compose -f docker/docker-compose.dev.yml up -d

# Arrêter
docker-compose -f docker/docker-compose.yml down
```

## Fonctionnalités

- **Watermark visible** : Texte avec semantic steering pour perturber les IA
- **Watermark invisible** : Encodage TrustMark pour vérification
- **Presets** : Default, Confidential, Copyright, Draft, Internal, Proof, Custom
- **Chaos noise** : Couche de bruit pour perturber les modèles de diffusion

## Tests

```bash
# Lancer tous les tests
pytest

# Avec rapport de couverture
pytest --cov=. --cov-report=html
```

## Technologies

- Flask 3.0
- Pillow (traitement d'images)
- NumPy
- TrustMark (optionnel)
