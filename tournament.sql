CREATE TABLE tournaments (
    id serial PRIMARY KEY,
    title text NOT NULL
);


CREATE TABLE players (
    id serial PRIMARY KEY,
    name text NOT NULL,
    tournament int REFERENCES tournaments (id) ON DELETE SET NULL
);


CREATE TABLE matches (
    id serial PRIMARY KEY,
    winner int REFERENCES players (id) ON DELETE CASCADE,
    loser int REFERENCES players (id) ON DELETE CASCADE,
    tournament int REFERENCES tournaments (id) ON DELETE CASCADE
);


CREATE VIEW standings AS
    SELECT p.id as id, p.name as name, count(
        CASE WHEN p.id = m.winner THEN 1 END) as wins,
        count(m.id) as matches, p.tournament as tournament
    FROM players as p LEFT JOIN matches as m
    ON (p.id = m.winner OR p.id = m.loser) AND p.tournament = m.tournament
    GROUP BY p.id
    ORDER BY p.tournament, wins DESC;


CREATE VIEW pairings AS
    SELECT a.id as id1, a.name as name1, b.id as id2, b.name as name2, 
    a.tournament as tournament, a.wins + b.wins as totalwins
    FROM standings as a INNER JOIN standings as b
    ON ((a.wins = b.wins) OR (a.wins - b.wins = 1) OR (b.wins - a.wins = 1))
    AND a.tournament = b.tournament
    WHERE a.id < b.id
    ORDER BY totalwins DESC;


CREATE TABLE names (
  id SERIAL PRIMARY KEY,
  name varchar(255) default NULL
);


INSERT INTO "names" (name) VALUES ('Maldonado'),('Lott'),('Kent'),('Cochran'),('Osborn'),('Cherry'),('English'),('Pittman'),('Myers'),('Herrera');
INSERT INTO "names" (name) VALUES ('Duffy'),('Vang'),('Skinner'),('Landry'),('Kirk'),('Banks'),('Curtis'),('Mclaughlin'),('Kennedy'),('Fields');
INSERT INTO "names" (name) VALUES ('Mcmahon'),('Day'),('Maddox'),('Baxter'),('Hendrix'),('Cohen'),('Ramsey'),('Klein'),('Diaz'),('Buckner');
INSERT INTO "names" (name) VALUES ('Berger'),('Tyler'),('Barron'),('Schneider'),('Owens'),('Bright'),('Lewis'),('Mckenzie'),('Craft'),('Walter');
INSERT INTO "names" (name) VALUES ('Justice'),('Bernard'),('Coffey'),('Kane'),('Bonner'),('Oconnor'),('Paul'),('Ayala'),('Randolph'),('Ingram');
INSERT INTO "names" (name) VALUES ('Mcmahon'),('Andrews'),('Klein'),('Armstrong'),('Peterson'),('Berger'),('Peck'),('Marsh'),('Gonzalez'),('Lawrence');
INSERT INTO "names" (name) VALUES ('Nixon'),('Hammond'),('Bridges'),('Watts'),('Strickland'),('Vega'),('Malone'),('Pickett'),('Carey'),('Shepard');
INSERT INTO "names" (name) VALUES ('Ford'),('Tyson'),('Banks'),('Bartlett'),('Pruitt'),('Mclaughlin'),('Mccarthy'),('Ruiz'),('Coffey'),('Rosario');
INSERT INTO "names" (name) VALUES ('Cantu'),('Day'),('Morrison'),('Farmer'),('Ratliff'),('Nichols'),('Oneil'),('Mann'),('Waller'),('Nielsen');
INSERT INTO "names" (name) VALUES ('Holman'),('Nelson'),('Richard'),('Mejia'),('Byers'),('Wright'),('Forbes'),('Solomon'),('Robbins'),('Prince');
