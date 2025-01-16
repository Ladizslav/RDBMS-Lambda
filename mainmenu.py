from db_connector import get_connection
from trainerdao import TrainerDAO
from pokemondao import PokemonDAO
from gymdao import GymDAO
from trainergymdao import TrainerGymDAO
from pokemonstatsdao import PokemonStatsDAO

def show_menu():
    print("\n=== Pokémon Database Menu ===")
    print("1. Manage Trainers")
    print("2. Manage Pokémon")
    print("3. Manage Gyms")
    print("4. Manage Trainer-Gym Assignments")
    print("5. Manage Pokémon Stats")
    print("6. Exit")

def manage_trainers():
    print("\n=== Trainer Menu ===")
    print("1. Add Trainer")
    print("2. View Trainers")
    print("3. Delete Trainer")
    choice = input("Choose an option: ")

    if choice == "1":
        name = input("Enter trainer name: ")
        age = int(input("Enter trainer age: "))
        team = input("Enter trainer team: ")
        TrainerDAO.create_trainer(name, age, team)
    elif choice == "2":
        trainers = TrainerDAO.get_all_trainers(get_connection())
        for trainer in trainers:
            print(trainer)
    elif choice == "3":
        trainer_id = int(input("Enter trainer ID to delete: "))
        TrainerDAO.delete_trainer(trainer_id)
    else:
        print("Invalid choice. Returning to main menu.")

def manage_pokemons():
    print("\n=== Pokémon Menu ===")
    print("1. Add Pokémon")
    print("2. View Pokémon")
    print("3. Delete Pokémon")
    choice = input("Choose an option: ")

    if choice == "1":
        name = input("Enter Pokémon name: ")
        type = input("Enter Pokémon type (Fire, Water, Grass): ")
        level = int(input("Enter Pokémon level: "))
        trainer_id = input("Enter Trainer ID (or leave blank): ")
        trainer_id = int(trainer_id) if trainer_id else None
        PokemonDAO.create_pokemon(name, type, level, trainer_id)
    elif choice == "2":
        pokemons = PokemonDAO.get_all_pokemons(get_connection())
        for pokemon in pokemons:
            print(pokemon)
    elif choice == "3":
        pokemon_id = int(input("Enter Pokémon ID to delete: "))
        PokemonDAO.delete_pokemon(pokemon_id)
    else:
        print("Invalid choice. Returning to main menu.")

def manage_gyms():
    print("\n=== Gym Menu ===")
    print("1. Add Gym")
    print("2. View Gyms")
    print("3. Delete Gym")
    choice = input("Choose an option: ")

    if choice == "1":
        name = input("Enter gym name: ")
        city = input("Enter gym city: ")
        GymDAO.create_gym(name, city)
    elif choice == "2":
        gyms = GymDAO.get_all_gyms(get_connection())
        for gym in gyms:
            print(gym)
    elif choice == "3":
        gym_id = int(input("Enter gym ID to delete: "))
        GymDAO.delete_gym(gym_id)
    else:
        print("Invalid choice. Returning to main menu.")

def manage_trainer_gym_assignments():
    print("\n=== Trainer-Gym Assignment Menu ===")
    print("1. Assign Trainer to Gym")
    print("2. View Gyms for a Trainer")
    print("3. Unassign Trainer from Gym")
    choice = input("Choose an option: ")

    if choice == "1":
        trainer_id = int(input("Enter Trainer ID: "))
        gym_id = int(input("Enter Gym ID: "))
        TrainerGymDAO.assign_trainer_to_gym(trainer_id, gym_id)
    elif choice == "2":
        trainer_id = int(input("Enter Trainer ID to view their gyms: "))
        gyms = TrainerGymDAO.get_gyms_for_trainer(trainer_id)
        for gym in gyms:
            print(gym)
    elif choice == "3":
        trainer_id = int(input("Enter Trainer ID: "))
        gym_id = int(input("Enter Gym ID to unassign: "))
        TrainerGymDAO.unassign_trainer_from_gym(trainer_id, gym_id)
    else:
        print("Invalid choice. Returning to main menu.")

def manage_pokemon_stats():
    print("\n=== Pokémon Stats Menu ===")
    print("1. Add Pokémon Stats")
    print("2. View Stats for a Pokémon")
    print("3. Delete Stats for a Pokémon")
    choice = input("Choose an option: ")

    if choice == "1":
        pokemon_id = int(input("Enter Pokémon ID: "))
        speed = float(input("Enter Pokémon speed: "))
        strength = float(input("Enter Pokémon strength: "))
        defense = float(input("Enter Pokémon defense: "))
        PokemonStatsDAO.create_stats(pokemon_id, speed, strength, defense)
    elif choice == "2":
        pokemon_id = int(input("Enter Pokémon ID to view stats: "))
        stats = PokemonStatsDAO.get_stats_by_pokemon_id(pokemon_id)
        print(stats)
    elif choice == "3":
        pokemon_id = int(input("Enter Pokémon ID to delete stats: "))
        PokemonStatsDAO.delete_stats(pokemon_id)
    else:
        print("Invalid choice. Returning to main menu.")

def main():
    try:
        connection = get_connection()
        if connection is None:
            print("Failed to connect to the database.")
            return

        with connection:
            while True:
                show_menu()
                choice = input("Choose an option: ")

                if choice == "1":
                    manage_trainers()
                elif choice == "2":
                    manage_pokemons()
                elif choice == "3":
                    manage_gyms()
                elif choice == "4":
                    manage_trainer_gym_assignments()
                elif choice == "5":
                    manage_pokemon_stats()
                elif choice == "6":
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()
