from manimlib import *


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

        text = Text("Normal complex plane")
        text.to_corner(UL)
        self.add(text)

        # Create vertical and horizontal lines

        vertical_lines = []
        for m in range(-10, 11):
            vertical = []
            for n in range(-10, 11):
                vertical.append(0.1*m + 0.1*n*1j)
            vertical_lines.append(vertical)

        for vertical_line in vertical_lines:
            points = [plane.n2p(z) for z in vertical_line]
            straight_line = VMobject().set_points_as_corners(points)
            self.add(straight_line)

        horizontal_lines = []
        for m in range(-10, 11):
            horizontal = []
            for n in range(-10, 11):
                horizontal.append(0.1*n + 0.1*m*1j)
            horizontal_lines.append(horizontal)

        for horizontal_line in horizontal_lines:
            points = [plane.n2p(z) for z in horizontal_line]
            straight_line = VMobject().set_points_as_corners(points)
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

        text2 = Text("z = z**2")
        text2.to_corner(UR)
        self.add(text2)

        # Transformation of the lines in the first plane

        vertical_lines2 = []
        for vertical_line in vertical_lines:
            new_vertical_line = [z**2 for z in vertical_line]
            vertical_lines2.append(new_vertical_line)

        for vertical_line2 in vertical_lines2:
            points = [plane2.n2p(z) for z in vertical_line2]
            straight_line = VMobject().set_points_as_corners(points)
            self.add(straight_line)

        horizontal_lines2 = []
        for horizontal_line in horizontal_lines:
            new_horizontal_line = [z**2 for z in horizontal_line]
            horizontal_lines2.append(new_horizontal_line)

        for horizontal_line2 in horizontal_lines2:
            points = [plane2.n2p(z) for z in horizontal_line2]
            straight_line = VMobject().set_points_as_corners(points)
            self.add(straight_line)

        # Animation


        # The End