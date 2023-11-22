from vector2d import Vector2D
from graphics import egi
from hitbox import Hitbox


class WorldObject:
    def __init__(self, pos_x: float, pos_y: float, radius: int):
        # ? Defaults
        self.radius = radius
        self.world = None
        self.color = "ORANGE"

        self.position = Vector2D(pos_x, pos_y)
        self.velocity = Vector2D(0, 0)
        self.max_speed = 100

        self.hitbox = Hitbox(self.position, self.radius)
        self.show_info = False

    def update(self, delta):
        self.hitbox.update(self)

    def render(self):
        egi.set_pen_color(name=self.color)
        egi.circle(self.position, self.radius)

        if self.show_info:
            scale = 0.5

            egi.red_pen()
            egi.line_with_arrow(self.position, self.position + self.velocity * scale, 5)

            self.hitbox.set_visible()
