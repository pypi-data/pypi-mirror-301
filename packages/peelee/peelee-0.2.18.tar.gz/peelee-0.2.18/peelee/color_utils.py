#!/usr/bin/env python3
"""
Color utilities.
"""
import colorsys


def fg(hex_color, msg):
    """Decorate msg with hex_color in foreground."""
    _rgb = hex2rgb(hex_color)
    return f"\x01\x1b[38;2;{_rgb[0]};{_rgb[1]};{_rgb[2]}m\x02{msg}\x01\x1b[0m"


def bg(hex_color, msg):
    """Decorate msg with hex_color in background."""
    _rgb = hex2rgb(hex_color)
    return f"\x01\x1b[48;2;{_rgb[0]};{_rgb[1]};{_rgb[2]}m\x02{msg}\x01\x1b[0m"


def hex2rgb(hex_color):
    """ "Convert."""
    hex_color = hex_color.lstrip("#")
    rgb_color = tuple(int(hex_color[i: i + 2], 16) for i in (0, 2, 4))
    return rgb_color


def hex2hls(hex_color):
    """ "Convert."""
    rgb_color = hex2rgb(hex_color)
    normalized_rgb = (
        rgb_color[0] / 255.0,
        rgb_color[1] / 255.0,
        rgb_color[2] / 255.0,
    )
    hls_color = colorsys.rgb_to_hls(
        normalized_rgb[0], normalized_rgb[1], normalized_rgb[2]
    )
    return hls_color


def hls2hex(hls_color):
    """
    Convert HSL color to HEX code.

    Parameter:
    hls_color - tuple containing hue, lightness, and saturation color codes
    such as (0.5277777777777778, 0.04, 1).
    """
    rgb_color = colorsys.hls_to_rgb(hls_color[0], hls_color[1], hls_color[2])
    scaled_rgb = tuple(int(c * 255) for c in rgb_color)
    return rgb2hex(scaled_rgb)


def rgb2hex(rgb_color):
    """ "Convert."""
    scaled_rgb = rgb_color
    if isinstance(rgb_color[0], float):
        scaled_rgb = tuple(int(c * 255) for c in rgb_color)
    hex_color = f"#{scaled_rgb[0]:02X}{scaled_rgb[1]:02X}{scaled_rgb[2]:02X}"
    return hex_color


def color_palette_plain_text(palette_plain_text):
    """Show palette."""
    for line in palette_plain_text.splitlines():
        _, hex_color = line.strip().split(":")
        print(bg(hex_color, line))