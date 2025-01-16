class Gym:
    def __init__(self, gym_id, name, city):
        self.gym_id = gym_id
        self.name = name
        self.city = city

    def __repr__(self):
        return f"<Gym(id={self.gym_id}, name='{self.name}', city='{self.city}')>"
