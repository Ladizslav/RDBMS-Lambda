class Pokemon:
    def __init__(self, pokemon_id, name, type, level, trainer_id=None):
        self.pokemon_id = pokemon_id
        self.name = name
        self.type = type
        self.level = level
        self.trainer_id = trainer_id

    def __repr__(self):
        return f"<Pokemon(id={self.pokemon_id}, name='{self.name}', type='{self.type}', level={self.level}, trainer_id={self.trainer_id})>"
