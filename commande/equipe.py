from commande.commands import Command

class EquipWeaponCommand(Command):
    def __init__(self, player, weapon):
        self.player = player
        self.weapon = weapon

    def execute(self, ctx) -> None:
        self.player.equip_weapon(self.weapon)
        ctx.bus.publish("log", f"🗡 {self.player.name} équipe : {self.weapon.name}")