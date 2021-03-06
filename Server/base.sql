BEGIN TRANSACTION;
DROP TABLE IF EXISTS "Meteo";
CREATE TABLE IF NOT EXISTS "Meteo" (
	"pays"	VARCHAR(255),
	"date_debut"	DATE,
	"date_fin"	DATE,
	"meteo"	VARCHAR(255),
	PRIMARY KEY("pays","date_debut","date_fin"),
	FOREIGN KEY("pays") REFERENCES "Destination"("pays")
);
DROP TABLE IF EXISTS "Offre";
CREATE TABLE IF NOT EXISTS "Offre" (
	"id_offre"	INT NOT NULL,
	"ville"	VARCHAR(255),
	"nom_vendeur"	VARCHAR(255),
	"moyen_transport"	VARCHAR(255),
	"ville_depart"	VARCHAR(255),
	"date_offre"	DATE NOT NULL,
	"prix_offre"	FLOAT NOT NULL,
	"site"	VARCHAR(255),
	PRIMARY KEY("id_offre"),
	FOREIGN KEY("nom_vendeur") REFERENCES "Vendeur"("nom_vendeur"),
	FOREIGN KEY("ville") REFERENCES "Destination"("ville")
);
DROP TABLE IF EXISTS "Vendeur";
CREATE TABLE IF NOT EXISTS "Vendeur" (
	"nom_vendeur"	VARCHAR(255),
	"email"	VARCHAR(255) UNIQUE,
	"mdp"	VARCHAR(255),
	PRIMARY KEY("nom_vendeur"),
	FOREIGN KEY("nom_vendeur") REFERENCES "Offre"("nom_vendeur")
);
DROP TABLE IF EXISTS "Destination";
CREATE TABLE IF NOT EXISTS "Destination" (
	"ville"	VARCHAR(255),
	"pays"	VARCHAR(255),
	"environnement"	VARCHAR(255),
	"urbanisme"	VARCHAR(255),
	PRIMARY KEY("ville"),
	FOREIGN KEY("ville") REFERENCES "Destination"("ville"),
	FOREIGN KEY("pays") REFERENCES "Meteo"("pays")
);
COMMIT;
