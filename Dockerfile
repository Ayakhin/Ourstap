# Utilisation d'une image Python légère
FROM python:3.9-slim

# Définition du répertoire de travail
WORKDIR /app

# Copie des fichiers nécessaires
COPY requirements.txt .

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Exposition du port
EXPOSE 5555

# Commande de démarrage
ENTRYPOINT ["python", "chat.py", "server"]
