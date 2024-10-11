from yta_multimedia.video.edition.effect.moviepy.moviepy_effect import MoviepyEffect
from moviepy.editor import vfx, VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union


class FlipVerticallyMoviepyEffect(MoviepyEffect):
    """
    This effect flips the video vertically.
    """
    __MOVIEPY_EFFECT_NAME = 'mirror_y'
    __parameters = {}

    def __init__(self, clip: Union[VideoFileClip, CompositeVideoClip, ImageClip]):
        self.__clip = clip

    def get_moviepy_vfx_effect(self):
        return getattr(vfx, self.__MOVIEPY_EFFECT_NAME, None)
    
    def process_parameters(self):
        return self.__parameters
    
    def apply(self):
        """
        Applies the effect to the provided 'clip' and with the also
        provided parameters needed by this effect.
        """
        return self.__clip.fx(self.get_moviepy_vfx_effect(), **self.process_parameters())
