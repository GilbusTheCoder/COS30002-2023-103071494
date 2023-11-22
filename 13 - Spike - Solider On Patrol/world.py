from object import WorldObject
from matrix33 import Matrix33


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

    # Cheers Clinton!
    def transform_points(self, points, pos, forward, side, scale):
        wld_pts = [pt.copy() for pt in points]
        mat = Matrix33()
        mat.scale_update(scale.x, scale.y)
        mat.rotate_by_vectors_update(forward, side)
        mat.translate_update(pos.x, pos.y)
        mat.transform_vector2d_list(wld_pts)
        return wld_pts

    def transform_point(self, point, pos, forward, side):
        wld_point = point.copy()
        matrix = Matrix33()
        matrix.rotate_by_vectors_update(forward, side)
        matrix.translate_update(pos.x, pos.y)
        matrix.transform_vector2d(wld_point)
        return wld_point
