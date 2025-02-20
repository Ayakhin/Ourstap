

---

# **🔐 Chat Sécurisé avec Chiffrement de Bout en Bout (E2EE)**
Ce projet est une **application de chat sécurisée** utilisant un **chiffrement de bout en bout (E2EE)** avec **RSA** et **AES**. Il permet à plusieurs clients de communiquer **en toute confidentialité**, garantissant que seul le destinataire peut lire les messages.

---

## **📌 Technologies Utilisées**
- **Python** → Langage de programmation principal.
- **Sockets** → Communication entre le serveur et les clients.
- **PyCryptodome** → Librairie de cryptographie utilisée pour RSA & AES.
- **Threading** → Permet au serveur de gérer plusieurs clients simultanément.
- **JSON** → Format pour structurer les messages envoyés.
- **Unittest & Mock** → Framework de tests pour garantir la robustesse de l'application.

---

## **📌 Fonctionnalités**
✅ **Chiffrement de bout en bout (E2EE)** → Personne d'autre ne peut lire les messages.  
✅ **RSA** → Utilisé pour **échanger la clé AES** en toute sécurité.  
✅ **AES** → Utilisé pour **chiffrer et déchiffrer les messages** envoyés.  
✅ **Serveur multi-clients** → Plusieurs clients peuvent discuter en même temps.  
✅ **Sécurité renforcée** → Les messages circulent uniquement sous forme chiffrée.  
✅ **Tests unitaires et d'intégration** → Vérification automatique du bon fonctionnement.  

---

## **📌 Installation**
### **1️⃣ Cloner le projet**
```bash
git clone https://github.com/ton-repo/chat-e2ee.git
cd chat-e2ee
```

### **2️⃣ Installer les dépendances**
Assurez-vous d’avoir **Python 3.x** installé, puis exécutez :
```bash
pip install -r requirements.txt
```

Si vous utilisez un **environnement virtuel** :
```bash
python -m venv env
source env/bin/activate  # Sur Linux/Mac
env\Scripts\activate  # Sur Windows
pip install -r requirements.txt
```

---

## **📌 Comment utiliser le chat ?**
### **1️⃣ Démarrer le serveur**
Lancez cette commande dans un terminal :
```bash
python chat.py server
```
📌 **Le serveur écoutera sur `127.0.0.1:5555` et attendra des connexions.**

### **2️⃣ Ouvrir plusieurs clients**
Dans **deux autres terminaux**, exécutez :
```bash
python chat.py client
```
💡 **Chaque client génère sa propre clé RSA et reçoit une clé AES sécurisée.**

### **3️⃣ Envoyer un message**
Dans le terminal du client, tapez un message :
```bash
Vous : Salut !
```
👀 **Le message sera envoyé chiffré au serveur et retransmis aux autres clients.**

---

# **📌 Vérification des Tests : Unit Testing & Mock Testing**
Ce projet inclut des tests pour **garantir la conformité avec la consigne de tests** demandée.

### **📌 1️⃣ Exécuter tous les tests**
Lancez la commande suivante pour exécuter **tous les tests unitaires et d'intégration** :
```bash
python -m unittest discover
```
Si tout fonctionne correctement, vous devriez voir :
```
..
----------------------------------------------------------------------
Ran X tests in Y.YYYs

OK
```

---

### **📌 2️⃣ Vérifier la couverture des tests**
Nous devons nous assurer que **toutes les fonctionnalités critiques sont couvertes**.

1️⃣ Installez `coverage` si ce n'est pas encore fait :
```bash
pip install coverage
```
2️⃣ Exécutez les tests avec couverture :
```bash
coverage run -m unittest discover
```
3️⃣ Affichez le rapport :
```bash
coverage report -m
```
📌 **Le taux de couverture doit être proche de 100%**. Si certaines lignes ne sont pas couvertes, ajoutez des tests pour celles-ci.

---

### **📌 3️⃣ Vérifier les Tests Unitaires**
Les tests unitaires se trouvent dans **`test_chat.py`** et **`test_crypto.py`**.
Ils testent les fonctionnalités suivantes :

| Fonction | Description | Testé dans |
|----------|------------|------------|
| `encrypt_rsa()` | Chiffrement RSA | `test_chat.py` |
| `decrypt_rsa()` | Déchiffrement RSA | `test_chat.py` |
| `encrypt_aes()` | Chiffrement AES | `test_crypto.py` |
| `decrypt_aes()` | Déchiffrement AES | `test_crypto.py` |

📌 **Pour exécuter uniquement les tests unitaires :**
```bash
python test_chat.py
python test_crypto.py
```
✅ Si tout fonctionne, les tests passent sans erreur.

---

### **📌 4️⃣ Vérifier les Tests d'Intégration**
Les **tests d'intégration** vérifient si **le serveur et les clients communiquent correctement**.

📌 **Exécutez le test d'intégration avec :**
```bash
python test_integration.py
```
💡 **Ce test :**
- Lance un serveur.
- Connecte **deux clients automatiquement**.
- Envoie un message de **Client 1 → Client 2**.
- Vérifie que **Client 2 reçoit et déchiffre correctement le message**.

✅ **Si le message est reçu correctement, le test est réussi.**

---

## **📌 Autres Vérifications : Debug et Capture des Messages**
Pour s’assurer que les messages sont bien chiffrés :
1️⃣ **Activez les logs de debug** en ajoutant :
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
2️⃣ **Utilisez Wireshark ou tcpdump** pour capturer les paquets réseau :
```bash
sudo tcpdump -i lo0 port 5555 -A
```
📌 **Les messages capturés doivent être illisibles (chiffrés en AES).**

---

## **📌 Résumé : Comment Vérifier que les Tests Respectent la Consigne**
✔ **Exécuter `unittest` pour valider les tests unitaires et d'intégration.**  
✔ **Utiliser `coverage` pour s’assurer d’une couverture maximale.**  
✔ **Utiliser `mock.patch` pour isoler les dépendances réseau.**  
✔ **Observer les logs et capturer le trafic réseau pour valider le chiffrement.**  

🚀 **Si tous ces critères sont validés, nous avons bien respecté la consigne des tests !**

---

## **📌 Auteur & Licence**
👤 **Développé par : [Ton Nom]**  
📜 **Licence : MIT**  
📌 **Projet Open-Source - Contribuez et améliorez-le !** 🚀  

🚀 **Bon chat sécurisé !** 🔐  

--- 🚀
