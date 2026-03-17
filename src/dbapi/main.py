import mysql.connector
from src.common.config import DB_CONFIG
from src.common.helpers import print_menu


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def list_clients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_client, nom, prenom, email FROM client ORDER BY id_client")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()


def create_client(nom: str, prenom: str, email: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO client(nom, prenom, email) VALUES (%s, %s, %s)",
        (nom, prenom, email),
    )
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    print_menu("Mode DB-API")
    print("Fichier à compléter : src/dbapi/main.py")
    print("Commande d'exécution : python -m src.dbapi.main")
    print()
    list_clients()
    print("
Compléter ce fichier pour réaliser le CRUD demandé.")
