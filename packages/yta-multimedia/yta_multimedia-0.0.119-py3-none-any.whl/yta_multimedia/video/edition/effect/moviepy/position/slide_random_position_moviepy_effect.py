from yta_multimedia.video.edition.effect.moviepy.position.objects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.move import MoveLinearPositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.static import StayAtPositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.enums import ScreenPosition
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips
from typing import Union


class SlideRandomPositionMoviepyEffect(BasePositionMoviepyEffect):
    """
    Effect of appearing from TOP, TOP_LEFT, BOTTOM, RIGHT, etc. 
    staying at the center, and dissapearing from the opposite 
    edge. This animation will spend 1/6 of the time in the 
    entrance, 4/6 of the time staying at the center, and 1/6 of 
    the time in the exit.
    """

    @staticmethod
    def apply(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip]):
        return SlideRandomPositionMoviepyEffect.apply_over_video(clip, super().get_black_background_clip(clip.duration))

    @staticmethod
    def apply_over_video(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], background_clip: Union[VideoFileClip, CompositeVideoClip, ImageClip]):
        background_clip = super().apply_over_video(background_clip)

        random_position = ScreenPosition.in_and_out_positions_as_list()

        movement_time = background_clip.duration / 6
        stay_time = background_clip.duration / 6 * 4

        effect = concatenate_videoclips([
            MoveLinearPositionMoviepyEffect(clip.subclip(0, movement_time)).apply_over_video(background_clip.subclip(0, movement_time), random_position[0], ScreenPosition.CENTER),
            StayAtPositionMoviepyEffect(clip.subclip(movement_time, movement_time + stay_time)).apply_over_video(background_clip.subclip(movement_time, movement_time + stay_time), ScreenPosition.CENTER),
            MoveLinearPositionMoviepyEffect(clip.subclip(movement_time + stay_time, clip.duration)).apply_over_video(background_clip.subclip(movement_time + stay_time, clip.duration), ScreenPosition.CENTER, random_position[1])
        ])

        return effect