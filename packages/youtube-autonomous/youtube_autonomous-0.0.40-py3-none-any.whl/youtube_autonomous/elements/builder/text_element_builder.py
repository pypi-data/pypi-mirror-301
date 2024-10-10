from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.segments.enums import SegmentField
from yta_multimedia.video.generation.manim.classes.text.text_word_by_word_manim_animation import TextWordByWordManimAnimation
from moviepy.editor import VideoFileClip
from typing import Union


class TextElementBuilder(ElementBuilder):
    @classmethod
    def build_custom_from_text_class_name(cls, text_class_name: str, **parameters):
        ElementParameterValidator.validate_text_class_name(text_class_name)

        text_class = None
        if text_class == 'text_word_by_word':
            text_class = TextWordByWordManimAnimation
        else:
            raise Exception(f'The provided "text_class" parameter {text_class} is not a valid text class name.')
        
        return cls.build_custom(text_class, **parameters)


    @classmethod
    def build_custom(cls, text_animation_class, **parameters):
        """
        This method instantiates the 'text_animation_class' Manim
        text animation class and uses the provided 'parameters' to
        build the text animation. The provided 'parameters' must 
        fit the ones requested by the provided class 'generate'
        method.
        """
        raise Exception('Not implemented yet.')
        # TODO: Apply TextManimAnimation to 'text_animatino_class'
        # TODO: Check that 'text_animation_class' is subclass of 
        # abstract TextManimAnimation (that I need to create)
        # TODO: Check that I have the required parameters. Is
        # this possible (?)
        filename = text_animation_class().generate(**parameters)

        return VideoFileClip(filename)

    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        # TODO: This parameter must be an enum and, is this the definitive
        # one (?)
        # TODO: If narration, the transcription should be here, if no 
        # narration, the text
        text = enhancement.get('text', None)
        # TODO: I should always have 'calculated_duration' when duration
        # has been processed
        duration = enhancement.get('calculated_duration', None)

        return cls.build(text, duration)

    @classmethod
    def build_from_segment(cls, segment: dict):
        text = segment.get(SegmentField.TEXT.value, None)
        duration = segment.get(SegmentField.DURATION.value, None)

        return cls.build(text, duration)

    @classmethod
    def build(cls, text: str, duration: Union[int, float]):
        """
        Basic example to test that the building process and
        the class are working correctly.

        TODO: Remove this in the future when 'custom' is 
        working perfectly.
        """
        ElementParameterValidator.validate_text(text)
        ElementParameterValidator.validate_duration(duration)

        filename = TextWordByWordManimAnimation().generate(text, duration)

        video = VideoFileClip(filename)

        return video