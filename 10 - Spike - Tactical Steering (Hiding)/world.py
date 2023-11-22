"""A 2d world that supports agents with steering behaviour

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publicly share or post this code without permission.

"""

from vector2d import Vector2D
from matrix33 import Matrix33
from planet import Planet

from graphics import egi
from random import uniform
from math import cos, sin, atan


class World(object):
    def __init__(self, cx, cy):
        self.cy = cy
        self.cx = cx

        self.agents = []
        self.hunter = None
        self.planets = self.build_planets()
        self.hidden_positions = []

        self.paused = False
        self.show_info = False
        self.target = Vector2D(cx / 2, cy / 2)

    def update(self, delta):
        if not self.paused:
            for agent in self.agents:
                if agent is self.agents[0]:
                    agent.update(delta)
                    self.hidden_positions = self.find_hidden_pos(self.agents[0], delta)
                else:
                    agent.update(delta)

    def render(self):
        for agent in self.agents:
            agent.render()

        for planet in self.planets:
            planet.render()

        if self.target:
            egi.red_pen()
            egi.cross(self.target, 10)

        if self.show_info:
            infotext = ", ".join(set(agent.mode for agent in self.agents))
            egi.white_pen()
            egi.text_at_pos(0, 0, infotext)

            egi.red_pen()
            for pos in self.hidden_positions:
                egi.cross(pos, 10)

    def build_planets(self) -> list:
        planets = []
        planets.append(Planet(self.cx, self.cy))

        planet_count = int(uniform(3, 5))
        max_planets = 11

        while planet_count < max_planets:
            new_planet = Planet(self.cx, self.cy)
            planets.append(new_planet)
            planet_count += 1

        for subject_planet in planets:
            for comparison_planet in planets:
                if subject_planet.hitbox.is_collision(comparison_planet.hitbox):
                    planets.remove(subject_planet)

        return planets

    # Summary: Returns a list of positions where the agents can seek to
    #          stay hidden from the hunter

    #          Notes: The hunter will always be agents[0] for this example
    #                 If you want to see the working for the calculations,
    #                 a pdf can be found in the submissions directory
    def find_hidden_pos(self, hunter, delta):
        hidden_positions = []

        for planet in self.planets:
            to_planet = Vector2D(
                planet.origin.x - hunter.pos.x,
                planet.origin.y - hunter.pos.y,
            )
            theta = atan(to_planet.x / to_planet.y)

            hidden_pos = Vector2D(
                hunter.pos.x + to_planet.x - (planet.hidden_radius * sin(theta)),
                hunter.pos.y + to_planet.y - (planet.hidden_radius * cos(theta)),
            )

            hidden_positions.append(hidden_pos)

        return hidden_positions

    def wrap_around(self, pos):
        """Treat world as a toroidal space. Updates parameter object pos"""
        max_x, max_y = self.cx, self.cy
        if pos.x > max_x:
            pos.x = pos.x - max_x
        elif pos.x < 0:
            pos.x = max_x - pos.x
        if pos.y > max_y:
            pos.y = pos.y - max_y
        elif pos.y < 0:
            pos.y = max_y - pos.y

    def transform_points(self, points, pos, forward, side, scale):
        """Transform the given list of points, using the provided position,
        direction and scale, to object world space."""
        # make a copy of original points (so we don't trash them)
        wld_pts = [pt.copy() for pt in points]
        # create a transformation matrix to perform the operations
        mat = Matrix33()
        # scale,
        mat.scale_update(scale.x, scale.y)
        # rotate
        mat.rotate_by_vectors_update(forward, side)
        # and translate
        mat.translate_update(pos.x, pos.y)
        # now transform all the points (vertices)
        mat.transform_vector2d_list(wld_pts)
        # done
        return wld_pts

    def transform_point(self, point, pos, forward, side):
        wld_point = point.copy()
        matrix = Matrix33()
        matrix.rotate_by_vectors_update(forward, side)
        matrix.translate_update(pos.x, pos.y)
        matrix.transform_vector2d(wld_point)
        return wld_point
