class PokemonStats:
    def __init__(self, stats_id, pokemon_id, speed, strength, defense):
        self.stats_id = stats_id
        self.pokemon_id = pokemon_id
        self.speed = speed
        self.strength = strength
        self.defense = defense

    def __repr__(self):
        return f"<PokemonStats(id={self.stats_id}, pokemon_id={self.pokemon_id}, speed={self.speed}, strength={self.strength}, defense={self.defense})>"
