# Guide SQLAlchemy ORM

## Où se trouve le point d'entrée de ce mode

- Fichier principal à compléter : `src/orm/main.py`
- Répertoire de travail : racine du dépôt `ccf_boutikpro_codespaces/`

## Comment lancer ce mode

### En GitHub Codespaces

Depuis le terminal ouvert à la racine du projet :

```bash
python -m src.orm.main
```

### En local

Après activation de l'environnement virtuel et depuis la racine du projet :

```bash
python -m src.orm.main
```

### Script d'aide disponible

```bash
bash scripts/run_orm.sh
```

Ce lancement permet de vérifier que la connexion à MySQL fonctionne avant de compléter le CRUD demandé dans le CCF.

## Principe

L'ORM de SQLAlchemy permet de représenter les tables par des classes Python et les lignes par des objets.

Dans ce mode d'accès :
- les tables sont décrites par des classes ;
- les opérations CRUD passent souvent par une `Session` ;
- les modifications sont validées avec `session.commit()` ;
- certaines opérations LDD et LCD restent plus simples à exécuter via `text()`.

## Connexion type

```python
from sqlalchemy import create_engine              # Crée le moteur de connexion.
from sqlalchemy.orm import DeclarativeBase, Session  # DeclarativeBase sert de base à toutes les classes ORM.

engine = create_engine("mysql+pymysql://student:studentpwd@db:3306/boutikpro_ccf")  # Connexion à MySQL.

class Base(DeclarativeBase):  # Classe mère de tous les modèles ORM.
    pass
```

## Exemple minimal de modèle

```python
from sqlalchemy import Integer, String                 # Types SQLAlchemy utilisés par les colonnes.
from sqlalchemy.orm import Mapped, mapped_column       # Outils de déclaration typée des colonnes.

class Client(Base):
    __tablename__ = "client"                          # Nom exact de la table en base.

    id_client: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # Clé primaire auto-incrémentée.
    nom: Mapped[str] = mapped_column(String(50))       # Colonne texte pour le nom.
    prenom: Mapped[str] = mapped_column(String(50))    # Colonne texte pour le prénom.
    e_mail: Mapped[str] = mapped_column(String(100))   # Colonne texte pour l'adresse mail.
```

---

# Exemples de requêtes LDD (Langage de Définition de Données)

## 1. Créer une table depuis les classes ORM

```python
from sqlalchemy import Integer, String                 # Types de colonnes.
from sqlalchemy.orm import Mapped, mapped_column       # Déclaration des colonnes mappées.

class Marque(Base):
    __tablename__ = "marque"                          # Nom de la table à créer.

    id_marque: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # Clé primaire.
    nom_marque: Mapped[str] = mapped_column(String(100), unique=True)                       # Nom unique.

Base.metadata.create_all(engine)  # Crée en base toutes les tables déclarées dans les classes ORM.
```

## 2. Créer uniquement certaines tables

```python
Base.metadata.create_all(engine, tables=[Marque.__table__])  # Crée uniquement la table Marque.
```

## 3. Supprimer une table ORM

```python
Base.metadata.drop_all(engine, tables=[Marque.__table__])  # Supprime uniquement la table Marque.
```

## 4. Exécuter un ALTER TABLE via l'ORM + SQL brut

```python
from sqlalchemy import text  # Encapsule une requête SQL brute.

with engine.begin() as conn:
    conn.execute(text("ALTER TABLE produit ADD COLUMN description VARCHAR(255) NULL"))  # Ajoute une colonne via SQL brut.
```

## 5. Modifier une colonne via SQL brut

```python
with engine.begin() as conn:
    conn.execute(text("ALTER TABLE produit MODIFY COLUMN prix DECIMAL(10,2) NOT NULL"))  # Modifie le type de la colonne prix.
```

## 6. Créer une table d'association via SQL brut

```python
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS contient (              -- Crée la table d'association.
            id_commande VARCHAR(50) NOT NULL,              -- Référence vers commande.
            id_produit VARCHAR(50) NOT NULL,               -- Référence vers produit.
            quantite INT NOT NULL DEFAULT 1,               -- Quantité commandée.
            PRIMARY KEY (id_commande, id_produit),         -- Clé primaire composée.
            CONSTRAINT fk_contient_commande
                FOREIGN KEY (id_commande) REFERENCES commande(id_commande),  -- Lien vers commande.
            CONSTRAINT fk_contient_produit
                FOREIGN KEY (id_produit) REFERENCES produit(id_produit)      -- Lien vers produit.
        )
    """))
```

---

# Exemples de requêtes LMD (Langage de Manipulation de Données)

## Modèle ORM utilisé dans les exemples

```python
from sqlalchemy import Integer, String                 # Types de colonnes SQLAlchemy.
from sqlalchemy.orm import Mapped, mapped_column       # Outils de mapping ORM.

class Client(Base):
    __tablename__ = "client"                          # Table visée en base.

    id_client: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # Clé primaire.
    nom: Mapped[str] = mapped_column(String(50))       # Colonne nom.
    prenom: Mapped[str] = mapped_column(String(50))    # Colonne prénom.
    e_mail: Mapped[str] = mapped_column(String(100))   # Colonne email.
```

## 1. INSERT

```python
with Session(engine) as session:  # Ouvre une session ORM.
    client = Client(nom="Durand", prenom="Alice", e_mail="alice.durand@example.com")  # Crée un objet Python représentant une ligne.
    session.add(client)           # Place l'objet dans la session pour insertion.
    session.commit()              # Envoie l'INSERT à la base et valide la transaction.
```

## 2. INSERT multiple

```python
with Session(engine) as session:
    clients = [
        Client(nom="Martin", prenom="Léo", e_mail="leo@example.com"),   # Premier objet à insérer.
        Client(nom="Petit", prenom="Nina", e_mail="nina@example.com")   # Deuxième objet à insérer.
    ]
    session.add_all(clients)      # Ajoute plusieurs objets ORM en une seule fois.
    session.commit()              # Valide toutes les insertions.
```

## 3. SELECT simple

```python
from sqlalchemy import select  # Fonction de construction de requêtes SELECT.

with Session(engine) as session:
    stmt = select(Client).order_by(Client.nom)  # Sélectionne les objets Client triés par nom.
    clients = session.scalars(stmt).all()       # Récupère directement les objets Client.
    for client in clients:
        print(client.id_client, client.nom, client.prenom)  # Affiche les attributs de chaque objet.
```

## 4. SELECT avec filtre

```python
with Session(engine) as session:
    stmt = select(Client).where(Client.nom == "Durand")  # Filtre les clients dont le nom vaut Durand.
    client = session.scalars(stmt).first()                # Récupère le premier résultat ou None.
    print(client)
```

## 5. SELECT avec SQL brut via session

```python
from sqlalchemy import text  # Permet d'exécuter une requête SQL écrite manuellement.

with Session(engine) as session:
    result = session.execute(text("""
        SELECT c.id_commande, cl.nom, cl.prenom, c.date_commande, c.montant_total  -- Colonnes retournées.
        FROM commande c                         -- Table commande aliasée en c.
        JOIN client cl ON c.id_client = cl.id_client  -- Jointure avec client.
        ORDER BY c.date_commande DESC          -- Tri décroissant par date.
    """))
    for row in result:
        print(row)
```

## 6. UPDATE

```python
with Session(engine) as session:
    client = session.get(Client, 1)          # Charge l'objet Client dont la clé primaire vaut 1.
    if client is not None:
        client.e_mail = "nouveau.mail@example.com"  # Modifie l'attribut Python.
        session.commit()                     # SQLAlchemy génère automatiquement l'UPDATE.
```

## 7. DELETE

```python
with Session(engine) as session:
    client = session.get(Client, 1)          # Recherche le client à supprimer.
    if client is not None:
        session.delete(client)               # Marque l'objet pour suppression.
        session.commit()                     # Exécute le DELETE en base.
```

## 8. Transaction ORM

```python
with Session(engine) as session:
    try:
        client = Client(nom="Bernard", prenom="Tom", e_mail="tom.bernard@example.com")  # Prépare un nouvel objet.
        session.add(client)                  # Ajoute l'objet à la transaction en cours.
        session.commit()                     # Valide la transaction.
    except Exception:
        session.rollback()                   # Annule la transaction en cas d'erreur.
        raise                               # Relance l'exception pour traitement ultérieur.
```

---

# Exemples de requêtes LCD (Langage de Contrôle de Données)

## Remarque importante

Même avec l'ORM, les opérations LCD passent en pratique par du SQL brut.
Elles nécessitent en général un compte administrateur MySQL.

## 1. Créer un utilisateur

```python
from sqlalchemy import text  # Requêtes SQL brutes nécessaires pour le LCD.

with engine.begin() as conn:
    conn.execute(text("CREATE USER IF NOT EXISTS 'tp_user'@'%' IDENTIFIED BY 'MotDePasse123!'"))  # Crée un compte SQL.
```

## 2. Donner des droits SELECT

```python
with engine.begin() as conn:
    conn.execute(text("GRANT SELECT ON boutikpro_ccf.* TO 'tp_user'@'%'"))  # Accorde la lecture sur toute la base.
```

## 3. Donner des droits SELECT, INSERT, UPDATE, DELETE

```python
with engine.begin() as conn:
    conn.execute(text("GRANT SELECT, INSERT, UPDATE, DELETE ON boutikpro_ccf.* TO 'tp_user'@'%'"))  # Accorde les principaux privilèges de manipulation.
```

## 4. Donner des droits sur une table

```python
with engine.begin() as conn:
    conn.execute(text("GRANT SELECT, INSERT ON boutikpro_ccf.commande TO 'tp_user'@'%'"))  # Restreint les droits à la table commande.
```

## 5. Retirer des droits

```python
with engine.begin() as conn:
    conn.execute(text("REVOKE INSERT ON boutikpro_ccf.commande FROM 'tp_user'@'%'"))  # Retire le privilège INSERT.
```
