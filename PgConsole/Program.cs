using System;
using System.Data;
using Npgsql;

class PgConsole
{
    static void Main()
    {
        string connectionString =
            "Host=localhost;Port=5433;Username=postgres;Password=admin;Database=postgres";

        Console.WriteLine("=== Console interactive PostgreSQL ===");
        Console.WriteLine("Connecté à pg18_a (PostgreSQL)");
        Console.WriteLine("Tapez \\q pour quitter.");

        try
        {
            using var conn = new NpgsqlConnection(connectionString);
            conn.Open();
            Console.WriteLine("Connexion réussie !");

            while (true)
            {
                Console.Write("\npg18_a=# ");
                string input = Console.ReadLine();

                if (string.IsNullOrWhiteSpace(input))
                    continue;

                // Commande quitter
                if (input.Trim() == "\\q")
                {
                    Console.WriteLine("Déconnexion...");
                    break;
                }

                // Commandes internes
                if (input.Trim() == "\\dt")
                {
                    input = "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog', 'information_schema');";
                }
                else if (input.Trim() == "\\db")
                {
                    input = "SELECT datname FROM pg_database WHERE datistemplate = false;";
                }

                try
                {
                    using var cmd = new NpgsqlCommand(input, conn);

                    // Exécution
                    using var reader = cmd.ExecuteReader();

                    // S'il n'y a pas de résultat
                    if (!reader.HasRows)
                    {
                        Console.WriteLine("(aucune ligne)");
                        continue;
                    }

                    // Lecture du schéma
                    DataTable schema = reader.GetSchemaTable();
                    int colCount = schema.Rows.Count;

                    // Affichage des en-têtes
                    foreach (DataRow row in schema.Rows)
                        Console.Write($"{row["ColumnName"],-20}");
                    Console.WriteLine();

                    // Affichage des résultats
                    while (reader.Read())
                    {
                        for (int i = 0; i < colCount; i++)
                            Console.Write($"{reader.GetValue(i),-20}");
                        Console.WriteLine();
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Erreur SQL : " + ex.Message);
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine("Erreur de connexion : " + ex.Message);
        }
    }
}

