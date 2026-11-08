from manimlib import *
import numpy as np

# Static wave centered in origin constructed by circles of a "photography" of a harmonic
class StaticWaveFromOrigin(InteractiveScene):
    def construct(self):
        # Set up axes
        axes = ThreeDAxes()

        self.frame.reorient(20, 19, 1, (0,0,0), 10)

        # Display wave functions
        single_wave_points = []

        A = 1
        w = 5
        phi_0 = 0
        for n in range(500):
            x = n/100
            y = 0
            z = A*np.sin(w*x+phi_0)

            new_point = [x,y,z]
            single_wave_points.append(new_point)

            new_point = [x,y,z]

        colors = color_gradient([GREEN, YELLOW], 201)
        whole_wave = VGroup()
        for point in single_wave_points:
            circle = Circle(radius=point[0], arc_center=[0,0,point[2]]).set_opacity(.6).set_color(colors[int(point[2]*100+100)])
            whole_wave.add(circle)

        self.add(whole_wave)

# The (first) end