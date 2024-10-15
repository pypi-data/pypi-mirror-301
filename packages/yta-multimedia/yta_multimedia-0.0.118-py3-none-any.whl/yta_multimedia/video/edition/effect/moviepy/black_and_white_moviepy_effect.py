from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union


class BlackAndWhiteMoviepyEffect(VideoEffect):
    """
    This effect will make the clip appear in black and
    white colors.
    """

    @staticmethod
    def apply(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip]):
        """
        Applies the effect to the provided 'clip'.
        """
        clip = super().parse_moviepy_video(clip)

        effect_name = super().get_moviepy_vfx_effect('blackwhite')
        parameters = {}

        return clip.fx(effect_name, **parameters)
