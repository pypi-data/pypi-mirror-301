from yta_multimedia.video.edition.effect.moviepy.moviepy_effect import MoviepyEffect
from moviepy.editor import vfx, VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union


class FadeOutMoviepyEffect(MoviepyEffect):
    """
    This effect will make the video disappear 
    progressively lasting the provided 'duration' 
    time or the whole clip time duration if None
    'duration' provided.
    """
    __MOVIEPY_EFFECT_NAME = 'fadeout'
    __parameters = {}

    def __init__(self, clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], duration: float = None, color = None):
        self.__clip = clip

        if duration is None:
            duration = self.__clip.duration

        if color is None:
            color = [0, 0, 0]

        self.__parameters['duration'] = duration
        self.__parameters['final_color'] = color

    def get_moviepy_vfx_effect(self):
        return getattr(vfx, self.__MOVIEPY_EFFECT_NAME, None)
    
    def process_parameters(self):
        if not self.__parameters['duration']:
            self.__parameters['duration'] = self.__clip.duration
        else:
            if self.__parameters['duration'] > self.__clip.duration:
                self.__parameters['duration'] = self.__clip.duration
            elif self.__parameters['duration'] <= 0:
                self.__parameters['duration'] = 0

        if not self.__parameters['final_color']:
            self.__parameters['final_color'] = [0, 0, 0]
        # TODO: Check color is a valid value.

        return self.__parameters
    
    def apply(self):
        """
        Applies the effect to the provided 'clip' and with the also
        provided parameters needed by this effect.
        """
        return self.__clip.fx(self.get_moviepy_vfx_effect(), **self.process_parameters())
