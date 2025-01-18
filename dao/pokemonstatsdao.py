from db.db_connector import get_connection
from classes.pokemonstats import PokemonStats

class PokemonStatsDAO:
    @staticmethod
    def create_stats(pokemon_id, speed, strength, defense):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                insert into pokemon_stats (pokemon_id, speed, strength, defense)
                values (%s, %s, %s, %s)
                """
                cursor.execute(query, (pokemon_id, speed, strength, defense))
            connection.commit()
        except Exception as e:
            print(f"Chyba při vytváření statistik pokémona: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def get_stats_by_pokemon_id(pokemon_id):
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = "select * from pokemon_stats where pokemon_id = %s"
                cursor.execute(query, (pokemon_id,))
                row = cursor.fetchone()
                if row:
                    return PokemonStats(**row)
        except Exception as e:
            print(f"Chyba při načítání statistik pokémona: {e}")
        finally:
            connection.close()

    @staticmethod
    def delete_stats(pokemon_id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "delete from pokemon_stats where pokemon_id = %s"
                cursor.execute(query, (pokemon_id,))
            connection.commit()
        except Exception as e:
            print(f"Chyba při mazání statistik pokémona: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def defeat_pokemon(pokemon_id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "update pokemon_stats set is_alive = %s where pokemon_id = %s"
                cursor.execute(query, (False, pokemon_id))  
            connection.commit()
        except Exception as e:
            print(f"Chyba při porážce pokémona: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def revive_pokemon(pokemon_id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "update pokemon_stats set is_alive = %s where pokemon_id = %s"
                cursor.execute(query, (True, pokemon_id))
            connection.commit()
            print(f"Pokémon ID {pokemon_id} byl oživen.")
        except Exception as e:
            print(f"Chyba při oživení Pokémona ID {pokemon_id}: {e}")
            connection.rollback()
        finally:
            connection.close()