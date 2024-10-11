from yta_multimedia.video.edition.effect.moviepy.moviepy_effect import MoviepyEffect
from moviepy.editor import vfx, VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union


class ScrollMoviepyEffect(MoviepyEffect):
    """
    This effect will make the clip appear in black and
    white colors.
    """
    __MOVIEPY_EFFECT_NAME = 'scroll'
    __parameters = {}

    def __init__(self, clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], width: int = None, height: int = None, x_speed: int = None, y_speed: int = None, x_start: int = None, y_start: int = None):
        self.__clip = clip

        if width is None:
            width = 960

        if height is None:
            height = 540

        if x_speed is None:
            x_speed = 20

        if y_speed is None:
            y_speed = 20

        if x_start is None:
            x_start = 100

        if y_start is None:
            y_start = 100

        self.__parameters['w'] = width
        self.__parameters['h'] = height
        self.__parameters['x_speed'] = x_speed
        self.__parameters['y_speed'] = y_speed
        self.__parameters['x_start'] = x_start
        self.__parameters['y_start'] = y_start

    def get_moviepy_vfx_effect(self):
        return getattr(vfx, self.__MOVIEPY_EFFECT_NAME, None)
    
    def process_parameters(self):
        if not self.__parameters['w']:
            self.__parameters['w'] = self.__clip.w / 2 - self.__clip.w / 2
            self.__parameters['h'] = self.__clip.h / 2 - self.__clip.h / 2
            self.__parameters['x_speed'] = 5
            self.__parameters['y_speed'] = 5
            self.__parameters['x_start'] = self.__clip.w / 2 - self.__clip.w / 2
            self.__parameters['y_start'] = self.__clip.h / 2 - self.__clip.h / 2

        return self.__parameters
    
    def apply(self):
        """
        Applies the effect to the provided 'clip' and with the also
        provided parameters needed by this effect.
        """
        return self.__clip.fx(self.get_moviepy_vfx_effect(), **self.process_parameters()).resize(self.__clip.size)
