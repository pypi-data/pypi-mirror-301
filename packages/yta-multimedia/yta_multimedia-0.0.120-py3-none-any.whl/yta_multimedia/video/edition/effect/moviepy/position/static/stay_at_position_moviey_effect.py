from yta_multimedia.video.edition.effect.moviepy.position.objects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate_center import CoordinateCenter
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate_corner import CoordinateCorner
from yta_multimedia.video.edition.effect.moviepy.position.enums import ScreenPosition
from yta_multimedia.video.edition.effect.moviepy.position.utils.position import position_video_in
from yta_general_utils.file.checker import file_is_video_file
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip
from typing import Union


class StayAtPositionMoviepyEffect(BasePositionMoviepyEffect):
    """
    Effect of keeping the given 'video' inmobile in a specific
    position given (if given as parameter when applying) or randomly
    generated (inside the bounds according to the also provided
    'background_video' dimensions).
    """

    @staticmethod
    def apply(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], position: Union[ScreenPosition, CoordinateCorner, CoordinateCenter] = ScreenPosition.RANDOM_INSIDE):
        return StayAtPositionMoviepyEffect.apply_over_video(clip, super().get_black_background_clip(clip.duration), position)

    @staticmethod
    def apply_over_video(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], background_clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], position: Union[ScreenPosition, CoordinateCorner, CoordinateCenter] = ScreenPosition.RANDOM_INSIDE):
        super().validate_position(position)

        background_clip = super().apply_over_video(background_clip)

        effect = position_video_in(clip, background_clip, position).set_start(0).set_duration(clip.duration)

        return CompositeVideoClip([
            background_clip,
            effect
        ])