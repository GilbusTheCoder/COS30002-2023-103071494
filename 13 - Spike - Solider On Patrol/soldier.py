from time import time
from math import cos, sin, radians
from random import random, randint, uniform
from graphics import egi, KEY
from vector2d import Vector2D
from random import choice

from world import World
from object import WorldObject, SPEEDS
from enemy import Enemy
from gun_stuff import *

WEAPONS = {
    KEY.NUM_1: "ak47",
    KEY.NUM_2: "grenade",
    KEY.NUM_3: "deagle",
    KEY.NUM_4: "rocket",
}

# HACK: A better solution would be to use a combination of integers to specify
# which state the player is in. E.g. 0, 0 = Patrol, wander. 1, 2 = attack, fallback
# much more concise but i got 2 jobs and this is easier
MACRO_STATES = [
    "patrol",
    "attack",
]

ATTACK_STATES = [
    "shoot",
    "reload",
    "fall_back",
]

PATROL_STATES = {KEY.W: "wander", KEY.P: "point_patrol"}


# Look. I know i can hold all the weapon data in a multi-dimensional array. I just cant be
# arsed. Please forgive my transgressions.
class Soldier(WorldObject):
    time_between_shots = {
        "ak47": 0.3,
        "grenade": 5.0,
        "deagle": 0.8,
        "rocket": 3.0,
    }

    bullets_per_mag = {
        "ak47": 30,
        "grenade": 3,  # ? 3 total nades for the soldier
        "deagle": 7,
        "rocket": 2,
    }

    reload_time = {
        "ak47": 1,
        "grenade": 2,
        "deagle": 0.8,
        "rocket": 10,
    }

    def __init__(self, world: World, pos_x: float, pos_y: float, radius: int):
        WorldObject.__init__(self, pos_x, pos_y, radius)
        self.world = world
        self.wx = world.width
        self.wy = world.height

        self.time = time()
        self.color = "BLUE"

        # * Combat details
        self.can_fire = True
        self.has_bullets = True
        self.off_cooldown = True
        self.weapon = "deagle"
        self.prev_shot_time = self.time - Soldier.time_between_shots[self.weapon]
        self.bullets_shot_this_mag = 0

        # * Sight and memory
        self.macro_state = "patrol"
        self.micro_state = "point_patrol"

        self.vision_radius = 200
        self.seen_enemies = []
        self.target = None
        self.enemy_count_before_panic: int = 4
        self.is_panicked = False

        # * Movement & Wander data
        self.allow_state_selection: bool = True

        self.mass = 1
        self.max_speed = 150
        self.max_force = 200

        initial_heading = radians(random() * 360)
        self.dir = Vector2D(sin(initial_heading), cos(initial_heading))
        self.side = self.dir.perp()

        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 1.0 * radius
        self.wander_radius = 1.0 * radius
        self.wander_jitter = 10.0 * radius
        self.wander_bRadius = radius

        self.wnd_pos = Vector2D(self.wander_dist, 0)
        self.wld_pos = self.world.transform_point(
            self.wnd_pos, self.position, self.dir, self.side
        )

        self.patrol_points = [
            Vector2D(randint(50, self.wx - 50), randint(50, self.wy - 50)),
            Vector2D(randint(50, self.wx - 50), randint(50, self.wy - 50)),
            Vector2D(randint(50, self.wx - 50), randint(50, self.wy - 50)),
            Vector2D(randint(50, self.wx - 50), randint(50, self.wy - 50)),
        ]
        self.point_index: int = 0
        self.patrol_point_threshold: float = 50.0
        self.has_arrived: bool = False

    def update(self, delta):
        self.time = time()
        self.seen_enemies = self.search_enemies_in_range()
        self.target = self.pick_target()
        self.macro_state = self.check_macro_state()
        self.micro_state = self.check_micro_state()

        self.take_action()

        force = self.calculate_force(delta)
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

        if self.show_info:
            egi.green_pen()
            egi.circle(self.position, self.vision_radius)

    #! ----- Movement & state control

    # Summary: Returns a force vector relative to the current state of the
    # soldier.
    #
    # Though the macro state check isn't required it remains for
    # as redundancy.
    def calculate_force(self, delta) -> Vector2D:
        # ? Patrol Macro State
        if self.macro_state == "patrol":
            if self.micro_state == "wander":
                force = self.wander(delta)
                self.force = force
                return force
            if self.micro_state == "point_patrol":
                force = self.patrol("normal")
                self.force = force
                return force

        # ? Attack macro state
        if self.macro_state == "attack":
            target = self.pick_target()
            if self.micro_state == "shoot":
                force = WorldObject.seek(self, target.position)
                self.force = force
                return force
            if self.micro_state == "fall_back":
                force = self.flee(target.position)
                self.force = force
                return force
            if self.micro_state == "reload":
                force = Vector2D(0, 0)
                self.force = force
                return force

        force = Vector2D(0, 0)
        self.force = force
        return force

    def take_action(self):
        if self.macro_state == "attack":
            if self.micro_state == "reload":
                self.reload()
            elif self.micro_state == "fall_back":
                self.shoot(self.target.position)
            else:
                self.shoot(self.target.position)

    def check_macro_state(self) -> str:
        if len(self.seen_enemies) >= 1:
            self.allow_state_selection = False
            return "attack"
        else:
            self.allow_state_selection = True
            return "patrol"

    def check_micro_state(self):
        if self.macro_state == "attack":
            self.is_panicked = self.check_panic()
            self.has_bullets != self.check_need_reload()
            self.off_cooldown = self.check_weapon_off_cooldown()
            self.can_fire = self.can_shoot()

            if self.is_panicked:
                return "fall_back"
            elif not self.has_bullets:
                return "reload"
            else:
                return "shoot"

        if self.macro_state == "patrol":
            return self.micro_state

    # Summary: The soldiers substate will not be user controlled. This method
    # returns the attacking substate based on the world state.
    def check_attack_substate(self):
        if not self.has_bullets:
            return "reload"

    # Summary: Returns true if there are too many enemies around the soldier
    def check_panic(self) -> bool:
        return len(self.seen_enemies) >= self.enemy_count_before_panic

    # Summary: Returns true if the soldier needs a reload
    def check_need_reload(self) -> bool:
        return self.bullets_shot_this_mag >= self.bullets_per_mag[self.weapon]

    # Summary: Returns true if the weapon is off cooldown and false if otherwise
    def check_weapon_off_cooldown(self) -> bool:
        if self.time - self.prev_shot_time >= Soldier.time_between_shots[self.weapon]:
            self.prev_shot_time = self.time
            return True
        return False

    # Summary: Will return true if the soldier doesn't need to reload and isn't
    # panicked.
    def can_shoot(self) -> bool:
        return self.has_bullets and not self.is_panicked and self.off_cooldown

    def wander(self, delta):
        wander_target = self.wander_target
        jitter = self.wander_jitter * delta

        wander_target += Vector2D(uniform(-1, 1) * jitter, uniform(-1, 1) * jitter)
        wander_target.normalise()
        wander_target *= self.wander_radius
        target = wander_target + Vector2D(self.wander_dist, 0)
        wt = self.world.transform_point(target, self.position, self.dir, self.side)

        return WorldObject.seek(self, wt)

    def patrol(self, speed):
        deceleration = SPEEDS[speed]

        target = self.patrol_points[self.point_index]
        to_target = target - self.position
        dist_to_target = to_target.length()

        if WorldObject.check_has_arrived(self, target):
            speed = dist_to_target / deceleration
            speed = min(speed, self.max_speed)
            velocity = to_target * (speed / dist_to_target)
            self.increment_point_index()

            return velocity - self.velocity

        if dist_to_target > self.patrol_point_threshold:
            velocity = (
                self.patrol_points[self.point_index] - self.position
            ).normalise() * self.max_speed
            return velocity - self.velocity

    def increment_point_index(self):
        self.point_index += 1

        if self.point_index >= len(self.patrol_points):
            self.point_index = 0

    def flee(self, target: Vector2D):
        to_target = target - self.position
        dist_to_target = to_target.length()
        if self.is_panicked:
            speed = self.max_speed
            velocity = -1 * to_target * (speed / dist_to_target)
            return velocity

        return Vector2D(0, 0)

    #! ----- Enemy tracking & target selection

    def search_enemies_in_range(self) -> list:
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
            target = choice(self.seen_enemies)
            self.target = target
            return target

        return None

    def check_object_in_range(self, object: WorldObject):
        if (object.position - self.position).lengthSq() < (
            self.vision_radius * self.vision_radius
        ):
            return True
        return False

    #! ----- Gun Stuff
    def shoot(self, target: Vector2D):
        weapon = self.weapon

        if self.off_cooldown:
            if weapon == "ak47":
                projectile = Rifle_Round(
                    self.position.x,
                    self.position.y,
                    5,
                    target,
                    Vector2D(1, 1),
                    self.world,
                )
                self.world.append_obj(projectile)
                self.bullets_shot_this_mag += 1

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
                self.bullets_shot_this_mag += 1

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
                self.bullets_shot_this_mag += 1

            elif weapon == "rocket":
                projectile = Rocket(
                    self.position.x,
                    self.position.y,
                    8,
                    target,
                    Vector2D(1, 1),
                    self.world,
                )
                self.world.append_obj(projectile)
                self.bullets_shot_this_mag += 1

    def reload(self):
        self.bullets_shot_this_mag = 0
