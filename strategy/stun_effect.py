from strategy.status_effects import StatusEffect


class Stun(StatusEffect):
    def __init__(self):
        super().__init__(duration_turns=1)
        self.applied = False
    
    def should_skip_turn(self) -> bool:
        """Retourne True si la cible doit passer son tour"""
        return not self.applied
    
    def on_end_turn(self, target, ctx):
        if not self.applied:
            ctx.bus.publish("log", f" {target.name} est étourdi et passe son tour !")
            self.applied = True
        self.duration_turns = 0  # expire apres 1 tour
