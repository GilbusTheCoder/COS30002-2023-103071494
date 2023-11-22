# I'm sure you get alot of classes called Target...
class Kmart:
    def update(self, gameinfo): 
        if gameinfo.my_planets and gameinfo.not_my_planets:
            src = max(gameinfo.my_planets.values(), key=lambda p: p.num_ships)
            dest = min(gameinfo.not_my_planets.values(), key=lambda p: p.num_ships)

            gameinfo.planet_order(src, dest, int(src.num_ships * 0.9))
