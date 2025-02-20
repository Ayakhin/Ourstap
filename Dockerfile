# Utilisation d'une image Python complète avec les outils nécessaires pour la compilation
FROM python:3.9

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système requises
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    python3-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source dans le conteneur
COPY . .

# Exposer le port utilisé par le serveur
EXPOSE 5555

# Commande par défaut pour lancer le serveur
CMD ["python", "chat.py", "server"]
