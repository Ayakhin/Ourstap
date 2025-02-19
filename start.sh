#!/bin/bash

# Démarrer le serveur en arrière-plan
python3 chat.py server &

# Attendre que le serveur soit prêt (par exemple, 2 secondes)
sleep 2

# Lancer deux clients en arrière-plan
python3 chat.py client &
python3 chat.py client &

# Attendre que les processus se terminent
wait
