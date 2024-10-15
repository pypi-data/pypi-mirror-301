from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union


class ScrollMoviepyEffect(VideoEffect):
    """
    This effect will make the clip be scrolled like if a zoomed
    region was surfing through the clip.
    """
    
    @staticmethod
    def apply(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], width = None, height = None, x_speed = None, y_speed = None, x_start = None, y_start = None):
        """
        Applies the effect to the provided 'clip'.
        """
        clip = super().parse_moviepy_video(clip)

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

        effect_name = super().get_moviepy_vfx_effect('scroll')
        parameters = {}

        return clip.fx(effect_name, **parameters).resize(clip.size)