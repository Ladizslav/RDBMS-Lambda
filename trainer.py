class Trainer:
    def __init__(self, trainer_id, name, age, team):
        self.trainer_id = trainer_id
        self.name = name
        self.age = age
        self.team = team

    def __repr__(self):
        return f"<Trainer(id={self.trainer_id}, name='{self.name}', age={self.age}, team='{self.team}')>"
