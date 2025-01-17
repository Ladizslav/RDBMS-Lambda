from db_connector import get_connection

class TrainerGymDAO:
    @staticmethod
    def assign_trainer_to_gym(trainer_id, gym_id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO trainer_gym (trainer_id, gym_id) VALUES (%s, %s)"
                cursor.execute(query, (trainer_id, gym_id))
            connection.commit()
        except Exception as e:
            print(f"Chyba při přiřazení trenéra ke gymu: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def get_gyms_for_trainer(trainer_id):
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT g.gym_id, g.name, g.city
                FROM trainer_gym tg
                JOIN Gym g ON tg.gym_id = g.gym_id
                WHERE tg.trainer_id = %s
                """
                cursor.execute(query, (trainer_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Chyba při načítání Gymů pro trenéra: {e}")
        finally:
            connection.close()

    @staticmethod
    def unassign_trainer_from_gym(trainer_id, gym_id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "DELETE FROM trainer_gym WHERE trainer_id = %s AND gym_id = %s"
                cursor.execute(query, (trainer_id, gym_id))
            connection.commit()
        except Exception as e:
            print(f"Chyba při odpojení trenéra od gymu: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def get_gyms_for_trainer_by_gym_id(gym_id):
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT tg.trainer_id, tg.gym_id, t.name AS trainer_name, g.name AS gym_name
                FROM Trainer_Gym tg
                JOIN Trainer t ON tg.trainer_id = t.trainer_id
                JOIN Gym g ON tg.gym_id = g.gym_id
                WHERE tg.gym_id = %s
                """
                cursor.execute(query, (gym_id,))
                return cursor.fetchall() 
        except Exception as e:
            print(f"Chyba při načítání trenérů pro gym: {e}")
        finally:
            connection.close()

    @staticmethod
    def get_all_trainers_and_gyms():
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT t.trainer_id, t.name AS trainer_name, g.gym_id, g.name AS gym_name, g.city
                FROM Trainer t
                LEFT JOIN Trainer_Gym tg ON t.trainer_id = tg.trainer_id
                LEFT JOIN Gym g ON tg.gym_id = g.gym_id
                """
                cursor.execute(query)
                return cursor.fetchall() 
        except Exception as e:
            print(f"Chyba při načítání všech trenérů a gymů: {e}")
        finally:
            connection.close()