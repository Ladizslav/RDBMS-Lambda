from db_connector import get_connection
from pokemon import Pokemon

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
            with connection.cursor() as cursor:
                query = "DELETE FROM Pokemon WHERE pokemon_id = %s"
                cursor.execute(query, (pokemon_id,))
            connection.commit()
        except Exception as e:
            print(f"Chyba při mazání Pokémona: {e}")
            connection.rollback()
        finally:
            connection.close()
