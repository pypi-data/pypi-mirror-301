from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union


class FlipVerticallyMoviepyEffect(VideoEffect):
    """
    This effect flips the video vertically.
    """

    @staticmethod
    def apply(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip]):
        """
        Applies the effect to the provided 'clip'.
        """
        clip = super().parse_moviepy_video(clip)

        effect_name = super().get_moviepy_vfx_effect('mirror_y')
        parameters = {}

        return clip.fx(effect_name, **parameters)