import sqlite3
import random

DB_FILE = "kikoll.db"

PSEUDOS_EXCLUSIFS = [
    "Neon_Wraith", "Cyber_Ronin", "Data_Ghost", "Silicon_Pulse",
    "Net_Runner", "Void_Walker", "Code_Breaker", "Synth_Wave",
    "Digital_Shadow", "Glitch_Phantom", "Quantum_Drifter", "Nexus_Prime"
]

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