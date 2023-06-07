from units import Color, Object3D

class Scene:
    def __init__(self, objects: list[Object3D], background_color: str, ambient_lighting: float = 1) -> None:
        assert 0 <= ambient_lighting <= 1, "lighting can only be numbers >= 0 and <= 1"
        self.objects: list[Object3D] = objects
        self.background_color: Color = Color(*(int(background_color[i:i+2], 16) for i in (0, 2, 4)))
        self.ambient_lighting: float = ambient_lighting

    def add_obj(self, obj: Object3D):
        self.objects.append(obj)


