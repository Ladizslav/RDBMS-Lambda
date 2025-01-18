import datetime
class Trainer:
    def __init__(self, id, name, age, team, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.age = age
        self.team = team
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()

    def __str__(self):
        return f"Trenér(id={self.id}, jméno='{self.name}', věk={self.age}, tým='{self.team}, vytvořeno='{self.created_at}', upraveno='{self.updated_at}')"

