-- 1. Ajouter le champ telephone à client
ALTER TABLE client
ADD COLUMN telephone VARCHAR(20) NULL;

-- 2. Ajouter le champ stock à produit
ALTER TABLE produit
ADD COLUMN stock INT NOT NULL DEFAULT 0;

-- 3. Table de suivi d'état de commande
CREATE TABLE etat_commande (
  id_etat_commande INT PRIMARY KEY AUTO_INCREMENT,
  id_commande INT NOT NULL,
  statut ENUM('brouillon', 'validee', 'facturee') NOT NULL DEFAULT 'brouillon',
  date_statut DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_etat_commande FOREIGN KEY (id_commande) REFERENCES commande(id_commande)
);

-- 4. Tester les modifications
INSERT INTO etat_commande (id_commande, statut) VALUES (1, 'facturee');
INSERT INTO etat_commande (id_commande, statut) VALUES (2, 'validee');

SELECT * FROM etat_commande;
SELECT id_client, nom, prenom, telephone FROM client;
SELECT id_produit, libelle, prix, stock FROM produit;