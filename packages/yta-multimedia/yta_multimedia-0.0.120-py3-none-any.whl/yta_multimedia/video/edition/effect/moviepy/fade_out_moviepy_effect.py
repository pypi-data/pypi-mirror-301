from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union


class FadeOutMoviepyEffect(VideoEffect):
    """
    This effect will make the video disappear 
    progressively lasting the provided 'duration' 
    time or the whole clip time duration if None
    'duration' provided.

    The 'color' provided must be an array containing
    the rgb colors (default is [0, 0, 0], which is black).
    """

    @staticmethod
    def apply(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], duration = None, color = None):
        """
        Applies the effect to the provided 'clip'.
        """
        clip = super().parse_moviepy_video(clip)

        if duration is None:
            duration = clip.duration

        if color is None:
            color = [0, 0, 0]

        effect_name = super().get_moviepy_vfx_effect('fadeout')
        parameters = {
            'duration': duration,
            'final_color': color
        }

        return clip.fx(effect_name, **parameters)