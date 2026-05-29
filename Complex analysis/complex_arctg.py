from manimlib import *
import numpy as np

# Inici

def get_complex_graph(axes, wave, func, delta_t=0.01): # f: real -> complex

    t_min, t_max = axes.z_range[:2]
    ts = np.arange(t_min, t_max, delta_t)
    ss = wave(ts, func)

    points = np.array([
        (np.real(s), np.imag(s), t)
        for s, t in zip(ss, ts)
    ])

    curve = VMobject()
    curve.set_points_as_corners([axes.c2p(x, y, z) for x, y, z in points])
    return curve # This function draws the curve each time that the always draw based on valuetracker t changes its value

# Scene
class ComplexArctg(InteractiveScene):
    def construct(self):

        # Axes
        max_x = 2
        initial_time = -5
        final_time = 5
        axes = ThreeDAxes(
            x_range=(-max_x, max_x), # Real part
            y_range=(-max_x, max_x), # Imaginary part
            z_range=(initial_time, final_time) # Time evolution
        )
        self.add(axes)
        frame = self.frame
        frame.reorient(0, -90, 0, (0, 0, 5), 10)
        # frame.reorient(0, -2, 0, (-0.25, 0, 0), 7)

        # Complex plane
        plane = ComplexPlane(
            x_range=(-max_x, max_x),
            y_range=(-max_x, max_x)
        )
        self.add(plane)

        # Arctangent
        t_tracker = ValueTracker(initial_time)
        get_t = t_tracker.get_value

        def arctangent(t):
            arctangent = (1j/2)*np.log(t+1j)-(1j/2)*np.log(t-1j)
            return arctangent
        
        def euler_cosine(t):
            cosine = (np.exp(1j * t) + np.exp(-1j * t))/2
            return cosine
        
        def wave(ts, func):
            current_time = get_t()

            return np.array([
                func(t)
                if t <= current_time else np.nan + 1j * np.nan
                for t in ts
            ])
        
        graph = always_redraw(lambda: get_complex_graph(
            axes,
            wave,
            euler_cosine)) # Modify this function for different outputs
        self.add(graph)

        self.play(t_tracker.animate.set_value(final_time), run_time=2, rate_func=linear)
# The End