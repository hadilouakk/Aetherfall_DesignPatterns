from strategy.status_effects import StatusEffect


class Shield(StatusEffect):
    def __init__(self, duration_turns: int, shield_amount: int):
        super().__init__(duration_turns)
        self.shield_amount = shield_amount
    
    def absorb(self, damage: int) -> int:
        """Absorbe les degats et renvoie les degats restants"""
        absorbed = min(self.shield_amount, damage)
        self.shield_amount -= absorbed
        remaining = damage - absorbed
        if self.shield_amount <= 0:
            self.duration_turns = 0  # bouclier brisé
        return remaining
    
    def on_end_turn(self, target, ctx):
        # le bouclier ne fait rien en fin de tour, il absorbe au moment de l impact
        if self.shield_amount > 0:
            ctx.bus.publish("log", f"  Bouclier actif sur {target.name} ({self.shield_amount} pts restants)")
