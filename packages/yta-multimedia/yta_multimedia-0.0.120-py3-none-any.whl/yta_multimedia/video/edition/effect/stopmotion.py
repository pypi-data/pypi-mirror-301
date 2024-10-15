from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from yta_multimedia.video.frames import get_frame_from_video_by_frame_number
from moviepy.editor import CompositeVideoClip, VideoFileClip, ImageClip, concatenate_videoclips
from typing import Union


class StopMotionVideoEffect(VideoEffect):
    """
    Creates a Stop Motion effect in the provided video by dropping the frames
    per second but maintaining the original frames ratio.
    """
    
    @staticmethod
    def apply(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip]):
        """
        Applies the effect on the provided 'clip'.
        """
        clip = super().parse_moviepy_video(clip)

        FRAMES_TO_JUMP = 5

        clips = []
        for frame_number in range((int) (clip.fps * clip.duration)):
            if frame_number % FRAMES_TO_JUMP == 0:
                frame = get_frame_from_video_by_frame_number(clip, frame_number)
                clips.append(ImageClip(frame, duration = FRAMES_TO_JUMP / clip.fps).set_fps(clip.fps))

        return concatenate_videoclips(clips).set_audio(clip.audio).set_fps(clip.fps)


    