from random import choice


class Rando(object):
    def update(self, gameinfo):
        # ? If we have fleets then we must have planets, also checks that there are unowned planets
        if gameinfo.my_planets and gameinfo.not_my_planets:
            src = choice(list(gameinfo.my_planets.values()))
            dest = choice(list(gameinfo.not_my_planets.values()))

            if src.num_ships > 10:
                gameinfo.planet_order(src, dest, int(src.num_ships * 0.75))
