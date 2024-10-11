from yta_multimedia.video.utils import generate_videoclip_from_image
from yta_multimedia.resources.image.drive_urls import YOUTUBE_SEARCH_IMAGE_GOOGLE_DRIVE_DOWNLOAD_URL
from yta_multimedia.audio.sound.generation.sound_generator import SoundGenerator
from yta_multimedia.resources import get_resource
from yta_multimedia.video.edition.effect.constants import EFFECTS_RESOURCES_FOLDER
from moviepy.editor import TextClip, CompositeVideoClip


# TODO: This is too repetitive with the same videos around the search
# please, make it dynamic, maybe with scrapper and saving frames
class YoutubeSearch():
    __EXTENDED_DURATION = 0.5
    __DURATION = 3

    def __init__(self, text):
        self.text = text

    def generate(self):
        # Download the resource we need
        TMP_FILENAME = get_resource(YOUTUBE_SEARCH_IMAGE_GOOGLE_DRIVE_DOWNLOAD_URL, EFFECTS_RESOURCES_FOLDER + 'images/youtube_search.png')
        clip = clip = generate_videoclip_from_image(TMP_FILENAME, self.__DURATION + self.__EXTENDED_DURATION)

        # Calculate each char duration and set texts according to this
        text_len = len(self.text)
        each_char_duration = self.__DURATION / text_len

        clips = []
        for i in range(text_len):
            # Generate a text clip for each text writing part
            txt_clip = TextClip(self.text[:i + 1], font = 'Arial', fontsize = 25, color = 'black')
            clip_duration = each_char_duration
            
            if i == (text_len - 1):
                clip_duration = each_char_duration + self.__EXTENDED_DURATION
            
            txt_clip = txt_clip.set_position([540, 37]).set_duration(clip_duration).set_start(i * each_char_duration)

            clips.append(txt_clip)

        video = CompositeVideoClip([clip] + clips)
        # Here we have the text being written, we need the sound
        audio = SoundGenerator().create_typing_audio()
        video = video.set_audio(audio)

        return video