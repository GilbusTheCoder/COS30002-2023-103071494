"""An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

"""

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path
from planet import Hitbox

AGENT_MODES = {
    KEY._1: "seek",
    KEY._2: "arrive_slow",
    KEY._3: "arrive_normal",
    KEY._4: "arrive_fast",
    KEY._5: "flee",
    KEY._6: "pursuit",
    KEY._7: "follow_path",
    KEY._8: "wander",
    None: "hunt",
}

# Agents can only receive orders in a calm state
AGENT_STATES = ["neutral", "panicked"]


class Agent(object):
    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {"slow": 0.9, "normal": 1.2, "fast": 1.5}

    def __init__(self, world=None, scale=30.0, mass=1.0, mode="wander"):
        ### keep a reference to the world object
        self.world = world
        self.state = "neutral"
        self.mode = mode

        ### where am i and where am i going? random start pos
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        dir = radians(random() * 360)
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.is_collision = False

        self.mass = mass
        self.vel = Vector2D()
        self.accel = Vector2D()  # current acceleration due to force
        self.force = Vector2D()  # current steering force

        ### data for drawing this agent
        self.scale = Vector2D(scale, scale)
        self.color = "ORANGE"
        self.vehicle_shape = [
            Point2D(-1.0, 0.6),
            Point2D(1.0, 0.0),
            Point2D(-1.0, -0.6),
        ]
        ### limits?
        self.max_speed = 10.0 * scale
        self.max_force = 500

        ### path to follow?
        self.max_waypoints: int = 8
        self.waypoint_threshold = 100.0
        self.path = Path()
        self.randomize_path()

        ### wander details
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = 1.0 * scale
        self.wander_jitter = 10.0 * scale
        self.wander_bRadius = scale
        self.wnd_pos = Vector2D(self.wander_dist, 0)
        self.wld_pos = self.world.transform_point(
            self.wnd_pos, self.pos, self.heading, self.side
        )

        self.hunter = None
        self.panic_distance = 500
        self.hidden_threshold = 50.0
        self.hitbox = Hitbox(self.wld_pos, self.wander_radius)
        self.hiding_spot = None

        ### debug draw info?
        self.show_info = False

    def randomize_path(self):
        cx = self.world.cx
        cy = self.world.cy
        margin = min(cx, cy)

        self.path.create_random_path(
            num_pts=4,
            minx=margin,
            miny=margin,
            maxx=cx,
            maxy=cy,
            looped=True,
        )

    def calculate(self, delta):
        if self.state == "neutral":
            mode = self.mode
            if mode == "seek":
                force = self.seek(self.world.target)
            elif mode == "arrive_slow":
                force = self.arrive(self.world.target, "slow")
            elif mode == "arrive_normal":
                force = self.arrive(self.world.target, "normal")
            elif mode == "arrive_fast":
                force = self.arrive(self.world.target, "fast")
            elif mode == "pursuit":
                force = self.pursuit(self.world.hunter)
            elif mode == "wander":
                force = self.wander(delta)
            elif mode == "follow_path":
                force = self.follow_path("normal")
            elif mode == "hunt":
                force = self.hunt(delta)
            else:
                force = Vector2D()
            self.force = force
            return force

        elif self.state == "panicked":
            self.hiding_spot = self.find_hiding_pos(self.world.hidden_positions)
            force = self.hide()
            self.force = force
            return force

    # Summary: Calculates the force which needs to be applied to the agent each
    #          tick.
    def update(self, delta):
        """update vehicle position and orientation"""
        self.hunter = self.world.agents[0]

        if self is not self.hunter:
            if self.is_panicked():
                self.state = "panicked"

            if self.hiding_spot:
                if self.is_hidden():
                    self.state = "neutral"

        self.wnd_pos = Vector2D(self.wander_dist, 0)
        self.wld_pos = self.world.transform_point(
            self.wnd_pos, self.pos, self.heading, self.side
        )
        self.hitbox = Hitbox(self.wld_pos, self.wander_radius)

        for planet in self.world.planets:
            self.is_collision = self.hitbox.is_collision(planet.hitbox)

        force = self.calculate(delta)
        force.truncate(self.max_force)

        self.accel = force / self.mass  # ? Redundant if mass = 1
        self.vel += self.accel * delta
        self.vel.truncate(self.max_speed)  # ? check for limits of new vel

        self.pos += self.vel * delta

        if self.vel.lengthSq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()

        self.world.wrap_around(self.pos)  # ? Toroidal world-space

    def render(self, color=None):
        if self.state == "neutral":
            egi.set_pen_color(name=self.color)
        elif self.state == "panicked":
            egi.set_pen_color(name="RED")

        pts = self.world.transform_points(
            self.vehicle_shape, self.pos, self.heading, self.side, self.scale
        )
        egi.closed_shape(pts)

        if self.show_info:
            self.hitbox.render()

            # ? Draw wander circle
            egi.green_pen()
            egi.circle(self.wld_pos, self.wander_radius)

            # ? Draw jitter circle
            egi.red_pen()
            wnd_pos = self.wander_target + Vector2D(self.wander_dist, 0)
            self.wld_pos = self.world.transform_point(
                wnd_pos, self.pos, self.heading, self.side
            )
            egi.circle(self.wld_pos, 3)

            s = 0.5  # <-- scaling factor

            # force
            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)

            # velocity
            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)

            # net (desired) change
            egi.white_pen()
            egi.line_with_arrow(
                self.pos + self.vel * s, self.pos + (self.force + self.vel) * s, 5
            )
            egi.line_with_arrow(self.pos, self.pos + (self.force + self.vel) * s, 5)

            # Show hunter radius
            if self is self.hunter:
                egi.aqua_pen()
                egi.circle(self.pos, self.panic_distance)

    def speed(self):
        return self.vel.length()

    # -------------------------------------------------------------------------
    # Summary: The agent will calculate the closest hiding spot before arriving
    #          at those coordinates.
    def hide(self):
        return self.arrive(self.hiding_spot, "fast")

    def find_hiding_pos(self, positions: list):
        furthest_dist = 10.0  # ? <-- filler dist

        for position in positions:
            to_pos = position - self.hunter.pos
            dist_to_pos = to_pos.length()

            if dist_to_pos > furthest_dist:
                furthest_dist = dist_to_pos
                hidden_pos = position

        return hidden_pos

    def follow_path(self, speed):
        target_pos = self.path.current_pt()
        to_target = target_pos - self.pos
        dist_to_target = to_target.length()
        deceleration = self.DECELERATION_SPEEDS[speed]

        if self.path.is_finished():
            speed = dist_to_target / deceleration
            speed = min(speed, self.max_speed)
            velocity = to_target * (speed / dist_to_target)
            return velocity - self.vel

        if dist_to_target > self.waypoint_threshold:
            self.path.inc_current_pt()
            velocity = (self.path.current_pt() - self.pos).normalise() * self.max_speed
            return velocity - self.vel

        return Vector2D(0, 0)

    def seek(self, target_pos) -> bool:
        """move towards target position"""
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return desired_vel - self.vel

    def is_panicked(self):
        to_hunter = Vector2D(
            self.hunter.pos.x - self.pos.x, self.hunter.pos.y - self.pos.y
        )
        dist_to_hunter = to_hunter.length()

        if dist_to_hunter < self.panic_distance:
            return True
        else:
            return False

    def is_hidden(self):
        to_hiding = self.hiding_spot - self.pos
        dist = to_hiding.length()

        if dist < self.hidden_threshold and not self.is_panicked():
            return True
        else:
            return False

    def arrive(self, target_pos, speed):
        """this behaviour is similar to seek() but it attempts to arrive at
        the target position with a zero velocity"""
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()

        if dist > 0:
            speed = dist / decel_rate
            speed = min(speed, self.max_speed)
            desired_vel = to_target * (speed / dist)
            return desired_vel - self.vel

        return Vector2D(0, 0)

    def pursuit(self, evader):
        """this behaviour predicts where an agent will be in time T and seeks
        towards that point to intercept it."""
        ## OPTIONAL EXTRA... pursuit (you'll need something to pursue!)
        return Vector2D()

    def wander(self, delta):
        """Random wandering using a projected jitter circle."""
        wander_target = self.wander_target
        jitter = self.wander_jitter * delta

        wander_target += Vector2D(uniform(-1, 1) * jitter, uniform(-1, 1) * jitter)
        wander_target.normalise()
        wander_target *= self.wander_radius
        target = wander_target + Vector2D(self.wander_dist, 0)
        wt = self.world.transform_point(target, self.pos, self.heading, self.side)

        return self.seek(wt)

    # TODO: This will be pursuit later, this is temp
    def hunt(self, delta):
        """Random wandering using a projected jitter circle."""
        wander_target = self.wander_target
        jitter = self.wander_jitter * delta

        wander_target += Vector2D(uniform(-1, 1) * jitter, uniform(-1, 1) * jitter)
        wander_target.normalise()
        wander_target *= self.wander_radius
        target = wander_target + Vector2D(self.wander_dist, 0)
        wt = self.world.transform_point(target, self.pos, self.heading, self.side)

        return self.seek(wt)
