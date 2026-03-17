# Option 1 - Installation distante avec GitHub Codespaces

Ce mode d'installation utilise un environnement distant prêt à l'emploi.

## Outils nécessaires
- un compte GitHub
- GitHub Codespaces activé pour votre compte
- un navigateur Web moderne
- l'éditeur PlantUML en ligne : `https://editor.plantuml.com/`

## Étapes
1. Créer un dépôt à partir du template.
2. Ouvrir le dépôt dans GitHub Codespaces.
3. Attendre la fin du build.
4. Dans le terminal, exécuter :

```bash
bash scripts/setup.sh
bash scripts/check_db.sh
```

5. Vérifier que :
- l'environnement virtuel Python est prêt ;
- les dépendances sont installées ;
- la base MySQL répond ;
- les tables sont présentes.

## PlantUML en ligne
1. Ouvrir l'adresse suivante dans votre navigateur :

```text
https://editor.plantuml.com/
```

2. Copier le contenu de `uml/usecase.puml` dans l'éditeur en ligne.
3. Modifier le diagramme.
4. Copier le résultat final dans votre fichier local `uml/usecase.puml` du dépôt.

## Vérifications recommandées
```bash
python src/dbapi/main.py
python src/core/main.py
python src/orm/main.py
```

## Ordre de travail conseillé
1. `START-HERE.md`
2. `docs/phase-01/01-diagramme-cas-utilisation.md`
3. `docs/guides/MCD_MLD.md`
4. `sql/student_upgrade.sql`
5. le mode Python choisi


## Lancer les modes Python

Depuis la racine du projet dans le terminal Codespaces :

```bash
python -m src.dbapi.main
python -m src.core.main
python -m src.orm.main
```

Ou avec les scripts :

```bash
bash scripts/run_dbapi.sh
bash scripts/run_core.sh
bash scripts/run_orm.sh
```
