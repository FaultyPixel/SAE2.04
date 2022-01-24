DROP TABLE IF EXISTS PANIER;
DROP TABLE IF EXISTS LIGNE;
DROP TABLE IF EXISTS COMMANDE;
DROP TABLE IF EXISTS ETAT;
DROP TABLE IF EXISTS USER;
DROP TABLE IF EXISTS Vendu;
DROP TABLE IF EXISTS FOURNISSEUR;
DROP TABLE IF EXISTS SKI;
DROP TABLE IF EXISTS NOYAU;
DROP TABLE IF EXISTS FIXATION;
DROP TABLE IF EXISTS FABRICANT;
DROP TABLE IF EXISTS VILLE;
DROP TABLE IF EXISTS PAYS_FABRICATION;
DROP TABLE IF EXISTS POIDS_SKIEUR;
DROP TABLE IF EXISTS NIVEAU_SKIEUR;
DROP TABLE IF EXISTS ANNEE;
DROP TABLE IF EXISTS SEXE;
DROP TABLE IF EXISTS TYPE_SKI;

-- user (id,username, password, role, est_actif, pseudo, email)
CREATE TABLE IF NOT EXISTS USER(
    id INT AUTO_INCREMENT NOT NULL,
    username VARCHAR(30),
    password VARCHAR(2000),
    role VARCHAR(30),
    est_actif BOOLEAN,
    pseudo VARCHAR(30),
    email VARCHAR(50),
    PRIMARY KEY (id)
);
-- etat (id, libelle ) 
CREATE TABLE IF NOT EXISTS ETAT (
    id INT AUTO_INCREMENT NOT NULL,
    libelle VARCHAR(20),
    PRIMARY KEY (id)
);
-- commande (id, date_achat, #user_id, #etat_id)
CREATE TABLE IF NOT EXISTS COMMANDE (
    id INT AUTO_INCREMENT NOT NULL,
    date_achat DATE,
    user_id INT,
    etat_id INT,
    PRIMARY KEY (id),
    CONSTRAINT fk_commande_user FOREIGN KEY (user_id) REFERENCES USER(id),
    CONSTRAINT fk_commande_etat FOREIGN KEY (etat_id) REFERENCES ETAT(id)
);

CREATE TABLE TYPE_SKI(
   id_type_ski INT,
   libelle_type_ski VARCHAR(30),
   PRIMARY KEY(id_type_ski)
);

CREATE TABLE SEXE(
   id_sexe INT,
   libelle_sexe VARCHAR(30),
   PRIMARY KEY(id_sexe)
);

CREATE TABLE ANNEE(
   id_annee INT,
   libelle_annee DATE,
   PRIMARY KEY(id_annee)
);

CREATE TABLE NIVEAU_SKIEUR(
   id_niveau_skieur INT,
   libelle_niveau_skieur VARCHAR(30),
   PRIMARY KEY(id_niveau_skieur)
);

CREATE TABLE POIDS_SKIEUR(
   id_poids_skieur INT,
   poids_skieur_min DECIMAL(5,2),
   poids_skieur_max DECIMAL(5,2),
   PRIMARY KEY(id_poids_skieur)
);

CREATE TABLE PAYS_FABRICATION(
   id_pays_fabrication INT,
   libelle_pays_fabrication VARCHAR(30),
   PRIMARY KEY(id_pays_fabrication)
);

CREATE TABLE VILLE(
   id_ville INT,
   libelle_ville VARCHAR(30),
   code_postal_ville VARCHAR(5),
   PRIMARY KEY(id_ville)
);

CREATE TABLE FABRICANT(
   id_fabricant INT,
   libelle_fabricant VARCHAR(30),
   telephone_fabricant VARCHAR(10),
   mail_fabricant VARCHAR(30),
   id_ville INT NOT NULL,
   PRIMARY KEY(id_fabricant),
   FOREIGN KEY(id_ville) REFERENCES VILLE(id_ville)
);

CREATE TABLE FIXATION(
   id_fixation INT,
   libelle_fixation DATE,
   PRIMARY KEY(id_fixation)
);

CREATE TABLE NOYAU(
   id_noyau INT,
   libelle_noyau DATE,
   PRIMARY KEY(id_noyau)
);

CREATE TABLE SKI(
   id_ski INT,
   modele_ski VARCHAR(30),
   image_ski VARCHAR(30),
   prix_ski DECIMAL(8,2),
   poids_ski DECIMAL(4,2),
   longueur_ski DECIMAL(5,2),
   largeur_ski DECIMAL(4,2),
   id_pays_fabrication INT NOT NULL,
   id_niveau_skieur INT,
   id_poids_skieur INT,
   id_noyau INT NOT NULL,
   id_fixation INT,
   id_annee INT NOT NULL,
   id_sexe INT NOT NULL,
   id_fabricant INT NOT NULL,
   id_type_ski INT NOT NULL,
   PRIMARY KEY(id_ski),
   FOREIGN KEY(id_pays_fabrication) REFERENCES PAYS_FABRICATION(id_pays_fabrication),
   FOREIGN KEY(id_niveau_skieur) REFERENCES NIVEAU_SKIEUR(id_niveau_skieur),
   FOREIGN KEY(id_poids_skieur) REFERENCES POIDS_SKIEUR(id_poids_skieur),
   FOREIGN KEY(id_noyau) REFERENCES NOYAU(id_noyau),
   FOREIGN KEY(id_fixation) REFERENCES FIXATION(id_fixation),
   FOREIGN KEY(id_annee) REFERENCES ANNEE(id_annee),
   FOREIGN KEY(id_sexe) REFERENCES SEXE(id_sexe),
   FOREIGN KEY(id_fabricant) REFERENCES FABRICANT(id_fabricant),
   FOREIGN KEY(id_type_ski) REFERENCES TYPE_SKI(id_type_ski)
);

CREATE TABLE FOURNISSEUR(
   id_fournisseur INT,
   libelle_fournisseur VARCHAR(30),
   telephone_fournisseur VARCHAR(10),
   mail_fournisseur VARCHAR(30),
   id_ville INT NOT NULL,
   PRIMARY KEY(id_fournisseur),
   FOREIGN KEY(id_ville) REFERENCES VILLE(id_ville)
);

CREATE TABLE Vendu(
   id_ski INT,
   id_fournisseur INT,
   PRIMARY KEY(id_ski, id_fournisseur),
   FOREIGN KEY(id_ski) REFERENCES SKI(id_ski),
   FOREIGN KEY(id_fournisseur) REFERENCES FOURNISSEUR(id_fournisseur)
);
-- ligne_commande ( #commande_id , #ski_id , prix_unit, quantite)
CREATE TABLE  IF NOT EXISTS LIGNE (
    commande_id INT,
    ski_id INT,
    prix_unit DECIMAL(8, 2),
    quantite INT,
    PRIMARY KEY (commande_id, ski_id),
    CONSTRAINT fk_ligne_commande FOREIGN KEY (commande_id) REFERENCES COMMANDE(id),
    CONSTRAINT fk_ligne_article FOREIGN KEY (ski_id) REFERENCES SKI(id_ski)
);
-- panier (id, date_ajout,  #user_id , #ski_id, prix_unit, quantite)
CREATE TABLE IF NOT EXISTS PANIER (
    id INT AUTO_INCREMENT NOT NULL,
    date_ajout DATE,
    user_id INT,
    ski_id INT,
    prix_unit DECIMAL(8, 2),
    quantite INT,
    PRIMARY KEY (id),
    CONSTRAINT fk_panier_user FOREIGN KEY (user_id) REFERENCES USER(id),
    CONSTRAINT fk_panier_ski FOREIGN KEY (ski_id) REFERENCES SKI(id_ski)
);
