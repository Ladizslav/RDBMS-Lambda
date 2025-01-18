class PokemonStats:
    def __init__(self, id, pokemon_id, speed, strength, defense, is_alive=True):
        self.id = id
        self.pokemon_id = pokemon_id
        self.speed = speed
        self.strength = strength
        self.defense = defense
        self.is_alive = is_alive  

    def __str__(self):
        return f"Statistiky Pokémona: ID: {self.id}, Pokémon ID: {self.pokemon_id}, Rychlost: {self.speed}, Síla: {self.strength}, Obrana: {self.defense}, Je živý: {self.is_alive}"
