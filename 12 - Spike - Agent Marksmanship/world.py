from vector2d import Vector2D
from graphics import egi
from object import WorldObject


class World:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.objects = []
        self.paused = True
        self.show_info = False

    def update(self, delta):
        for object in self.objects:
            object.update(delta)

    def render(self):
        for object in self.objects:
            object.render()

    def append_obj(self, object: WorldObject):
        self.objects.append(object)
        object.world = self

    def remove_obj(self, object: WorldObject):
        self.objects.remove(object)
