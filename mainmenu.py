from db_connector import get_connection
from table_initiator import create_tables_and_views
from pokemondao import PokemonDAO
from trainerdao import TrainerDAO
from gymdao import GymDAO

def show_menu():
    print("\n=== Pokémon Database Menu ===")
    print("1. Add Trainer")
    print("2. Add Pokémon")
    print("3. Add Gym")
    print("4. View Trainers")
    print("5. View Pokémon")
    print("6. View Gyms")
    print("7. Simulate Non-Repeatable Read")
    print("8. Simulate Phantom Read")
    print("9. Exit")

def main():
    connection = get_connection()
    if connection is None:
        print("Failed to connect to the database. Exiting...")
        return

    create_tables_and_views(connection)

    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter trainer name: ")
            age = int(input("Enter trainer age: "))
            team = input("Enter trainer team: ")
            TrainerDAO.add_trainer(connection, name, age, team)
        elif choice == "2":
            name = input("Enter Pokémon name: ")
            type = input("Enter Pokémon type (Fire, Water, Grass, Electric, Psychic): ")
            level = int(input("Enter Pokémon level: "))
            trainer_id = input("Enter Trainer ID (or leave blank): ")
            trainer_id = int(trainer_id) if trainer_id else None
            PokemonDAO.add_pokemon(connection, name, type, level, trainer_id)
        elif choice == "3":
            name = input("Enter gym name: ")
            city = input("Enter gym city: ")
            GymDAO.add_gym(connection, name, city)
        elif choice == "4":
            trainers = TrainerDAO.get_all_trainers(connection)
            for trainer in trainers:
                print(trainer)
        elif choice == "5":
            pokemons = PokemonDAO.get_all_pokemons(connection)
            for pokemon in pokemons:
                print(pokemon)
        elif choice == "6":
            gyms = GymDAO.get_all_gyms(connection)
            for gym in gyms:
                print(gym)
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()

    print("\nSimulating Phantom Read...")
    connection.start_transaction(isolation_level="REPEATABLE READ")
    cursor = connection.cursor()

    # Thread 1: Count Pokémon
    cursor.execute("SELECT COUNT(*) FROM Pokemon")
    print("Initial Count:", cursor.fetchone()[0])

    # Simulate another thread adding a Pokémon
    cursor.execute("INSERT INTO Pokemon (name, type, level) VALUES ('Gyarados', 'Water', 30)")
    connection.commit()

    # Thread 1: Re-count Pokémon
    cursor.execute("SELECT COUNT(*) FROM Pokemon")
    print("Second Count:", cursor.fetchone()[0])

    print("Phantom Read demonstrated.")

if __name__ == "__main__":
    main()
