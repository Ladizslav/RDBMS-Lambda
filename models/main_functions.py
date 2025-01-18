from dao.gymdao import GymDAO
from dao.trainerdao import TrainerDAO
from dao.pokemondao import PokemonDAO
from dao.trainergymdao import TrainerGymDAO
from dao.pokemonstatsdao import PokemonStatsDAO
from utils.validators import get_non_empty_input, get_int_in_range, get_valid_trainer_id, get_trainer_id_input, get_valid_pokemon_type, get_pokemon_id_input, get_valid_pokemon_with_stats_id, get_valid_gym_id, get_valid_trainer_id_for_trainer_gym, get_valid_float, get_valid_gym_id_for_trainer_gym, get_pokemon_type_report, get_trainer_stats_report
from db.db_connector import get_connection
import threading
import time

current_isolation_level = "READ COMMITTED"

def set_isolation_level(level):
    global current_isolation_level
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"set session transaction isolation level {level}")
        connection.commit()
        print(f"Izolační úroveň nastavena na {level}.")
        current_isolation_level = level
    except Exception as e:
        print(f"Chyba při nastavování izolační úrovně: {e}")
    finally:
        connection.close()

def show_menu():
    print("\n=== Hlavní menu Pokémon databáze ===")
    print("1. Správa trenérů")
    print("2. Správa Pokémonů")
    print("3. Správa Gymů")
    print("4. Správa přiřazení trenéra a gymu")
    print("5. Správa statistik Pokémonů")
    print("6. Ukázka Phantom Read")
    print("7. Zvolení izolační úrovně")
    print("8. Zobrazení počtů typů pokémonů")
    print("9. Zobrazení statistik trenérů")
    print("10. Konec")


def manage_trainers():
    while True:
        print("\n=== Menu trenérů ===")
        print("1. Přidat trenéra")
        print("2. Zobrazit všechny trenéry")
        print("3. Aktualizovat trenéra")
        print("4. Smazat trenéra")
        print("5. Importovat trenéry z CSV")
        print("6. Návrat do hlavního menu")
        choice = input("Vyberte možnost: ")

        if choice == "1":
            try:
                name = get_non_empty_input("Zadejte jméno trenéra: ")
                age = get_int_in_range("Zadejte věk trenéra: ", 1, 100)
                team = get_non_empty_input("Zadejte tým trenéra: ")
                TrainerDAO.create_trainer(name, age, team)
                print(f"Trenér {name} byl úspěšně přidán!")
            except Exception as e:
                print(f"Chyba při přidávání trenéra: {e}")

        elif choice == "2":
            trainers = TrainerDAO.get_all_trainers()
            if trainers:
                print("\n=== Všichni trenéři ===")
                for trainer in trainers:
                    print(trainer)
            else:
                print("Nebyl nalezen žádný trenér.")

        elif choice == "3":
            try:
                trainer_id = get_valid_trainer_id("Zadejte ID trenéra pro aktualizaci: ")
                name = get_non_empty_input("Zadejte nové jméno trenéra: ")
                age = get_int_in_range("Zadejte nový věk trenéra: ", 1, 100)
                team = get_non_empty_input("Zadejte nový tým trenéra: ")
                TrainerDAO.update_trainer(trainer_id, name, age, team)
                print(f"Trenér s ID {trainer_id} byl úspěšně aktualizován!")
            except Exception as e:
                print(f"Došlo k chybě při aktualizaci trenéra: {e}")

        elif choice == "4":
            trainer_id = get_valid_trainer_id("Zadejte ID trenéra pro smazání: ")
            TrainerDAO.delete_trainer(trainer_id)

        elif choice == "5":
            file_path = "csv/trainer.csv"
            TrainerDAO.import_trainers_from_csv(file_path)

        elif choice == "6":
            print("Návrat do hlavního menu...")
            break

        else:
            print("Neplatná volba, zkuste to znovu.")

def manage_pokemons():
    while True:
        print("\n=== Pokémon Menu ===")
        print("1. Přidat Pokémona")
        print("2. Zobrazit všechny Pokémony")
        print("3. Smazat Pokémona")
        print("4. Importovat Pokémony z CSV")
        print("5. Návrat do hlavního menu")
        choice = input("Vyberte možnost: ")

        if choice == "1":
            name = get_non_empty_input("Zadejte jméno Pokémona: ")
            p_type = get_valid_pokemon_type("Zadejte typ Pokémona (Fire, Water, Grass): ")
            level = get_int_in_range("Zadejte úroveň Pokémona (1-100): ", 1, 100)
            trainer_id = get_trainer_id_input("Zadejte ID trenéra (nebo nechte prázdné): ")
            try:
                PokemonDAO.create_pokemon(name, p_type, level, trainer_id)
                print(f"Pokémon {name} byl úspěšně přidán!")
            except Exception as e:
                print(f"Chyba při vytváření Pokémona: {e}")

        elif choice == "2":
            pokemons = PokemonDAO.get_all_pokemons(get_connection())
            for pokemon in pokemons:
                print(f"ID: {pokemon['id']}, Jméno: {pokemon['name']}, Typ: {pokemon['type']}, Úroveň: {pokemon['level']}, ID trenéra: {pokemon['trainer_id']}")

        elif choice == "3":
            pokemon_id = get_pokemon_id_input("Zadejte ID Pokémona pro smazání: ")
            try:
                PokemonDAO.delete_pokemon(pokemon_id)
                print(f"Pokémon s ID {pokemon_id} byl úspěšně smazán!")
            except Exception as e:
                print(f"Chyba při mazání Pokémona: {e}")

        elif choice == "4":
            file_path = "csv/pokemon.csv"
            PokemonDAO.import_pokemons_from_csv(file_path)
            
        elif choice == "5":
            break  

        else:
            print("Neplatná volba. Zkuste to znovu.")

def manage_gyms():
    while True:
        print("\n=== Menu Gymů ===")
        print("1. Přidat Gym")
        print("2. Zobrazit Gymy")
        print("3. Smazat Gym")
        print("4. Návrat do hlavního menu")
        choice = input("Vyberte možnost: ")

        if choice == "1":
            name = get_non_empty_input("Zadejte název gymu: ")  
            city = get_non_empty_input("Zadejte město gymu: ") 
            GymDAO.create_gym(name, city)

        elif choice == "2":
            gyms = GymDAO.get_all_gyms()
            if gyms:
                for gym in gyms:
                   print(gym) 
            else:
                print("Nebyl nalezen žádný gym.")

        elif choice == "3":
            gym_id = get_valid_gym_id("Zadejte ID gymu pro smazání: ")  
            GymDAO.delete_gym(gym_id)
            print(f"Gym s ID {gym_id} byl úspěšně smazán.")

        elif choice == "4":
            print("Návrat do hlavního menu...")
            break
        else:
            print("Neplatná volba. Návrat do hlavního menu.")

def manage_trainer_gym_assignments():
    while True:
        print("\n=== Menu přiřazení trenéra a gymu ===")
        print("1. Přiřadit trenéra k gymu")
        print("2. Zobrazit všechny trenéry a jejich gymy")
        print("3. Odebrat trenéra z gymu")
        print("4. Návrat do hlavního menu")
        choice = input("Vyberte možnost: ")

        if choice == "1":
            trainer_id = get_valid_trainer_id("Zadejte ID trenéra: ")
            gym_id = get_valid_gym_id("Zadejte ID gymu: ")
            TrainerGymDAO.assign_trainer_to_gym(trainer_id, gym_id)
            print(f"Trenér s ID {trainer_id} byl úspěšně přiřazen k gymu s ID {gym_id}.")
        elif choice == "2":
            trainers_and_gyms = TrainerGymDAO.get_all_trainers_and_gyms()
            if trainers_and_gyms:
                for entry in trainers_and_gyms:
                    gym_name = entry['gym_name'] if entry['gym_name'] else "Žádný gym není přiřazen"
                    city = entry['city'] if entry['city'] else "N/A"
                    print(f"Trenér: {entry['trainer_name']} (ID: {entry['trainer_id']}) - Gym: {gym_name} (ID: {entry['gym_id'] if entry['gym_id'] else 'N/A'}), Město: {city}")
            else:
                print("Nebyl nalezen žádný trenér nebo gym.")

        elif choice == "3":
            trainer_id = get_valid_trainer_id_for_trainer_gym("Zadejte ID trenéra: ")
            gym_id = get_valid_gym_id_for_trainer_gym("Zadejte ID gymu pro odebrání: ")
            TrainerGymDAO.unassign_trainer_from_gym(trainer_id, gym_id)
            print(f"Trenér s ID {trainer_id} byl úspěšně odebrán z gymu s ID {gym_id}.")
        elif choice == "4":
            print("Návrat do hlavního menu...")
            break
        else:
            print("Neplatná volba. Zkuste to znovu.")

def manage_pokemon_stats():
    while True:
        print("\n=== Menu statistik Pokémonů ===")
        print("1. Přidat statistiky Pokémona")
        print("2. Zobrazit statistiky pro Pokémona")
        print("3. Smazat statistiky pro Pokémona")
        print("4. Porazit Pokémona")
        print("5. Oživit Pokémona")
        print("6. Návrat do hlavního menu")
        choice = input("Vyberte možnost: ")

        if choice == "1":
            pokemon_id = get_pokemon_id_input("Zadejte ID Pokémona: ")
            speed = get_valid_float("Zadejte rychlost Pokémona: ")
            strength = get_valid_float("Zadejte sílu Pokémona: ")
            defense = get_valid_float("Zadejte obranu Pokémona: ")
            PokemonStatsDAO.create_stats(pokemon_id, speed, strength, defense)
            print(f"Statistiky pro Pokémona ID {pokemon_id} byly přidány.")
        elif choice == "2":
            pokemon_id = get_valid_pokemon_with_stats_id("Zadejte ID Pokémona pro zobrazení statistik: ")
            stats = PokemonStatsDAO.get_stats_by_pokemon_id(pokemon_id)
            if stats:
                if stats.is_alive:
                    print(f"Statistiky pro Pokémona ID {pokemon_id}: Rychlost: {stats.speed}, Síla: {stats.strength}, Obrana: {stats.defense}")
                else:
                    print(f"Pokémon ID {pokemon_id} byl poražen a nelze zobrazit statistiky.")
            else:
                print(f"Žádné statistiky nenalezeny pro Pokémona ID {pokemon_id}.")
        elif choice == "3":
            pokemon_id = get_valid_pokemon_with_stats_id("Zadejte ID Pokémona pro smazání statistik: ")
            PokemonStatsDAO.delete_stats(pokemon_id)
            print(f"Statistiky pro Pokémona ID {pokemon_id} byly smazány.")
        elif choice == "4":
            pokemon_id = get_valid_pokemon_with_stats_id("Zadejte ID Pokémona pro poražení: ")
            PokemonStatsDAO.defeat_pokemon(pokemon_id)
        elif choice == "5":
            pokemon_id = get_valid_pokemon_with_stats_id("Zadejte ID Pokémona pro oživení: ")
            PokemonStatsDAO.revive_pokemon(pokemon_id)
        elif choice == "6":
            print("Návrat do hlavního menu...")
            break
        else:
            print("Neplatná volba. Návrat do hlavního menu.")

def manage_transaction_isolation():
    print("\n=== Nastavení izolační úrovně ===")
    print(f"Aktuální izolační úroveň: {current_isolation_level}")
    print("1. READ UNCOMMITTED")
    print("2. READ COMMITTED")
    print("3. REPEATABLE READ")
    print("4. SERIALIZABLE")
    choice = input("Vyberte izolační úroveň: ")

    if choice == "1":
        set_isolation_level("READ UNCOMMITTED")
    elif choice == "2":
        set_isolation_level("READ COMMITTED")
    elif choice == "3":
        set_isolation_level("REPEATABLE READ")
    elif choice == "4":
        set_isolation_level("SERIALIZABLE")
    else:
        print("Neplatná volba, prosím vyberte znovu.")

def test_phantom_read(trainer_id):
    isolation_level = current_isolation_level
    main_connection = get_connection()
    main_connection.start_transaction(isolation_level=isolation_level)

    try:
        print(f"\nAktuální izolační úroveň: {isolation_level}")
        print("\nPřed přidáním pokémona:")
        pokemon_list_before = PokemonDAO.get_pokemons_by_trainer_id(trainer_id, main_connection)
        print(f"Počet pokémonů pro trenéra ID {trainer_id}: {len(pokemon_list_before)}")

        def add_pokemon():
            thread_connection = get_connection()
            try:
                PokemonDAO.create_pokemon("Charmander", "Fire", 5, trainer_id)
                thread_connection.commit()
            finally:
                thread_connection.close()

        thread = threading.Thread(target=add_pokemon)
        thread.start()
        time.sleep(2)

        print("\nPo přidání pokémona:")
        pokemon_list_after = PokemonDAO.get_pokemons_by_trainer_id(trainer_id, main_connection)
        print(f"Počet pokémonů pro trenéra ID {trainer_id}: {len(pokemon_list_after)}")

    finally:
        main_connection.commit()
        main_connection.close()

def show_pokemon_type_report():
    pokemon_report = get_pokemon_type_report()
    if pokemon_report:
        print("\nPočty pokémonů podle typů:")
        for row in pokemon_report:
            print(f"Typ: {row[0]}, Počet: {row[1]}")
    else:
        print("Chyba při získávání počtů pokémonů podle typů.")

def show_trainer_stats_report():
    trainer_report = get_trainer_stats_report()
    if trainer_report:
        print("\nStatistiky trenérů:")
        for row in trainer_report:
            trainer_name = row[0]
            total_pokemon = row[1]
            avg_level = row[2] if row[2] is not None else "N/A" 
            print(f"Trenér: {trainer_name}, Počet pokémonů: {total_pokemon}, Průměrná úroveň: {avg_level}")
    else:
        print("Chyba při získávání statistik trenérů.")
