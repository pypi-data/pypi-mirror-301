from yta_multimedia.video.edition.effect.moviepy.fade_in_moviepy_effect import FadeInMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.fade_out_moviepy_effect import FadeOutMoviepyEffect
from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips
from typing import Union


class BlinkMoviepyEffect(VideoEffect):
    """
    This method makes the provided video blink, that is a composition of
    a FadeOut and a FadeIn consecutively to build this effect. The duration
    will be the whole clip duration. The FadeIn will last the half of the
    clip duration and the FadeOut the other half.

    The 'color' parameter is the color you want for the blink effect as the
    background color. The default value is black ([0, 0, 0]).
    """

    @staticmethod
    def apply(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], color = None):
        """
        Applies the effect to the provided 'clip'.
        """
        clip = super().parse_moviepy_video(clip)

        if color is None:
            color = [0, 0, 0]

        half_duration = clip.duration / 2
        clip = concatenate_videoclips([
            FadeOutMoviepyEffect(clip.subclip(0, half_duration), duration = half_duration, color = color).apply(),
            FadeInMoviepyEffect(clip.subclip(half_duration, clip.duration), duration = half_duration, color = color).apply(),
        ])

        return clip