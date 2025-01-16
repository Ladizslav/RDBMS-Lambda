from db_connector import get_connection

class TrainerGymDAO:
    @staticmethod
    def assign_trainer_to_gym(trainer_id, gym_id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO TrainerGym (trainer_id, gym_id) VALUES (%s, %s)"
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
                FROM TrainerGym tg
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
                query = "DELETE FROM TrainerGym WHERE trainer_id = %s AND gym_id = %s"
                cursor.execute(query, (trainer_id, gym_id))
            connection.commit()
        except Exception as e:
            print(f"Chyba při odpojení trenéra od gymu: {e}")
            connection.rollback()
        finally:
            connection.close()
