using Npgsql;

// Get the connection string
string connectionString = ConfigurationHelper.GetConnectionString("DefaultConnection");


// Connect to the PostgreSQL server
await using var conn = new NpgsqlConnection(connectionString);
await conn.OpenAsync();

Console.WriteLine($"The PostgreSQL version: {conn.PostgreSqlVersion}");
