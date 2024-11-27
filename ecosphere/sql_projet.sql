DROP TABLE IF EXISTS Inscription;
DROP TABLE IF EXISTS Evaluation;
DROP TABLE IF EXISTS Participant;
DROP TABLE IF EXISTS Seance;
DROP TABLE IF EXISTS Atelier;
DROP TABLE IF EXISTS Lieu;
DROP TABLE IF EXISTS Animateur;


CREATE TABLE Animateur(
    N_Animateur INT AUTO_INCREMENT ,
    Nom_Animateur VARCHAR(255),
    PRIMARY KEY(N_Animateur)
);

CREATE TABLE Lieu(
    IDlieu INT AUTO_INCREMENT,
    NomLieu VARCHAR(255),
    PRIMARY KEY(IDlieu)
);

CREATE TABLE Atelier(
    id_atelier  INT AUTO_INCREMENT,
    Nom_Atelier VARCHAR(255),
    N_Animateur INT,
    FOREIGN KEY (N_Animateur) REFERENCES Animateur(N_Animateur),
    PRIMARY KEY (id_atelier)
);

CREATE TABLE Seance(
    id_Seance INT AUTO_INCREMENT,
    DateSeance DATE,
    PlacesDisponibles INT,
    IDlieu INT,
    id_atelier INT,
    FOREIGN KEY (IDlieu) REFERENCES Lieu(IDlieu),
    FOREIGN KEY (id_atelier) REFERENCES Atelier(id_atelier),
    PRIMARY KEY (id_Seance)
);

CREATE TABLE Participant(
    idParticipant INT AUTO_INCREMENT,
    Nom_Participant VARCHAR(255),
    Email_Participant VARCHAR(255),
    PRIMARY KEY (idParticipant)
);

CREATE TABLE Inscription(
    id_inscription INT AUTO_INCREMENT,
    idSeance INT,
    idParticipant INT,
    date_insccription DATE,
    priInscription INT,
    PRIMARY KEY (id_inscription),
    FOREIGN KEY (idSeance) REFERENCES Seance(id_Seance),
    FOREIGN KEY (idParticipant) REFERENCES Participant(idParticipant)
);

CREATE TABLE Evaluation(
    id_evaluation INT AUTO_INCREMENT,
    N_Animateur    INT,
    idSeance       INT,
    idParticipant  INT,
    Note_Seance    INT,
    Note_Animation INT,
    PRIMARY KEY (id_evaluation),
    FOREIGN KEY (N_Animateur) REFERENCES Animateur (N_Animateur),
    FOREIGN KEY (idSeance) REFERENCES Seance (id_Seance),
    FOREIGN KEY (idParticipant) REFERENCES Participant (idParticipant)
);


INSERT INTO  Animateur VALUES (NULL,'Enzo'),
                              (NULL,'Axel'),
                              (NULL,'Sirta');

INSERT INTO Lieu VALUES (NULL, 'Strasbourg'),
                        (NULL, 'Perpignan'),
                        (NULL, 'Belfort');

INSERT INTO Atelier VALUES (NULL, 'la Fresque du Climat', 2),
                           (NULL, 'Ma Terre en 180 miutes', 1),
                           (NULL, 'La Fresque du Numérique', 3);

INSERT INTO Seance VALUES (NULL,'2024-12-01',50,2,2),
                          (NULL,'2024-12-24',77,3,1),
                          (null,'2024-11-29',666,2,3);

INSERT INTO Participant VALUES (NULL,'Anas','anas@gmail.com'),
                               (NULL,'Katherine','katherine@gmail.com'),
                               (NULL,'Sara','sara@gmail.com');

INSERT INTO Inscription VALUES (NULL,1,3,'2025-01-25',14),
                               (NULL,1,1,'2025-02-13',11),
                               (NULL,3,2,'2025-03-01',66);

INSERT INTO Evaluation VALUES (NULL,1,1,1,20,17),
                              (NULL,2,2,2,19,20),
                              (NULL,3,3,3,15,11);



SELECT COUNT(Inscription.idParticipant) AS TotalInscriptions , SUM(Seance.PlacesDisponibles) AS TotalPlacesDisponibles
FROM Inscription
INNER JOIN Seance ON Inscription.idSeance = Seance.id_Seance
WHERE Seance.id_Seance = 1
;

SELECT Participant.Nom_Participant,AVG(Evaluation.Note_Seance) AS MoyenneNoteSeance,AVG(Evaluation.Note_Animation) AS MoyenneNoteAnimation
FROM Participant
INNER JOIN Inscription ON Participant.idParticipant = Inscription.idParticipant
INNER JOIN Evaluation ON Participant.idParticipant = Evaluation.idParticipant
WHERE Evaluation.idSeance = 1
GROUP BY Participant.Nom_Participant
;



SELECT Atelier.Nom_Atelier,SUM(Seance.PlacesDisponibles) AS TotalPlacesDisponibles
FROM Atelier
LEFT JOIN Seance ON Atelier.id_atelier = Seance.id_atelier
WHERE Seance.PlacesDisponibles < 100
GROUP BY Atelier.Nom_Atelier
;


SELECT Seance.DateSeance, COUNT(Inscription.idParticipant) AS NombreParticipants, Seance.PlacesDisponibles
FROM Seance
LEFT JOIN Inscription ON Seance.id_Seance = Inscription.idSeance
GROUP BY Seance.id_Seance
;


