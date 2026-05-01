import sqlite3
import random

import os

DB_FILE = "kikoll.db"
WORDLIST_FILE = "rockyou.txt"

# Liste de secours si le fichier n'est pas trouvé
PSEUDOS_SECOURS = [
    "password", "qwerty", "dragon", "shadow", "monkey", "superman", "iloveyou",
    "princess", "admin", "root", "toor", "kali", "rockyou", "letmein", "hacker",
    "ninja", "matrix", "starwars", "pokemon", "batman", "master", "123456",
    "freedom", "destiny", "secret", "welcome", "sunshine", "joshua", "god"
]

def load_passwords():
    if os.path.exists(WORDLIST_FILE):
        print(f"✅ Chargement des mots de passe depuis {WORDLIST_FILE}...")
        # L'encodage latin-1 (ou utf-8 avec erreurs ignorées) est souvent nécessaire pour rockyou
        with open(WORDLIST_FILE, "r", encoding="utf-8", errors="ignore") as f:
            return [line.strip() for line in f if line.strip()]
    else:
        print(f"⚠️ Fichier {WORDLIST_FILE} introuvable. Utilisation de la liste de secours.")
        return PSEUDOS_SECOURS

PSEUDOS_EXCLUSIFS = load_passwords()

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            pseudo TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_or_create_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Vérifier si l'utilisateur existe déjà
    cursor.execute("SELECT pseudo FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    if result:
        conn.close()
        return result[0] # Renvoie le pseudo existant
    else:
        # Créer un nouveau pseudo
        pseudo = random.choice(PSEUDOS_EXCLUSIFS)
        cursor.execute("INSERT INTO users (user_id, pseudo) VALUES (?, ?)", (user_id, pseudo))
        conn.commit()
        conn.close()
        return pseudo