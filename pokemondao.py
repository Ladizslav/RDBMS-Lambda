from db_connector import get_connection
from pokemon import Pokemon
import csv

class PokemonDAO:
    @staticmethod
    def create_pokemon(name, pokemon_type, level, trainer_id=None):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO Pokemon (name, type, level, trainer_id) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (name, pokemon_type, level, trainer_id))
            connection.commit()
        except Exception as e:
            print(f"Chyba při vytváření Pokémona: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def get_pokemon_by_id(pokemon_id):
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM Pokemon WHERE pokemon_id = %s"
                cursor.execute(query, (pokemon_id,))
                row = cursor.fetchone()
                if row:
                    return Pokemon(**row)
        except Exception as e:
            print(f"Chyba při načítání Pokémona: {e}")
        finally:
            connection.close()

    @staticmethod
    def delete_pokemon(pokemon_id):
        connection = get_connection()
        try:
            PokemonDAO.show_pokemons_count(connection)
            with connection.cursor() as cursor:
                query = "DELETE FROM Pokemon WHERE pokemon_id = %s"
                cursor.execute(query, (pokemon_id,))
            connection.commit()
            PokemonDAO.show_pokemons_count(connection)
        except Exception as e:
            print(f"Chyba při mazání Pokémona: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def show_pokemons_count(connection):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Pokemon")
            row = cursor.fetchone()
            print(f"Počet Pokémonů: {row[0]}")

    @staticmethod
    def import_pokemons_from_csv(file_path):
        connection = get_connection()
        try:
            with open(file_path, mode='r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                with connection.cursor() as cursor:
                    for row in reader:
                        try:
                            query = """
                                INSERT INTO Pokemon (name, type, level, trainer_id) 
                                VALUES (%s, %s, %s, %s)
                            """
                            cursor.execute(query, (row['name'], row['type'], int(row['level']),int(row['trainer_id']) if row['trainer_id'] else None))
                    connection.commit()
                    print("Import Pokémonů dokončen.")
        except FileNotFoundError:
            print(f"Soubor {file_path} nebyl nalezen.")
        except Exception as e:
            print(f"Chyba při importu Pokémonů: {e}")
            connection.rollback()
        finally:
            connection.close()
