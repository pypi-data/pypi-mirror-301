from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union


class ChangeSpeedMoviepyEffect(VideoEffect):
    """
    This effect changes the speed of the video to fit the requested
    'final_duration', that will accelerate or decelerate the video
    speed.
    """

    @staticmethod
    def apply(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], final_duration = None):
        """
        Applies the effect to the provided 'clip'.
        """
        clip = super().parse_moviepy_video(clip)

        if final_duration is None:
            final_duration = clip.duration

        effect_name = super().get_moviepy_vfx_effect('speedx')
        parameters = {
            'final_duration': final_duration
        }

        return clip.fx(effect_name, **parameters)
