from db_connector import get_connection
from trainerdao import TrainerDAO
from pokemondao import PokemonDAO
from gymdao import GymDAO
from trainergymdao import TrainerGymDAO
from pokemonstatsdao import PokemonStatsDAO
from table_initiator import create_tables_and_views

def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")

def get_int_in_range(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Value must be between {min_value} and {max_value}. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_int_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Please enter a valid integer.")

def get_valid_pokemon_type(prompt):
    valid_types = ['Fire', 'Water', 'Grass']
    while True:
        p_type = input(prompt).capitalize().strip()
        if p_type in valid_types:
            return p_type
        else:
            print("Invalid Pokémon type. Please choose from Fire, Water, or Grass.")

def get_trainer_id_input(prompt):
    while True:
        trainer_id_input = input(prompt).strip()
        if trainer_id_input == "":
            return None
        try:
            trainer_id = int(trainer_id_input)
            trainer = TrainerDAO.get_trainer_by_id(trainer_id)
            if trainer:
                return trainer_id
            else:
                print(f"Trainer ID {trainer_id} does not exist. Setting trainer_id to NULL.")
                return None
        except ValueError:
            print("Invalid Trainer ID entered. Setting trainer_id to NULL.")
            return None

def get_pokemon_id_input(prompt):
    while True:
        try:
            pokemon_id = int(input(prompt))
            pokemon = PokemonDAO.get_pokemon_by_id(pokemon_id)  
            if pokemon:
                return pokemon_id
            else:
                print(f"Pokémon ID {pokemon_id} does not exist. Please enter a valid Pokémon ID.")
        except ValueError:
            print("Please enter a valid integer for Pokémon ID.")

def get_valid_trainer_id(prompt):
    while True:
        try:
            trainer_id = int(input(prompt))
            trainer = TrainerDAO.get_trainer_by_id(trainer_id)  
            if trainer:
                return trainer_id
            else:
                print(f"Trainer with ID {trainer_id} does not exist. Please enter a valid Trainer ID.")
        except ValueError:
            print("Please enter a valid integer for Trainer ID.")

def get_valid_gym_id(prompt):
    while True:
        try:
            gym_id = int(input(prompt)) 
            gym = GymDAO.get_gym_by_id(gym_id) 
            if gym:
                return gym_id  
            else:
                print(f"Gym with ID {gym_id} does not exist. Please enter a valid Gym ID.")
        except ValueError:
            print("Please enter a valid integer for Gym ID.")

def get_valid_gym_id_for_trainer_gym(prompt):
    while True:
        try:
            gym_id = int(input(prompt))  
            gym = GymDAO.get_gym_by_id(gym_id)  
            if gym:
                gyms_for_trainer = TrainerGymDAO.get_gyms_for_trainer_by_gym_id(gym_id)
                if gyms_for_trainer:
                    return gym_id  
                else:
                    print(f"Gym with ID {gym_id} is not assigned to any trainer. Please enter a valid Gym ID that has a trainer assigned.")
            else:
                print(f"Gym with ID {gym_id} does not exist. Please enter a valid Gym ID.")
        except ValueError:
            print("Please enter a valid integer for Gym ID.") 

def get_valid_trainer_id_for_trainer_gym(prompt):
    while True:
        try:
            trainer_id = int(input(prompt))  
            trainer = TrainerDAO.get_trainer_by_id(trainer_id) 
            if trainer:
                gyms_for_trainer = TrainerGymDAO.get_gyms_for_trainer(trainer_id)
                if gyms_for_trainer:
                    return trainer_id  
                else:
                    print(f"Trainer with ID {trainer_id} is not assigned to any gym. Please enter a valid Trainer ID that is assigned to a gym.")
            else:
                print(f"Trainer with ID {trainer_id} does not exist. Please enter a valid Trainer ID.")
        except ValueError:
            print("Please enter a valid integer for Trainer ID.") 

def get_valid_float(prompt, min_value=0.0):
    while True:
        try:
            value = float(input(prompt))
            if value >= min_value:
                return value
            else:
                print(f"Value must be at least {min_value}. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_valid_pokemon_with_stats_id(prompt):
    while True:
        try:
            pokemon_id = int(input(prompt))
            stats = PokemonStatsDAO.get_stats_by_pokemon_id(pokemon_id)
            if stats:
                return pokemon_id
            else:
                print(f"Pokémon with ID {pokemon_id} does not have stats yet. Please enter a valid Pokémon ID.")
        except ValueError:
            print("Invalid input. Please enter a valid integer for Pokémon ID.")


def show_menu():
    print("\n=== Pokémon Database Menu ===")
    print("1. Manage Trainers")
    print("2. Manage Pokémon")
    print("3. Manage Gyms")
    print("4. Manage Trainer-Gym Assignments")
    print("5. Manage Pokémon Stats")
    print("6. Exit")

def manage_trainers():
    while True:
        print("\n=== Trainer Menu ===")
        print("1. Add Trainer")
        print("2. View All Trainers")
        print("3. Update Trainer")
        print("4. Delete Trainer")
        print("5. Import Trainers from CSV")
        print("6. Back to Main Menu")
        choice = input("Choose an option: ")

        if choice == "1":
            try:
                name = get_non_empty_input("Enter trainer name: ")
                age = get_int_in_range("Enter trainer age: ", 1, 100)
                team = get_non_empty_input("Enter trainer team: ")
                TrainerDAO.create_trainer(name, age, team)
                print(f"Trainer {name} successfully added!")
            except Exception as e:
                print(f"An error occurred while adding the trainer: {e}")

        elif choice == "2":
            trainers = TrainerDAO.get_all_trainers()
            if trainers:
                print("\n=== All Trainers ===")
                for trainer in trainers:
                    print(f"ID: {trainer.trainer_id}, Name: {trainer.name}, Age: {trainer.age}, Team: {trainer.team}")
            else:
                print("No trainers found.")

        elif choice == "3":
            try:
                trainer_id = get_valid_trainer_id("Enter Trainer ID to update: ")
                name = get_non_empty_input("Enter new trainer name: ")
                age = get_int_in_range("Enter new trainer age: ", 1, 100)
                team = get_non_empty_input("Enter new trainer team: ")
                TrainerDAO.update_trainer(trainer_id, name, age, team)
                print(f"Trainer with ID {trainer_id} successfully updated!")
            except Exception as e:
                print(f"An error occurred while updating the trainer: {e}")

        elif choice == "4":
            trainer_id = get_valid_trainer_id("Enter Trainer ID to delete: ")
            TrainerDAO.delete_trainer(trainer_id)

        elif choice == "5":
            file_path = "trainer.csv"
            TrainerDAO.import_trainers_from_csv(file_path)

        elif choice == "6":
            print("Returning to Main Menu...")
            break

        else:
            print("Invalid choice, please try again.")

def manage_pokemons():
    while True:
        print("\n=== Pokémon Menu ===")
        print("1. Add Pokémon")
        print("2. View All Pokémon")
        print("3. Update Pokémon")
        print("4. Delete Pokémon")
        print("5. Import Pokémon from CSV")
        print("6. Back to Main Menu")
        choice = input("Choose an option: ")

        if choice == "1":
            name = get_non_empty_input("Enter Pokémon name: ")
            p_type = get_valid_pokemon_type("Enter Pokémon type (Fire, Water, Grass): ")
            level = get_int_in_range("Enter Pokémon level (1-100): ", 1, 100)
            trainer_id = get_trainer_id_input("Enter Trainer ID (or leave blank): ")
            try:
                PokemonDAO.create_pokemon(name, p_type, level, trainer_id)
                print(f"Pokémon {name} successfully added!")
            except Exception as e:
                print(f"Chyba při vytváření Pokémona: {e}")

        elif choice == "2":
            pokemons = PokemonDAO.get_all_pokemons(get_connection())
            for pokemon in pokemons:
                print(pokemon)

        elif choice == "3":
            pokemon_id = get_pokemon_id_input("Enter Pokémon ID to update: ")
            name = get_non_empty_input("Enter new Pokémon name: ")
            p_type = get_valid_pokemon_type("Enter new Pokémon type (Fire, Water, Grass): ")
            level = get_int_in_range("Enter new Pokémon level (1-100): ", 1, 100)
            trainer_id = get_trainer_id_input("Enter new Trainer ID (or leave blank): ")
            try:
                PokemonDAO.update_pokemon(pokemon_id, name, p_type, level, trainer_id)
                print(f"Pokémon with ID {pokemon_id} successfully updated!")
            except Exception as e:
                print(f"Chyba při aktualizaci Pokémona: {e}")

        elif choice == "4":
            pokemon_id = get_pokemon_id_input("Enter Pokémon ID to delete: ")
            try:
                PokemonDAO.delete_pokemon(pokemon_id)
                print(f"Pokémon with ID {pokemon_id} successfully deleted!")
            except Exception as e:
                print(f"Chyba při mazání Pokémona: {e}")

        elif choice == "5":
            file_path = "pokemon.csv"
            PokemonDAO.import_pokemons_from_csv(file_path)
            
        elif choice == "6":
            break  

        else:
            print("Invalid choice. Please try again.")

def manage_gyms():
    while True:
        print("\n=== Gym Menu ===")
        print("1. Add Gym")
        print("2. View Gyms")
        print("3. Delete Gym")
        print("4. Back to Main Menu")
        choice = input("Choose an option: ")

        if choice == "1":
            name = get_non_empty_input("Enter gym name: ")  
            city = get_non_empty_input("Enter gym city: ") 
            GymDAO.create_gym(name, city)

        elif choice == "2":
            gyms = GymDAO.get_all_gyms()
            if gyms:
                for gym in gyms:
                   print(gym) 
            else:
                print("No gyms found.")

        elif choice == "3":
            gym_id = get_valid_gym_id("Enter gym ID to delete: ")  
            GymDAO.delete_gym(gym_id)
            print(f"Gym with ID {gym_id} successfully deleted.")

        elif choice == "4":
            print("Returning to Main Menu...")
            break

        else:
            print("Invalid choice. Returning to main menu.")

def manage_trainer_gym_assignments():
    while True:
        print("\n=== Trainer-Gym Assignment Menu ===")
        print("1. Assign Trainer to Gym")
        print("2. View All Trainers and Their Gyms")
        print("3. Unassign Trainer from Gym")
        print("4. Back to Main Menu")
        choice = input("Choose an option: ")

        if choice == "1":
            trainer_id = get_valid_trainer_id("Enter Trainer ID: ")
            gym_id = get_valid_gym_id("Enter Gym ID: ")
            TrainerGymDAO.assign_trainer_to_gym(trainer_id, gym_id)
            print(f"Trainer with ID {trainer_id} successfully assigned to Gym with ID {gym_id}.")
        elif choice == "2":
            trainers_and_gyms = TrainerGymDAO.get_all_trainers_and_gyms()
            if trainers_and_gyms:
                for entry in trainers_and_gyms:
                    trainer_name = entry['trainer_name']
                    gym_name = entry['gym_name'] if entry['gym_name'] else "No gym assigned"
                    print(f"Trainer: {trainer_name} (ID: {entry['trainer_id']}) - Gym: {gym_name} (ID: {entry['gym_id'] if entry['gym_id'] else 'N/A'})")
            else:
                print("No trainers or gyms found.")
        elif choice == "3":
            trainer_id = get_valid_trainer_id_for_trainer_gym("Enter Trainer ID: ")
            gym_id = get_valid_gym_id_for_trainer_gym("Enter Gym ID to unassign: ")
            TrainerGymDAO.unassign_trainer_from_gym(trainer_id, gym_id)
            print(f"Trainer with ID {trainer_id} successfully unassigned from Gym with ID {gym_id}.")
        elif choice == "4":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please try again.")



def manage_pokemon_stats():
    print("\n=== Pokémon Stats Menu ===")
    print("1. Add Pokémon Stats")
    print("2. View Stats for a Pokémon")
    print("3. Delete Stats for a Pokémon")
    print("4. Back to Main Menu")
    choice = input("Choose an option: ")

    if choice == "1":
        pokemon_id = get_pokemon_id_input("Enter Pokémon ID: ")
        speed = get_valid_float("Enter Pokémon speed: ")
        strength = get_valid_float("Enter Pokémon strength: ")
        defense = get_valid_float("Enter Pokémon defense: ")
        PokemonStatsDAO.create_stats(pokemon_id, speed, strength, defense)
        print(f"Stats for Pokémon ID {pokemon_id} have been added.")
    elif choice == "2":
        pokemon_id = get_valid_pokemon_with_stats_id("Enter Pokémon ID to view stats: ")
        stats = PokemonStatsDAO.get_stats_by_pokemon_id(pokemon_id)
        if stats:
            print(f"Stats for Pokémon ID {pokemon_id}: Speed: {stats['speed']}, Strength: {stats['strength']}, Defense: {stats['defense']}")
        else:
            print(f"No stats found for Pokémon ID {pokemon_id}.")
    elif choice == "3":
        pokemon_id = get_valid_pokemon_with_stats_id("Enter Pokémon ID to delete stats: ")
        PokemonStatsDAO.delete_stats(pokemon_id)
        print(f"Stats for Pokémon ID {pokemon_id} have been deleted.")
    elif choice == "4":
        print("Returning to Main Menu...")
    else:
        print("Invalid choice. Returning to main menu.")


def main():
    try:
        connection = get_connection()
        if connection is None:
            print("Failed to connect to the database.")
            return

        with connection:
            create_tables_and_views(connection)
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
