using Npgsql;
using System;
using System.Collections.Generic;

public class EmployeeRepository
{
    public void CreateTable()
    {
        using var conn = Database.GetConnection();
        string sql = @"
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name TEXT,
                age INT
            );";
        using var cmd = new NpgsqlCommand(sql, conn);
        cmd.ExecuteNonQuery();
    }

    public void Insert(string name, int age)
    {
        using var conn = Database.GetConnection();
        using var cmd = new NpgsqlCommand("INSERT INTO employees (name, age) VALUES (@name, @age)", conn);
        cmd.Parameters.AddWithValue("name", name);
        cmd.Parameters.AddWithValue("age", age);
        cmd.ExecuteNonQuery();
    }

    public void Update(int id, string name, int age)
    {
        using var conn = Database.GetConnection();
        using var cmd = new NpgsqlCommand("UPDATE employees SET name=@name, age=@age WHERE id=@id", conn);
        cmd.Parameters.AddWithValue("id", id);
        cmd.Parameters.AddWithValue("name", name);
        cmd.Parameters.AddWithValue("age", age);
        cmd.ExecuteNonQuery();
    }

    public void Delete(int id)
    {
        using var conn = Database.GetConnection();
        using var cmd = new NpgsqlCommand("DELETE FROM employees WHERE id=@id", conn);
        cmd.Parameters.AddWithValue("id", id);
        cmd.ExecuteNonQuery();
    }

    public List<(int Id, string Name, int Age)> GetAll()
    {
        var list = new List<(int, string, int)>();
        using var conn = Database.GetConnection();
        using var cmd = new NpgsqlCommand("SELECT id, name, age FROM employees", conn);
        using var reader = cmd.ExecuteReader();
        while (reader.Read())
        {
            list.Add((reader.GetInt32(0), reader.GetString(1), reader.GetInt32(2)));
        }
        return list;
    }
}


