from yta_multimedia.video.frames import get_frame_from_video_by_frame_number
from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from moviepy.editor import ImageClip, concatenate_videoclips


class StopMotionVideoEffect(VideoEffect):
    """
    Creates a Stop Motion effect in the provided video by dropping the frames
    per second but maintaining the original frames ratio.
    """
    def apply(self):
        # This value is this one by default by now
        FRAMES_TO_JUMP = 5

        clips = []
        for frame_number in range((int) (self.video.fps * self.video.duration)):
            if frame_number % FRAMES_TO_JUMP == 0:
                frame = get_frame_from_video_by_frame_number(self.video, frame_number)
                clips.append(ImageClip(frame, duration = FRAMES_TO_JUMP / self.video.fps).set_fps(self.video.fps))

        return concatenate_videoclips(clips).set_audio(self.video.audio).set_fps(self.video.fps)


    