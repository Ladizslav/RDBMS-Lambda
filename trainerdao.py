from db_connector import get_connection
from trainer import Trainer

class TrainerDAO:
    @staticmethod
    def create_trainer(name, age, team):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO Trainer (name, age, team) VALUES (%s, %s, %s)"
                cursor.execute(query, (name, age, team))
            connection.commit()
        except Exception as e:
            print(f"Chyba při vytváření trenéra: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def get_trainer_by_id(trainer_id):
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM Trainer WHERE trainer_id = %s"
                cursor.execute(query, (trainer_id,))
                row = cursor.fetchone()
                if row:
                    return Trainer(**row)
        except Exception as e:
            print(f"Chyba při načítání trenéra: {e}")
        finally:
            connection.close()

    @staticmethod
    def delete_trainer(trainer_id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "DELETE FROM Trainer WHERE trainer_id = %s"
                cursor.execute(query, (trainer_id,))
            connection.commit()
        except Exception as e:
            print(f"Chyba při mazání trenéra: {e}")
            connection.rollback()
        finally:
            connection.close()
