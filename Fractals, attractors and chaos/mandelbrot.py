from manimlib import *
import numpy as np

# General functions

def escape_iterations(c, z_max, i_max, recursive_func):

    i = 0
    znp1 = 0
    for _ in range(i_max):
        if np.abs(recursive_func(znp1)) < z_max:
            znp1 = recursive_func(znp1)
            i += 1
        else:
            break
    
    return i

def mandelbrot_set(plane, z_from, z_to, detail, z_max, i_max, colors):

    real_range = (np.real(z_to) - np.real(z_from))
    imag_range = (np.imag(z_to) - np.imag(z_from))
    dreal = real_range/detail
    dimag = imag_range/detail

    c0 = z_from

    csandi = [] # List with complex numbers and their nth iteration to escape
    for n in range(int(real_range/dreal)):
        for m in range(int(imag_range/dimag)):
            c = c0 + n*dreal + m*dimag*1j
            i = escape_iterations(c, z_max, i_max, lambda zn: zn**2 + c)
            candi = [c, i]
            csandi.append(candi)

    csandi_ready = VGroup()
    for candi in csandi:
        color = colors[candi[1]-1]

        rectangle = Rectangle(width=(dreal*plane.get_x_unit_size()), height=(dimag*plane.get_x_unit_size()), color=color) # Add depth=i for 3d
        rectangle.set_fill(color, opacity=1.0)
        rectangle.set_stroke(width=0)
        rectangle.move_to(plane.n2p(candi[0]))

        csandi_ready.add(rectangle)

    return csandi_ready

def fix_ranges_in_frame(x_obs, y_obs):
    x_len = x_obs[1]-x_obs[0]
    y_len = y_obs[1]-y_obs[0]

    current_ratio = x_len/y_len
    wanted_ratio = 16/9

    x_range = x_obs
    y_range = y_obs

    if x_len <= 0 or y_len <= 0:
        raise ValueError("Ranges must have positive length") # Just in case I wrongly set the coordinates

    if current_ratio > wanted_ratio:
        y_should = x_len/wanted_ratio
        increment = (y_should - y_len)/2
        y_range = (y_obs[0]-increment, y_obs[1]+increment)
    elif current_ratio < wanted_ratio:
        x_should = y_len*wanted_ratio
        increment = (x_should - x_len)/2
        x_range = (x_obs[0]-increment, x_obs[1]+increment)

    return x_range, y_range

# Scene
class MandelbrotSet(InteractiveScene):
    def construct(self):

        # Complex plane and frame
        x_observation = (-0.9, -0.7)
        y_observation = (-0.4, 0.4)

        x_range, y_range = fix_ranges_in_frame(x_observation, y_observation)
        
        plane = ComplexPlane(
            x_range=(*x_range, 1),
            y_range=(*y_range, 1),
            faded_line_ratio=0,
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT
        )

        # Mandelbrot Set

        detail = 50
        z_from = plane.get_all_ranges()[0][0] + plane.get_all_ranges()[1][0]*1j
        z_to = plane.get_all_ranges()[0][1] + plane.get_all_ranges()[1][1]*1j
        z_max = 2 # Module at which we consider c has escaped
        i_max = 50 # Number of iterations
        colors = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, BLACK], i_max)

        mandelbrot_values = mandelbrot_set(plane, z_from, z_to, detail, z_max, i_max, colors)
        self.add(mandelbrot_values)

        # 3D Mandelbrot Set
        self.play(self.frame.animate.reorient(-60, 46, 1, (-4.25,-0.75,0), 10))
        
        # fer apareixer els prismes amb animació


        # The End