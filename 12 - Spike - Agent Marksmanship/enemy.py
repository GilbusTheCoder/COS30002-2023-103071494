from graphics import KEY
from math import sin, cos, radians
from random import randint, random

from vector2d import Vector2D
from world import World
from object import WorldObject
from hitbox import Hitbox


ENEMY_MODES = {KEY._1: "2_point_strafe"}
SPEEDS = {"slow": 0.8, "normal": 1.2, "fast": 1.6}


class Enemy(WorldObject):
    def __init__(self, world: World, pos_x: float, pos_y: float, radius: int):
        WorldObject.__init__(self, pos_x, pos_y, radius)
        self.world = world
        self.wx = world.width
        self.wy = world.height
        self.color: str = "ORANGE"

        # * Physics and movement data
        self.mass = 1
        self.position = Vector2D(pos_x, pos_y)
        self.acceleration = Vector2D()
        self.force = Vector2D()

        initial_heading = radians(random() * 360)
        self.heading = Vector2D(sin(initial_heading), cos(initial_heading))
        self.side = self.heading.perp()

        self.max_speed: int = 150
        self.max_force: int = 200

        self.mode: str = "2_point_strafe"
        self.way_points = {
            0: Vector2D(randint(100, self.wx - 100), randint(100, self.wy - 100)),
            1: Vector2D(randint(100, self.wx - 100), randint(100, self.wy - 100)),
        }
        self.has_arrived: bool = False

    def update(self, delta):
        WorldObject.update(self, delta)

        force = self.calculate_movement()
        force.truncate(self.max_force)
        self.acceleration = force / self.mass

        self.velocity += self.acceleration * delta
        self.velocity.truncate(self.max_speed)

        self.position += self.velocity * delta

        if self.velocity.lengthSq() > 0.00000001:
            self.heading = self.velocity.get_normalised()
            self.side = self.heading.perp()

    def render(self):
        WorldObject.render(self)

    def calculate_movement(self) -> Vector2D:
        mode = self.mode

        if mode == "2_point_strafe":
            target = self.way_points[self.has_arrived]
            self.has_arrived = self.check_has_arrived(target)

            force = self.arrive(target, "normal")
            self.force = force
            return force

        force = Vector2D(0, 0)
        self.force = force
        return

    def seek(self, target: Vector2D):
        desired_vel = (target - self.position).normalise() * self.max_speed
        return desired_vel - self.velocity

    def check_has_arrived(self, target: Vector2D):
        to_target = target - self.position
        dist_to_target = to_target.length()

        if dist_to_target < 5:
            return True
        else:
            return False

    def arrive(self, target: Vector2D, speed):
        deceleration = SPEEDS[speed]
        to_target = target - self.position
        dist_to_target = to_target.length()

        if dist_to_target > 0:
            velocity = dist_to_target / deceleration
            velocity = min(velocity, self.max_speed)

            desired_velocity = to_target * (velocity / dist_to_target)
            return desired_velocity
        return Vector2D(0, 0)
