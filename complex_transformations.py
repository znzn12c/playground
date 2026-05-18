from manimlib import *


# General functions
def draw_complex_plane(plane2, vertical_lines, horizontal_lines, func):
    vertical_lines2 = []
    for vertical_line in vertical_lines:
        new_vertical_line = [func(z) for z in vertical_line]
        vertical_lines2.append(new_vertical_line)

    v_straight_lines = VGroup()
    for vertical_line2 in vertical_lines2:
        points = [plane2.n2p(np.real(z) + 1j*np.imag(z)) for z in vertical_line2]
        straight_line = VMobject().set_points_as_corners(points)
        straight_line.set_color(RED)
        v_straight_lines.add(straight_line)

    horizontal_lines2 = []
    for horizontal_line in horizontal_lines:
        new_horizontal_line = [func(z) for z in horizontal_line]
        horizontal_lines2.append(new_horizontal_line)

    h_straight_lines = VGroup()
    for horizontal_line2 in horizontal_lines2:
        points = [plane2.n2p(np.real(z) + 1j*np.imag(z)) for z in horizontal_line2]
        straight_line = VMobject().set_points_as_corners(points)
        straight_line.set_color(RED)
        h_straight_lines.add(straight_line)

    return v_straight_lines, h_straight_lines


# Scene
class ComplexTransformations(InteractiveScene):
    def construct(self):

        # Add base complex
        x_max = 1
        plane = ComplexPlane(
            x_range=(-x_max, x_max, 1),
            y_range=(-x_max, x_max, 1),
            background_line_style=dict(stroke_opacity=0),
            faded_line_ratio=0,
            width = FRAME_WIDTH / 3,
            height = FRAME_HEIGHT / 3
        )
        plane.to_edge(LEFT)
        self.add(plane)

        # Create vertical and horizontal lines

        vertical_lines = []
        for m in range(-10, 11):
            vertical = []
            for n in range(-10, 11):
                vertical.append(0.1*m + 0.1*n*1j)
            vertical_lines.append(vertical)

        vertical_straight_lines = []
        for vertical_line in vertical_lines:
            points = [plane.n2p(z) for z in vertical_line]
            straight_line = VMobject().set_points_as_corners(points)
            vertical_straight_lines.append(straight_line)
            self.add(straight_line)

        horizontal_lines = []
        for m in range(-10, 11):
            horizontal = []
            for n in range(-10, 11):
                horizontal.append(0.1*n + 0.1*m*1j)
            horizontal_lines.append(horizontal)

        horizontal_straight_lines = []
        for horizontal_line in horizontal_lines:
            points = [plane.n2p(z) for z in horizontal_line]
            straight_line = VMobject().set_points_as_corners(points)
            horizontal_straight_lines.append(straight_line)
            self.add(straight_line)

        # First transformation
        x_max = 1
        plane2 = ComplexPlane(
            x_range=(-x_max, x_max, 1),
            y_range=(-x_max, x_max, 1),
            background_line_style=dict(stroke_opacity=0),
            faded_line_ratio=0,
            width = FRAME_WIDTH / 3,
            height = FRAME_HEIGHT / 3
        )
        plane2.to_edge(RIGHT)
        self.add(plane2)

        # Transformation of the lines in the first plane

        a, b = draw_complex_plane(plane2, vertical_lines, horizontal_lines, lambda z: np.log(z))

        # Animation

        self.play(
            *[Transform(horizontal_line, b1) for horizontal_line, b1 in zip(horizontal_straight_lines, b)],
            rate_func=smooth,
            run_time=3
        )
        self.play(
            *[Transform(vertical_line, a1) for vertical_line, a1 in zip(vertical_straight_lines, a)],
            rate_func=smooth,
            run_time=3
        )


        # The End