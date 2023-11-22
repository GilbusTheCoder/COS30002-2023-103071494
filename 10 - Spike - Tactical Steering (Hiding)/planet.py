from vector2d import Vector2D
from point2d import Point2D
from graphics import egi
from random import uniform, randrange
from math import sqrt

# & Project: Task 10 - Spike - Tactical Steering (Hiding)
# & Author: Thomas Horsley - 103071494
# & Last Edit: 27/04/23

#! ======================================================================================== !#
#!                                        Overview

# * IMPORTANT
# * As there's so many comments contained in these files, I'd 110% recommend installing the
# * colorful comments VSCode extension to aid in readability.

# HACK: Stepping away from hitboxes for the moment and trying to use raycasts to
#       simulate hiding behaviour


# ^ Hitbox class for easier planet collision detection
class Hitbox:
    def __init__(self, origin: Vector2D, radius: float):
        self.ox = float(origin.x)
        self.oy = float(origin.y)

        self.corners = [
            self.ox - radius,  # Left
            self.oy + radius,  # Top
            self.ox + radius,  # Right
            self.oy - radius,  # Bottom
        ]

    def render(self):
        egi.white_pen()
        egi.rect(
            left=self.corners[0],
            top=self.corners[1],
            right=self.corners[2],
            bottom=self.corners[3],
        )

    # Summary: If my top right coordinate is less than the other
    #          boxes top left and vice versa then collision has occurred.
    def is_collision(self, other) -> bool:
        if (
            self.corners[2] > other.corners[0]
            and self.corners[1] > other.corners[3]
            and self.corners[2] < other.corners[2]
            and self.corners[1] < other.corners[1]
        ):
            return True
        elif (
            self.corners[1] > other.corners[3]
            and self.corners[0] < other.corners[2]
            and self.corners[1] < other.corners[1]
            and self.corners[0] > other.corners[0]
        ):
            return True
        elif (
            self.corners[3] < other.corners[1]
            and self.corners[0] < other.corners[2]
            and self.corners[3] > other.corners[3]
            and self.corners[0] > other.corners[0]
        ):
            return True
        elif (
            self.corners[3] < other.corners[1]
            and self.corners[2] > other.corners[0]
            and self.corners[3] > other.corners[3]
            and self.corners[2] < other.corners[2]
        ):
            return True
        else:
            return False


# ^ Simple planet instance, planets will be drawn when the world is initialized
# ^ will probably end up using the origin and radius for collision detection
class Planet:
    def __init__(self, x, y):
        self.show_info = False

        self.origin = Vector2D(randrange(0, x), randrange(0, y))
        self.radius: float = None
        self.hidden_radius: float = None
        self.build_planet(40, 100)

        self.hitbox = Hitbox(self.origin, self.radius)

    # This update function assumes the hunter is the first ship in the list
    def update(self, world):
        pass

    def build_planet(self, min_radius, max_radius):
        self.radius = uniform(min_radius, max_radius)
        self.hidden_radius = self.radius + (0.4 * self.radius)

    def render(self):
        egi.blue_pen()
        egi.circle(self.origin, self.radius)

        if self.show_info:
            self.render_details()

    def render_details(self):
        egi.aqua_pen()
        egi.circle(self.origin, self.hidden_radius)

        self.hitbox.render()
