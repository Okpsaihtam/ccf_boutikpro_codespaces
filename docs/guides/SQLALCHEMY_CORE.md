# Guide SQLAlchemy Core

## Où se trouve le point d'entrée de ce mode

- Fichier principal à compléter : `src/core/main.py`
- Répertoire de travail : racine du dépôt `ccf_boutikpro_codespaces/`

## Comment lancer ce mode

### En GitHub Codespaces

Depuis le terminal ouvert à la racine du projet :

```bash
python -m src.core.main
```

### En local

Après activation de l'environnement virtuel et depuis la racine du projet :

```bash
python -m src.core.main
```

### Script d'aide disponible

```bash
bash scripts/run_core.sh
```

Ce lancement permet de vérifier que la connexion à MySQL fonctionne avant de compléter le CRUD demandé dans le CCF.

## Principe

SQLAlchemy Core permet de travailler avec SQL de manière structurée sans utiliser de classes métiers mappées sur les tables.

Dans ce mode d'accès :
- vous créez un moteur (`engine`) ;
- vous exécutez des requêtes SQL avec `text()` ou avec les objets SQLAlchemy ;
- vous gérez les transactions avec `engine.begin()` ;
- vous restez très proche du SQL.

## Connexion type

```python
from sqlalchemy import create_engine, text  # create_engine ouvre l'accès à la base, text encapsule une requête SQL textuelle.

engine = create_engine("mysql+pymysql://student:studentpwd@db:3306/boutikpro_ccf")  # Crée le moteur de connexion.

with engine.begin() as conn:               # Ouvre une transaction automatiquement validée à la fin si tout se passe bien.
    rows = conn.execute(text("SELECT id_client, nom FROM client"))  # Exécute une requête SELECT.
    for row in rows:
        print(row)                         # Affiche chaque ligne retournée.
```

## Idée générale

SQLAlchemy Core est adapté lorsque l'on souhaite :
- garder la maîtrise des requêtes SQL ;
- factoriser le code de connexion ;
- bénéficier d'une gestion plus propre des transactions.

---

# Exemples de requêtes LDD (Langage de Définition de Données)

## 1. Créer une table

```python
from sqlalchemy import create_engine, text  # Importe le moteur SQLAlchemy et l'objet text.

engine = create_engine("mysql+pymysql://student:studentpwd@db:3306/boutikpro_ccf")  # Définit la connexion à MySQL.

with engine.begin() as conn:                # Démarre une transaction.
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS marque (           -- Crée la table si elle n'existe pas.
            id_marque INT AUTO_INCREMENT PRIMARY KEY, -- Clé primaire auto-incrémentée.
            nom_marque VARCHAR(100) NOT NULL UNIQUE   -- Nom obligatoire et unique.
        )
    """))
```

## 2. Ajouter une colonne

```python
with engine.begin() as conn:                # Ouvre une transaction d'écriture.
    conn.execute(text("""
        ALTER TABLE produit                 -- Modifie la table produit.
        ADD COLUMN description VARCHAR(255) NULL  -- Ajoute une colonne texte facultative.
    """))
```

## 3. Modifier une colonne

```python
with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE produit                      -- Travaille sur la table produit.
        MODIFY COLUMN prix DECIMAL(10,2) NOT NULL  -- Remplace le type de la colonne prix.
    """))
```

## 4. Créer une table d'association

```python
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS contient (              -- Crée la table d'association.
            id_commande VARCHAR(50) NOT NULL,              -- Référence vers commande.
            id_produit VARCHAR(50) NOT NULL,               -- Référence vers produit.
            quantite INT NOT NULL DEFAULT 1,               -- Quantité avec valeur par défaut.
            PRIMARY KEY (id_commande, id_produit),         -- Clé primaire composée.
            CONSTRAINT fk_contient_commande
                FOREIGN KEY (id_commande) REFERENCES commande(id_commande),  -- Clé étrangère vers commande.
            CONSTRAINT fk_contient_produit
                FOREIGN KEY (id_produit) REFERENCES produit(id_produit)      -- Clé étrangère vers produit.
        )
    """))
```

## 5. Supprimer une table

```python
with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS marque"))  # Supprime la table marque si elle existe.
```

---

# Exemples de requêtes LMD (Langage de Manipulation de Données)

## 1. INSERT

```python
with engine.begin() as conn:   # Ouvre une transaction d'écriture.
    conn.execute(
        text("""
            INSERT INTO client (nom, prenom, e_mail)   -- Table et colonnes ciblées.
            VALUES (:nom, :prenom, :email)             -- Paramètres nommés SQLAlchemy.
        """),
        {"nom": "Durand", "prenom": "Alice", "email": "alice.durand@example.com"}  # Valeurs associées aux paramètres.
    )
```

## 2. INSERT multiple

```python
with engine.begin() as conn:
    conn.execute(
        text("""
            INSERT INTO produit (id_produit, libelle, prix, id_categorie_produit)  -- Colonnes remplies.
            VALUES (:id_produit, :libelle, :prix, :id_categorie)                    -- Paramètres nommés.
        """),
        [
            {"id_produit": "P900", "libelle": "Webcam", "prix": 59.90, "id_categorie": 1},  # Première ligne.
            {"id_produit": "P901", "libelle": "Casque", "prix": 39.90, "id_categorie": 1}   # Deuxième ligne.
        ]
    )
```

## 3. SELECT simple

```python
with engine.connect() as conn:   # Ouvre une connexion de lecture.
    result = conn.execute(text("SELECT id_client, nom, prenom FROM client ORDER BY nom"))  # Exécute une requête triée.
    for row in result:
        print(row)               # Affiche chaque ligne du résultat.
```

## 4. SELECT avec jointure

```python
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT c.id_commande, cl.nom, cl.prenom, c.date_commande, c.montant_total  -- Colonnes affichées.
        FROM commande c                         -- Table commande aliasée en c.
        JOIN client cl ON c.id_client = cl.id_client  -- Jointure avec client.
        ORDER BY c.date_commande DESC          -- Tri du plus récent au plus ancien.
    """))
    for row in result:
        print(row)
```

## 5. SELECT avec agrégat

```python
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT id_client, COUNT(*) AS nb_commandes, SUM(montant_total) AS total_depense  -- Statistiques calculées.
        FROM commande                         -- Table source.
        GROUP BY id_client                    -- Regroupe par client.
        HAVING COUNT(*) >= 1                  -- Garde les groupes non vides.
    """))
    for row in result:
        print(row)
```

## 6. UPDATE

```python
with engine.begin() as conn:
    conn.execute(
        text("UPDATE client SET e_mail = :email WHERE id_client = :id_client"),  # Met à jour le mail d'un client.
        {"email": "nouveau.mail@example.com", "id_client": 1}                # Valeurs des paramètres nommés.
    )
```

## 7. DELETE

```python
with engine.begin() as conn:
    conn.execute(
        text("DELETE FROM facture WHERE id_facture = :id_facture"),  # Supprime la facture visée.
        {"id_facture": 10}                                          # Identifiant de la facture à supprimer.
    )
```

## 8. Transaction sur plusieurs requêtes

```python
with engine.begin() as conn:   # Une seule transaction pour plusieurs requêtes.
    conn.execute(
        text("""
            INSERT INTO commande (id_commande, date_commande, montant_total, id_client)  -- Création d'une commande.
            VALUES (:id_commande, NOW(), :montant_total, :id_client)                     -- NOW() donne la date/heure SQL courante.
        """),
        {"id_commande": "CMD950", "montant_total": 129.90, "id_client": 1}
    )

    conn.execute(
        text("""
            INSERT INTO facture (id_facture, montant_ttc, date_facture, id_commande)  -- Création de la facture liée.
            VALUES (:id_facture, :montant_ttc, CURDATE(), :id_commande)               -- CURDATE() donne la date du jour.
        """),
        {"id_facture": 950, "montant_ttc": 129.90, "id_commande": "CMD950"}
    )
```

---

# Exemples de requêtes LCD (Langage de Contrôle de Données)

## Remarque importante

Les requêtes LCD nécessitent généralement un compte MySQL administrateur.
Ces exemples sont fournis à titre pédagogique.

## 1. Créer un utilisateur

```python
with engine.begin() as conn:
    conn.execute(text("CREATE USER IF NOT EXISTS 'tp_user'@'%' IDENTIFIED BY 'MotDePasse123!'"))  # Crée le compte SQL.
```

## 2. Accorder des droits SELECT

```python
with engine.begin() as conn:
    conn.execute(text("GRANT SELECT ON boutikpro_ccf.* TO 'tp_user'@'%'"))  # Accorde la lecture sur toute la base.
```

## 3. Accorder des droits SELECT, INSERT, UPDATE, DELETE

```python
with engine.begin() as conn:
    conn.execute(text("GRANT SELECT, INSERT, UPDATE, DELETE ON boutikpro_ccf.* TO 'tp_user'@'%'"))  # Accorde les principaux droits de LMD.
```

## 4. Accorder des droits sur une table précise

```python
with engine.begin() as conn:
    conn.execute(text("GRANT SELECT, INSERT ON boutikpro_ccf.commande TO 'tp_user'@'%'"))  # Limite les droits à la table commande.
```

## 5. Retirer un droit

```python
with engine.begin() as conn:
    conn.execute(text("REVOKE INSERT ON boutikpro_ccf.commande FROM 'tp_user'@'%'"))  # Retire le droit INSERT.
```

## 6. Afficher les droits

```python
with engine.connect() as conn:
    result = conn.execute(text("SHOW GRANTS FOR 'tp_user'@'%'"))  # Liste les privilèges du compte.
    for row in result:
        print(row)  # Affiche chaque ligne de privilèges.
```
