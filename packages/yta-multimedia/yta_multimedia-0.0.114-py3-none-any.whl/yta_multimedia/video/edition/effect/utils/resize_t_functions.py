def zoom_in_t_func(zoom_ratio: float = 0.2):
    """
    Function that returns the resize value to make a moviepy
    video be zoomed in the 'zoom_ratio' zoom all the time.
    """
    return 1 + zoom_ratio

def zoom_out_t_func(zoom_ratio: float = 0.2):
    """
    Function that returns the resize value to make a moviepy
    video be zoomed out the 'zoom_ratio' zoom all the time.
    """
    return 1 - zoom_ratio

def linear_zoom_in_t_func(t, duration, zoom_ratio: float = 0.2):
    """
    Function that returns the resize value to make a moviepy
    video zoom in linearly to the 'zoom_ratio' zoom.
    """
    # TODO: Check 'zoom_ratio' is valid

    return 1 + zoom_ratio * (t / duration)
    """
    if t < 4:
        return 1 + 0.2 * t  # Zoom-in.
    elif 4 <= t <= 6:
        return 1 + 0.2 * 4  # Stay.
    else: # 6 < t
        return 1 + 0.2 * (duration - t)  # Zoom-out.
    """

def linear_zoom_out_t_func(t, duration, zoom_ratio: float = 0.2):
    """
    Function that returns the resize value to make a moviepy
    video zoom out linearly to the 'zoom_ratio' zoom.
    """
    # TODO: Check 'zoom_ratio' is valid

    return 1 + zoom_ratio * (duration - (t / duration))

