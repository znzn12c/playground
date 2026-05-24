from manimlib import *
import numpy as np
from PIL import Image


def fix_ranges_in_frame(x_obs, y_obs):
    x_len = x_obs[1] - x_obs[0]
    y_len = y_obs[1] - y_obs[0]
    current_ratio = x_len / y_len
    wanted_ratio = 16 / 9

    if x_len <= 0 or y_len <= 0:
        raise ValueError("Ranges must have positive length")

    x_range = x_obs
    y_range = y_obs

    if current_ratio > wanted_ratio:
        y_should = x_len / wanted_ratio
        increment = (y_should - y_len) / 2
        y_range = (y_obs[0] - increment, y_obs[1] + increment)
    elif current_ratio < wanted_ratio:
        x_should = y_len * wanted_ratio
        increment = (x_should - x_len) / 2
        x_range = (x_obs[0] - increment, x_obs[1] + increment)

    return x_range, y_range


class MandelbrotExplorer(InteractiveScene):
    def construct(self):
        x_observation = (-0.9, -0.7)
        y_observation = (-0.4, 0.4)
        x_range, y_range = fix_ranges_in_frame(x_observation, y_observation)

        plane = ComplexPlane(
            x_range=(x_range[0], x_range[1], 1),
            y_range=(y_range[0], y_range[1], 1),
            faded_line_ratio=1,
            background_line_style={"stroke_color": GREY, "stroke_opacity": 0.3},
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT,
        )
        self.plane = plane
        self.add(self.plane)

        self.detail = 200
        self.i_max = 100
        self.zoom_factor = 0.1
        self.colors = color_gradient(
            [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, BLACK], self.i_max
        )

        self.z_from = x_range[0] + y_range[0] * 1j
        self.z_to = x_range[1] + y_range[1] * 1j

        self.update_fractal()

    def compute_mandelbrot(self):
        real_vals = np.linspace(np.real(self.z_from), np.real(self.z_to), self.detail)
        imag_vals = np.linspace(np.imag(self.z_from), np.imag(self.z_to), self.detail)
        C = real_vals[np.newaxis, :] + 1j * imag_vals[:, np.newaxis]
        Z = np.zeros_like(C)
        iterations = np.full(C.shape, self.i_max, dtype=int)

        for i in range(self.i_max):
            mask = np.abs(Z) < 2
            if not mask.any():
                break
            Z[mask] = Z[mask] ** 2 + C[mask]
            escaped = mask & (np.abs(Z) >= 2)
            iterations[escaped] = i + 1

        return iterations, C

    def iterations_to_rgba(self, iterations, i_max, color_list):
        normalized = iterations / i_max
        color_rgbas = np.array([color_to_rgba(c) for c in color_list])

        n_colors = len(color_rgbas)
        float_idx = normalized * (n_colors - 1)
        low_idx = np.floor(float_idx).astype(int)
        high_idx = np.clip(low_idx + 1, 0, n_colors - 1)
        t = float_idx - low_idx

        low_color = color_rgbas[low_idx]
        high_color = color_rgbas[high_idx]
        rgba = (1 - t[..., np.newaxis]) * low_color + t[..., np.newaxis] * high_color
        return (rgba * 255).astype(np.uint8)

    def update_fractal(self):
        iterations, C = self.compute_mandelbrot()
        rgba = self.iterations_to_rgba(iterations, self.i_max, self.colors)

        # Save to disk
        img = Image.fromarray(rgba, mode="RGBA")
        img.save("fractal_frame.png")

        if not hasattr(self, "image_mob"):
            self.image_mob = ImageMobject("fractal_frame.png")
            self.size_and_position_image()
            self.add(self.image_mob)
        else:
            # Save current position/size
            old = self.image_mob
            center = old.get_center()
            w = old.get_width()
            h = old.get_height()
            # Create fresh ImageMobject with updated file
            self.image_mob = ImageMobject("fractal_frame.png")
            self.image_mob.move_to(center)
            self.image_mob.set_width(w)
            self.image_mob.set_height(h)
            # Swap
            self.remove(old)
            self.add(self.image_mob)

    def size_and_position_image(self):
        bottom_left = self.plane.n2p(self.z_from)
        top_right = self.plane.n2p(self.z_to)
        width = top_right[0] - bottom_left[0]
        height = top_right[1] - bottom_left[1]
        centre = (bottom_left + top_right) / 2
        self.image_mob.set_width(width)
        self.image_mob.set_height(height)
        self.image_mob.move_to(centre)

    def on_mouse_drag(self, point, d_point, buttons, modifiers):
        # This signature should be fine, but if you get errors, check
        # whether ManimGL passes additional arguments in this version
        x_unit = self.plane.get_x_unit_size()
        y_unit = self.plane.get_y_unit_size()
        d_complex = (-d_point[0] / x_unit) + (d_point[1] / y_unit) * 1j
        self.z_from += d_complex
        self.z_to += d_complex
        self.update_fractal()

    def on_mouse_scroll(self, point, offset, x_offset, y_offset):
        c_point = self.plane.p2n(point)
        if c_point is None:
            return

        # Use y_offset directly for vertical scroll
        scroll_amount = float(y_offset)
        
        factor = 1 - self.zoom_factor * scroll_amount
        factor = max(0.2, min(5.0, factor))

        new_real_min = c_point.real + (self.z_from.real - c_point.real) * factor
        new_real_max = c_point.real + (self.z_to.real - c_point.real) * factor
        new_imag_min = c_point.imag + (self.z_from.imag - c_point.imag) * factor
        new_imag_max = c_point.imag + (self.z_to.imag - c_point.imag) * factor

        self.z_from = new_real_min + new_imag_min * 1j
        self.z_to = new_real_max + new_imag_max * 1j
        self.update_fractal()