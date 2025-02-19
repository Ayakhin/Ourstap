# Utiliser une image Python comme base
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

COPY chat.py .

# Copier le reste du code
COPY . .


CMD ["python", "chat.py"]
