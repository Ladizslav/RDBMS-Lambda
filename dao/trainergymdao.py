from db.db_connector import get_connection

class TrainerGymDAO:
    @staticmethod
    def assign_trainer_to_gym(trainer_id, gym_id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "insert into trainer_gym (trainer_id, gym_id) values (%s, %s)"
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
                select gym.id, gym.name, gym.city
                from trainer_gym
                join gym on trainer_gym.gym_id = gym.id
                where trainer_gym.trainer_id = %s
                """
                cursor.execute(query, (trainer_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Chyba při načítání gymů pro trenéra: {e}")
        finally:
            connection.close()

    @staticmethod
    def unassign_trainer_from_gym(trainer_id, gym_id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "delete from trainer_gym where trainer_id = %s and gym_id = %s"
                cursor.execute(query, (trainer_id, gym_id))
            connection.commit()
        except Exception as e:
            print(f"Chyba při odpojení trenéra: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def get_gyms_for_trainer_by_gym_id(gym_id):
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                select trainer_gym.trainer_id, trainer_gym.gym_id, trainer.name as trainer_name, gym.name as gym_name
                from trainer_gym
                join trainer on trainer_gym.trainer_id = trainer.id
                join gym on trainer_gym.gym_id = gym.id
                where trainer_gym.gym_id = %s
                """
                cursor.execute(query, (gym_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Chyba při načítání trenérů: {e}")
        finally:
            connection.close()

    @staticmethod
    def get_all_trainers_and_gyms():
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                select trainer.id as trainer_id, trainer.name as trainer_name, gym.id as gym_id, gym.name as gym_name, gym.city
                from trainer
                left join trainer_gym on trainer.id = trainer_gym.trainer_id
                left join gym on trainer_gym.gym_id = gym.id
                """
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Chyba při načítání trenérů a gymů: {e}")
        finally:
            connection.close()
