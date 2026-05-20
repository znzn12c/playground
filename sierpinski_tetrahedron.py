from manimlib import *

# Sierpinski tetrahedron adaptation in manim from Ben Spark's video "Fractal Tetrahedron Live Build"

# Functions
def construct_tetrahedron(cube, color=YELLOW, opacity=0.5):
    
    corners = cube.get_all_corners()
    tetrahedron = VGroup(
            Polygon(
                corners[0], corners[3], corners[5],
                stroke_color=color,
                fill_color=color,
                fill_opacity=opacity
            ),
            Polygon(
                corners[0], corners[3], corners[6],
                stroke_color=color,
                fill_color=color,
                fill_opacity=opacity
            ),
            Polygon(
                corners[0], corners[5], corners[6],
                stroke_color=color,
                fill_color=color,
                fill_opacity=opacity
            ),
            Polygon(
                corners[3], corners[5], corners[6],
                stroke_color=color,
                fill_color=color,
                fill_opacity=opacity
            )
        )
    
    return tetrahedron

def nth_iteration_cubes(iterations, scale_factor, cubes=False):
    iterations -= 1

    if cubes is False:
        cubes = Group(Cube())
    
    new_scaled_cubes = Group()
    for n in range(4):
        previous_scaled_cubes = cubes.copy()
        previous_scaled_cubes.scale(scale_factor)
        if n == 1:
            previous_scaled_cubes.shift(scale_factor * (LEFT + DOWN + IN))
        elif n == 2:
            previous_scaled_cubes.shift(scale_factor * (RIGHT + DOWN + OUT))
        elif n == 3:
            previous_scaled_cubes.shift(scale_factor * (RIGHT + UP + IN))
        else:
            previous_scaled_cubes.shift(scale_factor * (LEFT + UP + OUT))
        
        new_scaled_cubes.add(previous_scaled_cubes)

    
    if iterations != 0:
        return nth_iteration_cubes(iterations, scale_factor, cubes=new_scaled_cubes)
    else:
        return new_scaled_cubes

def construct_sierpinski_tetrahedron(iterations, scale_factor):
    matryoshka_cubes_group = nth_iteration_cubes(iterations, scale_factor).get_family()
    cubes = [cube for cube in matryoshka_cubes_group if isinstance(cube, Cube)]

    nth_iteration_tetrahedrons = VGroup()
    for cube in cubes:
        new_tetrahedron = construct_tetrahedron(cube)
        nth_iteration_tetrahedrons.add(new_tetrahedron)
    
    return nth_iteration_tetrahedrons


# Scene
class SierpinskiTetrahedron(InteractiveScene):
    def construct(self):
        
        # Set up 3D Space
        axes = ThreeDAxes()

        frame = self.frame
        frame.reorient(50, 60, 1, ORIGIN, 3.8)

        # Build Sierpinski tetrahedron
        iterations_ = 4
        scale_factor_ = 0.5

        sierpinski_tetrahedron_ = construct_sierpinski_tetrahedron(iterations=iterations_, scale_factor=scale_factor_)
        self.add(sierpinski_tetrahedron_)
    
    # The End