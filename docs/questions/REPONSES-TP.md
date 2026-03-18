# Réponses aux questions du TP — BoutikPro

---

## 1. Qu'est-ce qu'un acteur dans un diagramme de cas d'utilisation ?

Un acteur est une entité extérieure au système (personne, autre logiciel) qui interagit avec lui.
Dans BoutikPro, les acteurs sont par exemple l'Employé commercial ou le Comptable.

---

## 2. Qu'est-ce qu'un cas d'utilisation ?

Un cas d'utilisation représente une fonctionnalité offerte par le système à un acteur.
Par exemple "Enregistrer une commande" ou "Générer une facture".

---

## 3. Pourquoi utiliser un acteur générique `Utilisateur` dans ce sujet ?

Car tous les acteurs partagent des actions communes (comme "Se connecter").
L'acteur générique `Utilisateur` regroupe ces actions communes pour éviter la répétition dans le diagramme.

---

## 4. Quel est l'intérêt de l'héritage entre acteurs en UML ?

Il permet de factoriser les cas d'utilisation communs dans l'acteur parent.
Les acteurs fils héritent automatiquement des cas d'utilisation du parent et ajoutent les leurs propres.

---

## 5. Quel lien existe entre diagramme de cas d'utilisation et MCD ?

Le diagramme de cas d'utilisation identifie les besoins métier et les données manipulées.
Le MCD modélise ensuite ces données et leurs relations.
Les entités du MCD correspondent aux objets manipulés dans les cas d'utilisation.

---

## 6. Qu'est-ce qu'un MCD ?

Un Modèle Conceptuel de Données représente les données d'un système et leurs associations,
indépendamment de toute technologie. Il est composé d'entités, d'associations et de cardinalités.

---

## 7. Quelle différence entre MCD et MLD ?

Le MCD est conceptuel et indépendant de la technologie.
Le MLD (Modèle Logique de Données) traduit le MCD en tables relationnelles avec clés primaires
et clés étrangères, en vue d'une implémentation en SQL.

---

## 8. Comment traduit-on une association 1,N en relationnel ?

On ajoute une clé étrangère dans la table du côté N qui référence la clé primaire de la table du côté 1.
Par exemple, `commande` contient `id_client` qui référence `client`.

---

## 9. Comment traduit-on une association N,N en relationnel ?

On crée une table d'association qui contient les clés primaires des deux tables concernées.
Par exemple, `contient` relie `commande` et `produit` avec une clé primaire composée
de `id_commande` et `id_produit`.

---

## 10. Quel est le rôle d'une clé étrangère ?

Une clé étrangère garantit l'intégrité référentielle entre deux tables.
Elle assure qu'une valeur dans une table enfant correspond toujours à une valeur existante
dans la table parente.

---

## 11. Pourquoi la relation `Commande` / `Facture` peut-elle nécessiter une contrainte `UNIQUE` ?

Car une commande ne peut avoir qu'une seule facture.
La contrainte `UNIQUE` sur `id_commande` dans la table `facture` empêche qu'on génère
deux factures pour la même commande.

---

## 12. Quelle différence entre Python DB-API et SQLAlchemy ORM ?

Python DB-API exécute du SQL brut directement via un curseur — on écrit les requêtes SQL soi-même.
SQLAlchemy ORM représente les tables comme des classes Python et génère automatiquement le SQL —
on manipule des objets plutôt que des requêtes.

---

## 13. Qu'est-ce qu'un CRUD ?

CRUD est l'acronyme de Create, Read, Update, Delete.
Ce sont les quatre opérations de base pour manipuler des données : créer, lire, modifier et supprimer.

---

## 14. Pourquoi faut-il exécuter `commit()` après certaines requêtes ?

Les requêtes INSERT, UPDATE et DELETE sont exécutées dans une transaction qui n'est pas validée
automatiquement. `commit()` valide définitivement les modifications en base.
Sans `commit()`, les changements sont annulés à la fermeture de la connexion.

---

## 15. À quoi sert une requête avec jointure dans ce contexte ?

Une jointure permet de récupérer des données issues de plusieurs tables en une seule requête.
Par exemple, afficher les factures avec le nom du client nécessite une jointure entre
`facture`, `commande` et `client`.