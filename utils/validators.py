from dao.gymdao import GymDAO
from dao.trainerdao import TrainerDAO
from dao.pokemondao import PokemonDAO
from dao.trainergymdao import TrainerGymDAO
from dao.pokemonstatsdao import PokemonStatsDAO
from db_connector import get_connection



def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Toto pole nemůže být prázdné.")

def get_int_in_range(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Hodnota musí být mezi {min_value} a {max_value}.")
        except ValueError:
            print("Neplatný vstup.")

def get_int_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Zadejte platné číslo.")

def get_valid_pokemon_type(prompt):
    valid_types = ['Fire', 'Water', 'Grass']
    while True:
        p_type = input(prompt).capitalize().strip()
        if p_type in valid_types:
            return p_type
        else:
            print("Neplatný typ Pokémona. Zvolte ze seznamu Fire, Water nebo Grass.")

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
                print(f"Trenér neexistuje. Nastavuji trainer_id na NULL.")
                return None
        except ValueError:
            print("Neplatné ID trenéra. Nastavuji trainer_id na NULL.")
            return None

def get_pokemon_id_input(prompt):
    while True:
        try:
            pokemon_id = int(input(prompt))
            pokemon = PokemonDAO.get_pokemon_by_id(pokemon_id)  
            if pokemon:
                return pokemon_id
            else:
                print(f"Pokémon neexistuje. Zadejte platné ID Pokémona.")
        except ValueError:
            print("Zadejte platné celé číslo pro ID Pokémona.")

def get_valid_trainer_id(prompt):
    while True:
        try:
            trainer_id = int(input(prompt))
            trainer = TrainerDAO.get_trainer_by_id(trainer_id)  
            if trainer:
                return trainer_id
            else:
                print(f"Trenér neexistuje. Zadejte platné ID trenéra.")
        except ValueError:
            print("Zadejte platné číslo pro ID trenéra.")

def get_valid_gym_id(prompt):
    while True:
        try:
            gym_id = int(input(prompt)) 
            gym = GymDAO.get_gym_by_id(gym_id) 
            if gym:
                return gym_id  
            else:
                print(f"Gym s neexistuje. Zadejte platné ID Gymu.")
        except ValueError:
            print("Zadejte platné číslo pro ID Gymu.")

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
                    print(f"Gym není přiřazen žádnému trenérovi. Zadejte platné ID Gymu, který má přiřazeného trenéra.")
            else:
                print(f"Gym neexistuje. Zadejte platné ID Gymu.")
        except ValueError:
            print("Zadejte platné celé číslo pro ID Gymu.") 

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
                    print(f"Trenér není přiřazen žádnému gymu. Zadejte platné ID trenéra.")
            else:
                print(f"Trenér neexistuje. Zadejte platné ID trenéra.")
        except ValueError:
            print("Zadejte platné celé číslo pro ID trenéra.") 

def get_valid_float(prompt, min_value=0.0):
    while True:
        try:
            value = float(input(prompt))
            if value >= min_value:
                return value
            else:
                print(f"Hodnota musí být alespoň {min_value}. Zkuste to znovu.")
        except ValueError:
            print("Neplatný vstup. Zadejte platné číslo.")

def get_valid_pokemon_with_stats_id(prompt):
    while True:
        try:
            pokemon_id = int(input(prompt))
            stats = PokemonStatsDAO.get_stats_by_pokemon_id(pokemon_id)
            if stats:
                return pokemon_id
            else:
                print(f"Pokémon s ID {pokemon_id} ještě nemá statistiky. Zadejte platné ID Pokémona.")
        except ValueError:
            print("Neplatný vstup. Zadejte platné celé číslo pro ID Pokémona.")


def get_pokemon_count_for_trainer(trainer_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("select count(*) from pokemon where trainer_id = %s", (trainer_id,))
            result = cursor.fetchone()
            print(f"Počet pokémonů pro trenéra ID {trainer_id}: {result[0]}")
    except Exception as e:
        print(f"Chyba při získávání počtu pokémonů: {e}")
    finally:
        connection.close()

def add_pokemon_for_trainer(trainer_id, name, pokemon_type, level, connection=None):
    own_connection = connection is None
    connection = get_connection()  
    try:
        PokemonDAO.create_pokemon(name, pokemon_type, level, trainer_id)
        if own_connection:
            connection.commit()  
        print(f"Pokémon {name} byl úspěšně přidán trenérovi s ID {trainer_id}.")
    except Exception as e:
        print(f"Chyba při přidávání pokémona: {e}")
        if own_connection:
            connection.rollback()  
    finally:
        if own_connection:
            connection.close()

def get_pokemon_type_report():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("select * from pokemon_type_report;")
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Chyba při získávání pokemon_type_report: {e}")
        return []
    finally:
        connection.close()

def get_trainer_stats_report():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("select * from trainer_stats;")
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Chyba při získávání trainer_stats_report: {e}")
        return []
    finally:
        connection.close()
