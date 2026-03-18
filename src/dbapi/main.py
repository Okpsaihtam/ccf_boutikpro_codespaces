import mysql.connector
from mysql.connector import Error
from src.common.config import DB_CONFIG
from src.common.helpers import print_menu


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ─── CLIENTS ────────────────────────────────────────────────

def list_clients():
    """Affiche tous les clients (READ)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_client, nom, prenom, email, telephone FROM client ORDER BY id_client")
    rows = cur.fetchall()
    print(f"\n{'ID':<5} {'Nom':<15} {'Prénom':<15} {'Email':<30} {'Téléphone'}")
    print("-" * 75)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]:<30} {row[4] or 'N/A'}")
    cur.close()
    conn.close()


def create_client(nom, prenom, email, telephone=None):
    """Crée un nouveau client (CREATE)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO client (nom, prenom, email, telephone) VALUES (%s, %s, %s, %s)",
        (nom, prenom, email, telephone),
    )
    conn.commit()
    print(f"✅ Client '{prenom} {nom}' créé avec l'ID {cur.lastrowid}.")
    cur.close()
    conn.close()


def update_client(id_client, nom, prenom, email, telephone=None):
    """Modifie un client existant (UPDATE)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE client SET nom=%s, prenom=%s, email=%s, telephone=%s WHERE id_client=%s",
        (nom, prenom, email, telephone, id_client),
    )
    conn.commit()
    print(f"✅ Client ID {id_client} mis à jour.")
    cur.close()
    conn.close()


def delete_client(id_client):
    """Supprime un client et toutes ses données liées (DELETE)."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Supprimer les recommandations liées
        cur.execute("DELETE FROM recommande WHERE id_client_source=%s OR id_client_cible=%s", (id_client, id_client))
        # Supprimer la carte de fidélité
        cur.execute("DELETE FROM carte_fidelite WHERE id_client=%s", (id_client,))
        # Récupérer les commandes du client
        cur.execute("SELECT id_commande FROM commande WHERE id_client=%s", (id_client,))
        commandes = [row[0] for row in cur.fetchall()]
        for id_cmd in commandes:
            cur.execute("DELETE FROM contient WHERE id_commande=%s", (id_cmd,))
            cur.execute("DELETE FROM etat_commande WHERE id_commande=%s", (id_cmd,))
            cur.execute("DELETE FROM facture WHERE id_commande=%s", (id_cmd,))
            cur.execute("DELETE FROM commande WHERE id_commande=%s", (id_cmd,))
        # Supprimer le client
        cur.execute("DELETE FROM client WHERE id_client=%s", (id_client,))
        conn.commit()
        print(f"✅ Client ID {id_client} supprimé.")
    except Error as e:
        conn.rollback()
        print(f"❌ Erreur : {e}")
    finally:
        cur.close()
        conn.close()


# ─── PRODUITS ───────────────────────────────────────────────

def list_produits():
    """Affiche tous les produits."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id_produit, p.libelle, p.prix, p.stock, c.nom_categorie
        FROM produit p
        JOIN categorie_produit c ON p.id_categorie_produit = c.id_categorie_produit
        ORDER BY p.id_produit
    """)
    rows = cur.fetchall()
    print(f"\n{'ID':<5} {'Libellé':<25} {'Prix':>8} {'Stock':>6}  {'Catégorie'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<25} {row[2]:>8.2f} {row[3]:>6}  {row[4]}")
    cur.close()
    conn.close()


# ─── COMMANDES ──────────────────────────────────────────────

def create_commande(id_client, lignes):
    """
    Enregistre une commande et ses lignes (CREATE).
    lignes = liste de tuples (id_produit, quantite)
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Calcul du montant total
        montant_total = 0
        for id_produit, quantite in lignes:
            cur.execute("SELECT prix FROM produit WHERE id_produit=%s", (id_produit,))
            prix = cur.fetchone()[0]
            montant_total += float(prix) * quantite

        # Insertion de la commande
        cur.execute(
            "INSERT INTO commande (date_commande, montant_total, id_client) VALUES (NOW(), %s, %s)",
            (montant_total, id_client),
        )
        id_commande = cur.lastrowid

        # Insertion des lignes de commande
        for id_produit, quantite in lignes:
            cur.execute(
                "INSERT INTO contient (id_commande, id_produit, quantite) VALUES (%s, %s, %s)",
                (id_commande, id_produit, quantite),
            )

        # État initial de la commande
        cur.execute(
            "INSERT INTO etat_commande (id_commande, statut) VALUES (%s, 'brouillon')",
            (id_commande,),
        )

        conn.commit()
        print(f"✅ Commande ID {id_commande} créée pour le client {id_client}. Montant : {montant_total:.2f} €")
    except Error as e:
        conn.rollback()
        print(f"❌ Erreur lors de la création de la commande : {e}")
    finally:
        cur.close()
        conn.close()


# ─── FACTURES ───────────────────────────────────────────────

def list_factures():
    """Affiche les factures avec jointure (READ + JOIN)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT f.id_facture, f.date_facture, f.montant_ttc,
               c.id_commande, cl.nom, cl.prenom
        FROM facture f
        JOIN commande c ON f.id_commande = c.id_commande
        JOIN client cl ON c.id_client = cl.id_client
        ORDER BY f.date_facture DESC
    """)
    rows = cur.fetchall()
    print(f"\n{'ID Fact':<8} {'Date':<12} {'Montant TTC':>12}  {'ID Cmd':<8} {'Client'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<8} {str(row[1]):<12} {row[2]:>12.2f}  {row[3]:<8} {row[4]} {row[5]}")
    cur.close()
    conn.close()


# ─── STATISTIQUES ───────────────────────────────────────────

def stats_clients():
    """Affiche les statistiques de commandes par client (agrégation)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT cl.id_client, cl.nom, cl.prenom,
               COUNT(c.id_commande) AS nb_commandes,
               SUM(c.montant_total) AS total_depense
        FROM client cl
        LEFT JOIN commande c ON cl.id_client = c.id_client
        GROUP BY cl.id_client, cl.nom, cl.prenom
        ORDER BY total_depense DESC
    """)
    rows = cur.fetchall()
    print(f"\n{'ID':<5} {'Nom':<15} {'Prénom':<15} {'Nb cmd':>7} {'Total dépensé':>14}")
    print("-" * 60)
    for row in rows:
        total = row[4] or 0
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]:>7} {float(total):>14.2f} €")
    cur.close()
    conn.close()


# ─── MENU PRINCIPAL ─────────────────────────────────────────

def menu():
    while True:
        print("\n" + "=" * 40)
        print("       BOUTIKPRO — Menu principal")
        print("=" * 40)
        print("1. Lister les clients")
        print("2. Créer un client")
        print("3. Modifier un client")
        print("4. Supprimer un client")
        print("5. Lister les produits")
        print("6. Enregistrer une commande")
        print("7. Lister les factures")
        print("8. Statistiques clients (agrégation)")
        print("0. Quitter")
        print("-" * 40)
        choix = input("Votre choix : ").strip()

        if choix == "1":
            list_clients()
            input("\nAppuyez sur Entrée pour continuer...")

        elif choix == "2":
            nom = input("Nom : ").strip()
            prenom = input("Prénom : ").strip()
            email = input("Email : ").strip()
            tel = input("Téléphone (optionnel, Entrée pour ignorer) : ").strip() or None
            create_client(nom, prenom, email, tel)
            input("\nAppuyez sur Entrée pour continuer...")

        elif choix == "3":
            list_clients()
            id_c = int(input("ID du client à modifier : "))
            nom = input("Nouveau nom : ").strip()
            prenom = input("Nouveau prénom : ").strip()
            email = input("Nouvel email : ").strip()
            tel = input("Nouveau téléphone (optionnel) : ").strip() or None
            update_client(id_c, nom, prenom, email, tel)
            input("\nAppuyez sur Entrée pour continuer...")

        elif choix == "4":
            list_clients()
            id_c = int(input("ID du client à supprimer : "))
            confirm = input(f"Confirmer la suppression du client {id_c} ? (o/n) : ").strip().lower()
            if confirm == "o":
                delete_client(id_c)
            input("\nAppuyez sur Entrée pour continuer...")

        elif choix == "5":
            list_produits()
            input("\nAppuyez sur Entrée pour continuer...")

        elif choix == "6":
            list_clients()
            id_c = int(input("ID du client : "))
            list_produits()
            lignes = []
            while True:
                id_p = input("ID produit à ajouter (Entrée pour terminer) : ").strip()
                if not id_p:
                    break
                qte = int(input("Quantité : "))
                lignes.append((int(id_p), qte))
            if lignes:
                create_commande(id_c, lignes)
            input("\nAppuyez sur Entrée pour continuer...")

        elif choix == "7":
            list_factures()
            input("\nAppuyez sur Entrée pour continuer...")

        elif choix == "8":
            stats_clients()
            input("\nAppuyez sur Entrée pour continuer...")

        elif choix == "0":
            print("Au revoir !")
            break

        else:
            print("Choix invalide, réessaie.")
            input("\nAppuyez sur Entrée pour continuer...")