from manimlib import *
import numpy as np
from random import randint

# General function
def chaos_game(vertices, fraction, point0, iterations, axes):
    polygon = RegularPolygon(vertices)
    polygon.set_height(FRAME_HEIGHT*4/5)
    vertices_points = polygon.get_vertices()

    chaos_game_points = VGroup()
    point0 = point0
    for i in range(iterations):
        vertice = vertices_points[random.randint(0,len(vertices_points)-1)]
        vector = vertice - point0
        half_way_point = point0 + vector*fraction
        chaos_game_points.add(Dot(half_way_point, radius=0.01))
        point0 = half_way_point
    
    return chaos_game_points

# Scene
class ChaosGame(InteractiveScene):
    def construct(self):
        # Set axes
        axes = Axes()

        # Fractal lab
        vertices = 3
        fraction = 1/2
        iterations = 5000
        point0 = ORIGIN

        fractal = chaos_game(vertices=vertices, fraction=fraction, point0=point0, iterations=iterations, axes=axes)
        self.add(fractal)


# The End