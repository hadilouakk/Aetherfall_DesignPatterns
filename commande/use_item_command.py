from commande.commands import Command


class UseItemCommand(Command):
    def __init__(self, consumable, user, target, inventory):
        self.consumable = consumable
        self.user = user
        self.target = target
        self.inventory = inventory
    
    def execute(self, ctx) -> None:
        self.inventory.use_consumable(self.consumable, self.user, self.target, ctx)
