from db_connector import get_connection
from pokemonstats import PokemonStats

class PokemonStatsDAO:
    @staticmethod
    def create_stats(pokemon_id, speed, strength, defense):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                INSERT INTO PokemonStats (pokemon_id, speed, strength, defense)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (pokemon_id, speed, strength, defense))
            connection.commit()
        except Exception as e:
            print(f"Chyba při vytváření statistik Pokémona: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def get_stats_by_pokemon_id(pokemon_id):
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM PokemonStats WHERE pokemon_id = %s"
                cursor.execute(query, (pokemon_id,))
                row = cursor.fetchone()
                if row:
                    return PokemonStats(**row)
        except Exception as e:
            print(f"Chyba při načítání statistik Pokémona: {e}")
        finally:
            connection.close()

    @staticmethod
    def delete_stats(pokemon_id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "DELETE FROM PokemonStats WHERE pokemon_id = %s"
                cursor.execute(query, (pokemon_id,))
            connection.commit()
        except Exception as e:
            print(f"Chyba při mazání statistik Pokémona: {e}")
            connection.rollback()
        finally:
            connection.close()
