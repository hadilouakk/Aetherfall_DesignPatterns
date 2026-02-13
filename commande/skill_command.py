from commande.commands import Command

class SkillCommand(Command):
    def __init__(self, skill, caster, target):
        self.skill = skill
        self.caster = caster
        self.target = target

    def execute (self, ctx) -> None: 
        self.skill.use (self.caster, self.target, ctx)