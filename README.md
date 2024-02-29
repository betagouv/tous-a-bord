# Tous à bord !

## Introduction

L'application web qui soutient le produit "Tous à bord !".

## Installation

### PostgreSQL

Installer PostgreSQL en fonction de votre OS : https://www.postgresql.org/download/
puis créer une base de données au nom choisi dans DATABASE_NAME de votre fichier .env.

### pre-commit

[Pre-commit](https://pre-commit.com/) permet de linter et formatter votre code avant chaque commit. Par défaut ici, il exécute :

- [black](https://github.com/psf/black) pour formatter automatiquement vos fichiers .py en conformité avec la PEP 8 (gestion des espaces, longueur des lignes, etc)
- [flake8](https://github.com/pycqa/flake8) pour soulever les "infractions" restantes (import non utilisés, etc)
- [isort](https://github.com/pycqa/isort) pour ordonner vos imports

Pour l'installer :

```bash
pre-commit install
```

Vous pouvez effectuer un premier passage sur tous les fichiers du repo avec :

```bash
pre-commit run --all-files
```

### Installation locale

```bash
# Copier les variables d'environnement 
cp .env.example .env

# Initialiser et activez l'environnement Python
python -m venv venv
. venv/bin/activate

# Installer les packages nécessaires
pip install -r requirements.txt

# Effectuer les migrations pour initialiser la base de données
python manage.py migrate
```

## Utilisation 

### Lancement du serveur en local
```bash

# Si vous n'êtes pas déjà dans l'environnement Python
. venv/bin/activate

# Lancer le serveur
python manage.py runserver
```

### Exécuter les tests manuellement
```bash
python manage.py test
```
