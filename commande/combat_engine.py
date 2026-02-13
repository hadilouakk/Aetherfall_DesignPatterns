from commande.commands import AttackCommand

class CombatEngine:
    def run(self, ctx, player_command_provider):
        ctx.bus.publish("log", " Début du combat !")

        while ctx.player.is_alive() and ctx.enemy.is_alive():
            ctx.bus.publish("log", f"--- Tour {ctx.turn} ---")

            
            p_cmd = player_command_provider(ctx)
            p_cmd.execute(ctx)

            if not ctx.enemy.is_alive():
                ctx.bus.publish("log", f" {ctx.enemy.name} est vaincu !")
                break

            
            e_cmd = ctx.enemy.decide(ctx)
            e_cmd.execute(ctx)

            if not ctx.player.is_alive():
                ctx.bus.publish("log", f" {ctx.player.name} est vaincu !")
                ctx.player.reset_defense()
                ctx.enemy.reset_defense()
                
                break

            ctx.player.apply_end_turn_statuses(ctx)
            ctx.enemy.apply_end_turn_statuses(ctx)


            ##ctx.player.reset_defense()
            ##ctx.enemy.reset_defense()

            ctx.turn += 1
            