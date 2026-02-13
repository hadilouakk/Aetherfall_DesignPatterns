from abc import ABC, abstractmethod

class StatusEffect(ABC):
    def __init__(self, duration_turns: int):
        self.duration_turns = duration_turns

    @abstractmethod
    def on_end_turn(self, target, ctx):
        ...

    def tick(self):
        self.duration_turns -= 1

    def is_expired(self) -> bool:
        return self.duration_turns <= 0


class Poison(StatusEffect):
    def __init__(self, duration_turns: int, dmg_per_turn: int):
        super().__init__(duration_turns)
        self.dmg_per_turn = dmg_per_turn

    def on_end_turn(self, target, ctx):
        target.take_damage(self.dmg_per_turn)
        ctx.bus.publish("log", f" {target.name} subit {self.dmg_per_turn} dégâts de poison.")