from gym import Gym
from db_connector import get_connection

class GymDAO:
    @staticmethod
    def create_gym(name, city):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO Gym (name, city) VALUES (%s, %s)"
                cursor.execute(query, (name, city))
            connection.commit()
        except Exception as e:
            print(f"Chyba při vytváření Gymu: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def get_gym_by_id(gym_id):
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM Gym WHERE gym_id = %s"
                cursor.execute(query, (gym_id,))
                row = cursor.fetchone()
                if row:
                    return Gym(**row)
        except Exception as e:
            print(f"Chyba při načítání Gymu: {e}")
        finally:
            connection.close()

    @staticmethod
    def delete_gym(gym_id):
        connection = get_connection()
        try:
            GymDAO.show_gyms_count(connection)
            
            with connection.cursor() as cursor:
                query = "DELETE FROM Gym WHERE gym_id = %s"
                cursor.execute(query, (gym_id,))
            connection.commit()
            GymDAO.show_gyms_count(connection)
            
        except Exception as e:
            print(f"Chyba při mazání Gymu: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def show_gyms_count(connection):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Gym")
            row = cursor.fetchone()
            print(f"Počet gymů: {row[0]}")

    @staticmethod
    def get_all_gyms():
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM Gym"
                cursor.execute(query)
                gyms = cursor.fetchall()
                return gyms
        except Exception as e:
            print(f"Chyba při načítání všech gymů: {e}")
            return []
        finally:
            connection.close()
