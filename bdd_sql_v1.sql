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

#====CREATE TABLE IF NOT EXISTS====
CREATE TABLE IF NOT EXISTS TYPE_SKI(
   id_type_ski INT AUTO_INCREMENT NOT NULL,
   libelle_type_ski VARCHAR(30),
   PRIMARY KEY(id_type_ski)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS FOURNISSEUR(
   id_fournisseur INT AUTO_INCREMENT NOT NULL,
   libelle_fournisseur VARCHAR(30),
   telephone_fournisseur VARCHAR(10),
   mail_fournisseur VARCHAR(30),
   adresse_fournisseur VARCHAR(100),
   PRIMARY KEY(id_fournisseur)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS SEXE(
   id_sexe INT AUTO_INCREMENT NOT NULL,
   libelle_sexe VARCHAR(30),
   PRIMARY KEY(id_sexe)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS NIVEAU_SKIEUR(
   id_niveau_skieur INT AUTO_INCREMENT NOT NULL,
   libelle_niveau_skieur VARCHAR(30),
   PRIMARY KEY(id_niveau_skieur)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS POIDS_SKIEUR(
   id_poids_skieur INT AUTO_INCREMENT NOT NULL,
   poids_skieur_min INT,
   poids_skieur_max INT,
   PRIMARY KEY(id_poids_skieur)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS PAYS_FABRICATION(
   id_pays_fabrication INT AUTO_INCREMENT NOT NULL,
   libelle_pays_fabrication VARCHAR(30),
   PRIMARY KEY(id_pays_fabrication)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS FABRICANT(
   id_fabricant INT AUTO_INCREMENT NOT NULL,
   libelle_fabricant VARCHAR(30),
   telephone_fabricant VARCHAR(10),
   mail_fabricant VARCHAR(30),
   PRIMARY KEY(id_fabricant)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS FIXATION(
   id_fixation INT AUTO_INCREMENT NOT NULL,
   libelle_fixation VARCHAR(50),
   PRIMARY KEY(id_fixation)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS NOYAU(
   id_noyau INT AUTO_INCREMENT NOT NULL,
   libelle_noyau VARCHAR(50),
   PRIMARY KEY(id_noyau)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS USER(
   id_user INT AUTO_INCREMENT NOT NULL,
   username_user VARCHAR(30),
   password_user VARCHAR(5000),
   role_user VARCHAR(30),
   est_actif_user BOOLEAN,
   email_user VARCHAR(50),
   adresse_user VARCHAR(100),
   PRIMARY KEY(id_user)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS ETAT(
   id_etat INT AUTO_INCREMENT NOT NULL,
   libelle_etat VARCHAR(20),
   PRIMARY KEY(id_etat)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS LIVRAISON_STOCK(
   id_livraison_stock INT AUTO_INCREMENT NOT NULL,
   date_livraison_stock DATE,
   id_etat INT NOT NULL,
   id_fournisseur INT NOT NULL,
   PRIMARY KEY(id_livraison_stock),
   FOREIGN KEY(id_etat) REFERENCES ETAT(id_etat),
   FOREIGN KEY(id_fournisseur) REFERENCES FOURNISSEUR(id_fournisseur)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS SKI(
   id_ski INT AUTO_INCREMENT NOT NULL,
   modele_ski VARCHAR(150),
   image_ski VARCHAR(50),
   prix_ski DECIMAL(8,2),
   poids_ski INT,
   longueur_ski INT,
   stock_ski INT,
   note_ski DECIMAL(2,1),
   nb_note INT,
   AAAA INT,
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
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS PANIER(
   id_panier INT AUTO_INCREMENT NOT NULL,
   quantite_panier INT,
   id_user INT NOT NULL,
   id_ski INT NOT NULL,
   PRIMARY KEY(id_panier),
   FOREIGN KEY(id_user) REFERENCES USER(id_user),
   FOREIGN KEY(id_ski) REFERENCES SKI(id_ski)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS COMMANDE(
   id_commande INT AUTO_INCREMENT NOT NULL,
   date_achat_commande DATE,
   id_etat INT NOT NULL,
   id_user INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_etat) REFERENCES ETAT(id_etat),
   FOREIGN KEY(id_user) REFERENCES USER(id_user)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS COMMENTAIRE(
   id_commentaire INT AUTO_INCREMENT NOT NULL,
   texte_commentaire VARCHAR(5000),
   id_user INT NOT NULL,
   id_ski INT NOT NULL,
   PRIMARY KEY(id_commentaire),
   FOREIGN KEY(id_user) REFERENCES USER(id_user),
   FOREIGN KEY(id_ski) REFERENCES SKI(id_ski)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS Fourni(
   id_ski INT,
   id_fournisseur INT,
   PRIMARY KEY(id_ski, id_fournisseur),
   FOREIGN KEY(id_ski) REFERENCES SKI(id_ski),
   FOREIGN KEY(id_fournisseur) REFERENCES FOURNISSEUR(id_fournisseur)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS Ligne(
   id_ski INT,
   id_commande INT,
   prix_unit_ligne DECIMAL(8,2),
   quantite_ligne INT,
   PRIMARY KEY(id_ski, id_commande),
   FOREIGN KEY(id_ski) REFERENCES SKI(id_ski),
   FOREIGN KEY(id_commande) REFERENCES COMMANDE(id_commande)
)CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS Est_contenu(
   id_ski INT,
   id_livraison_stock INT,
   prix_unit_est_contenu DECIMAL(8,2),
   quantite_est_contenu INT,
   PRIMARY KEY(id_ski, id_livraison_stock),
   FOREIGN KEY(id_ski) REFERENCES SKI(id_ski),
   FOREIGN KEY(id_livraison_stock) REFERENCES LIVRAISON_STOCK(id_livraison_stock)
)CHARACTER SET utf8mb4;

# INSERTION BASE USERS
INSERT INTO USER (id_user, email_user, username_user, password_user, role_user,  est_actif_user) VALUES
(NULL, 'admin@admin.fr', 'admin', 'sha256$pBGlZy6UukyHBFDH$2f089c1d26f2741b68c9218a68bfe2e25dbb069c27868a027dad03bcb3d7f69a', 'ROLE_admin', 1);
INSERT INTO USER  (id_user, email_user, username_user, password_user, role_user,  est_actif_user) VALUES
(NULL, 'client@client.fr', 'client', 'sha256$Q1HFT4TKRqnMhlTj$cf3c84ea646430c98d4877769c7c5d2cce1edd10c7eccd2c1f9d6114b74b81c4', 'ROLE_client', 1);
INSERT INTO USER  (id_user, email_user, username_user, password_user, role_user,  est_actif_user) VALUES
(NULL, 'client2@client2.fr', 'client2', 'sha256$ayiON3nJITfetaS8$0e039802d6fac2222e264f5a1e2b94b347501d040d71cfa4264cad6067cf5cf3', 'ROLE_client',1);

# LOAD DATA LOCAL INFILE 'user.csv' INTO TABLE USER FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE './JeuTest/fabricant.csv' INTO TABLE FABRICANT FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE './JeuTest/fixation.csv' INTO TABLE FIXATION FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE './JeuTest/fournisseur.csv' INTO TABLE FOURNISSEUR FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE './JeuTest/noyau.csv' INTO TABLE NOYAU FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE './JeuTest/pays_fabrication.csv' INTO TABLE PAYS_FABRICATION FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE './JeuTest/poids_skieur.csv' INTO TABLE POIDS_SKIEUR FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE './JeuTest/sexe.csv' INTO TABLE SEXE FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE './JeuTest/type_ski.csv' INTO TABLE TYPE_SKI FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE './JeuTest/niveau_skieur.csv' INTO TABLE NIVEAU_SKIEUR FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE './JeuTest/ski.csv' INTO TABLE SKI FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE './JeuTest/fourni.csv' INTO TABLE Fourni FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE './JeuTest/etat.csv' INTO TABLE ETAT FIELDS TERMINATED BY ',';
