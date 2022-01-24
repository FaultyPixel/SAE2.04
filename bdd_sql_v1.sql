DROP TABLE IF EXISTS PANIER;
DROP TABLE IF EXISTS LIGNE;
DROP TABLE IF EXISTS COMMANDE;
DROP TABLE IF EXISTS ETAT;
DROP TABLE IF EXISTS USER;

-- user (id,username, password, role, est_actif, pseudo, email)
CREATE TABLE IF NOT EXISTS USER(
    id INT AUTO_INCREMENT NOT NULL,
    username VARCHAR(30),
    password VARCHAR(50),
    role VARCHAR(30),
    est_actif BOOLEAN,
    pseudo VARCHAR(30),
    email VARCHAR(50),
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
-- ligne_commande ( #commande_id , #ski_id , prix_unit, quantite)
CREATE TABLE  IF NOT EXISTS LIGNE (
    commande_id INT,
    ski_id INT,
    prix_unit DECIMAL(8, 2),
    quantite INT,
    PRIMARY KEY (commande_id, ski_id),
    CONSTRAINT fk_ligne_commande FOREIGN KEY (commande_id) REFERENCES COMMANDE(id),
    CONSTRAINT fk_ligne_article FOREIGN KEY (ski_id) REFERENCES SKI(id)
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
    CONSTRAINT fk_panier_ski FOREIGN KEY (ski_id) REFERENCES SKI(id)
);
-- etat (id, libelle ) 
CREATE TABLE IF NOT EXISTS ETAT (
    id INT AUTO_INCREMENT NOT NULL,
    libelle VARCHAR(20),
    PRIMARY KEY (id)
);