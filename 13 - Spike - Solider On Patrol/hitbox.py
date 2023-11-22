from vector2d import Vector2D
from graphics import egi


class Hitbox:
    def __init__(self, origin: Vector2D, radius: float):
        self.origin = origin
        self.radius = radius

        self.corners = [
            self.origin.x - self.radius,  # Left
            self.origin.y + self.radius,  # Top
            self.origin.x + self.radius,  # Right
            self.origin.y - self.radius,  # Bottom
        ]

    def update(self, parent):
        self.origin = parent.position

        self.corners = [
            self.origin.x - self.radius,  # Left
            self.origin.y + self.radius,  # Top
            self.origin.x + self.radius,  # Right
            self.origin.y - self.radius,  # Bottom
        ]

    def set_visible(self):
        egi.white_pen()
        egi.rect(
            left=self.corners[0],
            top=self.corners[1],
            right=self.corners[2],
            bottom=self.corners[3],
        )

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
        elif (
            self.corners[0] > other.corners[0]
            and self.corners[1] < other.corners[1]
            and self.corners[2] < other.corners[2]
            and self.corners[3] > other.corners[3]
        ):
            return True
        else:
            return False
