# ============================================================
# LISTE DES LIVRES
# ============================================================

LIST_BOOKS = """
SELECT
    l.id_livre,
    l.titre,

    COALESCE(
        STRING_AGG(
            DISTINCT a.prenom || ' ' || a.nom,
            ', '
            ORDER BY a.prenom || ' ' || a.nom
        ),
        ''
    ) AS auteurs,

    COALESCE(
        STRING_AGG(
            DISTINCT c.nom,
            ', '
            ORDER BY c.nom
        ),
        ''
    ) AS categories,

    COALESCE(
        STRING_AGG(
            DISTINCT e.editeur,
            ', '
            ORDER BY e.editeur
        ),
        ''
    ) AS editeurs,

    l.annee_parution,
    l.nb_pages,

    COUNT(DISTINCT ex.id_exemplaire) AS exemplaires,

    COALESCE(
        STRING_AGG(
            DISTINCT ex.emplacement,
            ', '
            ORDER BY ex.emplacement
        )
        FILTER (
            WHERE ex.emplacement IS NOT NULL
            AND ex.emplacement <> ''
        ),
        ''
    ) AS emplacements

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

GROUP BY
    l.id_livre,
    l.titre,
    l.annee_parution,
    l.nb_pages

ORDER BY
    l.titre;
"""


# ============================================================
# RECHERCHE
# ============================================================

SEARCH_BOOKS = """
SELECT
    l.id_livre,
    l.titre,

    COALESCE(
        STRING_AGG(
            DISTINCT a.prenom || ' ' || a.nom,
            ', '
            ORDER BY a.prenom || ' ' || a.nom
        ),
        ''
    ) AS auteurs,

    COALESCE(
        STRING_AGG(
            DISTINCT c.nom,
            ', '
            ORDER BY c.nom
        ),
        ''
    ) AS categories,

    COALESCE(
        STRING_AGG(
            DISTINCT e.editeur,
            ', '
            ORDER BY e.editeur
        ),
        ''
    ) AS editeurs,

    l.annee_parution,
    l.nb_pages,

    COUNT(DISTINCT ex.id_exemplaire) AS exemplaires,

    COALESCE(
        STRING_AGG(
            DISTINCT ex.emplacement,
            ', '
            ORDER BY ex.emplacement
        )
        FILTER (
            WHERE ex.emplacement IS NOT NULL
            AND ex.emplacement <> ''
        ),
        ''
    ) AS emplacements

FROM bibliotheque.livre l

LEFT JOIN bibliotheque.livre_auteur la
    ON la.id_livre = l.id_livre

LEFT JOIN bibliotheque.auteur a
    ON a.id_auteur = la.id_auteur

LEFT JOIN bibliotheque.livre_categorie lc
    ON lc.id_livre = lc.id_livre

LEFT JOIN bibliotheque.categorie c
    ON c.id_categorie = lc.id_categorie

LEFT JOIN bibliotheque.edition e
    ON e.id_livre = l.id_livre

LEFT JOIN bibliotheque.exemplaire ex
    ON ex.id_edition = e.id_edition

WHERE
       l.titre ILIKE %(search)s
    OR a.nom ILIKE %(search)s
    OR a.prenom ILIKE %(search)s
    OR c.nom ILIKE %(search)s

GROUP BY
    l.id_livre,
    l.titre,
    l.annee_parution,
    l.nb_pages

ORDER BY
    l.titre;
"""


# ============================================================
# FICHE DETAILLEE DU LIVRE
# ============================================================

BOOK_DETAIL = """
SELECT
    l.id_livre,
    l.titre,
    l.sous_titre,
    l.annee_parution,
    l.resume,
    l.nb_pages,

    COALESCE(
        STRING_AGG(
            DISTINCT a.prenom || ' ' || a.nom,
            ', '
            ORDER BY a.prenom || ' ' || a.nom
        ),
        ''
    ) AS auteurs,

    COALESCE(
        STRING_AGG(
            DISTINCT c.nom,
            ', '
            ORDER BY c.nom
        ),
        ''
    ) AS categories

FROM bibliotheque.livre l

LEFT JOIN bibliotheque.livre_auteur la
    ON la.id_livre = l.id_livre

LEFT JOIN bibliotheque.auteur a
    ON a.id_auteur = la.id_auteur

LEFT JOIN bibliotheque.livre_categorie lc
    ON lc.id_livre = l.id_livre

LEFT JOIN bibliotheque.categorie c
    ON c.id_categorie = lc.id_categorie

WHERE
    l.id_livre = %(id_livre)s

GROUP BY
    l.id_livre,
    l.titre,
    l.sous_titre,
    l.annee_parution,
    l.resume,
    l.nb_pages;
"""


# ============================================================
# EDITIONS
# ============================================================

EDITIONS = """
SELECT
    id_edition,
    editeur,
    annee_edition,
    isbn13,
    format

FROM bibliotheque.edition

WHERE
    id_livre = %(id_livre)s

ORDER BY
    annee_edition NULLS LAST,
    editeur;
"""


# ============================================================
# EXEMPLAIRES
# ============================================================

COPIES = """
SELECT
    ex.id_exemplaire,
    e.editeur,
    e.isbn13,
    ex.etat,
    ex.emplacement,
    ex.date_achat,
    ex.prix_achat

FROM bibliotheque.exemplaire ex

JOIN bibliotheque.edition e
    ON e.id_edition = ex.id_edition

WHERE
    e.id_livre = %(id_livre)s

ORDER BY
    ex.id_exemplaire;
"""


# ============================================================
# LECTURES
# ============================================================

READINGS = """
SELECT
    le.id_lecture,
    ex.id_exemplaire,
    le.date_debut,
    le.date_fin,
    le.statut,
    le.note

FROM bibliotheque.lecture le

JOIN bibliotheque.exemplaire ex
    ON ex.id_exemplaire = le.id_exemplaire

JOIN bibliotheque.edition e
    ON e.id_edition = ex.id_edition

WHERE
    e.id_livre = %(id_livre)s

ORDER BY
    le.date_debut DESC NULLS LAST;
"""


# ============================================================
# NOTES
# ============================================================

NOTES = """
SELECT
    n.id_note,
    n.id_lecture,
    n.titre,
    n.contenu

FROM bibliotheque.note n

JOIN bibliotheque.lecture le
    ON le.id_lecture = n.id_lecture

JOIN bibliotheque.exemplaire ex
    ON ex.id_exemplaire = le.id_exemplaire

JOIN bibliotheque.edition e
    ON e.id_edition = ex.id_edition

WHERE
    e.id_livre = %(id_livre)s

ORDER BY
    n.id_note;
"""


# ============================================================
# DOCUMENTS / PDF
# ============================================================

DOCUMENTS = """
SELECT
    id_document,
    nom_fichier,
    chemin_fichier,
    type_document

FROM bibliotheque.document

WHERE
    id_livre = %(id_livre)s

ORDER BY
    nom_fichier;
"""
