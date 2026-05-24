from manimlib import *
from scipy.integrate import odeint
from scipy.integrate import solve_ivp


# Define important functions

def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt)
    )
    return solution.y.T


# Scene
class LorenzAttractor(InteractiveScene):
    def construct(self):
        # Set up axes
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(-0, 50, 5),
            width=16,
            height=16,
            depth=8
        )
        axes.set_width(FRAME_WIDTH)
        axes.center()

        self.frame.reorient(43, 76, 1, IN, 10)
        self.add(axes)

        # Display Lorenz solutions
        epsilon = 1e-5
        evolution_time = 30
        states = [
            [10, 10, 10 + n * epsilon]
            for n in range(10)
        ]
        colors = color_gradient([BLUE, TEAL], len(states))

        curves = VGroup()

        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            curve = VMobject().set_points_as_corners(axes.c2p(*points.T))
            curve.set_stroke(color, 2)
            curves.add(curve)

        dots = Group(GlowDot(color=color, radius=0.5) for color in colors)

        def update_dots(dots, curves=curves):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())

        dots.add_updater(update_dots)
        
        self.add(dots)
        self.play(
            *(
                ShowCreation(curve, rate_func=linear)
                for curve in curves
            ),
            FadeOut(curves),
            self.frame.animate.reorient(270, 72, 0, (0.0, 0.0, -1.0), 10.00),
            run_time=evolution_time
        )


        # The End