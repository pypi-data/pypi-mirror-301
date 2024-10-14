from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from yta_multimedia.greenscreen.custom.image_greenscreen import ImageGreenscreen
from yta_multimedia.greenscreen.custom.video_greenscreen import VideoGreenscreen
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip, ImageClip, AudioFileClip, AudioClip, CompositeAudioClip
from typing import Union


class GreenscreenElementBuilder(ElementBuilder):
    """
    This builders allows you to generate 'GREENSCREEN' content.
    """
    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        filename = enhancement.filename
        url = enhancement.url
        # TODO: I need the 'segment' video to apply the greenscreen
        video = None

        # TODO: Make this dynamic, please
        return ImageGreenscreen('https://drive.google.com/file/d/1WQVnXY1mrw-quVXOqTBJm8x9scEO_JNz/view?usp=sharing')

        if filename:
            # TODO: Check if 'image' or 'video'
            is_video = True
            # TODO: Build with filename
            if is_video:
                return cls.build_with_video_greenscreen(filename, video)
            return cls.build_with_image_greenscreen(filename, video)
        # TODO: Check if 'image' or 'video'
        is_video = True
        # TODO: Build with url
        if is_video:
            return cls.build_with_video_greenscreen(url, video)
        return cls.build_with_image_greenscreen(url, video)

    # TODO: Remove this method below when the other one is dynamic
    @classmethod
    def build_with_video_greenscreen(cls, filename_or_google_drive_url: str, video: Union[VideoFileClip, CompositeVideoClip, ColorClip, ImageClip]):
        ElementParameterValidator.validate_string_mandatory_parameter('filename_or_google_drive_url', filename_or_google_drive_url)
        # TODO: Validate it is filename or url
        # TODO: Check if it is video or image to dynamically use 
        # the ImageGreenscreen or the VideoGreenscreen
        return VideoGreenscreen(filename_or_google_drive_url).from_video_to_video(video)

    @classmethod
    def build_with_image_greenscreen(cls, filename_or_google_drive_url: str, video: Union[VideoFileClip, CompositeVideoClip, ColorClip, ImageClip]):
        ElementParameterValidator.validate_string_mandatory_parameter('filename_or_google_drive_url', filename_or_google_drive_url)
        # TODO: Validate it is filename or url
        # TODO: Check if it is video or image to dynamically use 
        # the ImageGreenscreen or the VideoGreenscreen
        return ImageGreenscreen(filename_or_google_drive_url).from_video_to_video(video)

    @classmethod
    def build(cls, video: Union[VideoFileClip, CompositeVideoClip, ColorClip, ImageClip]):
        """
        Basic example to test that the building process and
        the class are working correctly.

        TODO: Remove this in the future when 'custom' is 
        working perfectly.
        """
        return ImageGreenscreen('https://drive.google.com/file/d/1WQVnXY1mrw-quVXOqTBJm8x9scEO_JNz/view?usp=sharing')

        return ImageGreenscreen('https://drive.google.com/file/d/1WQVnXY1mrw-quVXOqTBJm8x9scEO_JNz/view?usp=sharing').from_video_to_video(video)
        # return VideoGreenscreen('https://drive.google.com/file/d/1hL677Q87jn-_y5vqSwev3lir_dCYRQwS/view?usp=sharing').apply()