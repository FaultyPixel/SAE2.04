#====DROP TABLE====
DROP TABLE IF EXISTS Est_contenu;
DROP TABLE IF EXISTS Ligne;
DROP TABLE IF EXISTS Fourni;
DROP TABLE IF EXISTS COMMENTAIRE;
DROP TABLE IF EXISTS COMMANDE;
DROP TABLE IF EXISTS PANIER;
DROP TABLE IF EXISTS SKI;
DROP TABLE IF EXISTS LIVRAISON_STOCK;
DROP TABLE IF EXISTS ETAT;
DROP TABLE IF EXISTS USER;
DROP TABLE IF EXISTS NOYAU;
DROP TABLE IF EXISTS FIXATION;
DROP TABLE IF EXISTS FABRICANT;
DROP TABLE IF EXISTS PAYS_FABRICATION;
DROP TABLE IF EXISTS POIDS_SKIEUR;
DROP TABLE IF EXISTS NIVEAU_SKIEUR;
DROP TABLE IF EXISTS SEXE;
DROP TABLE IF EXISTS FOURNISSEUR;
DROP TABLE IF EXISTS TYPE_SKI;

#====CREATE TABLE====
CREATE TABLE TYPE_SKI(
   id_type_ski INT AUTO_INCREMENT NOT NULL,
   libelle_type_ski VARCHAR(30),
   PRIMARY KEY(id_type_ski)
);

CREATE TABLE FOURNISSEUR(
   id_fournisseur INT AUTO_INCREMENT NOT NULL,
   libelle_fournisseur VARCHAR(30),
   telephone_fournisseur VARCHAR(10),
   mail_fournisseur VARCHAR(30),
   adresse_fournisseur VARCHAR(100),
   PRIMARY KEY(id_fournisseur)
);

CREATE TABLE SEXE(
   id_sexe INT AUTO_INCREMENT NOT NULL,
   libelle_sexe VARCHAR(30),
   PRIMARY KEY(id_sexe)
);

CREATE TABLE NIVEAU_SKIEUR(
   id_niveau_skieur INT AUTO_INCREMENT NOT NULL,
   libelle_niveau_skieur VARCHAR(30),
   PRIMARY KEY(id_niveau_skieur)
);

CREATE TABLE POIDS_SKIEUR(
   id_poids_skieur INT AUTO_INCREMENT NOT NULL,
   poids_skieur_min DECIMAL(5,2),
   poids_skieur_max DECIMAL(5,2),
   PRIMARY KEY(id_poids_skieur)
);

CREATE TABLE PAYS_FABRICATION(
   id_pays_fabrication INT AUTO_INCREMENT NOT NULL,
   libelle_pays_fabrication VARCHAR(30),
   PRIMARY KEY(id_pays_fabrication)
);

CREATE TABLE FABRICANT(
   id_fabricant INT AUTO_INCREMENT NOT NULL,
   libelle_fabricant VARCHAR(30),
   telephone_fabricant VARCHAR(10),
   mail_fabricant VARCHAR(30),
   PRIMARY KEY(id_fabricant)
);

CREATE TABLE FIXATION(
   id_fixation INT AUTO_INCREMENT NOT NULL,
   libelle_fixation VARCHAR(30),
   PRIMARY KEY(id_fixation)
);

CREATE TABLE NOYAU(
   id_noyau INT AUTO_INCREMENT NOT NULL,
   libelle_noyau VARCHAR(30),
   PRIMARY KEY(id_noyau)
);

CREATE TABLE USER(
   id_user INT AUTO_INCREMENT NOT NULL,
   username_user VARCHAR(30),
   password_user VARCHAR(5000),
   role_user VARCHAR(30),
   est_actif_user BOOLEAN,
   email_user VARCHAR(50),
   adresse_user VARCHAR(100),
   PRIMARY KEY(id_user)
);

CREATE TABLE ETAT(
   id_etat INT AUTO_INCREMENT NOT NULL,
   libelle_etat VARCHAR(20),
   PRIMARY KEY(id_etat)
);

CREATE TABLE LIVRAISON_STOCK(
   id_livraison_stock INT AUTO_INCREMENT NOT NULL,
   date_livraison_stock DATE,
   id_etat INT NOT NULL,
   id_fournisseur INT NOT NULL,
   PRIMARY KEY(id_livraison_stock),
   FOREIGN KEY(id_etat) REFERENCES ETAT(id_etat),
   FOREIGN KEY(id_fournisseur) REFERENCES FOURNISSEUR(id_fournisseur)
);

CREATE TABLE SKI(
   id_ski INT AUTO_INCREMENT NOT NULL,
   modele_ski VARCHAR(150),
   image_ski VARCHAR(50),
   prix_ski DECIMAL(8,2),
   poids_ski DECIMAL(4,2),
   longueur_ski DECIMAL(5,2),
   stock_ski INT,
   note_ski DECIMAL(2,1),
   AAAA DATE,
   id_pays_fabrication INT NOT NULL,
   id_niveau_skieur INT,
   id_poids_skieur INT,
   id_noyau INT NOT NULL,
   id_fixation INT,
   id_sexe INT NOT NULL,
   id_fabricant INT NOT NULL,
   id_type_ski INT NOT NULL,
   PRIMARY KEY(id_ski),
   FOREIGN KEY(id_pays_fabrication) REFERENCES PAYS_FABRICATION(id_pays_fabrication),
   FOREIGN KEY(id_niveau_skieur) REFERENCES NIVEAU_SKIEUR(id_niveau_skieur),
   FOREIGN KEY(id_poids_skieur) REFERENCES POIDS_SKIEUR(id_poids_skieur),
   FOREIGN KEY(id_noyau) REFERENCES NOYAU(id_noyau),
   FOREIGN KEY(id_fixation) REFERENCES FIXATION(id_fixation),
   FOREIGN KEY(id_sexe) REFERENCES SEXE(id_sexe),
   FOREIGN KEY(id_fabricant) REFERENCES FABRICANT(id_fabricant),
   FOREIGN KEY(id_type_ski) REFERENCES TYPE_SKI(id_type_ski)
);

CREATE TABLE PANIER(
   id_panier INT AUTO_INCREMENT NOT NULL,
   date_ajout_panier DATE,
   quantite_panier INT,
   id_user INT NOT NULL,
   id_ski INT NOT NULL,
   PRIMARY KEY(id_panier),
   FOREIGN KEY(id_user) REFERENCES USER(id_user),
   FOREIGN KEY(id_ski) REFERENCES SKI(id_ski)
);

CREATE TABLE COMMANDE(
   id_commande INT AUTO_INCREMENT NOT NULL,
   date_achat_commande DATE,
   id_etat INT NOT NULL,
   id_user INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_etat) REFERENCES ETAT(id_etat),
   FOREIGN KEY(id_user) REFERENCES USER(id_user)
);

CREATE TABLE COMMENTAIRE(
   id_commentaire INT AUTO_INCREMENT NOT NULL,
   texte_commentaire VARCHAR(5000),
   id_user INT NOT NULL,
   id_ski INT NOT NULL,
   PRIMARY KEY(id_commentaire),
   FOREIGN KEY(id_user) REFERENCES USER(id_user),
   FOREIGN KEY(id_ski) REFERENCES SKI(id_ski)
);

CREATE TABLE Fourni(
   id_ski INT,
   id_fournisseur INT,
   PRIMARY KEY(id_ski, id_fournisseur),
   FOREIGN KEY(id_ski) REFERENCES SKI(id_ski),
   FOREIGN KEY(id_fournisseur) REFERENCES FOURNISSEUR(id_fournisseur)
);

CREATE TABLE Ligne(
   id_ski INT,
   id_commande INT,
   prix_unit_ligne DECIMAL(8,2),
   quantite_ligne INT,
   PRIMARY KEY(id_ski, id_commande),
   FOREIGN KEY(id_ski) REFERENCES SKI(id_ski),
   FOREIGN KEY(id_commande) REFERENCES COMMANDE(id_commande)
);

CREATE TABLE Est_contenu(
   id_ski INT,
   id_livraison_stock INT,
   prix_unit_est_contenu DECIMAL(8,2),
   quantite_est_contenu INT,
   PRIMARY KEY(id_ski, id_livraison_stock),
   FOREIGN KEY(id_ski) REFERENCES SKI(id_ski),
   FOREIGN KEY(id_livraison_stock) REFERENCES LIVRAISON_STOCK(id_livraison_stock)
);

INSERT INTO user (id_user, email_user, username_user, password_user, role_user,  est_actif_user) VALUES
(NULL, 'admin@admin.fr', 'admin', 'sha256$pBGlZy6UukyHBFDH$2f089c1d26f2741b68c9218a68bfe2e25dbb069c27868a027dad03bcb3d7f69a', 'ROLE_admin', 1);
INSERT INTO user  (id_user, email_user, username_user, password_user, role_user,  est_actif_user) VALUES
(NULL, 'client@client.fr', 'client', 'sha256$Q1HFT4TKRqnMhlTj$cf3c84ea646430c98d4877769c7c5d2cce1edd10c7eccd2c1f9d6114b74b81c4', 'ROLE_client', 1);
INSERT INTO user  (id_user, email_user, username_user, password_user, role_user,  est_actif_user) VALUES
(NULL, 'client2@client2.fr', 'client2', 'sha256$ayiON3nJITfetaS8$0e039802d6fac2222e264f5a1e2b94b347501d040d71cfa4264cad6067cf5cf3', 'ROLE_client',1);
INSERT INTO etat (id_etat, libelle_etat) VALUES
(NULL, 'Livrée');
INSERT INTO commande (id_commande, date_achat_commande, id_etat, id_user) VALUES
(NULL, '2022-02-03', 1, 2);
