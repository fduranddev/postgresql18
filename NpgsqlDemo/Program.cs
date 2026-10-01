using System;

class Program
{
    static void Main()
    {
        var repo = new EmployeeRepository();
        repo.CreateTable();

        bool exit = false;

        while (!exit)
        {
            Console.WriteLine("\n=== MENU EMPLOYES ===");
            Console.WriteLine("1. Lister les employés");
            Console.WriteLine("2. Ajouter un employé");
            Console.WriteLine("3. Mettre à jour un employé");
            Console.WriteLine("4. Supprimer un employé");
            Console.WriteLine("5. Quitter");
            Console.Write("Choix : ");

            string choice = Console.ReadLine() ?? "";

            switch (choice)
            {
                case "1":
                    ListEmployees(repo);
                    break;
                case "2":
                    AddEmployee(repo);
                    break;
                case "3":
                    UpdateEmployee(repo);
                    break;
                case "4":
                    DeleteEmployee(repo);
                    break;
                case "5":
                    exit = true;
                    break;
                default:
                    Console.WriteLine("Choix invalide !");
                    break;
            }
        }
    }

    static void ListEmployees(EmployeeRepository repo)
    {
        var employees = repo.GetAll();
        Console.WriteLine("\nListe des employés :");
        foreach (var emp in employees)
            Console.WriteLine($"[{emp.Id}] {emp.Name} ({emp.Age} ans)");
    }

    static void AddEmployee(EmployeeRepository repo)
    {
        Console.Write("Nom : ");
        string name = Console.ReadLine() ?? "";
        Console.Write("Âge : ");
        if (!int.TryParse(Console.ReadLine(), out int age))
        {
            Console.WriteLine("Âge invalide !");
            return;
        }
        repo.Insert(name, age);
        Console.WriteLine("Employé ajouté !");
    }

    static void UpdateEmployee(EmployeeRepository repo)
    {
        Console.Write("ID de l'employé à mettre à jour : ");
        if (!int.TryParse(Console.ReadLine(), out int id))
        {
            Console.WriteLine("ID invalide !");
            return;
        }
        Console.Write("Nouveau nom : ");
        string name = Console.ReadLine();
        Console.Write("Nouvel âge : ");
        if (!int.TryParse(Console.ReadLine(), out int age))
        {
            Console.WriteLine("Âge invalide !");
            return;
        }
        repo.Update(id, name, age);
        Console.WriteLine("Employé mis à jour !");
    }

    static void DeleteEmployee(EmployeeRepository repo)
    {
        Console.Write("ID de l'employé à supprimer : ");
        if (!int.TryParse(Console.ReadLine(), out int id))
        {
            Console.WriteLine("ID invalide !");
            return;
        }
        repo.Delete(id);
        Console.WriteLine("Employé supprimé !");
    }
}

