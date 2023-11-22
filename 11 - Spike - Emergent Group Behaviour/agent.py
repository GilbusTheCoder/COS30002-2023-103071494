"""An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

"""

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform


AGENT_MODES = {
    KEY._1: "seek",
    KEY._2: "arrive_slow",
    KEY._3: "arrive_normal",
    KEY._4: "arrive_fast",
    KEY._5: "wander",
}


class Agent(object):
    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {"slow": 0.9, "normal": 1.2, "fast": 1.5}

    def __init__(self, world=None, scale=10.0, mass=0.3, mode="wander"):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        # where am i and where am i going? random start pos
        dir = radians(random() * 360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()  # current steering force
        self.accel = Vector2D()  # current acceleration due to force
        self.mass = mass

        # data for drawing this agent
        self.color = "ORANGE"
        self.vehicle_shape = [
            Point2D(-1.0, 0.6),
            Point2D(1.0, 0.0),
            Point2D(-1.0, -0.6),
        ]
        # limits?
        self.max_speed = 30.0 * scale
        self.max_waypoints: int = 8
        self.max_force = 500

        # Group behaviour data
        self.neighbours = []
        self.vision_rad = 10 * scale
        self.alignment_scale = 1
        self.cohesion_scale = 3
        self.separation_scale = 5
        self.wander_scale = 3

        ### wander details
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = self.vision_rad
        self.wander_jitter = 10.0 * scale

        # debug draw info?
        self.show_info = False

    def calculate(self, delta):
        mode = self.mode
        if mode == "seek":
            force = self.seek(self.world.target)
        elif mode == "arrive_slow":
            force = self.arrive(self.world.target, "slow")
        elif mode == "arrive_normal":
            force = self.arrive(self.world.target, "normal")
        elif mode == "arrive_fast":
            force = self.arrive(self.world.target, "fast")
        elif mode == "wander":
            self.neighbours = self.get_neighbours()
            if len(self.neighbours) > 0:
                force = self.group_wander(self.neighbours, delta)
            else:
                force = self.wander(delta)
        else:
            force = Vector2D()

        self.force = force
        return force

    def update(self, delta):
        """update vehicle position and orientation"""
        force = self.calculate(delta)
        force.truncate(self.max_force)
        self.accel = force / self.mass

        # new velocity
        self.vel += self.accel * delta
        self.vel.truncate(self.max_speed)

        # update position
        self.pos += self.vel * delta

        # update heading is non-zero velocity (moving)
        if self.vel.lengthSq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()

        self.world.wrap_around(self.pos)

    def render(self, color=None):
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(
            self.vehicle_shape, self.pos, self.heading, self.side, self.scale
        )
        # draw it!
        egi.closed_shape(pts)

        if self.show_info:
            s = 0.5

            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)

            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)

            egi.white_pen()
            egi.line_with_arrow(
                self.pos + self.vel * s, self.pos + (self.force + self.vel) * s, 5
            )
            egi.line_with_arrow(self.pos, self.pos + (self.force + self.vel) * s, 5)

            if self.mode == "wander":
                wnd_pos = Vector2D(self.wander_dist, 0)
                wld_pos = self.world.transform_point(
                    wnd_pos, self.pos, self.heading, self.side
                )
                egi.green_pen()
                egi.circle(wld_pos, self.wander_radius)
                egi.red_pen()

                wnd_pos = self.wander_target + Vector2D(self.wander_dist, 0)
                wld_pos = self.world.transform_point(
                    wnd_pos, self.pos, self.heading, self.side
                )
                egi.circle(wld_pos, 3)

                egi.aqua_pen()
                egi.circle(wld_pos, self.vision_rad)

    def speed(self):
        return self.vel.length()

    #! --------------------------------------------------------------------------

    def get_neighbours(self):
        return list(
            filter(
                lambda agent: agent != self
                and (agent.pos - self.pos).lengthSq()
                < self.vision_rad * self.vision_rad,
                self.world.agents,
            )
        )

    def calc_alignment(self, neighbours: list):
        group_alignment = Vector2D(0, 0)
        neighbour_count = len(neighbours)

        for agent in neighbours:
            group_alignment += agent.heading

        if neighbour_count > 0:
            group_alignment /= neighbour_count
            alignment = group_alignment.normalise() * self.max_speed
            return alignment
        else:
            return Vector2D(0, 0)

    def calc_cohesion(self, neighbours: list):
        centre = Vector2D(0, 0)
        neighbour_count = len(neighbours)

        for agent in neighbours:
            centre += agent.pos

        if neighbour_count > 0:
            centre /= neighbour_count
            cohesion_target = centre.normalise()
            return self.seek(cohesion_target) * self.max_speed
        else:
            return Vector2D(0, 0)

    def calc_separation(self, neighbours: list):
        group_separation = Vector2D(0, 0)
        for agent in neighbours:
            to_agent = self.pos - agent.pos
            group_separation += to_agent.normalise() / to_agent.length()

        return group_separation * self.max_speed

    def group_wander(self, neighbours: list, delta):
        group_movement = Vector2D(0, 0)
        separation = self.calc_separation(neighbours) * self.separation_scale
        cohesion = self.calc_cohesion(neighbours) * self.cohesion_scale
        alignment = self.calc_alignment(neighbours) * self.alignment_scale

        group_movement = separation + cohesion + alignment

        movement = group_movement + (self.wander(delta) * self.wander_scale)
        movement.truncate(self.max_speed)
        return movement

    #! --------------------------------------------------------------------------

    def seek(self, target_pos):
        """move towards target position"""
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return desired_vel - self.vel

    def arrive(self, target_pos, speed):
        """this behaviour is similar to seek() but it attempts to arrive at
        the target position with a zero velocity"""
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist > 0:
            # calculate the speed required to reach the target given the
            # desired deceleration rate
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max
            speed = min(speed, self.max_speed)
            # from here proceed just like Seek except we don't need to
            # normalize the to_target vector because we have already gone to the
            # trouble of calculating its length for dist.
            desired_vel = to_target * (speed / dist)
            return desired_vel - self.vel
        return Vector2D(0, 0)

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
