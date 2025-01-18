from classes.gym import Gym
from db_connector import get_connection

class GymDAO:
    @staticmethod
    def create_gym(name, city):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "insert into gym (name, city) values (%s, %s)"
                cursor.execute(query, (name, city))
            connection.commit()
        except Exception as e:
            print(f"Chyba při vytváření gymu: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def get_gym_by_id(gym_id):
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = "select * from gym where id = %s"
                cursor.execute(query, (gym_id,))
                row = cursor.fetchone()
                if row:
                    return Gym(**row)
        except Exception as e:
            print(f"Chyba při načítání gymu: {e}")
        finally:
            connection.close()

    @staticmethod
    def delete_gym(gym_id):
        connection = get_connection()
        try:
            GymDAO.show_gyms_count(connection)
            
            with connection.cursor() as cursor:
                query = "delete from gym where id = %s"
                cursor.execute(query, (gym_id,))
            connection.commit()
            GymDAO.show_gyms_count(connection)
            
        except Exception as e:
            print(f"Chyba při mazání gymu: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def show_gyms_count(connection):
        with connection.cursor() as cursor:
            cursor.execute("select count(*) from gym")
            row = cursor.fetchone()
            print(f"Počet gymů: {row[0]}")

    @staticmethod
    def get_all_gyms():
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = "select * from gym"
                cursor.execute(query)
                gyms = cursor.fetchall()
                return gyms
        except Exception as e:
            print(f"Chyba při načítání všech gymů: {e}")
            return []
        finally:
            connection.close()
