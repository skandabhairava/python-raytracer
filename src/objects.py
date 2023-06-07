from units import Vector, Object3D, Line, Color
from scene import Scene
from PIL import Image
from PIL.Image import Image as ImageObj
from multiprocess import pool
from multiprocessing.pool import ThreadPool
from typing import Callable
import math

###################################################################
##                          OBJECTS
###################################################################

class PointLighting(Object3D):
    def __init__(self, origin: Vector, normal: Vector, strength: int|float) -> None:
        super().__init__(origin, normal)
        assert 0 <= strength <= 1, "lighting strength can only be numbers >= 0 and <= 1"
        self.strength = strength

class Sphere(Object3D):
    def __init__(self, origin: Vector, normal: Vector, color: Color, radius: int|float) -> None:
        super().__init__(origin, normal)
        self.color: Color = color
        self.radius: int|float = radius

    def intersection(self, line: Line, scene: Scene, calc_brightness: bool=True, detailed = False) -> tuple[bool, Vector, Color]:

        # a = line.dir.dot(line.dir)
        # return False, Vector(0, 0, 0), Color(0, 0, 0)
        #calc shortest distance between line and center of sphere        

        µ = line.dir.x**2 + line.dir.y**2 + line.dir.z**2
        if µ == 0: return False, Vector(0, 0, 0), Color(0, 0, 0)
        λ = - (line.dir.x*(line.origin.x - self.origin.x) + line.dir.y*(line.origin.y - self.origin.y) + line.dir.z*(line.origin.z - self.origin.z)) / µ

        point = Vector(line.origin.x + line.dir.x*λ, line.origin.y + line.dir.y*λ, line.origin.z + line.dir.z*λ)
        dist = (point-self.origin).magnitude()

        #check if shortest dist is <= radius of sphere, if yes => it intersects
        if dist < self.radius:
            # find intersection point vec
            x: float = math.sqrt((self.radius**2 - dist**2))
            KP = (point - line.origin) #point is where the ray is closest to the sphere
            intersection_to_point = KP.normalize() * x

            line_origin_to_intersection = KP - intersection_to_point

            intersection_point = line.origin + line_origin_to_intersection
            point_int_to_ray_org = (-1 * line_origin_to_intersection)
            int_normal = (intersection_point - self.origin).normalize()

            if line.dir.dot(line_origin_to_intersection) <= 0: #doesnt intersect if intersection point is behind origin->dir
                return False, Vector(0, 0, 0), Color(0, 0, 0)

            total_brightness = scene.ambient_lighting
            if not calc_brightness: return True, intersection_point, self.color*(total_brightness)

            for obj in scene.objects:
                if total_brightness >= 1:
                    break

                if isinstance(obj, PointLighting):
                    point_int_to_light_vec = (obj.origin - intersection_point)
                    #check if this is blocked by another obj
                    if point__:=Camera.ray_intersect_nearest_obj(scene, Line(intersection_point, point_int_to_light_vec), non_cam_origin=self.origin):
                        if detailed:
                            print(f"obj: {self.color}, 2nd reflection: {point__, Line(intersection_point, point_int_to_light_vec)}")
                        return True, intersection_point, self.color*(scene.ambient_lighting)

                    # coinciding is just |a||b|, to calc angle b/w two vectors (denominator part)
                    #coinciding = point_int_to_light_vec.magnitude() * point_int_to_ray_org.magnitude()
                    #if coinciding == 0: return True, intersection_point, self.color*(scene.ambient_lighting)

                    angle = min(math.acos(int_normal.dot(point_int_to_light_vec.normalize()) / 1), math.pi)

                    # https://www.desmos.com/calculator/uhgizps2s3
                    # follows this graph ^^
                    y = (-math.pi*1.137*angle)/(math.pi+angle**2) + 1
                    total_brightness += y*obj.strength

            # print(total_brightness)
            total_brightness = min(max(total_brightness, scene.ambient_lighting), 1)
            return True, intersection_point, self.color*(total_brightness)
        
        return False, Vector(0, 0, 0), Color(0, 0, 0)

###################################################################
##                         CAMERA
###################################################################

def _zz(x, origin: Vector, width: int, height: int, scene: Scene, focal_length: int, orthogonals: tuple[Vector, Vector, Vector]) -> Callable[[int], None|tuple[Vector, Color]]:
    def _z_(z) -> None|tuple[Vector, Color]: # x=0 -> self.height

        dx, dz = x-(width//2), z-(height//2)

        ray = Line(Vector(origin.x, origin.y, origin.z), (orthogonals[1]*focal_length) + (orthogonals[0]*dx) + (orthogonals[2]*dz))
        obj = Camera.ray_intersect_nearest_obj(scene, ray)
        return obj
    return _z_

def _xx(origin: Vector, width: int, height: int, scene: Scene, focal_length: int, orthogonals: tuple[Vector, Vector, Vector]) -> Callable[[int], tuple[None|tuple[Vector, Color]]] :
    def _x_(x) -> tuple[None|tuple[Vector, Color]]: # x=0 -> self.width
        # with ThreadPool(processes=20) as pool_2:
        return tuple(map(
            _zz(x, origin, width, height, scene, focal_length, orthogonals),
            range(height)
        ))
    return _x_


class Camera(Object3D):
    def __init__(self, origin: Vector, normal: Vector, height: int, width: int, focal_length: int) -> None:
        """
            Cam origin denotes the cam obj position, and NOT the pixel window
            the pixel window is located [focal_length] distance in front of the camera object
        """
        super().__init__(origin, normal)
        self.height: int = height
        self.width: int = width
        self.focal_length: int = focal_length

        x_prime = Vector(self.normal.y, -self.normal.x, 0).normalize()
        z_prime = x_prime.cross(self.normal).normalize()
        self.orthogonals = (x_prime, self.normal, z_prime)

    @staticmethod
    def ray_intersect_nearest_obj(scene: Scene, ray: Line, non_cam_origin: Vector|None=None, detailed=False) -> None|tuple[Vector, Color]:
        objects_intersecting: list[tuple[Vector, Color]] = []
        for object in scene.objects:
            if object.origin == non_cam_origin:
                continue

            if isinstance(object, PointLighting):
                ...

            if isinstance(object, Sphere):
                intersection = object.intersection(ray, scene, False if non_cam_origin else True, detailed)
                if intersection[0]:
                    objects_intersecting.append(( 
                        intersection[1], intersection[2]
                    ))

        if detailed:
            print(f"Intersecting objects: {objects_intersecting}")

        # return the closest obj
        # print(objects_intersecting) #TEST
        closest_point = None
        if len(objects_intersecting) > 0:
            closest_dist = float("infinity")
            for obj in objects_intersecting:
                if (temp:=((obj[0]-ray.origin).magnitude())) < closest_dist:
                    closest_point = (obj[0], obj[1]) #tuple[vec(intersection point), color]
                    closest_dist = temp

            # print(closest_dist, closest_point)
            
        if detailed:
            print(f"Closest point of intersection: {closest_point}")
        return closest_point

    def render(self, scene: Scene) -> ImageObj:

        img = Image.new('RGB', (self.width, self.height), (scene.background_color.x, scene.background_color.y, scene.background_color.z))

        with pool.Pool(processes=1) as pool_:
            screen: tuple[tuple[None|tuple[Vector, Color]]] = tuple(
                pool_.map(_xx(self.origin, self.width, self.height, scene, self.focal_length, self.orthogonals), range(self.width))
            )

        for x in range(self.width):
            for z in range(self.height):
                # ray = Line(Vector(self.origin.x-(self.width//2) + x, self.origin.y, self.origin.z-(self.height//2)+z), self.normal)
                # obj = self.ray_intersect_nearest_obj(scene, ray)
                # if obj:
                #     img.putpixel((x, -z-1), (obj[1].x, obj[1].y, obj[1].z))

                obj = screen[x][z]
                if obj:
                    img.putpixel((x, -z-1), (obj[1].x, obj[1].y, obj[1].z))

        return img