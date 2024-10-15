from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union
from skimage.filters import gaussian


class BlurMoviepyEffect(VideoEffect):
    """
    This effect will zoom out the clip, on the center.

    TODO: This effect is not smooth as it makes it have
    a black border. Maybe removing it (?)
    """

    @staticmethod
    def apply(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], blur_radius = None):
        """
        Applies the effect to the provided 'clip'.
        """
        clip = super().parse_moviepy_video(clip)

        if blur_radius is None:
            blur_radius = 4

        return clip.fl(lambda get_frame, t: gaussian(get_frame(t).astype(float), sigma = blur_radius))
