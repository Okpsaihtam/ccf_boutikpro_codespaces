# Guide Python DB-API

## Où se trouve le point d'entrée de ce mode

- Fichier principal à compléter : `src/dbapi/main.py`
- Répertoire de travail : racine du dépôt `ccf_boutikpro_codespaces/`

## Comment lancer ce mode

### En GitHub Codespaces

Depuis le terminal ouvert à la racine du projet :

```bash
python -m src.dbapi.main
```

### En local

Après activation de l'environnement virtuel et depuis la racine du projet :

```bash
python -m src.dbapi.main
```

### Script d'aide disponible

```bash
bash scripts/run_dbapi.sh
```

Ce lancement permet de vérifier que la connexion à MySQL fonctionne avant de compléter le CRUD demandé dans le CCF.

## Principe

Python DB-API permet d'exécuter directement des requêtes SQL depuis Python à l'aide d'un connecteur MySQL.

Dans ce mode d'accès :
- vous écrivez vous-même les requêtes SQL ;
- vous utilisez un curseur pour les exécuter ;
- vous validez les modifications avec `commit()` ;
- vous gérez explicitement les erreurs et les transactions.

## Connexion type

```python
import mysql.connector  # Importe le connecteur MySQL pour Python.

conn = mysql.connector.connect(
    host="db",                # Nom d'hôte du serveur MySQL.
    port=3306,                 # Port réseau standard de MySQL.
    user="student",           # Nom de l'utilisateur MySQL.
    password="studentpwd",    # Mot de passe de l'utilisateur MySQL.
    database="boutikpro_ccf"  # Base de données ciblée.
)

cursor = conn.cursor()         # Crée un curseur pour exécuter les requêtes SQL.
```

## Structure minimale recommandée

```python
import mysql.connector              # Bibliothèque de connexion à MySQL.
from mysql.connector import Error   # Classe d'erreur spécifique au connecteur.

conn = None                         # Prépare la variable de connexion.
cursor = None                       # Prépare la variable de curseur.

try:
    conn = mysql.connector.connect(
        host="db",                # Serveur MySQL utilisé.
        port=3306,                 # Port du service MySQL.
        user="student",           # Identifiant SQL.
        password="studentpwd",    # Mot de passe SQL.
        database="boutikpro_ccf"  # Base sur laquelle on travaille.
    )
    cursor = conn.cursor()         # Ouvre un curseur pour envoyer les requêtes.

    cursor.execute("SELECT id_client, nom, prenom FROM client")  # Exécute une requête de lecture.
    for row in cursor.fetchall():  # Récupère toutes les lignes retournées.
        print(row)                 # Affiche chaque ligne.

except Error as e:
    print(f"Erreur MySQL : {e}")  # Affiche le message d'erreur si un problème survient.

finally:
    if cursor is not None:
        cursor.close()             # Ferme le curseur.
    if conn is not None and conn.is_connected():
        conn.close()               # Ferme proprement la connexion à MySQL.
```

## Rappel important

- utiliser `%s` pour les paramètres ;
- ne pas concaténer les valeurs utilisateur dans les requêtes SQL ;
- appeler `commit()` après une requête de type insertion, modification ou suppression ;
- utiliser `rollback()` si une erreur survient pendant une transaction.

---

# Exemples de requêtes LDD (Langage de Définition de Données)

Le LDD permet de créer, modifier ou supprimer la structure de la base.

## 1. Créer une table

```python
cursor.execute("""
CREATE TABLE IF NOT EXISTS marque (      -- Crée la table si elle n'existe pas déjà.
    id_marque INT AUTO_INCREMENT PRIMARY KEY,  -- Identifiant numérique auto-incrémenté et clé primaire.
    nom_marque VARCHAR(100) NOT NULL UNIQUE    -- Nom obligatoire et unique pour éviter les doublons.
)
""")
conn.commit()  # Valide définitivement la création de la table.
```

## 2. Ajouter une colonne

```python
cursor.execute("""
ALTER TABLE produit                 -- Modifie la structure de la table produit.
ADD COLUMN description VARCHAR(255) NULL  -- Ajoute une nouvelle colonne texte facultative.
""")
conn.commit()  # Valide la modification de structure.
```

## 3. Modifier le type d'une colonne

```python
cursor.execute("""
ALTER TABLE produit                      -- Travaille sur la table produit.
MODIFY COLUMN prix DECIMAL(10,2) NOT NULL  -- Remplace le type de prix par un nombre décimal obligatoire.
""")
conn.commit()  # Enregistre la modification de définition de colonne.
```

## 4. Supprimer une colonne

```python
cursor.execute("""
ALTER TABLE produit          -- Modifie la structure de la table produit.
DROP COLUMN description      -- Supprime la colonne description.
""")
conn.commit()  # Rend la suppression effective.
```

## 5. Créer une table d'association

```python
cursor.execute("""
CREATE TABLE IF NOT EXISTS contient (              -- Crée la table d'association commande/produit.
    id_commande VARCHAR(50) NOT NULL,              -- Référence obligatoire vers une commande.
    id_produit VARCHAR(50) NOT NULL,               -- Référence obligatoire vers un produit.
    quantite INT NOT NULL DEFAULT 1,               -- Quantité commandée, par défaut 1.
    PRIMARY KEY (id_commande, id_produit),         -- Clé primaire composée : un produit ne figure qu'une fois par commande.
    CONSTRAINT fk_contient_commande
        FOREIGN KEY (id_commande) REFERENCES commande(id_commande),  -- Lie la commande existante.
    CONSTRAINT fk_contient_produit
        FOREIGN KEY (id_produit) REFERENCES produit(id_produit)      -- Lie le produit existant.
)
""")
conn.commit()  # Valide la création de la table d'association.
```

## 6. Supprimer une table

```python
cursor.execute("DROP TABLE IF EXISTS marque")  # Supprime la table marque si elle existe.
conn.commit()  # Valide la suppression de la table.
```

---

# Exemples de requêtes LMD (Langage de Manipulation de Données)

Le LMD permet d'insérer, lire, modifier et supprimer des données.

## 1. INSERT

```python
cursor.execute(
    """
    INSERT INTO client (nom, prenom, e_mail)   -- Insère une nouvelle ligne dans la table client.
    VALUES (%s, %s, %s)                        -- Réserve trois emplacements pour les paramètres Python.
    """,
    ("Durand", "Alice", "alice.durand@example.com")  # Valeurs réellement injectées dans la requête.
)
conn.commit()  # Valide l'insertion dans la base.
```

## 2. INSERT multiple

```python
data = [
    ("C100", "Clavier", 49.90, 1),  # Première ligne à insérer.
    ("C101", "Souris", 19.90, 1)    # Deuxième ligne à insérer.
]

cursor.executemany(
    """
    INSERT INTO produit (id_produit, libelle, prix, id_categorie_produit)  -- Colonnes alimentées.
    VALUES (%s, %s, %s, %s)                                                 -- 4 paramètres par ligne.
    """,
    data  # Liste de tuples envoyée en bloc au serveur.
)
conn.commit()  # Valide l'ensemble des insertions.
```

## 3. SELECT simple

```python
cursor.execute("SELECT id_client, nom, prenom FROM client ORDER BY nom")  # Lit les clients triés par nom.
rows = cursor.fetchall()   # Récupère toutes les lignes retournées.
for row in rows:
    print(row)             # Affiche chaque enregistrement.
```

## 4. SELECT avec jointure

```python
cursor.execute("""
SELECT c.id_commande, cl.nom, cl.prenom, c.date_commande, c.montant_total  -- Colonnes à afficher.
FROM commande c                         -- Table commande avec alias c.
JOIN client cl ON c.id_client = cl.id_client  -- Jointure entre commande et client via la clé étrangère.
ORDER BY c.date_commande DESC          -- Trie du plus récent au plus ancien.
""")

for row in cursor.fetchall():          # Parcourt les lignes du résultat.
    print(row)                         # Affiche une ligne à la fois.
```

## 5. SELECT avec agrégat

```python
cursor.execute("""
SELECT id_client, COUNT(*) AS nb_commandes, SUM(montant_total) AS total_depense  -- Calcule le nombre de commandes et la somme dépensée.
FROM commande                         -- Table analysée.
GROUP BY id_client                    -- Regroupe les résultats par client.
HAVING COUNT(*) >= 1                  -- Conserve seulement les groupes ayant au moins une commande.
""")

for row in cursor.fetchall():         # Lit les lignes agrégées.
    print(row)                        # Affiche les statistiques par client.
```

## 6. UPDATE

```python
cursor.execute(
    "UPDATE client SET e_mail = %s WHERE id_client = %s",  # Modifie l'adresse mail du client ciblé.
    ("nouveau.mail@example.com", 1)                       # Nouveau mail puis identifiant du client.
)
conn.commit()  # Valide la modification.
```

## 7. DELETE

```python
cursor.execute("DELETE FROM facture WHERE id_facture = %s", (10,))  # Supprime la facture d'identifiant 10.
conn.commit()  # Valide la suppression.
```

## 8. Transaction manuelle

```python
try:
    cursor.execute(
        "INSERT INTO commande (id_commande, date_commande, montant_total, id_client) VALUES (%s, NOW(), %s, %s)",
        ("CMD900", 89.90, 1)  # Crée une commande avec son montant et le client associé.
    )
    cursor.execute(
        "INSERT INTO facture (id_facture, montant_ttc, date_facture, id_commande) VALUES (%s, %s, CURDATE(), %s)",
        (900, 89.90, "CMD900")  # Crée la facture correspondant à la commande précédente.
    )
    conn.commit()   # Valide les deux opérations ensemble.
except Error:
    conn.rollback() # Annule les deux opérations si l'une échoue.
    raise           # Relance l'erreur pour la signaler.
```

---

# Exemples de requêtes LCD (Langage de Contrôle de Données)

Le LCD permet de gérer les droits et la sécurité d'accès aux données.

## Remarque importante

Les requêtes LCD nécessitent généralement un compte administrateur MySQL.
Elles sont données ici comme exemples de cours et de révision.

## 1. Créer un utilisateur

```python
cursor.execute("CREATE USER IF NOT EXISTS 'tp_user'@'%' IDENTIFIED BY 'MotDePasse123!'")  # Crée un utilisateur SQL accessible à distance.
conn.commit()  # Valide la création du compte.
```

## 2. Donner des droits de lecture

```python
cursor.execute("GRANT SELECT ON boutikpro_ccf.* TO 'tp_user'@'%'")  # Autorise la lecture sur toutes les tables de la base.
conn.commit()  # Valide l'attribution des droits.
```

## 3. Donner des droits de lecture et modification

```python
cursor.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON boutikpro_ccf.* TO 'tp_user'@'%'")  # Autorise les opérations principales de LMD.
conn.commit()  # Valide les nouveaux privilèges.
```

## 4. Donner des droits sur une table précise

```python
cursor.execute("GRANT SELECT, INSERT ON boutikpro_ccf.commande TO 'tp_user'@'%'")  # Limite les droits à la seule table commande.
conn.commit()  # Rend ces droits actifs.
```

## 5. Retirer des droits

```python
cursor.execute("REVOKE INSERT ON boutikpro_ccf.commande FROM 'tp_user'@'%'")  # Retire le droit d'insertion sur la table commande.
conn.commit()  # Valide le retrait.
```

## 6. Afficher les droits d'un utilisateur

```python
cursor.execute("SHOW GRANTS FOR 'tp_user'@'%'")  # Demande au serveur la liste des privilèges de l'utilisateur.
for row in cursor.fetchall():
    print(row)  # Affiche chaque ligne de privilèges retournée.
```

## 7. Supprimer un utilisateur

```python
cursor.execute("DROP USER IF EXISTS 'tp_user'@'%'")  # Supprime le compte SQL s'il existe.
conn.commit()  # Valide la suppression de l'utilisateur.
```

---

# Exemple de mini CRUD complet en DB-API

```python
import mysql.connector  # Importe le connecteur MySQL.

conn = mysql.connector.connect(
    host="db",                # Serveur MySQL.
    port=3306,                 # Port MySQL.
    user="student",           # Utilisateur SQL.
    password="studentpwd",    # Mot de passe SQL.
    database="boutikpro_ccf"  # Base utilisée.
)
cursor = conn.cursor(dictionary=True)   # Curseur qui retourne des dictionnaires plutôt que des tuples.

# CREATE
cursor.execute(
    "INSERT INTO client (nom, prenom, e_mail) VALUES (%s, %s, %s)",  # Ajoute un nouveau client.
    ("Martin", "Léo", "leo.martin@example.com")                   # Valeurs du nouveau client.
)
conn.commit()                        # Valide l'insertion.
new_id = cursor.lastrowid            # Récupère l'identifiant généré automatiquement.

# READ
cursor.execute("SELECT id_client, nom, prenom, e_mail FROM client WHERE id_client = %s", (new_id,))  # Relit le client ajouté.
client = cursor.fetchone()           # Récupère une seule ligne.
print(client)                        # Affiche le client.

# UPDATE
cursor.execute(
    "UPDATE client SET e_mail = %s WHERE id_client = %s",            # Met à jour l'adresse mail du client.
    ("leo.martin.pro@example.com", new_id)                           # Nouveau mail et identifiant ciblé.
)
conn.commit()                        # Valide la modification.

# DELETE
cursor.execute("DELETE FROM client WHERE id_client = %s", (new_id,))  # Supprime le client créé pour le test.
conn.commit()                        # Valide la suppression.

cursor.close()  # Ferme le curseur.
conn.close()    # Ferme la connexion.
```
