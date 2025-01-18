from db.db_connector import get_connection
from classes.trainer import Trainer
import csv

class TrainerDAO:
    @staticmethod
    def create_trainer(name, age, team):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "insert into trainer (name, age, team) values (%s, %s, %s)"
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
                query = "select * from trainer where id = %s"
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
                    update trainer 
                    set name = %s, age = %s, team = %s 
                    where id = %s
                """
                cursor.execute(query, (name, age, team, trainer_id))
            connection.commit()
            print(f"Trenér s id {trainer_id} byl aktualizován.")
        except Exception as e:
            print(f"Chyba při aktualizaci trenéra: {e}")
            connection.rollback()
        finally:
            connection.close()


    @staticmethod
    def delete_trainer(trainer_id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "delete from trainer where id = %s"
                cursor.execute(query, (trainer_id,))
            connection.commit()
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
                query = "select * from trainer"
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
                cursor.execute("select count(*) from trainer")
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
                            insert into trainer (name, age, team) 
                            values (%s, %s, %s)
                        """
                        cursor.execute(query, (row['name'], int(row['age']), row['team']))
                    connection.commit()
                    print("Import trenérů dokončen.")
        except FileNotFoundError:
            print(f"Soubor {file_path} nebyl nalezen.")
        except Exception as e:
            print(f"Chyba při importu: {e}")
            connection.rollback()
        finally:
            connection.close()
