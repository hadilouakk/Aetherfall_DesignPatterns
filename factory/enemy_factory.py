from strategy.enemy import Wolf, Skeleton,Bandit

class EnemyFactory:
    @staticmethod
    def create (enemy_type:str):
        mapping = {
            "wolf": Wolf,
            "skelton":Skeleton,
            "bandit":Bandit,

        }
        if enemy_type not in mapping:
            raise ValueError(f"Enemmi inconnue de type : {enemy_type}")
        return mapping [enemy_type]()
    