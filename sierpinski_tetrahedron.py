from manimlib import *

# Sierpinski tetrahedron adaptation in manim from Ben Spark's video "Fractal Tetrahedron Live Build"

# Functions
def construct_tetrahedron(cube, color=YELLOW, opacity=1):
    
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

def tetrahedron_division(cube, scale_factor, color=BLUE, smaller=False):
    cube = cube.scale(scale_factor)

    if smaller:
        smaller_tetrahedrons = VGroup()
        for n in range(4):
            little_tetrahedron = construct_smaller_tetrahedron(cube, scale_factor=scale_factor, color=color)
            if n == 1:
                little_tetrahedron.shift(scale_factor * (LEFT + DOWN + IN))
            elif n == 2:
                little_tetrahedron.shift(scale_factor * (RIGHT + DOWN + OUT))
            elif n == 3:
                little_tetrahedron.shift(scale_factor * (RIGHT + UP + IN))
            else:
                little_tetrahedron.shift(scale_factor * (LEFT + UP + OUT))
            
            smaller_tetrahedrons.add(little_tetrahedron)
    else:
        smaller_tetrahedrons = VGroup()
        for n in range(4):
            little_tetrahedron = construct_tetrahedron(cube, color=color)
            if n == 1:
                little_tetrahedron.shift(scale_factor * (LEFT + DOWN + IN))
            elif n == 2:
                little_tetrahedron.shift(scale_factor * (RIGHT + DOWN + OUT))
            elif n == 3:
                little_tetrahedron.shift(scale_factor * (RIGHT + UP + IN))
            else:
                little_tetrahedron.shift(scale_factor * (LEFT + UP + OUT))
            
            smaller_tetrahedrons.add(little_tetrahedron)
    
    return smaller_tetrahedrons

def construct_smaller_tetrahedron(cube, scale_factor, color=BLUE):
    smaller_cube = cube
    
    smaller_tetrahedrons = VGroup()
    for n in range(4):
        little_tetrahedron = construct_tetrahedron(smaller_cube, color=color)
        if n == 1:
            little_tetrahedron.shift(scale_factor**2 * (LEFT + DOWN + IN))
        elif n == 2:
            little_tetrahedron.shift(scale_factor**2 * (RIGHT + DOWN + OUT))
        elif n == 3:
            little_tetrahedron.shift(scale_factor**2 * (RIGHT + UP + IN))
        else:
            little_tetrahedron.shift(scale_factor**2 * (LEFT + UP + OUT))
        
        smaller_tetrahedrons.add(little_tetrahedron)
    
    return smaller_tetrahedrons


# Scene
class SierpinskiTetrahedron(InteractiveScene):
    def construct(self):
        
        # Set up 3D Space
        axes = ThreeDAxes()
        self.add(axes)

        frame = self.frame
        frame.reorient(50, 100, 1, (1, 1, 1), 3.8)

        # Build initial tetrahedron
        cube = Cube(opacity=0.5)
        cube.shift(RIGHT + UP + OUT)

        tetrahedron = construct_tetrahedron(cube)

        smaller_tetrahedrons = tetrahedron_division(cube, scale_factor=0.5, color=BLUE)

        even_smaller_tetrahedrons = tetrahedron_division(cube, scale_factor=0.5, color=GREY, smaller=True)
        self.add(even_smaller_tetrahedrons)

    
    # The End