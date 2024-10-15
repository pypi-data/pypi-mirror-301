from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from yta_multimedia.resources.video.effect.sound.drive_urls import PHOTO_GOOGLE_DRIVE_DOWNLOAD_URL
from yta_multimedia.video.edition.effect.moviepy.blink_moviepy_effect import BlinkMoviepyEffect
from yta_multimedia.resources import get_resource
from yta_multimedia.video.edition.effect.constants import EFFECTS_RESOURCES_FOLDER
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, CompositeAudioClip, AudioFileClip, concatenate_videoclips
from typing import Union


class PhotoMoviepyEffect(VideoEffect):
    """
    Simulates that a photo is taken by making a white blink and
    a camera click sound.
    """
    
    @staticmethod
    def apply(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip]):
        """
        Applies the effect to the provided 'clip'.
        """
        clip = super().parse_moviepy_video(clip)

        TMP_FILENAME = get_resource(PHOTO_GOOGLE_DRIVE_DOWNLOAD_URL, EFFECTS_RESOURCES_FOLDER + 'sounds/photo_taken.mp3')

        # We force the effect to be last as much as the clip
        clip = concatenate_videoclips([
            BlinkMoviepyEffect.apply(clip, [255, 255, 255]),
        ])
        
        clip.audio = CompositeAudioClip([
            clip.audio,
            AudioFileClip(TMP_FILENAME).set_duration(clip.duration)
        ])

        return clip

        # This below was working previously but not for the whole clip
        # if clip.duration == effect_duration:
        #     # If clip is shorter than our default effect duration time, do it with
        #     # the clip duration
        #     clip = BlinkMoviepyEffect.apply(clip, effect_duration, [255, 255, 255])
        # else:
        #     # We force the effect to be 'effect_duration' seconds longer and in the
        #     # middle of the provided clip
        #     half_duration = self.__clip.duration / 2
        #     half_effect_duration = effect_duration / 2
        #     self.__clip = concatenate_videoclips([
        #         self.__clip.subclip(0, half_duration - effect_duration),
        #         BlinkMoviepyEffect(self.__clip.subclip(half_duration - half_effect_duration, half_duration + half_effect_duration), effect_duration, [255, 255, 255]).apply(),
        #         self.__clip.subclip(half_duration + half_effect_duration, self.__clip.duration)
        #     ])
        
        # self.__clip.audio = CompositeAudioClip([
        #     self.__clip.audio,
        #     AudioFileClip(TMP_FILENAME).set_duration(effect_duration)
        # ])

        # return self.__clip