#!/usr/bin/env python3
from scene import Scene
from units import Vector, Line, Color
from objects import Camera, Sphere, PointLighting

def main():

    #red ball
    test_sphere = Sphere(
        origin=Vector(0, 0, 50),
        normal=Vector(0, 1, 0),
        color=Color.from_hex("AA0000"),
        radius=80
    )

    #green ball
    test_sphere2 = Sphere(
        origin=Vector(-50, 0, -50),
        normal=Vector(0, 1, 0),
        color=Color.from_hex("00AA00"),
        radius=80
    )

    #blue ball
    test_sphere3 = Sphere(
        origin=Vector(50, 0, -50),
        normal=Vector(0, 1, 0),
        color=Color.from_hex("0000AA"),
        radius=80
    )

    test_lighting = PointLighting(
        origin=Vector(-50, -200, 10),
        normal=Vector(0, 1, 0),
        strength=1,
    )
    test_lighting2 = PointLighting(
        origin=Vector(-50, 200, 10),
        normal=Vector(0, 1, 0),
        strength=1,
    )
    
    test_cam = Camera(
        origin=Vector(0, -200, 0), 
        normal=Vector(0, 1, 0),
        height=800,
        width=800,
        focal_length=250
    )
    
    test_cam2 = Camera(
        origin=Vector(0, 200, 0), 
        normal=Vector(0, -1, 0),
        height=800,
        width=800,
        focal_length=250
    )

    main_scene = Scene([test_sphere, test_sphere2, test_sphere3, test_cam, test_lighting], "000000", 0.05)
    back_scene = Scene([test_sphere, test_sphere2, test_sphere3, test_cam2, test_lighting2], "000000", 0.05)
    # main_scene.add_obj(test_lighting2)

    # print(Color(255, 255, 255)*main_scene.ambient_lighting)

    # print(Vector(0, 1, 2).dot(Vector(5, 6, 7)))

    img = test_cam.render(main_scene)
    img.save("render.png")
    print("Done 1st cam")
    img2 = test_cam2.render(back_scene)
    img2.save("render2.png")

    # print(Camera.ray_intersect_nearest_obj(back_scene, Line(Vector(-50, 250, -50), Vector(0, -1, 0)), None, True))

def sun_moon():
    earth = Sphere(
        origin=Vector(0, -50, 80),
        normal=Vector(0, 1, 0),
        color=Color.from_hex("067FEB"),
        radius=80
    )

    moon = Sphere(
        origin=Vector(0, 0, -80),
        normal=Vector(0, 1, 0),
        color=Color.from_hex("FFFFFF"),
        radius=80
    )

    lighting = PointLighting(
        origin=Vector(0, -200, 110),
        normal=Vector(0, 1, 0),
        strength=1,
    )

    cam = Camera(
        origin=Vector(0, -300, 0),
        normal=Vector(0, 1, 0),
        height=400,
        width=400,
        focal_length=170)
    
    main_scene = Scene(
        objects=[earth, moon, lighting, cam],
        background_color="000000",
        ambient_lighting=0.07)

    img = cam.render(main_scene)
    img.save("earth-render.png")

if __name__ == "__main__":
    main()