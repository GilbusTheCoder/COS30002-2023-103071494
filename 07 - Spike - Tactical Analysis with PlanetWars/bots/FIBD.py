from math import sqrt
from random import choice

# & Project: Tactical Analysis with PlanetWars
# & Author: Thomas Horsley - 103071494
# & Date: 29/03/23

# * IMPORTANT
# * As there's so many comments contained in these files, I'd 110% recommend installing the
# * colorful comments VSCode extension to aid in readability.

#! ======================================================================================== !#
#!                                        Overview

# ^ This bot's named FIBD (First In Best Dressed, pronounced "Fib Dee"), FIBD
# ^ will prioritize colonizing weak planets closest to them. FIBD understands
# ^ when a a planet belongs to the enemy, how many ships are on that planet and
# ^ therefore will attack with a greater force if it can. If not it will inflict
# ^ chip damage.


class FIBD:
    # Summary: If this planet is an enemy then check if we can overwhelm with
    # our planets fleet, if so then attack with force.
    def update(self, gameinfo):
        if gameinfo.my_planets and gameinfo.not_my_planets:
            src = max(gameinfo.my_planets.values(), key=lambda p: p.num_ships)
            dest = self.findClosestPlanet(src, gameinfo.not_my_planets.values())
            gameinfo.planet_order(src, dest, self.determineFleetSize(src, dest))

    # Summary: Determine the distance between source planet and unowned planets
    def determinePlanetDistances(self, src, otherPlanets):
        distList = []
        # ? Calc dist between source planet and other planet
        for planet in otherPlanets:
            distList.append(
                [planet, sqrt((planet.x - src.x) ** 2 + (planet.y - src.y) ** 2)]
            )

        return distList

    # Summary: Take the planet distances, chose the planet associated with the min
    # distance and return it
    def findClosestPlanet(self, src, otherPlanets):
        dest = (None, 200)  # ? Initial value
        validPlanets = []

        for subset in self.determinePlanetDistances(src, otherPlanets):
            if subset[1] <= src.vision_range:  # ? Compare distances
                validPlanets.append(subset[0])

        if not validPlanets:
            for subset in self.determinePlanetDistances(src, otherPlanets):
                if subset[1] <= dest[1]:  # ? Compare distances
                    validPlanets.append(subset[0])

        return choice(validPlanets)

    # Summary: Determine the size of planets fleet and attack with overwhelming
    # force
    def determineFleetSize(self, src, dest):
        if src.num_ships > int(dest.num_ships * 0.9):
            return int(dest.num_ships * 1.1)

        return int(src.num_ships * 0.1)
