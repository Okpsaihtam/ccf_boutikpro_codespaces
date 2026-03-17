# Démarrage étudiant

## Parcours conseillé
1. Lire `SUBJECT.md`
2. Lire `docs/INSTALLATION-CODESPACE.md` ou `docs/INSTALLATION-LOCALE.md`
3. Réaliser le TP PlantUML : `docs/phase-01/01-diagramme-cas-utilisation.md`
4. Étudier le MCD dans `assets/MCD_schema_entite_association.jpg`
5. Réaliser les modifications SQL dans `sql/student_upgrade.sql`
6. Choisir un mode Python et développer le CRUD
7. Répondre aux questions du TP

## Où lancer les différents modes d'accès Python

Les fichiers à utiliser se trouvent dans `src/` :
- `src/dbapi/main.py`
- `src/core/main.py`
- `src/orm/main.py`

Depuis la racine du dépôt :

```bash
python -m src.dbapi.main
python -m src.core.main
python -m src.orm.main
```

En Codespaces, vous pouvez aussi lancer :

```bash
bash scripts/run_dbapi.sh
bash scripts/run_core.sh
bash scripts/run_orm.sh
```

Le mode choisi doit ensuite être complété par l'étudiant dans le fichier correspondant.
