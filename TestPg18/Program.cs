using System;
using Npgsql;

class Program
{
    static void Main()
    {
        // Chaîne de connexion au container pg18_a
        var connectionString = "Host=localhost;Port=5433;Username=postgres;Password=admin;Database=postgres";

        try
        {
            using var conn = new NpgsqlConnection(connectionString);
            conn.Open();
            Console.WriteLine("✔ Connexion réussie à PostgreSQL (pg18_a) !");

            // Petit test : exécuter SELECT version()
            using var cmd = new NpgsqlCommand("SELECT version();", conn);
            var version = cmd.ExecuteScalar();
            Console.WriteLine($"Version PostgreSQL : {version}");
        }
        catch (Exception ex)
        {
            Console.WriteLine("❌ Erreur lors de la connexion :");
            Console.WriteLine(ex.Message);
        }
    }
}

