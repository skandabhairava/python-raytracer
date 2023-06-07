class V3:
    def __init__(self, x, y, z) -> None:
        self.x: float|int = x
        self.y: float|int = y
        self.z: float|int = z

    def __add__(self, other: 'V3') -> 'V3':
        return V3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'V3') -> 'V3':
        return V3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, num: float|int) -> 'V3':
        return V3(self.x * num, self.y * num, self.z * num)
    
    def __truediv__(self, other: 'V3') -> 'V3':
        return V3(self.x / other.x, self.y / other.y, self.z / other.z)


class Color(V3):

    def __init__(self, x, y, z) -> None:
        self.x: int = x
        self.y: int = y
        self.z: int = z

    @classmethod
    def from_hex(cls, hex: str) -> 'Color':
        return Color(*(int(hex[i:i+2], 16) for i in (0, 2, 4)))
    
    def __add__(self, other: 'Color') -> 'Color':
        return Color(min(max(self.x + other.x, 0), 255), min(max(self.y + other.y, 0), 255), min(max(self.z + other.z, 0), 255))
    
    def __sub__(self, other: 'Color') -> 'Color':
        return Color(min(max(self.x - other.x, 0), 255), min(max(self.y - other.y, 0), 255), min(max(self.z - other.z, 0), 255))
    
    def __mul__(self, num: int|float) -> 'Color':
        assert 0 <= num <= 1, "colors can only be multiplied with numbers >= 0 and <= 1"
        return Color(min(max(int(self.x * num), 0), 255), min(max(int(self.y * num), 0), 255), min(max(int(self.z * num), 0), 255))
    
    def __repr__(self) -> str:
        return f"R{self.x} - G{self.y} - B{self.z}"

class Vector(V3):
    def __init__(self, i: float|int, j: float|int, k: float|int) -> None:
        self.x: float|int = i
        self.y: float|int = j
        self.z: float|int = k

    def magnitude(self) -> float:
        return ((self.x)**2 + (self.y)**2 + (self.z)**2)**(1/2)
    
    def normalize(self, magnitude=None) -> 'Vector':
        magnitude_ = self.magnitude() if magnitude is None else magnitude
        return Vector(self.x/magnitude_, self.y/magnitude_, self.z/magnitude_)
    
    def __repr__(self) -> str:
        return f"x: {self.x} | y: {self.y} | z: {self.z}"
    
    def __add__(self, other: 'Vector|int') -> 'Vector':
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        return Vector(self.x + other, self.y + other, self.z + other)
    
    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other: float|int) -> 'Vector':
        return Vector(self.x * other, self.y * other, self.z * other)
    
    def __rmul__(self, num: float|int) -> 'Vector':
        return Vector(self.x * num, self.y * num, self.z * num)
    
    def __truediv__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x / other.x, self.y / other.y, self.z / other.z)
    
    def dot(self, other: 'Vector') -> float:
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)
    
    def cross(self, other: 'Vector') -> 'Vector':
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
class Line:
    def __init__(self, origin: Vector, dir: Vector) -> None:
        self.origin: Vector = origin
        self.dir: Vector = dir.normalize()

    def __repr__(self) -> str:
        return f"Origin: ({self.origin}), Dir: ({self.dir})"

class Object3D:
    def __init__(self, origin: Vector, normal: Vector) -> None:
        self.origin: Vector = origin
        self.normal: Vector = normal.normalize()