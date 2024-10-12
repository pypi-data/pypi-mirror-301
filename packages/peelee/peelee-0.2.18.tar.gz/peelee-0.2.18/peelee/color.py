#!/usr/bin/env python3
"""
Utilities
"""
from enum import Enum

from loguru import logger

from peelee import color_utils as U, random_color as R

HLS_MAX = 10**16
SLICE_COLORS_TOTAL = 100


class ColorName(Enum):
    """Color names"""

    RED = 0
    GREEN = 1
    BLUE = 2
    YELLOW = 3
    CYAN = 4
    VIOLET = 5
    BLACK = 6
    RANDOM = 7


def crange(s, t, total):
    if s == t:
        return [s * HLS_MAX] * total
    _start = min(s, t)
    _end = max(s, t)
    _step = (_end - _start) / total
    _list = list(
        range(
            round(_start * HLS_MAX),
            round(_end * HLS_MAX),
            round(_step * HLS_MAX),
        )
    )
    if s not in _list:
        _list.insert(0, s * HLS_MAX)
    if t not in _list:
        _list.append(t * HLS_MAX)
    return _list


def generate_gradient_colors(hex_color_source, hex_color_target, total):
    """Generate gradient colors.

    Parameters:
        hex_color_source - hex color code of the source color
        hex_color_target - hex color code of the target color
        total - total number of colors

    Returns:
        list
    """
    h, l, s = U.hex2hls(hex_color_source)
    h_target, l_target, s_target = U.hex2hls(hex_color_target)
    h_list = crange(h, h_target, total)
    l_list = crange(l, l_target, total)
    s_list = crange(s, s_target, total)

    hls_list = [
        (
            h_list[index] / HLS_MAX,
            l_list[index] / HLS_MAX,
            s_list[index] / HLS_MAX,
        )
        for index in range(total)
    ]
    logger.debug(hls_list)
    gradient_colors = [U.hls2hex(hls) for hls in hls_list]
    if hex_color_source not in gradient_colors:
        gradient_colors.insert(0, hex_color_source)
    if hex_color_target not in gradient_colors:
        gradient_colors.append(hex_color_target)
    return gradient_colors


def calculate_relative_luminance(hex_color):
    """Calculate relative luminance for hex color codes.

    Refer to:
    https://www.w3.org/TR/WCAG20-TECHS/G17.html

    Parameter:
    hex_color - hex color code
    """

    rgb_8bit = U.hex2rgb(hex_color)
    rgb_srgb = tuple(_8bit / 255.0 for _8bit in rgb_8bit)
    r, g, b = tuple(
        _srgb / 12.92 if _srgb <= 0.03928 else ((_srgb + 0.055) / 1.055) ** 2.4
        for _srgb in rgb_srgb
    )

    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def calculate_contrast_ratio(hex_light_color, hex_dark_color):
    """Calculate contrast ratio for hex color codes.

    Parameter:
    hex_light_color - hex color code of the lighter of the foreground or background color
    hex_dark_color - hex color code of the darker of the foreground or background color

    Refer to:
    https://www.w3.org/TR/WCAG20-TECHS/G17.html
    """
    relative_luminance_light = calculate_relative_luminance(hex_light_color)
    relative_luminance_dark = calculate_relative_luminance(hex_dark_color)
    return (relative_luminance_light + 0.05) / (relative_luminance_dark + 0.05)


def convert_to_best_light_color(
    base_light_color,
    target_dark_color,
    min_contrast_ratio,
    max_contrast_ratio,
    choose_lightest=False,
):
    """Converts the given base light color to the best light color.

    This function converts the given base light color to the best light color based on contrast ratio.

    Parameters:
        base_light_color (str): The base light color.
        target_background_color (str): The target background color.
    """
    best_color = base_light_color
    contrast_ratio = calculate_contrast_ratio(base_light_color, target_dark_color)
    # already good enough contrast ratio, return directly
    if contrast_ratio >= min_contrast_ratio and contrast_ratio <= max_contrast_ratio:
        return best_color

    # if too light, choose the darkest light color; if too dark, choose the
    # lightest light color
    is_too_light = contrast_ratio > max_contrast_ratio
    is_too_dark = contrast_ratio < min_contrast_ratio
    if is_too_dark:
        better_colors = R.lighter(base_light_color, SLICE_COLORS_TOTAL)
    elif is_too_light:
        better_colors = R.darker(base_light_color, SLICE_COLORS_TOTAL)

    filter_better_colors = list(
        filter(
            lambda x: calculate_contrast_ratio(x, target_dark_color)
            >= min_contrast_ratio
            and calculate_contrast_ratio(x, target_dark_color) <= max_contrast_ratio,
            better_colors,
        )
    )
    # choose the darkest light color which has lowest contrast ratio
    # to make sure it's not too light
    if len(filter_better_colors) == 0:
        logger.warning(
            f"Not found best light color for {base_light_color} to adapt to the dark color: {target_dark_color}"
        )
        logger.warning(
            (
                base_light_color,
                target_dark_color,
                better_colors[0],
                better_colors[-1],
                min_contrast_ratio,
                max_contrast_ratio,
                calculate_contrast_ratio(better_colors[0], target_dark_color),
                calculate_contrast_ratio(better_colors[-1], target_dark_color),
                filter_better_colors,
            )
        )
        # for some colors, could not be even better (the pre-defined contrast
        # ratio is unrealistic), so just use the better colors
        filter_better_colors = better_colors
    # the darkest light color is the best light color
    # this is the proved best light color, don't make change to it
    _index = 0 if not choose_lightest else -1
    best_color = sorted(filter_better_colors)[_index]
    return best_color

def convert_to_best_dark_color(
    base_dark_color,
    target_light_color,
    min_contrast_ratio,
    max_contrast_ratio,
    choose_darkest=False,
):
    """Converts the given base light color to the best light color.

    This function converts the given base light color to the best light color based on contrast ratio.

    Parameters:
        base_light_color (str): The base light color.
        target_background_color (str): The target background color.
    """
    best_color = base_dark_color
    contrast_ratio = calculate_contrast_ratio(target_light_color, base_dark_color)
    if contrast_ratio >= min_contrast_ratio and contrast_ratio <= max_contrast_ratio:
        return best_color

    # if too dark, choose the lightest dark color; if too light, choose the
    # darkest dark color
    if contrast_ratio < min_contrast_ratio:
        better_colors = R.darker(base_dark_color, SLICE_COLORS_TOTAL)
    elif contrast_ratio > max_contrast_ratio:
        better_colors = R.lighter(base_dark_color, SLICE_COLORS_TOTAL)
    filter_better_colors = list(
        filter(
            lambda x: calculate_contrast_ratio(target_light_color, x)
            >= min_contrast_ratio
            and calculate_contrast_ratio(target_light_color, x)
            <= max_contrast_ratio,
            better_colors,
        )
    )
    # choose the lightest dark color which has lowest contrast ratio
    # to make sure it's not too dark
    if len(filter_better_colors) == 0:
        logger.debug(
            (
                base_dark_color,
                target_light_color,
                better_colors[0],
                better_colors[-1],
                min_contrast_ratio,
                max_contrast_ratio,
                calculate_contrast_ratio(target_light_color, better_colors[0]),
                calculate_contrast_ratio(target_light_color, better_colors[-1]),
                filter_better_colors,
            )
        )
        logger.warning(
            f"Not found best dark color for {base_dark_color} to adapt to the light color: {target_light_color}"
        )
        return best_color
    # the lightest dark color is the best one
    # this is the proved best dark color, don't make change to it
    # unless it's to find the best editor background color
    if choose_darkest:
        best_color = sorted(filter_better_colors)[0]
    else:
        best_color = sorted(filter_better_colors)[-1]
    return best_color
