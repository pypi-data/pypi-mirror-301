from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips
from yta_multimedia.video.edition.effect.moviepy.fade_in_moviepy_effect import FadeInMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.fade_out_moviepy_effect import FadeOutMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.moviepy_effect import MoviepyEffect
from typing import Union


class BlinkMoviepyEffect(MoviepyEffect):
    """
    This method makes the provided video blink, that is a composition of
    a FadeOut and a FadeIn consecutively to build this effect. The duration
    will be the whole clip duration. The FadeIn will last the half of the
    clip duration and the FadeOut the other half.

    The 'color' parameter is the color you want for the blink effect as the
    background color. The default value is black ([0, 0, 0]).
    """
    __parameters = {}

    def __init__(self, clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], color = None):
        self.__clip = clip

        if color is None:
            color = [0, 0, 0]

        self.__parameters['final_color'] = color

    def process_parameters(self):
        # TODO: Is this acutally needed (?) Is doing nothing
        # TODO: Check color is a valid value maybe (?)
        return self.__parameters
    
    def apply(self):
        """
        Applies the effect to the provided 'clip' and with the also
        provided parameters needed by this effect.
        """
        if not self.__clip:
            return None
        
        self.process_parameters()
        
        half_duration = self.__clip.duration / 2
        self.__clip = concatenate_videoclips([
            FadeOutMoviepyEffect(self.__clip.subclip(0, half_duration), duration = half_duration, color = self.__parameters['final_color']).apply(),
            FadeInMoviepyEffect(self.__clip.subclip(half_duration, self.__clip.duration), duration = half_duration, color = self.__parameters['final_color']).apply(),
        ])

        return self.__clip