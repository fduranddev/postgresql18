using System;

class Program
{
    static void Main()
    {
        var repo = new EmployeeRepository();

        repo.CreateTable();

        repo.Insert("Alice", 30);
        repo.Insert("Bob", 25);

        var employees = repo.GetAll();
        Console.WriteLine("Liste des employés :");
        foreach (var emp in employees)
        {
            Console.WriteLine($"[{emp.Id}] {emp.Name} ({emp.Age} ans)");
        }
    }
}

