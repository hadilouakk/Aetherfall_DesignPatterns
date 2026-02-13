class QuestState:
    NOT_STARTED = 0
    KEY_FOUND = 1
    BOSS_DEFEATED = 2


class MainQuest:
    def __init__(self):
        self.state = QuestState.NOT_STARTED
        self.has_dungeon_key = False
    
    def advance(self, trigger: str):
        """Fait avancer la quete selon le trigger"""
        if trigger == "key_found" and self.state == QuestState.NOT_STARTED:
            self.state = QuestState.KEY_FOUND
            self.has_dungeon_key = True
        elif trigger == "boss_defeated" and self.state == QuestState.KEY_FOUND:
            self.state = QuestState.BOSS_DEFEATED
    
    def can_enter_dungeon(self) -> bool:
        return self.has_dungeon_key
    
    def is_completed(self) -> bool:
        return self.state == QuestState.BOSS_DEFEATED
    
    def get_objective(self) -> str:
        """Retourne l objectif actuel"""
        if self.state == QuestState.NOT_STARTED:
            return "Explorez la Forêt pour trouver la Clé du Donjon"
        elif self.state == QuestState.KEY_FOUND:
            return "Rendez-vous au Donjon et affrontez le Gardien"
        else:
            return "Quête terminée ! Vous avez vaincu le Gardien du Donjon !"
    
    def to_dict(self):
        return {
            "state": self.state,
            "has_dungeon_key": self.has_dungeon_key
        }
    
    @classmethod
    def from_dict(cls, data):
        q = cls()
        q.state = data.get("state", 0)
        q.has_dungeon_key = data.get("has_dungeon_key", False)
        return q
