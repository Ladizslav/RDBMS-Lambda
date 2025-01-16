class TrainerGym:
    def __init__(self, trainer_id, gym_id):
        self.trainer_id = trainer_id
        self.gym_id = gym_id

    def __repr__(self):
        return f"<TrainerGym(trainer_id={self.trainer_id}, gym_id={self.gym_id})>"
