## Table des matières

1. [Le schéma](#1-le-schéma)
2. [Les relations](#2-les-relations)
   2.1. [Lecture des relations](#22-livre--auteur--nn)
   2.2. [LIVRE ↔ AUTEUR : N:N](#22-livre--auteur--nn)
   2.3. [LIVRE ↔ CATEGORIE : N:N](#23-livre--categorie--nn)
3. [Scripts](#3-script)
   3.1. [01_create_bibliotheque.sql](#31-01_create_bibliothequesql)
   3.2. [02_insert_bibliotheque.sql](#32-02_insert_bibliothequesql)
   3.3. [03_requetes_bibliotheque.sql](#33-03_requetes_bibliothequesql)
4. [Se connecter sous Linux](#4-se-connecter-sous-linux)

# 1. Le schéma

```text
                                  ┌──────────────────────────┐
                                  │          AUTEUR          │
                                  ├──────────────────────────┤
                                  │ PK id_auteur             │
                                  │    nom                   │
                                  │    prenom                │
                                  │    date_naissance        │
                                  │    date_deces            │
                                  └────────────┬─────────────┘
                                               │
                                               │ 1
                                               │
                                               │ N
                                  ┌────────────▼─────────────┐
                                  │       LIVRE_AUTEUR       │
                                  ├──────────────────────────┤
                                  │ PK,FK id_livre           │
                                  │ PK,FK id_auteur          │
                                  └────────────┬─────────────┘
                                               │
                                               │ N
                                               │
                                               │ 1
                                  ┌────────────▼─────────────┐
                                  │          LIVRE           │
                                  ├──────────────────────────┤
                                  │ PK id_livre              │
                                  │    titre                 │
                                  │    sous_titre            │
                                  │    annee_parution        │
                                  │    nb_pages              │
                                  │    resume                │
                                  └──────┬───────────┬───────┘
                                         │           │
                                      1  │           │ 1
                                         │           │
                                      N  │           │ N
                        ┌────────────────▼──┐      ┌─▼────────────────────┐
                        │ LIVRE_CATEGORIE   │      │        EDITION       │
                        ├───────────────────┤      ├──────────────────────┤
                        │ PK,FK id_livre    │      │ PK id_edition        │
                        │ PK,FK id_categorie│      │ FK id_livre          │
                        └────────┬──────────┘      │    editeur           │
                                 │                 │    annee_edition     │
                                 │ N               │    isbn13            │
                                 │                 │    format            │
                                 │ 1               └──────────┬───────────┘
                        ┌────────▼─────────┐                  │
                        │    CATEGORIE     │                  │ 1
                        ├──────────────────┤                  │
                        │ PK id_categorie  │                  │ N
                        │    nom           │       ┌──────────▼───────────┐
                        └──────────────────┘       │      EXEMPLAIRE      │
                                                   ├──────────────────────┤
                                                   │ PK id_exemplaire     │
                                                   │ FK id_edition        │
                                                   │    etat              │
                                                   │    emplacement       │
                                                   └──────────┬───────────┘
                                                              │
                                                              │ 1
                                                              │
                                                              │ N
                                                   ┌──────────▼───────────┐
                                                   │        LECTURE       │
                                                   ├──────────────────────┤
                                                   │ PK id_lecture        │
                                                   │ FK id_exemplaire     │
                                                   │    date_debut        │
                                                   │    date_fin          │
                                                   │    statut            │
                                                   │    note              │
                                                   └──────────┬───────────┘
                                                              │
                                                              │ 1
                                                              │
                                                              │ N
                                                   ┌──────────▼───────────┐
                                                   │         NOTE         │
                                                   ├──────────────────────┤
                                                   │ PK id_note           │
                                                   │ FK id_lecture        │
                                                   │    titre             │
                                                   │    contenu           │
                                                   └──────────────────────┘
               
```

#### [Table des matières](#table-des-matières)

---

# 2. Les relations
## 2.1. Lecture des relations

```text
       AUTEUR 1 ───── N LIVRE_AUTEUR N ───── 1 LIVRE
                                                   │
                                                   │
                       ┌───────────────────────────┼
                       │                           │                   
                       │ N                         │ N                 
                       ▼                           ▼                   
               LIVRE_CATEGORIE                 EDITION              
                       │ N                         │ 1              
                       │ 1                         │ N              
                       ▼                           ▼                
                   CATEGORIE                  EXEMPLAIRE               
                                                   │ 1                  
                                                   │ N                 
                                                   ▼                   
                                                LECTURE                 
                                                   │ 1                   
                                                   │ N                 
                                                   ▼                    
                                                  NOTE                  
```

| Relation                        | Cardinalité | Explication                                              |
| ------------------------------- | ----------- | -------------------------------------------------------- |
| `AUTEUR` → `LIVRE_AUTEUR`       | **1:N**     | Un auteur peut être associé à plusieurs livres           |
| `LIVRE` → `LIVRE_AUTEUR`        | **1:N**     | Un livre peut avoir plusieurs auteurs                    |
| `LIVRE` ↔ `AUTEUR`              | **N:N**     | Plusieurs auteurs peuvent écrire plusieurs livres        |
| `LIVRE` → `EDITION`             | **1:N**     | Une œuvre peut avoir plusieurs éditions                  |
| `EDITION` → `EXEMPLAIRE`        | **1:N**     | On peut posséder plusieurs exemplaires d'une édition     |
| `EXEMPLAIRE` → `LECTURE`        | **1:N**     | Un exemplaire peut être lu plusieurs fois                |
| `LECTURE` → `NOTE`              | **1:N**     | Une lecture peut produire plusieurs notes                |
| `LIVRE` → `LIVRE_CATEGORIE`     | **1:N**     | Un livre peut avoir plusieurs catégories                 |
| `CATEGORIE` → `LIVRE_CATEGORIE` | **1:N**     | Une catégorie peut contenir plusieurs livres             |
| `LIVRE` ↔ `CATEGORIE`           | **N:N**     | Un livre peut appartenir à plusieurs catégories          |

#### [Table des matières](#table-des-matières)

---

## 2.2. `LIVRE ↔ AUTEUR : N:N`

```text
                    AUTEUR
                      │
                1     │     N
                 \    │    /
                  \   │   /
                LIVRE_AUTEUR
                  /   │   \
                 /    │    \
                N     │     1
                      │
                    LIVRE
```

>Un auteur peut écrire plusieurs livres.
>Un livre peut être écrit par plusieurs auteurs. 2.3.

#### [Table des matières](#table-des-matières)

---

## 2.3. `LIVRE ↔ CATEGORIE : N:N`

```text
                 LIVRE
                   │
              N    │    N
               \   │   /
             LIVRE_CATEGORIE
               /   │   \
              /    │    \
             1     │     1
                   │
               CATEGORIE
```

>Un livre peut avoir plusieurs catégories, et une catégorie peut concerner plusieurs livres.

#### [Table des matières](#table-des-matières)

---

# 3. Script
## 3.1. 01_create_bibliotheque.sql

```sql
-- ============================================================
-- Fichier : 01_create_bibliotheque.sql
-- Objet   : Création de la base de données Bibliothèque
-- SGBD    : PostgreSQL
-- ============================================================

-- ============================================================
-- 1. CREATION DE LA BASE DE DONNEES
-- ============================================================

-- Cette partie doit être exécutée depuis une base existante
-- (par exemple postgres).
--
-- CREATE DATABASE bibliotheque;

-- Après création de la base :
-- \c bibliotheque


-- ============================================================
-- 2. CREATION DU SCHEMA
-- ============================================================

CREATE SCHEMA IF NOT EXISTS bibliotheque;

-- ============================================================
-- 3. TABLE AUTEUR
-- ============================================================

CREATE TABLE bibliotheque.auteur (
    id_auteur       BIGINT GENERATED ALWAYS AS IDENTITY,
    nom             VARCHAR(100) NOT NULL,
    prenom          VARCHAR(100),
    date_naissance  DATE,
    date_deces      DATE,

    CONSTRAINT pk_auteur
        PRIMARY KEY (id_auteur)
);

-- ============================================================
-- 4. TABLE LIVRE
-- ============================================================

CREATE TABLE bibliotheque.livre (
    id_livre        BIGINT GENERATED ALWAYS AS IDENTITY,
    titre           VARCHAR(500) NOT NULL,
    sous_titre      VARCHAR(500),
    annee_parution  INTEGER,
    nb_pages        INTEGER,
    resume          TEXT,

    CONSTRAINT pk_livre
        PRIMARY KEY (id_livre),

    CONSTRAINT ck_livre_annee
        CHECK (
            annee_parution IS NULL
            OR annee_parution > 0
        ),

    CONSTRAINT ck_livre_pages
        CHECK (
            nb_pages IS NULL
            OR nb_pages > 0
        )
);

-- ============================================================
-- 5. TABLE LIVRE_AUTEUR
--    Relation N:N entre LIVRE et AUTEUR
-- ============================================================

CREATE TABLE bibliotheque.livre_auteur (
    id_livre   BIGINT NOT NULL,
    id_auteur  BIGINT NOT NULL,

    CONSTRAINT pk_livre_auteur
        PRIMARY KEY (id_livre, id_auteur),

    CONSTRAINT fk_livre_auteur_livre
        FOREIGN KEY (id_livre)
        REFERENCES bibliotheque.livre (id_livre)
        ON DELETE CASCADE,

    CONSTRAINT fk_livre_auteur_auteur
        FOREIGN KEY (id_auteur)
        REFERENCES bibliotheque.auteur (id_auteur)
        ON DELETE CASCADE
);

-- ============================================================
-- 6. TABLE CATEGORIE
-- ============================================================

CREATE TABLE bibliotheque.categorie (
    id_categorie  BIGINT GENERATED ALWAYS AS IDENTITY,
    nom           VARCHAR(100) NOT NULL,

    CONSTRAINT pk_categorie
        PRIMARY KEY (id_categorie),

    CONSTRAINT uq_categorie_nom
        UNIQUE (nom)
);

-- ============================================================
-- 7. TABLE LIVRE_CATEGORIE
--    Relation N:N entre LIVRE et CATEGORIE
-- ============================================================

CREATE TABLE bibliotheque.livre_categorie (
    id_livre      BIGINT NOT NULL,
    id_categorie  BIGINT NOT NULL,

    CONSTRAINT pk_livre_categorie
        PRIMARY KEY (id_livre, id_categorie),

    CONSTRAINT fk_livre_categorie_livre
        FOREIGN KEY (id_livre)
        REFERENCES bibliotheque.livre (id_livre)
        ON DELETE CASCADE,

    CONSTRAINT fk_livre_categorie_categorie
        FOREIGN KEY (id_categorie)
        REFERENCES bibliotheque.categorie (id_categorie)
        ON DELETE CASCADE
);

-- ============================================================
-- 8. TABLE EDITION
-- ============================================================

CREATE TABLE bibliotheque.edition (
    id_edition     BIGINT GENERATED ALWAYS AS IDENTITY,
    id_livre       BIGINT NOT NULL,
    editeur        VARCHAR(200),
    annee_edition  INTEGER,
    isbn13         VARCHAR(13),
    format         VARCHAR(50),

    CONSTRAINT pk_edition
        PRIMARY KEY (id_edition),

    CONSTRAINT fk_edition_livre
        FOREIGN KEY (id_livre)
        REFERENCES bibliotheque.livre (id_livre)
        ON DELETE CASCADE,

    CONSTRAINT ck_edition_annee
        CHECK (
            annee_edition IS NULL
            OR annee_edition > 0
        ),

    CONSTRAINT ck_edition_isbn
        CHECK (
            isbn13 IS NULL
            OR isbn13 ~ '^[0-9]{13}$'
        )
);

-- ============================================================
-- 9. TABLE EXEMPLAIRE
--    Représente l'exemplaire physique possédé
-- ============================================================

CREATE TABLE bibliotheque.exemplaire (
    id_exemplaire  BIGINT GENERATED ALWAYS AS IDENTITY,
    id_edition     BIGINT NOT NULL,
    etat            VARCHAR(50),
    emplacement     VARCHAR(200),
    
    CONSTRAINT pk_exemplaire
        PRIMARY KEY (id_exemplaire),

    CONSTRAINT fk_exemplaire_edition
        FOREIGN KEY (id_edition)
        REFERENCES bibliotheque.edition (id_edition)
        ON DELETE RESTRICT,

    CONSTRAINT ck_exemplaire_prix
        CHECK (
            prix_achat IS NULL
            OR prix_achat >= 0
        )
);

-- ============================================================
-- 10. TABLE LECTURE
--     Historique des lectures
-- ============================================================

CREATE TABLE bibliotheque.lecture (
    id_lecture      BIGINT GENERATED ALWAYS AS IDENTITY,
    id_exemplaire   BIGINT NOT NULL,
    date_debut      DATE,
    date_fin        DATE,
    statut          VARCHAR(30) NOT NULL DEFAULT 'A_LIRE',
    note             NUMERIC(3,1),

    CONSTRAINT pk_lecture
        PRIMARY KEY (id_lecture),

    CONSTRAINT fk_lecture_exemplaire
        FOREIGN KEY (id_exemplaire)
        REFERENCES bibliotheque.exemplaire (id_exemplaire)
        ON DELETE CASCADE,

    CONSTRAINT ck_lecture_statut
        CHECK (
            statut IN (
                'A_LIRE',
                'EN_COURS',
                'TERMINE'
            )
        ),

    CONSTRAINT ck_lecture_note
        CHECK (
            note IS NULL
            OR note BETWEEN 0 AND 10
        ),

    CONSTRAINT ck_lecture_dates
        CHECK (
            date_fin IS NULL
            OR date_debut IS NULL
            OR date_fin >= date_debut
        )
);

-- ============================================================
-- 11. TABLE NOTE
--     Notes personnelles associées à une lecture
-- ============================================================

CREATE TABLE bibliotheque.note (
    id_note      BIGINT GENERATED ALWAYS AS IDENTITY,
    id_lecture   BIGINT NOT NULL,
    titre        VARCHAR(300),
    contenu      TEXT NOT NULL,

    CONSTRAINT pk_note
        PRIMARY KEY (id_note),

    CONSTRAINT fk_note_lecture
        FOREIGN KEY (id_lecture)
        REFERENCES bibliotheque.lecture (id_lecture)
        ON DELETE CASCADE
);

-- ============================================================
-- 12. INDEX
-- ============================================================

CREATE INDEX idx_livre_auteur_auteur
    ON bibliotheque.livre_auteur (id_auteur);

CREATE INDEX idx_livre_categorie_categorie
    ON bibliotheque.livre_categorie (id_categorie);

CREATE INDEX idx_edition_livre
    ON bibliotheque.edition (id_livre);

CREATE INDEX idx_exemplaire_edition
    ON bibliotheque.exemplaire (id_edition);

CREATE INDEX idx_lecture_exemplaire
    ON bibliotheque.lecture (id_exemplaire);

CREATE INDEX idx_note_lecture
    ON bibliotheque.note (id_lecture);

-- ============================================================
-- 13. VERIFICATION
-- ============================================================

SELECT
    table_schema,
    table_name
FROM information_schema.tables
WHERE table_schema = 'bibliotheque'
ORDER BY table_name;

-- ============================================================
-- FIN DU SCRIPT
-- ============================================================
```

### Utilisation

Il faut toutefois distinguer **la création de la base** de la création des tables.

Depuis votre terminal :

```bash
psql -h localhost -U postgres -p 5436
```

Puis :

```sql
CREATE DATABASE bibliotheque;
```

Quittez éventuellement `psql`, puis exécutez le fichier :

```bash
psql -h localhost -U postgres -p 5436 -d bibliotheque -f 01_create_bibliotheque.sql
```

Vous pouvez ensuite vérifier :

```sql
\c bibliotheque

\dt bibliotheque.*
```

On obtiens les **9 tables** :

```text
+--------------+-----------------+-------+----------+
|    Schema    |      Name       | Type  |  Owner   |
+--------------+-----------------+-------+----------+
| bibliotheque | auteur          | table | postgres |
| bibliotheque | categorie       | table | postgres |
| bibliotheque | edition         | table | postgres |
| bibliotheque | exemplaire      | table | postgres |
| bibliotheque | lecture         | table | postgres |
| bibliotheque | livre           | table | postgres |
| bibliotheque | livre_auteur    | table | postgres |
| bibliotheque | livre_categorie | table | postgres |
| bibliotheque | note            | table | postgres |
+--------------+-----------------+-------+----------+
```

Petite précision : le `CREATE DATABASE` n'est volontairement pas actif dans le fichier, car PostgreSQL ne permet pas d'exécuter `CREATE DATABASE` dans une transaction et il est plus propre de lancer cette étape séparément.

#### [Table des matières](#table-des-matières)

---

## 3.2. 02_insert_bibliotheque.sql

```sql
-- ============================================================
-- Fichier : 02_insert_bibliotheque.sql
-- Objet   : Jeu de données de démonstration
-- SGBD    : PostgreSQL
-- Base    : bibliotheque
-- ============================================================

BEGIN;

-- ============================================================
-- 1. AUTEURS
-- ============================================================

INSERT INTO bibliotheque.auteur
    (nom, prenom, date_naissance, date_deces)
VALUES
    ('Flaubert', 'Gustave', '1821-12-12', '1880-05-08'),
    ('Balzac', 'Honoré de', '1799-05-20', '1850-08-18'),
    ('Zola', 'Émile', '1840-04-02', '1902-09-29'),
    ('Stendhal', 'Henri', '1783-01-23', '1842-03-23'),
    ('Hugo', 'Victor', '1802-02-26', '1885-05-22'),
    ('Maupassant', 'Guy de', '1850-08-05', '1893-07-06'),
    ('Proust', 'Marcel', '1871-07-10', '1922-11-18'),
    ('Camus', 'Albert', '1913-11-07', '1960-01-04'),
    ('Sartre', 'Jean-Paul', '1905-06-21', '1980-04-15'),
    ('Nietzsche', 'Friedrich', '1844-10-15', '1900-08-25'),
    ('Bauman', 'Zygmunt', '1925-11-19', '2017-01-09'),
    ('Lasch', 'Christopher', '1932-06-01', '1994-02-14'),
    ('Debord', 'Guy', '1931-12-28', '1994-11-30'),
    ('Bourdieu', 'Pierre', '1930-08-01', '2002-01-23'),
    ('Polanyi', 'Karl', '1886-10-25', '1964-04-23'),
    ('Vernant', 'Jean-Pierre', '1914-01-04', '2007-01-09'),
    ('Gauchet', 'Marcel', '1946-04-23', NULL),
    ('Onfray', 'Michel', '1959-01-01', NULL),
    ('Todd', 'Emmanuel', '1951-05-16', NULL),
    ('Stiegler', 'Barbara', '1971-09-18', NULL);

-- ============================================================
-- 2. CATEGORIES
-- ============================================================

INSERT INTO bibliotheque.categorie (nom)
VALUES
    ('Roman'),
    ('Littérature française'),
    ('Philosophie'),
    ('Histoire'),
    ('Sociologie'),
    ('Politique'),
    ('Économie'),
    ('Anthropologie'),
    ('Psychologie'),
    ('Essai'),
    ('Classique'),
    ('Modernité');

-- ============================================================
-- 3. LIVRES
-- ============================================================

INSERT INTO bibliotheque.livre
    (titre, sous_titre, annee_parution, nb_pages, resume)
VALUES

-- 1
(
    'Madame Bovary',
    'Mœurs de province',
    1857,
    384,
    'Roman de Gustave Flaubert décrivant la vie et les désillusions d’Emma Bovary.'
),

-- 2
(
    'L''Éducation sentimentale',
    NULL,
    1869,
    576,
    'Roman retraçant les espoirs, les désillusions et la formation sentimentale de Frédéric Moreau.'
),

-- 3
(
    'Illusions perdues',
    NULL,
    1837,
    720,
    'Roman de Balzac consacré à l’ascension et aux désillusions de Lucien de Rubempré.'
),

-- 4
(
    'Le Père Goriot',
    NULL,
    1835,
    320,
    'Roman de La Comédie humaine consacré notamment aux rapports entre argent, ambition et famille.'
),

-- 5
(
    'Germinal',
    NULL,
    1885,
    512,
    'Roman décrivant la condition ouvrière et une grève dans une région minière du nord de la France.'
),

-- 6
(
    'L''Assommoir',
    NULL,
    1877,
    480,
    'Roman consacré à la vie ouvrière parisienne et aux ravages de l’alcoolisme.'
),

-- 7
(
    'Le Rouge et le Noir',
    'Chronique du XIXe siècle',
    1830,
    640,
    'Roman retraçant l’ascension sociale et la chute de Julien Sorel.'
),

-- 8
(
    'La Chartreuse de Parme',
    NULL,
    1839,
    512,
    'Roman mêlant politique, amour et aventure dans l’Italie napoléonienne.'
),

-- 9
(
    'Les Misérables',
    NULL,
    1862,
    1500,
    'Grande fresque sociale et historique de Victor Hugo.'
),

-- 10
(
    'Notre-Dame de Paris',
    '1482',
    1831,
    560,
    'Roman historique situé dans le Paris médiéval.'
),

-- 11
(
    'Bel-Ami',
    NULL,
    1885,
    384,
    'Roman décrivant l’ascension sociale de Georges Duroy dans le Paris journalistique.'
),

-- 12
(
    'À la recherche du temps perdu',
    'Du côté de chez Swann',
    1913,
    520,
    'Premier volume de la grande œuvre romanesque de Marcel Proust.'
),

-- 13
(
    'L''Étranger',
    NULL,
    1942,
    186,
    'Roman d’Albert Camus mettant en scène Meursault et sa confrontation avec l’absurde.'
),

-- 14
(
    'La Nausée',
    NULL,
    1938,
    250,
    'Roman philosophique de Jean-Paul Sartre consacré à l’expérience de l’existence et de la contingence.'
),

-- 15
(
    'Ainsi parlait Zarathoustra',
    'Un livre pour tous et pour personne',
    1883,
    350,
    'Œuvre philosophique majeure de Nietzsche développant notamment la volonté de puissance et le surhomme.'
),

-- 16
(
    'La Vie liquide',
    NULL,
    2005,
    180,
    'Analyse de Zygmunt Bauman consacrée à la fragilité et à la fluidité des relations sociales contemporaines.'
),

-- 17
(
    'La Culture du narcissisme',
    NULL,
    1979,
    320,
    'Analyse de Christopher Lasch sur les transformations culturelles et psychologiques des sociétés contemporaines.'
),

-- 18
(
    'La Société du spectacle',
    NULL,
    1967,
    160,
    'Critique de Guy Debord de la société organisée autour de la représentation et de la marchandise.'
),

-- 19
(
    'Les Héritiers',
    'Les étudiants et la culture',
    1964,
    189,
    'Étude de Pierre Bourdieu et Jean-Claude Passeron sur les inégalités culturelles et scolaires.'
),

-- 20
(
    'La Grande Transformation',
    NULL,
    1944,
    419,
    'Analyse historique de Karl Polanyi sur la formation de l’économie de marché moderne.'
);

-- ============================================================
-- 4. RELATION LIVRE / AUTEUR
-- ============================================================

INSERT INTO bibliotheque.livre_auteur
    (id_livre, id_auteur)
VALUES
    (1, 1),     -- Madame Bovary / Flaubert
    (2, 1),     -- L'Éducation sentimentale / Flaubert

    (3, 2),     -- Illusions perdues / Balzac
    (4, 2),     -- Le Père Goriot / Balzac

    (5, 3),     -- Germinal / Zola
    (6, 3),     -- L'Assommoir / Zola

    (7, 4),     -- Le Rouge et le Noir / Stendhal
    (8, 4),     -- La Chartreuse de Parme / Stendhal

    (9, 5),     -- Les Misérables / Hugo
    (10, 5),    -- Notre-Dame de Paris / Hugo

    (11, 6),    -- Bel-Ami / Maupassant

    (12, 7),    -- Du côté de chez Swann / Proust

    (13, 8),    -- L'Étranger / Camus

    (14, 9),    -- La Nausée / Sartre

    (15, 10),   -- Zarathoustra / Nietzsche

    (16, 11),   -- Vie liquide / Bauman

    (17, 12),   -- Culture du narcissisme / Lasch

    (18, 13),   -- Société du spectacle / Debord

    (19, 14),   -- Les Héritiers / Bourdieu

    (20, 15);   -- Grande Transformation / Polanyi

-- ============================================================
-- 5. RELATION LIVRE / CATEGORIE
-- ============================================================

INSERT INTO bibliotheque.livre_categorie
    (id_livre, id_categorie)
VALUES

    -- Madame Bovary
    (1, 1),     -- Roman
    (1, 2),     -- Littérature française
    (1, 11),    -- Classique

    -- Éducation sentimentale
    (2, 1),
    (2, 2),
    (2, 11),

    -- Illusions perdues
    (3, 1),
    (3, 2),
    (3, 11),

    -- Père Goriot
    (4, 1),
    (4, 2),
    (4, 11),

    -- Germinal
    (5, 1),
    (5, 2),
    (5, 5),

    -- Assommoir
    (6, 1),
    (6, 2),

    -- Rouge et Noir
    (7, 1),
    (7, 2),
    (7, 11),

    -- Chartreuse de Parme
    (8, 1),
    (8, 2),
    (8, 11),

    -- Misérables
    (9, 1),
    (9, 2),
    (9, 4),
    (9, 11),

    -- Notre-Dame
    (10, 1),
    (10, 2),
    (10, 4),
    (10, 11),

    -- Bel-Ami
    (11, 1),
    (11, 2),

    -- Proust
    (12, 1),
    (12, 2),

    -- Étranger
    (13, 1),
    (13, 2),
    (13, 3),

    -- Nausée
    (14, 1),
    (14, 3),

    -- Zarathoustra
    (15, 3),
    (15, 10),

    -- Vie liquide
    (16, 5),
    (16, 10),
    (16, 12),

    -- Culture du narcissisme
    (17, 5),
    (17, 9),
    (17, 10),

    -- Société du spectacle
    (18, 5),
    (18, 6),
    (18, 10),

    -- Héritiers
    (19, 5),
    (19, 10),

    -- Grande Transformation
    (20, 7),
    (20, 5),
    (20, 10);

-- ============================================================
-- 6. EDITIONS
-- ============================================================

INSERT INTO bibliotheque.edition
    (id_livre, editeur, annee_edition, isbn13, format)
VALUES

    (1,  'Gallimard',             2001, '9782070413119', 'Poche'),
    (2,  'Gallimard',             2005, '9782070307579', 'Poche'),

    (3,  'Le Livre de Poche',     2019, '9782253004133', 'Poche'),
    (4,  'Le Livre de Poche',     2018, '9782253003594', 'Poche'),

    (5,  'Gallimard',             2002, '9782070418428', 'Poche'),
    (6,  'Folio',                 2008, '9782070349241', 'Poche'),

    (7,  'Le Livre de Poche',     2019, '9782253008520', 'Poche'),
    (8,  'Folio',                 2003, '9782070410781', 'Poche'),

    (9,  'Pocket',                2019, '9782266298250', 'Poche'),
    (10, 'Le Livre de Poche',     2018, '9782253001170', 'Poche'),

    (11, 'Le Livre de Poche',     2015, '9782253001521', 'Poche'),

    (12, 'Gallimard',             1987, '9782070106461', 'Poche'),

    (13, 'Gallimard',             2017, '9782070360024', 'Poche'),

    (14, 'Gallimard',             2018, '9782070369302', 'Poche'),

    (15, 'Gallimard',             2019, '9782070360799', 'Poche'),

    (16, 'Fayard',                2006, '9782213624621', 'Broché'),

    (17, 'Climats',               2000, '9782080813765', 'Broché'),

    (18, 'Gallimard',             1992, '9782070320977', 'Poche'),

    (19, 'Minuit',                1964, '9782707301174', 'Broché'),

    (20, 'Gallimard',             1983, '9782070705873', 'Broché');

-- ============================================================
-- 7. EXEMPLAIRES
-- ============================================================

INSERT INTO bibliotheque.exemplaire
    (id_edition, etat, emplacement, date_achat, prix_achat)
VALUES

    (1,  'Bon',        'Bibliothèque - Étagère 1', '2024-02-10', 8.90),
    (2,  'Très bon',   'Bibliothèque - Étagère 1', '2024-03-15', 7.50),
    (3,  'Bon',        'Bibliothèque - Étagère 2', '2023-11-20', 9.90),
    (4,  'Très bon',   'Bibliothèque - Étagère 2', '2023-12-02', 7.90),
    (5,  'Bon',        'Bibliothèque - Étagère 3', '2024-01-15', 8.50),
    (6,  'Bon',        'Bibliothèque - Étagère 3', '2024-04-12', 7.20),
    (7,  'Très bon',   'Bibliothèque - Étagère 4', '2023-09-10', 8.90),
    (8,  'Bon',        'Bibliothèque - Étagère 4', '2023-10-18', 8.50),
    (9,  'Bon',        'Bibliothèque - Étagère 5', '2022-06-15', 10.90),
    (10, 'Très bon',   'Bibliothèque - Étagère 5', '2022-07-01', 9.50),
    (11, 'Bon',        'Bibliothèque - Étagère 6', '2024-05-20', 7.90),
    (12, 'Très bon',   'Bibliothèque - Étagère 6', '2024-06-10', 12.00),
    (13, 'Bon',        'Bibliothèque - Étagère 7', '2024-08-12', 6.90),
    (14, 'Très bon',   'Bibliothèque - Étagère 7', '2024-09-01', 7.90),
    (15, 'Excellent',  'Bibliothèque - Étagère 8', '2024-10-05', 9.90),
    (16, 'Bon',        'Bibliothèque - Étagère 9', '2025-01-10', 18.00),
    (17, 'Très bon',   'Bibliothèque - Étagère 9', '2025-02-15', 15.00),
    (18, 'Bon',        'Bibliothèque - Étagère 10', '2025-03-20', 8.00),
    (19, 'Bon',        'Bibliothèque - Étagère 10', '2025-04-10', 20.00),
    (20, 'Très bon',   'Bibliothèque - Étagère 11', '2025-05-05', 22.00);

-- ============================================================
-- 8. LECTURES
-- ============================================================

INSERT INTO bibliotheque.lecture
    (id_exemplaire, date_debut, date_fin, statut, note)
VALUES

    (1,  '2026-01-05', '2026-01-18', 'TERMINE', 9.0),

    (2,  '2026-02-01', '2026-02-20', 'TERMINE', 8.5),

    (3,  '2026-03-01', '2026-03-25', 'TERMINE', 9.0),

    (4,  '2026-04-01', '2026-04-15', 'TERMINE', 8.0),

    (5,  '2026-05-01', NULL, 'EN_COURS', NULL),

    (6,  NULL, NULL, 'A_LIRE', NULL),

    (7,  '2025-10-01', '2025-10-25', 'TERMINE', 9.5),

    (8,  NULL, NULL, 'A_LIRE', NULL),

    (9,  '2025-06-01', '2025-07-15', 'TERMINE', 10.0),

    (10, NULL, NULL, 'A_LIRE', NULL),

    (11, '2025-11-01', '2025-11-15', 'TERMINE', 8.0),

    (12, NULL, NULL, 'A_LIRE', NULL),

    (13, '2025-09-01', '2025-09-05', 'TERMINE', 9.0),

    (14, NULL, NULL, 'A_LIRE', NULL),

    (15, '2025-08-01', '2025-08-15', 'TERMINE', 9.0),

    (16, '2026-06-01', NULL, 'EN_COURS', NULL),

    (17, '2026-01-20', '2026-02-05', 'TERMINE', 8.5),

    (18, NULL, NULL, 'A_LIRE', NULL),

    (19, '2026-03-15', '2026-03-25', 'TERMINE', 8.0),

    (20, NULL, NULL, 'A_LIRE', NULL);

-- ============================================================
-- 9. NOTES PERSONNELLES
-- ============================================================

INSERT INTO bibliotheque.note
    (id_lecture, titre, contenu)
VALUES

    (
        1,
        'Le bovarysme',
        'Emma Bovary est prisonnière de représentations romanesques qui entrent constamment en conflit avec la réalité de son existence.'
    ),

    (
        1,
        'Le style de Flaubert',
        'Le travail stylistique de Flaubert cherche une forme d''impersonnalité et une grande précision dans la description.'
    ),

    (
        3,
        'La société et l''argent',
        'Balzac montre les mécanismes sociaux et économiques qui structurent les ambitions individuelles.'
    ),

    (
        7,
        'Julien Sorel',
        'Julien cherche à s''élever socialement dans une société fortement hiérarchisée.'
    ),

    (
        9,
        'La question sociale',
        'Hugo associe le destin individuel de ses personnages aux grandes transformations politiques et sociales du XIXe siècle.'
    ),

    (
        13,
        'L''absurde',
        'Meursault entretient un rapport détaché avec les conventions sociales et les événements de son existence.'
    ),

    (
        15,
        'Le surhomme',
        'Nietzsche critique les valeurs établies et cherche les conditions d''une nouvelle affirmation de la vie.'
    ),

    (
        16,
        'La modernité liquide',
        'Bauman décrit une société dans laquelle les structures, les relations et les identités deviennent plus mobiles et moins durables.'
    ),

    (
        17,
        'Le narcissisme contemporain',
        'Lasch analyse les transformations de la personnalité et de la culture dans les sociétés contemporaines.'
    ),

    (
        19,
        'Reproduction sociale',
        'Bourdieu montre comment les institutions scolaires peuvent contribuer à reproduire les différences sociales et culturelles.'
    );

-- ============================================================
-- 10. VERIFICATIONS
-- ============================================================

-- Nombre d'auteurs
SELECT
    COUNT(*) AS nombre_auteurs
FROM bibliotheque.auteur;

-- Nombre de livres
SELECT
    COUNT(*) AS nombre_livres
FROM bibliotheque.livre;

-- Nombre de catégories
SELECT
    COUNT(*) AS nombre_categories
FROM bibliotheque.categorie;

-- Nombre d'éditions
SELECT
    COUNT(*) AS nombre_editions
FROM bibliotheque.edition;

-- Nombre d'exemplaires
SELECT
    COUNT(*) AS nombre_exemplaires
FROM bibliotheque.exemplaire;

-- Nombre de lectures
SELECT
    COUNT(*) AS nombre_lectures
FROM bibliotheque.lecture;

-- Nombre de notes
SELECT
    COUNT(*) AS nombre_notes
FROM bibliotheque.note;

COMMIT;

-- ============================================================
-- FIN DU SCRIPT
-- ============================================================
```

#### [Table des matières](#table-des-matières)

---

## 3.3. 03_requetes_bibliotheque.sql

```sql
-- ============================================================
-- Fichier : 03_requetes_bibliotheque.sql
-- Objet   : Requêtes de consultation de la bibliothèque
-- SGBD    : PostgreSQL
-- Base    : bibliotheque
-- ============================================================

SET search_path TO bibliotheque, public;

-- ============================================================
-- 1. VERIFICATION GENERALE
-- ============================================================

-- Nombre d'auteurs
SELECT COUNT(*) AS nombre_auteurs
FROM bibliotheque.auteur;

-- Nombre de livres
SELECT COUNT(*) AS nombre_livres
FROM bibliotheque.livre;

-- Nombre de catégories
SELECT COUNT(*) AS nombre_categories
FROM bibliotheque.categorie;

-- Nombre d'éditions
SELECT COUNT(*) AS nombre_editions
FROM bibliotheque.edition;

-- Nombre d'exemplaires
SELECT COUNT(*) AS nombre_exemplaires
FROM bibliotheque.exemplaire;

-- Nombre de lectures
SELECT COUNT(*) AS nombre_lectures
FROM bibliotheque.lecture;

-- Nombre de notes
SELECT COUNT(*) AS nombre_notes
FROM bibliotheque.note;

-- ============================================================
-- 2. LISTE DES LIVRES
-- ============================================================

SELECT
    id_livre,
    titre,
    sous_titre,
    annee_parution,
    nb_pages
FROM bibliotheque.livre
ORDER BY titre;

-- ============================================================
-- 3. LIVRES AVEC LEUR AUTEUR
-- ============================================================

SELECT
    l.id_livre,
    l.titre,
    a.prenom || ' ' || a.nom AS auteur
FROM bibliotheque.livre l
JOIN bibliotheque.livre_auteur la
    ON la.id_livre = l.id_livre
JOIN bibliotheque.auteur a
    ON a.id_auteur = la.id_auteur
ORDER BY a.nom, a.prenom, l.titre;

-- ============================================================
-- 4. LIVRES AVEC AUTEUR ET CATEGORIE
-- ============================================================

SELECT
    l.titre,
    a.prenom || ' ' || a.nom AS auteur,
    c.nom AS categorie
FROM bibliotheque.livre l
JOIN bibliotheque.livre_auteur la
    ON la.id_livre = l.id_livre
JOIN bibliotheque.auteur a
    ON a.id_auteur = la.id_auteur
JOIN bibliotheque.livre_categorie lc
    ON lc.id_livre = l.id_livre
JOIN bibliotheque.categorie c
    ON c.id_categorie = lc.id_categorie
ORDER BY l.titre, c.nom;

-- ============================================================
-- 5. LIVRES PAR AUTEUR
-- ============================================================

SELECT
    a.prenom || ' ' || a.nom AS auteur,
    COUNT(la.id_livre) AS nombre_livres
FROM bibliotheque.auteur a
LEFT JOIN bibliotheque.livre_auteur la
    ON la.id_auteur = a.id_auteur
GROUP BY a.id_auteur, a.prenom, a.nom
ORDER BY nombre_livres DESC, auteur;

-- ============================================================
-- 6. LIVRES PAR CATEGORIE
-- ============================================================

SELECT
    c.nom AS categorie,
    COUNT(lc.id_livre) AS nombre_livres
FROM bibliotheque.categorie c
LEFT JOIN bibliotheque.livre_categorie lc
    ON lc.id_categorie = c.id_categorie
GROUP BY c.id_categorie, c.nom
ORDER BY nombre_livres DESC, c.nom;

-- ============================================================
-- 7. RECHERCHE PAR TITRE
-- ============================================================

-- Exemple : rechercher les livres contenant "vie"

SELECT
    id_livre,
    titre,
    sous_titre
FROM bibliotheque.livre
WHERE titre ILIKE '%vie%'
ORDER BY titre;

-- ============================================================
-- 8. RECHERCHE PAR AUTEUR
-- ============================================================

-- Exemple : rechercher les auteurs dont le nom contient "Flaub"

SELECT
    id_auteur,
    prenom,
    nom
FROM bibliotheque.auteur
WHERE nom ILIKE '%flaub%'
ORDER BY nom, prenom;

-- ============================================================
-- 9. LIVRES D'UN AUTEUR DONNE
-- ============================================================

-- Exemple : livres de Flaubert

SELECT
    l.titre,
    l.annee_parution
FROM bibliotheque.livre l
JOIN bibliotheque.livre_auteur la
    ON la.id_livre = l.id_livre
JOIN bibliotheque.auteur a
    ON a.id_auteur = la.id_auteur
WHERE a.nom = 'Flaubert'
ORDER BY l.annee_parution;

-- ============================================================
-- 10. LIVRES D'UNE CATEGORIE DONNEE
-- ============================================================

-- Exemple : catégorie Philosophie

SELECT
    l.titre,
    l.annee_parution
FROM bibliotheque.livre l
JOIN bibliotheque.livre_categorie lc
    ON lc.id_livre = l.id_livre
JOIN bibliotheque.categorie c
    ON c.id_categorie = lc.id_categorie
WHERE c.nom = 'Philosophie'
ORDER BY l.titre;

-- ============================================================
-- 11. LIVRES A LIRE
-- ============================================================

SELECT
    l.titre,
    a.prenom || ' ' || a.nom AS auteur,
    le.statut
FROM bibliotheque.lecture le
JOIN bibliotheque.exemplaire ex
    ON ex.id_exemplaire = le.id_exemplaire
JOIN bibliotheque.edition e
    ON e.id_edition = ex.id_edition
JOIN bibliotheque.livre l
    ON l.id_livre = e.id_livre
JOIN bibliotheque.livre_auteur la
    ON la.id_livre = l.id_livre
JOIN bibliotheque.auteur a
    ON a.id_auteur = la.id_auteur
WHERE le.statut = 'A_LIRE'
ORDER BY l.titre;

-- ============================================================
-- 12. LIVRES EN COURS DE LECTURE
-- ============================================================

SELECT
    l.titre,
    a.prenom || ' ' || a.nom AS auteur,
    le.date_debut
FROM bibliotheque.lecture le
JOIN bibliotheque.exemplaire ex
    ON ex.id_exemplaire = le.id_exemplaire
JOIN bibliotheque.edition e
    ON e.id_edition = ex.id_edition
JOIN bibliotheque.livre l
    ON l.id_livre = e.id_livre
JOIN bibliotheque.livre_auteur la
    ON la.id_livre = l.id_livre
JOIN bibliotheque.auteur a
    ON a.id_auteur = la.id_auteur
WHERE le.statut = 'EN_COURS'
ORDER BY le.date_debut;

-- ============================================================
-- 13. LIVRES TERMINES
-- ============================================================

SELECT
    l.titre,
    a.prenom || ' ' || a.nom AS auteur,
    le.date_debut,
    le.date_fin,
    le.note
FROM bibliotheque.lecture le
JOIN bibliotheque.exemplaire ex
    ON ex.id_exemplaire = le.id_exemplaire
JOIN bibliotheque.edition e
    ON e.id_edition = ex.id_edition
JOIN bibliotheque.livre l
    ON l.id_livre = e.id_livre
JOIN bibliotheque.livre_auteur la
    ON la.id_livre = l.id_livre
JOIN bibliotheque.auteur a
    ON a.id_auteur = la.id_auteur
WHERE le.statut = 'TERMINE'
ORDER BY le.date_fin DESC;

-- ============================================================
-- 14. CLASSEMENT DES LIVRES PAR NOTE
-- ============================================================

SELECT
    l.titre,
    a.prenom || ' ' || a.nom AS auteur,
    le.note
FROM bibliotheque.lecture le
JOIN bibliotheque.exemplaire ex
    ON ex.id_exemplaire = le.id_exemplaire
JOIN bibliotheque.edition e
    ON e.id_edition = ex.id_edition
JOIN bibliotheque.livre l
    ON l.id_livre = e.id_livre
JOIN bibliotheque.livre_auteur la
    ON la.id_livre = l.id_livre
JOIN bibliotheque.auteur a
    ON a.id_auteur = la.id_auteur
WHERE le.note IS NOT NULL
ORDER BY le.note DESC, l.titre;

-- ============================================================
-- 15. MOYENNE DES NOTES
-- ============================================================

SELECT
    ROUND(AVG(note), 2) AS note_moyenne
FROM bibliotheque.lecture
WHERE note IS NOT NULL;

-- ============================================================
-- 16. NOMBRE DE LIVRES PAR STATUT
-- ============================================================

SELECT
    statut,
    COUNT(*) AS nombre
FROM bibliotheque.lecture
GROUP BY statut
ORDER BY statut;

-- ============================================================
-- 17. NOMBRE DE LIVRES LUS PAR ANNEE
-- ============================================================

SELECT
    EXTRACT(YEAR FROM date_fin)::INTEGER AS annee,
    COUNT(*) AS nombre_livres
FROM bibliotheque.lecture
WHERE statut = 'TERMINE'
  AND date_fin IS NOT NULL
GROUP BY EXTRACT(YEAR FROM date_fin)
ORDER BY annee;

-- ============================================================
-- 18. NOMBRE DE PAGES LUES PAR ANNEE
-- ============================================================

SELECT
    EXTRACT(YEAR FROM le.date_fin)::INTEGER AS annee,
    SUM(l.nb_pages) AS nombre_pages
FROM bibliotheque.lecture le
JOIN bibliotheque.exemplaire ex
    ON ex.id_exemplaire = le.id_exemplaire
JOIN bibliotheque.edition e
    ON e.id_edition = ex.id_edition
JOIN bibliotheque.livre l
    ON l.id_livre = e.id_livre
WHERE le.statut = 'TERMINE'
  AND le.date_fin IS NOT NULL
GROUP BY EXTRACT(YEAR FROM le.date_fin)
ORDER BY annee;

-- ============================================================
-- 19. LIVRES LES PLUS LONGS
-- ============================================================

SELECT
    titre,
    nb_pages
FROM bibliotheque.livre
WHERE nb_pages IS NOT NULL
ORDER BY nb_pages DESC
LIMIT 10;

-- ============================================================
-- 20. LIVRES LES PLUS COURTS
-- ============================================================

SELECT
    titre,
    nb_pages
FROM bibliotheque.livre
WHERE nb_pages IS NOT NULL
ORDER BY nb_pages
LIMIT 10;

-- ============================================================
-- 21. EDITEUR ET NOMBRE D'EDITIONS
-- ============================================================

SELECT
    editeur,
    COUNT(*) AS nombre_editions
FROM bibliotheque.edition
WHERE editeur IS NOT NULL
GROUP BY editeur
ORDER BY nombre_editions DESC, editeur;

-- ============================================================
-- 22. VALEUR TOTALE DE LA BIBLIOTHEQUE
-- ============================================================

SELECT
    ROUND(SUM(prix_achat), 2) AS valeur_totale
FROM bibliotheque.exemplaire
WHERE prix_achat IS NOT NULL;

-- ============================================================
-- 23. LIVRES PAR EMPLACEMENT
-- ============================================================

SELECT
    emplacement,
    COUNT(*) AS nombre_exemplaires
FROM bibliotheque.exemplaire
GROUP BY emplacement
ORDER BY emplacement;

-- ============================================================
-- 24. DETAIL DES EXEMPLAIRES
-- ============================================================

SELECT
    l.titre,
    e.editeur,
    e.annee_edition,
    e.isbn13,
    ex.etat,
    ex.emplacement,
    ex.date_achat,
    ex.prix_achat
FROM bibliotheque.exemplaire ex
JOIN bibliotheque.edition e
    ON e.id_edition = ex.id_edition
JOIN bibliotheque.livre l
    ON l.id_livre = e.id_livre
ORDER BY l.titre;

-- ============================================================
-- 25. LIVRES SANS LECTURE ENREGISTREE
-- ============================================================

SELECT
    l.id_livre,
    l.titre
FROM bibliotheque.livre l
WHERE NOT EXISTS (
    SELECT 1
    FROM bibliotheque.edition e
    JOIN bibliotheque.exemplaire ex
        ON ex.id_edition = e.id_edition
    JOIN bibliotheque.lecture le
        ON le.id_exemplaire = ex.id_exemplaire
    WHERE e.id_livre = l.id_livre
)
ORDER BY l.titre;

-- ============================================================
-- 26. LIVRES SANS NOTE
-- ============================================================

SELECT DISTINCT
    l.titre,
    a.prenom || ' ' || a.nom AS auteur
FROM bibliotheque.livre l
JOIN bibliotheque.livre_auteur la
    ON la.id_livre = l.id_livre
JOIN bibliotheque.auteur a
    ON a.id_auteur = la.id_auteur
LEFT JOIN bibliotheque.edition e
    ON e.id_livre = l.id_livre
LEFT JOIN bibliotheque.exemplaire ex
    ON ex.id_edition = e.id_edition
LEFT JOIN bibliotheque.lecture le
    ON le.id_exemplaire = ex.id_exemplaire
WHERE le.note IS NULL
ORDER BY l.titre;

-- ============================================================
-- 27. NOTES PERSONNELLES
-- ============================================================

SELECT
    l.titre,
    n.titre AS titre_note,
    n.contenu
FROM bibliotheque.note n
JOIN bibliotheque.lecture le
    ON le.id_lecture = n.id_lecture
JOIN bibliotheque.exemplaire ex
    ON ex.id_exemplaire = le.id_exemplaire
JOIN bibliotheque.edition e
    ON e.id_edition = ex.id_edition
JOIN bibliotheque.livre l
    ON l.id_livre = e.id_livre
ORDER BY l.titre, n.titre;

-- ============================================================
-- 28. RECHERCHE DANS LES NOTES
-- ============================================================

-- Exemple : rechercher "société"

SELECT
    l.titre,
    n.titre AS note,
    n.contenu
FROM bibliotheque.note n
JOIN bibliotheque.lecture le
    ON le.id_lecture = n.id_lecture
JOIN bibliotheque.exemplaire ex
    ON ex.id_exemplaire = le.id_exemplaire
JOIN bibliotheque.edition e
    ON e.id_edition = ex.id_edition
JOIN bibliotheque.livre l
    ON l.id_livre = e.id_livre
WHERE n.contenu ILIKE '%société%'
ORDER BY l.titre;

-- ============================================================
-- 29. TABLEAU GENERAL DE LA BIBLIOTHEQUE
-- ============================================================

SELECT
    l.titre,
    STRING_AGG(
        DISTINCT a.prenom || ' ' || a.nom,
        ', '
        ORDER BY a.prenom || ' ' || a.nom
    ) AS auteurs,
    STRING_AGG(
        DISTINCT c.nom,
        ', '
        ORDER BY c.nom
    ) AS categories,
    COUNT(DISTINCT ex.id_exemplaire) AS exemplaires,
    MAX(le.statut) AS statut
FROM bibliotheque.livre l

LEFT JOIN bibliotheque.livre_auteur la
    ON la.id_livre = l.id_livre

LEFT JOIN bibliotheque.auteur a
    ON a.id_auteur = la.id_auteur

LEFT JOIN bibliotheque.livre_categorie lc
    ON lc.id_livre = l.id_livre

LEFT JOIN bibliotheque.categorie c
    ON c.id_categorie = lc.id_categorie

LEFT JOIN bibliotheque.edition e
    ON e.id_livre = l.id_livre

LEFT JOIN bibliotheque.exemplaire ex
    ON ex.id_edition = e.id_edition

LEFT JOIN bibliotheque.lecture le
    ON le.id_exemplaire = ex.id_exemplaire

GROUP BY l.id_livre, l.titre
ORDER BY l.titre;

-- ============================================================
-- 30. STATISTIQUES GENERALES
-- ============================================================

SELECT
    (SELECT COUNT(*)
     FROM bibliotheque.livre) AS livres,

    (SELECT COUNT(*)
     FROM bibliotheque.auteur) AS auteurs,

    (SELECT COUNT(*)
     FROM bibliotheque.categorie) AS categories,

    (SELECT COUNT(*)
     FROM bibliotheque.edition) AS editions,

    (SELECT COUNT(*)
     FROM bibliotheque.exemplaire) AS exemplaires,

    (SELECT COUNT(*)
     FROM bibliotheque.lecture
     WHERE statut = 'TERMINE') AS livres_lus,

    (SELECT COUNT(*)
     FROM bibliotheque.lecture
     WHERE statut = 'EN_COURS') AS lectures_en_cours,

    (SELECT COUNT(*)
     FROM bibliotheque.lecture
     WHERE statut = 'A_LIRE') AS livres_a_lire,

    (SELECT ROUND(AVG(note), 2)
     FROM bibliotheque.lecture
     WHERE note IS NOT NULL) AS note_moyenne,

    (SELECT ROUND(SUM(prix_achat), 2)
     FROM bibliotheque.exemplaire
     WHERE prix_achat IS NOT NULL) AS valeur_bibliotheque;

-- ============================================================
-- 31. TITRE, AUTEURS, CATEGORIES, EDITEURS, N_PAGES
-- ============================================================

SELECT
    l.titre,
    STRING_AGG(
        DISTINCT a.prenom || ' ' || a.nom,
        ', '
        ORDER BY a.prenom || ' ' || a.nom
    ) AS auteurs,
    STRING_AGG(
        DISTINCT c.nom,
        ', '
        ORDER BY c.nom
    ) AS categories,
    STRING_AGG(
        DISTINCT e.editeur,
        ', '
        ORDER BY e.editeur
    ) AS editeurs,
    MAX(l.nb_pages) AS nb_pages

FROM bibliotheque.livre l

LEFT JOIN bibliotheque.livre_auteur la
    ON la.id_livre = l.id_livre

LEFT JOIN bibliotheque.auteur a
    ON a.id_auteur = la.id_auteur

LEFT JOIN bibliotheque.livre_categorie lc
    ON lc.id_livre = l.id_livre

LEFT JOIN bibliotheque.categorie c
    ON c.id_categorie = lc.id_categorie

LEFT JOIN bibliotheque.edition e
    ON e.id_livre = l.id_livre

GROUP BY
    l.id_livre,
    l.titre

ORDER BY
    l.titre;

-- ====================================================================================================================
-- 31. TITRE, AUTEURS, CATEGORIES, EDITEUR, ANEE_EDITION, ISN13, FORMAT, ID_EXEMPLAIRE, ETAT, EMPLACEMENT, NB_PAGES
-- ====================================================================================================================

SELECT
    l.titre,
    STRING_AGG(
        DISTINCT a.prenom || ' ' || a.nom,
        ', '
        ORDER BY a.prenom || ' ' || a.nom
    ) AS auteurs,

    STRING_AGG(
        DISTINCT c.nom,
        ', '
        ORDER BY c.nom
    ) AS categories,

    e.editeur,
    e.annee_edition,
    e.isbn13,
    e.format,
    ex.id_exemplaire,
    ex.etat,
    ex.emplacement,
    l.nb_pages

FROM bibliotheque.livre l

LEFT JOIN bibliotheque.livre_auteur la
    ON la.id_livre = l.id_livre

LEFT JOIN bibliotheque.auteur a
    ON a.id_auteur = la.id_auteur

LEFT JOIN bibliotheque.livre_categorie lc
    ON lc.id_livre = l.id_livre

LEFT JOIN bibliotheque.categorie c
    ON c.id_categorie = lc.id_categorie

LEFT JOIN bibliotheque.edition e
    ON e.id_livre = l.id_livre

LEFT JOIN bibliotheque.exemplaire ex
    ON ex.id_edition = e.id_edition

WHERE l.titre = 'Madame Bovary'

GROUP BY
    l.id_livre,
    l.titre,
    l.nb_pages,
    e.id_edition,
    e.editeur,
    e.annee_edition,
    e.isbn13,
    e.format,
    ex.id_exemplaire,
    ex.etat,
    ex.emplacement

ORDER BY
    e.annee_edition,
    ex.id_exemplaire;

-- ============================================================
-- FIN DU SCRIPT
-- ============================================================
```

#### [Table des matières](#table-des-matières)

# 4. Se connecter sous Linux

```text
psql -h localhost -U postgres -p 5436 -d bibliotheque
```

#### [Table des matières](#table-des-matières)
