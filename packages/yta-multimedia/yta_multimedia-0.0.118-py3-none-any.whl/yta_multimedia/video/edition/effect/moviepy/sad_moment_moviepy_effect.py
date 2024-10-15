from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, AudioFileClip, ColorClip, vfx
from typing import Union
from yta_multimedia.resources.video.effect.sound.drive_urls import SAD_MOMENT_GOOGLE_DRIVE_DOWNLOAD_URL
from yta_multimedia.resources import get_resource
from yta_multimedia.video.edition.effect.constants import EFFECTS_RESOURCES_FOLDER


class SadMomentMoviepyEffect(VideoEffect):
    """
    This method gets the first frame of the provided 'clip' and returns a
    new clip that is an incredible 'sad_moment' effect with black and white
    filter, zoom in and rotating effect and also sad violin music.

    The 'duration' parameter is to set the returned clip duration, but the
    default value is a perfect one.
    """
    
    @staticmethod
    def apply(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], duration = None):
        """
        Applies the effect to the provided 'clip'.
        """
        clip = super().parse_moviepy_video(clip)

        if not duration:
            duration = 4.8

        # We freeze the first frame
        aux = ImageClip(clip.get_frame(0), duration = duration)
        aux.fps = clip.fps
        clip = aux

        # We then build the whole effect
        clip = clip.fx(vfx.blackwhite).resize(lambda t: 1 + 0.30 * (t / clip.duration)).set_position(lambda t: (-(0.15 * clip.w * (t / clip.duration)), -(0.15 * clip.h * (t / clip.duration)))).rotate(lambda t: 5 * (t / clip.duration), expand = False)

        # We set the effect audio
        TMP_FILENAME = get_resource(SAD_MOMENT_GOOGLE_DRIVE_DOWNLOAD_URL, EFFECTS_RESOURCES_FOLDER + 'sounds/sad_moment.mp3')
        clip.audio = AudioFileClip(TMP_FILENAME).set_duration(clip.duration)

        return CompositeVideoClip([
            ColorClip(color = [0, 0, 0], size = clip.size, duration = clip.duration),
            clip,
        ])