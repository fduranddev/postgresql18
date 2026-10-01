using Npgsql;
using Microsoft.Extensions.Configuration;
using System;
using System.IO;

public static class Database
{
    private static readonly string _connectionString;

    static Database()
    {
        var config = new ConfigurationBuilder()
            .SetBasePath(Directory.GetCurrentDirectory())  // <-- utiliser Directory.GetCurrentDirectory()
            .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
            .Build();

        _connectionString = config.GetConnectionString("DefaultConnection");
    }

    public static NpgsqlConnection GetConnection()
    {
        var conn = new NpgsqlConnection(_connectionString);
        conn.Open();
        return conn;
    }
}

