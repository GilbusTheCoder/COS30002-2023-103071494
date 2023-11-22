from time import time
from math import sqrt
from vector2d import Vector2D

from world import World
from object import WorldObject
from hitbox import Hitbox
from enemy import Enemy


class Projectile(WorldObject):
    def __init__(
        self,
        pos_x: float,
        pos_y: float,
        radius: int,
        target: Vector2D,
        range_modifier: Vector2D,
        world: World,
    ):
        WorldObject.__init__(self, pos_x, pos_y, radius)
        self.world = world
        self.spawn_time = time()
        self.life_span_seconds = 5
        self.color = "YELLOW"

        self.spawn_position = Vector2D(pos_x, pos_y)
        self.position = Vector2D(pos_x, pos_y)
        self.target = target
        self.target_position = self.target * range_modifier

        self.dir = (self.target - self.position).normalise()
        self.mass: float = 1.0
        self.velocity = Vector2D()
        self.force = Vector2D()

        self.max_speed: int = 400
        self.max_force: int = 500

        self.force = self.seek(self.target)
        self.force.truncate(self.max_force)
        self.acceleration = self.force / self.mass

        self.hitbox = Hitbox(self.position, radius)
        self.show_info = False

    def update(self, delta):
        self.check_time_despawn()
        self.murder_check()

        WorldObject.update(self, delta)

    def render(self):
        WorldObject.render(self)

    def murder_check(self):
        if type(self) == Rifle_Round:
            for object in self.world.objects:
                if type(object) == Enemy:
                    if self.hit_enemy(object):
                        self.world.remove_obj(self)
                        self.world.remove_obj(object)

        if type(self) == Pistol_Round:
            for object in self.world.objects:
                if type(object) == Enemy:
                    if self.hit_enemy(object):
                        self.world.remove_obj(self)
                        self.world.remove_obj(object)

        elif type(self) == Grenade or type(self) == Rocket:
            for object in self.world.objects:
                if type(object) == Enemy and self.has_detonated:
                    if self.hit_enemy(object):
                        self.world.remove_obj(object)

    def hit_enemy(self, object: Enemy) -> bool:
        target_dist = sqrt(object.position.distanceSq(self.position))

        # ? If the circles intersect or touch
        if target_dist <= (self.radius + object.radius):
            return True
        # ? If the circles are inside on-another
        elif target_dist <= (self.radius - object.radius) or target_dist <= (
            object.radius - self.radius
        ):
            return True
        else:
            return False

    # BUG: Grenade detonation not deleting themselves after detonation_length
    def check_time_despawn(self) -> bool:
        now = time()
        if type(self) == Rifle_Round:
            return now - self.spawn_time > self.life_span_seconds
        elif type(self) == Grenade:
            return now - self.detonation_time > self.detonation_length_seconds
        elif type(self) == Pistol_Round:
            return now - self.spawn_time > self.life_span_seconds

    def seek(self, target: Vector2D) -> Vector2D:
        desired_velocity = (target - self.position).normalise() * self.max_speed
        return desired_velocity - self.velocity


class Rifle_Round(Projectile):
    def __init__(
        self,
        pos_x: float,
        pos_y: float,
        radius: int,
        target: Enemy,
        range_modifier: Vector2D,
        world: World,
    ):
        Projectile.__init__(self, pos_x, pos_y, radius, target, range_modifier, world)
        self.color = "YELLOW"

    def update(self, delta):
        Projectile.update(self, delta)

    def render(self):
        WorldObject.render(self)


class Pistol_Round(Projectile):
    def __init__(
        self,
        pos_x: float,
        pos_y: float,
        radius: int,
        target: Enemy,
        range_modifier: Vector2D,
        world: World,
    ):
        Projectile.__init__(
            self,
            pos_x,
            pos_y,
            radius,
            target,
            range_modifier,
            world,
        )
        self.color = "AQUA"

        self.max_speed = 150
        self.max_force = 250

    def update(self, delta):
        Projectile.update(self, delta)

    def render(self):
        WorldObject.render(self)


class Grenade(Projectile):
    def __init__(
        self,
        pos_x: float,
        pos_y: float,
        radius: int,
        target: Enemy,
        range_modifier: Vector2D,
        world: World,
    ):
        Projectile.__init__(self, pos_x, pos_y, radius, target, range_modifier, world)
        self.max_speed = 50
        self.max_force = 150
        self.color = "GREEN"

        self.has_detonated = False
        self.detonation_time = self.spawn_time * 1000  # ? filler value
        self.detonation_radius = 50
        self.detonation_timer = 4
        self.detonation_length_seconds = 1

    def update(self, delta):
        if self.check_detonate() and not self.has_detonated:
            self.has_detonated = True
            self.detonation_time = time()
            self.radius = self.detonation_radius
            self.color = "RED"

        Projectile.update(self, delta)

    def render(self):
        WorldObject.render(self)

    def check_detonate(self) -> bool:
        now = time()
        return now - self.spawn_time > self.detonation_timer


class Rocket(Projectile):
    def __init__(
        self,
        pos_x: float,
        pos_y: float,
        radius: int,
        target: Enemy,
        range_modifier: Vector2D,
        world: World,
    ):
        Projectile.__init__(self, pos_x, pos_y, radius, target, range_modifier, world)
        self.color = "WHITE"

        self.max_speed = 100
        self.max_force = 150

        self.has_detonated = False
        self.detonation_time = self.spawn_time * 1000  # ? filler value
        self.detonation_radius = 150
        self.detonation_timer = 4
        self.detonation_length = 1

    def update(self, delta):
        if self.check_detonate() and not self.has_detonated:
            self.has_detonated = True
            self.detonation_time = time()
            self.radius = self.detonation_radius
            self.color = "RED"

        Projectile.update(self, delta)

    def render(self):
        WorldObject.render(self)

    def check_detonate(self) -> bool:
        now = time()
        return now - self.spawn_time > self.detonation_timer
