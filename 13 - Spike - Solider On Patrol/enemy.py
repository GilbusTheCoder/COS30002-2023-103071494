from graphics import KEY
from math import sin, cos, radians
from random import randint, random

from vector2d import Vector2D
from world import World
from object import WorldObject


ENEMY_MODES = {KEY._1: "2_point_strafe"}


class Enemy(WorldObject):
    def __init__(self, world: World, pos_x: float, pos_y: float, radius: int):
        WorldObject.__init__(self, pos_x, pos_y, radius)
        self.world = world
        self.wx = world.width
        self.wy = world.height

        self.color: str = "ORANGE"

        # * Physics and movement data
        self.mass = 1

        initial_heading = radians(random() * 360)
        self.dir = Vector2D(sin(initial_heading), cos(initial_heading))
        self.side = self.dir.perp()

        self.max_speed: int = 150
        self.max_force: int = 200

        self.mode: str = "2_point_strafe"
        self.way_points = [
            Vector2D(randint(100, self.wx - 100), randint(100, self.wy - 100)),
            Vector2D(randint(100, self.wx - 100), randint(100, self.wy - 100)),
        ]
        self.has_arrived: bool = False

    def update(self, delta):
        force = self.calculate_force()
        force.truncate(self.max_force)
        self.acceleration = force / self.mass

        self.velocity += self.acceleration * delta
        self.velocity.truncate(self.max_speed)

        self.position += self.velocity * delta

        if self.velocity.lengthSq() > 0.00000001:
            self.dir = self.velocity.get_normalised()
            self.side = self.dir.perp()

        self.hitbox.update(self)

    def render(self):
        WorldObject.render(self)

    def calculate_force(self) -> Vector2D:
        mode = self.mode

        if mode == "2_point_strafe":
            target = self.way_points[self.has_arrived]
            self.has_arrived = WorldObject.check_has_arrived(self, target)

            force = WorldObject.arrive(self, target, "normal")
            self.force = force
            return force

        force = Vector2D(0, 0)
        self.force = force
        return force
