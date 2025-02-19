# **📌 Chat Sécurisé avec Chiffrement de Bout en Bout (E2EE) 🔐**  

Ce projet est une **application de chat sécurisée** utilisant un **chiffrement de bout en bout (E2EE)** avec **RSA** et **AES**. Il permet à plusieurs clients de communiquer **en toute confidentialité**, garantissant que seul le destinataire peut lire les messages.

---

## **🛠️ Technologies Utilisées**
- **Python** → Langage de programmation principal.
- **Sockets** → Communication réseau entre le serveur et les clients.
- **PyCryptodome** → Librairie de cryptographie utilisée pour RSA & AES.
- **Threading** → Permet au serveur de gérer plusieurs clients simultanément.
- **JSON** → Format pour structurer les messages envoyés.

---

## **📌 Fonctionnalités**
✅ **Chiffrement de bout en bout (E2EE)** → Personne d'autre ne peut lire les messages.  
✅ **RSA** → Utilisé pour **échanger la clé AES** en toute sécurité.  
✅ **AES** → Utilisé pour **chiffrer et déchiffrer les messages** envoyés.  
✅ **Serveur multi-clients** → Plusieurs clients peuvent discuter en même temps.  
✅ **Sécurité renforcée** → Les messages circulent uniquement sous forme chiffrée.  

---

## **🚀 Installation**
### **1️⃣ Cloner le projet**
```bash
git clone https://github.com/Moh-testit/Ourstap.git
```

### **2️⃣ Installer les dépendances**
Assure-toi d’avoir Python **3.x** installé, puis exécute :
```bash
pip install pycryptodome
```

---

## **📌 Comment utiliser le chat ?**
### **1️⃣ Démarrer le serveur**
Lance cette commande dans un terminal :
```bash
python chat.py server ou utiliser un venv l'executer dedans par exemple /Users/test/Ourstap/Ourstap/.venv/bin/python chat.py server
```
📌 **Le serveur écoutera sur `127.0.0.1:5555` et attendra des connexions.**

### **2️⃣ Ouvrir plusieurs clients**
Dans **deux autres terminaux**, exécute :
```bash
python script.py client
```
💡 **Chaque client génère sa propre clé RSA et reçoit une clé AES sécurisée.**

### **3️⃣ Envoyer un message**
Dans le terminal du client, tape un message :
```bash
Vous : Salut !
```
👀 **Le message sera envoyé chiffré au serveur et retransmis aux autres clients.**

---

## **🔐 Explication du Chiffrement**
1️⃣ **Le serveur génère une clé AES** et la **chiffre avec la clé publique RSA du client**.  
2️⃣ **Le client déchiffre la clé AES** avec sa clé privée.  
3️⃣ **Les messages sont ensuite chiffrés avec AES** avant d’être envoyés.  
4️⃣ **Les autres clients déchiffrent les messages** avec la même clé AES.  

📌 **Aucun intermédiaire (y compris le serveur) ne peut lire les messages en clair !**  

---

## **📌 Tests de Sécurité**
✅ **Vérifier que les messages sont chiffrés**  
Ajoute ces logs dans le client pour observer :
```python
print(f"[DEBUG] Message chiffré AES : {encrypted_message}")
```
✅ **Capturer le trafic réseau avec Wireshark ou tcpdump**  
Dans un terminal :
```bash
sudo tcpdump -i lo0 -A port 5555
```
📌 **Tu ne dois voir que des messages illisibles (chiffrés en AES).**

---

## **📌 Améliorations possibles 🚀**
🔹 Ajouter une **interface graphique (Tkinter, PyQt)**.  
🔹 Supporter **un chiffrement asymétrique plus robuste** (ECC, RSA-4096).  
🔹 Ajouter un **système d'authentification** pour identifier les utilisateurs.  

---

## **📌 Auteur & Licence**
👤 **Développé par : Mohamed Mazu]**  
📜 **Licence : MIT**  
📌 **Projet Open-Source - Contribuez et améliorez-le !** 🚀  

---

### **💬 Besoin d’aide ? Une suggestion ?**
Ouvre une **issue** sur GitHub ou contacte-moi ! 😊

---
🚀 **Bon chat sécurisé !** 🔐
