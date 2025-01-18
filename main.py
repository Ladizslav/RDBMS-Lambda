from db_connector import get_connection
from table_initiator import create_tables_and_views
from models.main_functions import show_menu, manage_trainers, manage_pokemons, manage_gyms, manage_trainer_gym_assignments, manage_pokemon_stats, manage_transaction_isolation, test_phantom_read, show_pokemon_type_report, show_trainer_stats_report
from utils.validators import get_valid_trainer_id

def main():
    try:
        connection = get_connection()
        if connection is None:
            print("Nepodařilo se připojit k databázi.")
            return

        with connection:
            create_tables_and_views(connection)
            while True:
                show_menu()
                choice = input("Vyberte možnost: ")

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
                    trainer_id = get_valid_trainer_id("Zadejte ID trenéra pro ukázku Phantom Read: ")
                    test_phantom_read(trainer_id)
                elif choice == "7":
                    manage_transaction_isolation() 
                elif choice == "8":
                    show_pokemon_type_report()
                elif choice == "9":
                    show_trainer_stats_report()
                elif choice == "10":
                    print("Ukončuji aplikaci.")
                    break
                else:
                    print("Neplatná volba. Zkuste to znovu.")

    except Exception as e:
        print(f"Chyba: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()
