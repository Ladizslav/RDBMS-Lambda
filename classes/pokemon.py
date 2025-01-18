import datetime
class Pokemon:
    def __init__(self, id, name, type, level, trainer_id=None,created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.type = type
        self.level = level
        self.trainer_id = trainer_id
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()

    def __str__(self):
        return f"Pokémon(id={self.id}, jméno='{self.name}', typ='{self.type}', úroveň={self.level}, trenér_id={self.trainer_id}, vytvořeno='{self.created_at}', upraveno='{self.updated_at}')"
