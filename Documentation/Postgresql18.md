# 📀 Projet PosgreSQL DVD Rental 📀

### Table des matières
- [1. Connexion avec psql](#1-connexion-avec-psql)
- [2. Modèle Entités-Relations DVD Rental](#2-modèle-entités-relations-dvd-rental)
- [3. Téléchargement des données de la base de données DVDRENTAL](#3-téléchargement-des-données-de-la-base-de-données-dvdrental)
- [4. Modèle ER DVD Rental](#4-modèle-er-dvd-rental)
- [5. Créer l'utilisateur fdurand et accès à la base DVDRENTAL](#5-créer-lutilisateur-fdurand-et-accès-à-la-base-dvdrental)
- [6. Query01](#6-query01)
- [7. Query02](#7-query02)
- [8. Query03](#8-query03)
- [9. Query04](#9-query04)  
- [10. Query05](#10-query05)
- [11. Query06](#11-query06)
- [12. Query07](#12-query07)
- [13. Query08](#13-query08)
- [14. Query09](#14-query09)
- [15. Query10](#15-query10)

---

### 1. Connexion avec psql

<div style="background-color:#f5f5f5; padding:15px; border-radius:8px;">

```bash
PGPASSWORD=Tamerlan2026 psql -h 127.0.0.1 -U postgres -p 5433
```

---

```bash
podman run --name postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=admin \
  -p 5436:5432 \
  -v /home/durandf/postgres_data:/var/lib/postgresql:z \
  -d docker.io/library/postgres:latest

sudo chown -R durandf:durandf /home/durandf/postgres_data
sudo chmod -R 755 /home/durandf/postgres_data

cd /home/durandf/postgres_data/18/docker

apt update && apt upgrade -y && apt install vim -y

👉 postgresql.conf :
vi +/listen_addresses /var/lib/postgresql/18/docker/postgresql.conf

listen_addresses = '*'
port = 5432

👉 pg_hba.conf
vi +'/IPv4 local connections:' /var/lib/postgresql/18/docker/pg_hba.conf
                
host    all     all     0.0.0.0/0     md5


Sous wsl2:
psql -h 127.0.0.1 -U postgres -p 5436
```

</div>

### [↑ Table des matières](#table-des-matières)

---

### 2. Modèle Entités-Relations DVD Rental

<p align="center">
  <img src="https://github.com/gordonkwokkwok/DVD-Rental-PostgreSQL-Project/assets/112631794/5c55cbde-9e67-4363-99bc-177bf7903882" alt="Image" width="700">
</p

### [↑ Table des matières](#table-des-matières)

---

### 3. Téléchargement des données de la base de données DVDRENTAL

 [Lien](https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/) ; ou
- [Télécharger ici](https://github.com/gordonkwokkwok/DVD-Rental-PostgreSQL-Project/tree/main/dataset)

### [↑ Table des matières](#table-des-matières)

---

### 4. Modèle ER DVD Rental

<p align="center">
  <img src="https://github.com/gordonkwokkwok/DVD-Rental-PostgreSQL-Project/assets/112631794/5c55cbde-9e67-4363-99bc-177bf7903882" alt="Image" width="700">
</p>

### [↑ Table des matières](#table-des-matières)

---

### 5. Créer l'utilisateur fdurand et accès à la base DVDRENTAL

<div style="background-color:#f5f5f5; padding:15px; border-radius:8px;">

```bash
psql -U fdurand -h 127.0.0.1 -d postgres -p 5436
psql -h 127.0.0.1 -U postgres -p 5436 -d dvdrental
```

---

```sql
GRANT CONNECT ON DATABASE dvdrental TO fdurand;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO fdurand;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO fdurand;
```

---

### 6. Query01

```sql
SELECT first_name, last_name FROM actor WHERE first_name = 'Johnny';

+------------+--------------+
| first_name |  last_name   |
+------------+--------------+
| Johnny     | Lollobrigida |
| Johnny     | Cage         |
+------------+--------------+
```

### [↑ Table des matières](#table-des-matières)

---

### 7. Query02

```sql
SELECT film.title, COUNT(actor.actor_id) as actor_count
FROM film
INNER JOIN film_actor ON film.film_id = film_actor.film_id
INNER JOIN actor ON actor.actor_id = film_actor.actor_id
GROUP BY film.title LIMIT 10;

+------------------+-------------+
|      title       | actor_count |
+------------------+-------------+
| Academy Dinosaur |          10 |
| Ace Goldfinger   |           4 |
| Adaptation Holes |           5 |
| Affair Prejudice |           5 |
| African Egg      |           5 |
| Agent Truman     |           7 |
| Airplane Sierra  |           5 |
| Airport Pollock  |           4 |
| Alabama Devil    |           9 |
| Aladdin Calendar |           8 |
+------------------+-------------+
```

### [↑ Table des matières](#table-des-matières)

---

### 8. Query03

```sql
SELECT c.customer_id, c.first_name, c.last_name, p.amount 
FROM customer as c
LEFT JOIN payment as p 
ON c.customer_id = p.customer_id
ORDER BY p.amount DESC
LIMIT 10;

+-------------+------------+-----------+--------+
| customer_id | first_name | last_name | amount |
+-------------+------------+-----------+--------+
|         591 | Kent       | Arsenault |  11.99 |
|         195 | Vanessa    | Sims      |  11.99 |
|         116 | Victoria   | Gibson    |  11.99 |
|         237 | Tanya      | Gilbert   |  11.99 |
|         592 | Terrance   | Roush     |  11.99 |
|          13 | Karen      | Jackson   |  11.99 |
|         362 | Nicholas   | Barfield  |  11.99 |
|         204 | Rosemary   | Schmidt   |  11.99 |
|         571 | Johnnie    | Chisholm  |  10.99 |
|         558 | Jimmie     | Eggleston |  10.99 |
+-------------+------------+-----------+--------+
```

### [↑ Table des matières](#table-des-matières)

---

### 9. Query04

```sql
SELECT customer_id , count(*) AS Rental_Count
FROM rental
WHERE rental_date BETWEEN '2005-07-01' AND '2005-08-31' 
GROUP BY customer_id 
ORDER BY Rental_Count DESC LIMIT 10;

+-------------+--------------+
| customer_id | rental_count |
+-------------+--------------+
|         148 |           40 |
|         144 |           34 |
|         137 |           34 |
|         469 |           33 |
|         526 |           33 |
|         366 |           33 |
|         257 |           32 |
|         410 |           31 |
|         373 |           31 |
|          75 |           31 |
+-------------+--------------+
```

### [↑ Table des matières](#table-des-matières)

---

### 10. Query05

```sql
SELECT DISTINCT customer_id 
FROM rental 
WHERE customer_id IN (SELECT customer_id FROM payment WHERE amount > 10) LIMIT 10;

+-------------+
| customer_id |
+-------------+
|          87 |
|         477 |
|         550 |
|         272 |
|         292 |
|         529 |
|         187 |
|         331 |
|         307 |
|          54 |
+-------------+
```

### [↑ Table des matières](#table-des-matières)

---

#### 11. Query06

```sql
SELECT rating, 
       AVG(length) AS avg_length, 
       CASE 
         WHEN AVG(length) > 120 THEN 'Long'
         ELSE 'Short'
       END AS film_length_category
FROM film 
GROUP BY rating;

+--------+----------------------+----------------------+
| rating |      avg_length      | film_length_category |
+--------+----------------------+----------------------+
| G      | 111.0505617977528090 | Short                |
| NC-17  | 113.2285714285714286 | Short                |
| PG     | 112.0051546391752577 | Short                |
| PG-13  | 120.4439461883408072 | Long                 |
| R      | 118.6615384615384615 | Short                |
+--------+----------------------+----------------------+
```

### [↑ Table des matières](#table-des-matières)

---

#### 12. Query07

```sql
SELECT rental_id, customer_id, rental_date, 
       RANK() OVER (PARTITION BY customer_id ORDER BY rental_date) as rental_rank
FROM rental LIMIT 10;

+-----------+-------------+---------------------+-------------+
| rental_id | customer_id |     rental_date     | rental_rank |
+-----------+-------------+---------------------+-------------+
|        76 |           1 | 2005-05-25 11:30:37 |           1 |
|       573 |           1 | 2005-05-28 10:35:23 |           2 |
|      1185 |           1 | 2005-06-15 00:54:12 |           3 |
|      1422 |           1 | 2005-06-15 18:02:53 |           4 |
|      1476 |           1 | 2005-06-15 21:08:46 |           5 |
|      1725 |           1 | 2005-06-16 15:18:57 |           6 |
|      2308 |           1 | 2005-06-18 08:41:48 |           7 |
|      2363 |           1 | 2005-06-18 13:33:59 |           8 |
|      3284 |           1 | 2005-06-21 06:24:45 |           9 |
|      4526 |           1 | 2005-07-08 03:17:05 |          10 |
+-----------+-------------+---------------------+-------------+
```

### [↑ Table des matières](#table-des-matières)

---

#### 13. Query08

```sql
SELECT MIN(length) as min_length, MAX(length) as max_length 
FROM film 
WHERE title LIKE 'A%';

+------------+------------+
| min_length | max_length |
+------------+------------+
|         46 |        181 |
+------------+------------+
```

### [↑ Table des matières](#table-des-matières)

---

#### 14. Query09

```sql
SELECT customer.customer_id, customer.first_name, customer.last_name, rental.rental_id 
FROM customer 
RIGHT JOIN rental ON customer.customer_id = rental.customer_id 
ORDER BY rental.rental_date DESC LIMIT 10;

+-------------+------------+-----------+-----------+
| customer_id | first_name | last_name | rental_id |
+-------------+------------+-----------+-----------+
|         373 | Louis      | Leone     |     11739 |
|         532 | Neil       | Renner    |     14616 |
|         216 | Natalie    | Meyer     |     11676 |
|         374 | Jeremy     | Hurtado   |     15966 |
|         274 | Naomi      | Jennings  |     13486 |
|         168 | Regina     | Berry     |     15894 |
|         472 | Greg       | Robins    |     14928 |
|         282 | Jenny      | Castro    |     15430 |
|         287 | Becky      | Miles     |     14204 |
|         352 | Albert     | Crouse    |     13578 |
+-------------+------------+-----------+-----------+
```

### [↑ Table des matières](#table-des-matières)

---

#### 15. Query10

```sql
SELECT film.title, category.name 
FROM film 
CROSS JOIN category 
LIMIT 20;

+------------------+-------------+
|      title       |    name     |
+------------------+-------------+
| Chamber Italian  | Action      |
| Chamber Italian  | Animation   |
| Chamber Italian  | Children    |
| Chamber Italian  | Classics    |
| Chamber Italian  | Comedy      |
| Chamber Italian  | Documentary |
| Chamber Italian  | Drama       |
| Chamber Italian  | Family      |
| Chamber Italian  | Foreign     |
| Chamber Italian  | Games       |
| Chamber Italian  | Horror      |
| Chamber Italian  | Music       |
| Chamber Italian  | New         |
| Chamber Italian  | Sci-Fi      |
| Chamber Italian  | Sports      |
| Chamber Italian  | Travel      |
| Grosse Wonderful | Action      |
| Grosse Wonderful | Animation   |
| Grosse Wonderful | Children    |
| Grosse Wonderful | Classics    |
+------------------+-------------+
```

### [↑ Table des matières](#table-des-matières)