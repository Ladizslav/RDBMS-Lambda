from db_connector import get_connection
from trainer import Trainer
import csv

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
    def update_trainer(trainer_id, name, age, team):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                    UPDATE Trainer 
                    SET name = %s, age = %s, team = %s 
                    WHERE trainer_id = %s
                """
                cursor.execute(query, (name, age, team, trainer_id))
            connection.commit()
            print(f"Trenér s ID {trainer_id} byl aktualizován.")
        except Exception as e:
            print(f"Chyba při aktualizaci trenéra: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def delete_trainer(trainer_id):
        connection = get_connection()
        try:
            TrainerDAO.show_trainers_count(connection)
            with connection.cursor() as cursor:
                query = "DELETE FROM Trainer WHERE trainer_id = %s"
                cursor.execute(query, (trainer_id,))
            connection.commit()
            TrainerDAO.show_trainers_count(connection)
        except Exception as e:
            print(f"Chyba při mazání trenéra: {e}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def get_all_trainers():
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM Trainer"
                cursor.execute(query)
                rows = cursor.fetchall()
                return [Trainer(**row) for row in rows]
        except Exception as e:
            print(f"Chyba při načítání trenérů: {e}")
            return []
        finally:
            connection.close()

    @staticmethod
    def show_trainers_count(connection):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Trainer")
                row = cursor.fetchone()
                print(f"Počet trenérů: {row[0]}")
        except Exception as e:
            print(f"Chyba při získávání počtu trenérů: {e}")
            raise

    @staticmethod
    def import_trainers_from_csv(file_path):
        connection = get_connection()
        try:
            with open(file_path, mode='r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                with connection.cursor() as cursor:
                    for row in reader:
                        query = """
                            INSERT INTO Trainer (name, age, team) 
                            VALUES (%s, %s, %s)
                        """
                        cursor.execute(query, (row['name'], int(row['age']), row['team']))
                    connection.commit()
                    print("Import trenérů dokončen.")
        except FileNotFoundError:
            print(f"Soubor {file_path} nebyl nalezen.")
        except Exception as e:
            print(f"Chyba při importu trenérů: {e}")
            connection.rollback()
        finally:
            connection.close()
