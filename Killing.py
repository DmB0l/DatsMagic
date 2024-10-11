import math


class Killing:

    def is_low_hp(self, enemy, attackDamage):
        if enemy['health'] - attackDamage <= 0:
            return True
        else:
            return False

    def is_have_shield(self, enemy):
        if enemy['shieldLeftMs'] == 0:
            return True
        else:
            return False

    def is_our_not_attack(self, enemy, transports, now_transport, attackExplosionRadius):
        for transport in transports:
            if now_transport != transport:
                transport_x = transport['x']
                transport_y = transport['y']

                enemy_x = enemy['x']
                enemy_y = enemy['y']

                dest = {'x': enemy_x - transport_x, 'y': enemy_y - transport_y}
                length_to_our_transport = math.hypot(dest['x'], dest['y'])

                if length_to_our_transport <= attackExplosionRadius:
                    return 1
        return 2

    def try_to_kill(self, transports, enemies, attackRange, attackExplosionRadius, attackDamage):

        # проверка на то что наши ковры не в зоне атаки
        # если получаем больше, то стреляем и по своим
        # Проверка у кого меньше хп

        command_to_transports = []
        for transport in transports:
            if transport['attackCooldownMs'] == 0:
                transport_x = transport['x']
                transport_y = transport['y']

                near_enemies = []
                for enemy in enemies:
                    enemy_x = enemy['x']
                    enemy_y = enemy['y']

                    dest = {'x': enemy_x - transport_x, 'y': enemy_y - transport_y}
                    length_to_enemy = math.hypot(dest['x'], dest['y'])

                    if length_to_enemy <= attackRange:
                        near_enemies.append(enemy)

                if len(near_enemies) > 0:
                    sorted_enemies = sorted(
                        near_enemies,
                        key=lambda x: (self.is_have_shield(x),
                                       self.is_low_hp(x, attackDamage),
                                       self.is_our_not_attack(x, transports, transport, attackExplosionRadius),
                                       x['killBounty'])
                    )

                    command_to_transports.append(
                        {
                                "x": sorted_enemies[0]['x'],
                                "y": sorted_enemies[0]['y']
                        }
                    )
                else:
                    command_to_transports.append(
                        {
                            "x": 0,
                            "y": 0
                        }
                    )
            else:
                command_to_transports.append(
                    {
                        "x": 0,
                        "y": 0
                    }
                )

        return command_to_transports
