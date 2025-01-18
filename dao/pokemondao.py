from db_connector import get_connection
from classes.pokemon import Pokemon
import csv

class PokemonDAO:
    @staticmethod
    def create_pokemon(name, pokemon_type, level, trainer_id=None):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "insert into pokemon (name, type, level, trainer_id) values (%s, %s, %s, %s)"
                cursor.execute(query, (name, pokemon_type, level, trainer_id))
            connection.commit()
        except Exception as e:
            print(f"Chyba při vytváření pokémona: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def get_pokemon_by_id(pokemon_id):
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = "select * from pokemon where id = %s"
                cursor.execute(query, (pokemon_id,))
                row = cursor.fetchone()
                if row:
                    return Pokemon(**row)
        except Exception as e:
            print(f"Chyba při načítání pokémona: {e}")
        finally:
            connection.close()

    @staticmethod
    def delete_pokemon(pokemon_id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "delete from pokemon where id = %s"
                cursor.execute(query, (pokemon_id,))
            connection.commit()
        except Exception as e:
            print(f"Chyba při mazání pokémona: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def get_all_pokemons(connection):
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = "select * from pokemon"
                cursor.execute(query)
                pokemons = cursor.fetchall()
                return pokemons
        except Exception as e:
            print(f"Chyba při načítání pokémonů: {e}")
            return []

    @staticmethod
    def show_pokemons_count(connection):
        with connection.cursor() as cursor:
            cursor.execute("select count(*) from pokemon")
            row = cursor.fetchone()
            print(f"Počet pokémonů: {row[0]}")

    def import_pokemons_from_csv(file_path):
        connection = get_connection()
        try:
            with open(file_path, mode='r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                with connection.cursor() as cursor:
                    for row in reader:
                        trainer_id = int(row['trainer_id']) if row['trainer_id'] else None
                        query = """
                            insert into pokemon (name, type, level, trainer_id) 
                            values (%s, %s, %s, %s)
                        """
                        cursor.execute(query, (row['name'], row['type'], int(row['level']), trainer_id))
                    connection.commit()
                    print("import pokémonů dokončen.")
        except FileNotFoundError:
            print(f"Soubor {file_path} nebyl nalezen.")
        except Exception as e:
            print(f"Chyba při importu pokémonů: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def get_pokemons_by_trainer_id(trainer_id, connection):
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM pokemon WHERE trainer_id = %s FOR SHARE"
                cursor.execute(query, (trainer_id,))
                rows = cursor.fetchall()
                return [Pokemon(**row) for row in rows]
        except Exception as e:
            print(f"Chyba při načítání pokémonů: {e}")
            return []
