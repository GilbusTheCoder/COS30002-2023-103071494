from vector2d import Vector2D
from graphics import egi
from hitbox import Hitbox


SPEEDS = {"slow": 0.8, "normal": 1.2, "fast": 1.6}


class WorldObject:
    def __init__(self, pos_x: float, pos_y: float, radius: int):
        # ? Defaults
        self.world = None
        self.color = "ORANGE"

        self.radius = radius
        self.mass: float

        self.position = Vector2D(pos_x, pos_y)
        self.dir = Vector2D()
        self.side = Vector2D()
        self.velocity = Vector2D()
        self.acceleration = Vector2D()
        self.force = Vector2D()

        self.max_speed: int
        self.max_force: int

        self.hitbox = Hitbox(self.position, self.radius)
        self.show_info: bool = False

    def update(self, delta):
        self.velocity += self.acceleration * delta
        self.velocity.truncate(self.max_speed)

        self.position += self.velocity * delta

        if self.velocity.lengthSq() > 0.00000001:
            self.dir = self.velocity.get_normalised()
            self.side = self.dir.perp()

        self.hitbox.update(self)

    def render(self):
        egi.set_pen_color(name=self.color)
        egi.circle(self.position, self.radius)

        if self.show_info:
            scale = 0.5

            egi.red_pen()
            egi.line_with_arrow(self.position, self.position + self.velocity * scale, 5)

            self.hitbox.set_visible()

    def seek(self, target: Vector2D):
        desired_vel = (target - self.position).normalise() * self.max_speed
        return desired_vel - self.velocity

    def check_has_arrived(self, target: Vector2D):
        to_target = target - self.position
        dist_to_target = to_target.length()

        if dist_to_target < 100:
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
