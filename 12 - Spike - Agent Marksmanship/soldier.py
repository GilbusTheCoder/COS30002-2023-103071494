from time import time
from graphics import egi, KEY
from vector2d import Vector2D
from random import choice

from world import World
from object import WorldObject
from enemy import Enemy
from gun_stuff import *

WEAPONS = {
    KEY._1: "ak47",
    KEY._2: "grenade",
    KEY._3: "deagle",
    KEY._4: "rocket",
}


class Soldier(WorldObject):
    time_between_shots = {
        "ak47": 0.3,
        "grenade": 5.0,
        "deagle": 0.8,
        "rocket": 6.5,
    }

    def __init__(self, world: World, pos_x: float, pos_y: float, radius: int):
        WorldObject.__init__(self, pos_x, pos_y, radius)
        self.time = time()
        self.world = world
        self.seen_enemies = []

        self.color = "BLUE"
        self.vision_radius = 200

        self.weapon = "grenade"
        self.prev_shot_time = self.time - Soldier.time_between_shots[self.weapon]
        self.can_fire = True

    def update(self, delta):
        self.time = time()
        self.seen_enemies = self.find_enemies()

        self.can_fire = self.can_shoot()

        if self.can_fire:
            target = self.pick_target()
            if type(target) == Enemy:
                self.shoot(target)

        WorldObject.update(self, delta)

    def render(self):
        WorldObject.render(self)

        if self.show_info:
            egi.green_pen()
            egi.circle(self.position, self.vision_radius)

    def can_shoot(self) -> bool:
        if (
            self.time - self.prev_shot_time >= Soldier.time_between_shots[self.weapon]
            and self.seen_enemies
        ):
            self.prev_shot_time = self.time
            return True
        return False

    def find_enemies(self) -> list:
        enemies = []

        for object in list(
            filter(
                lambda world_object: isinstance(world_object, Enemy),
                self.world.objects,
            )
        ):
            if self.check_object_in_range(object):
                enemies.append(object)

        return enemies

    def pick_target(self) -> Enemy:
        if len(self.seen_enemies) > 0:
            return choice(self.seen_enemies)

        return None

    def check_object_in_range(self, object: WorldObject):
        if (object.position - self.position).lengthSq() < (
            self.vision_radius * self.vision_radius
        ):
            return True
        return False

    def shoot(self, target: Vector2D):
        weapon = self.weapon
        if weapon == "ak47":
            projectile = Rifle_Round(
                self.position.x, self.position.y, 5, target, Vector2D(1, 1), self.world
            )
            self.world.append_obj(projectile)

        elif weapon == "grenade":
            projectile = Grenade(
                self.position.x,
                self.position.y,
                6,
                target,
                Vector2D(uniform(0.5, 1.5), uniform(0.5, 1.5)),
                self.world,
            )
            self.world.append_obj(projectile)

        elif weapon == "deagle":
            projectile = Pistol_Round(
                self.position.x,
                self.position.y,
                3,
                target,
                Vector2D(uniform(0.8, 1.2), uniform(0.8, 1.2)),
                self.world,
            )
            self.world.append_obj(projectile)

        elif weapon == "rocket":
            projectile = Rocket(
                self.position.x, self.position.y, 8, target, Vector2D(1, 1), self.world
            )
            self.world.append_obj(projectile)
