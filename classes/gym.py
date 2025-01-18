class Gym:
    def __init__(self, id, name, city):
        self.id = id
        self.name = name
        self.city = city

    def __str__(self):
        return f"Gym(id={self.id}, název='{self.name}', město='{self.city}')"