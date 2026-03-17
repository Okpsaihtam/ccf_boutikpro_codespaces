from sqlalchemy import create_engine, text
from src.common.helpers import print_menu

engine = create_engine("mysql+pymysql://student:studentpwd@db:3306/boutikpro_ccf")


def list_clients():
    with engine.begin() as conn:
        rows = conn.execute(text("SELECT id_client, nom, prenom, email FROM client ORDER BY id_client"))
        for row in rows:
            print(row)


if __name__ == "__main__":
    print_menu("Mode SQLAlchemy Core")
    print("Fichier à compléter : src/core/main.py")
    print("Commande d'exécution : python -m src.core.main")
    print()
    list_clients()
    print("
Compléter ce fichier pour réaliser le CRUD demandé.")
