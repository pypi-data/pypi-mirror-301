from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.segments.enums import SegmentField
from yta_multimedia.video.generation.manim.classes.text.text_word_by_word_manim_animation import TextWordByWordManimAnimation
from yta_multimedia.video.generation.manim.classes.text.text_triplets_manim_animation import TextTripletsManimAnimation
from yta_general_utils.programming.enum import YTAEnum as Enum
from moviepy.editor import VideoFileClip
from typing import Union


# I don't know exactly how to manage this because I have
# classes and then the name that actually I make to be
# corresponding to that class
class TextPremade(Enum):
    TEXT_TRIPLETS = 'text_triplets'

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
    def build_from_enhancement(cls, enhancement: dict):
        text_premade_name = enhancement.keywords

        ElementParameterValidator.validate_premade_name(text_premade_name)

        parameters = super().extract_extra_params(enhancement, cls.text_premade_name_to_class(text_premade_name).generate, ['self', 'cls', 'args', 'kwargs', 'output_filename'])

        return cls.build_custom_from_premade_name(text_premade_name, **parameters)

    @classmethod
    def build_from_segment(cls, segment: dict):
        text_premade_name = segment.keywords

        ElementParameterValidator.validate_premade_name(text_premade_name)

        parameters = super().extract_extra_params(segment, cls.text_premade_name_to_class(text_premade_name).generate, ['self', 'cls', 'args', 'kwargs', 'output_filename'])

        return cls.build_custom_from_premade_name(text_premade_name, **parameters)
    
    @classmethod
    def text_premade_name_to_class(cls, text_premade_name: str):
        """
        Returns the corresponding text premade class according to
        the provided 'text_premade_name'. If no text premade class
        found, the return will be None.
        """
        text_premade_class = None

        if text_premade_name == TextPremade.TEXT_TRIPLETS.value:
            text_premade_class = TextTripletsManimAnimation
        else:
            raise Exception(f'The provided text premade name "{text_premade_name}" is not valid. The valid ones are: {TextPremade.get_all_values_as_str()}')
        
        return text_premade_class

    @classmethod
    def build_custom_from_text_premade_name(cls, text_premade_name, **parameters):
        """
        This method instantiates the 'text_animation_class' Manim
        text animation class and uses the provided 'parameters' to
        build the text animation. The provided 'parameters' must 
        fit the ones requested by the provided class 'generate'
        method.
        """
        ElementParameterValidator.validate_premade_name(text_premade_name)

        text_premade_class = cls.text_premade_name_to_class(text_premade_name)

        # We generate the animation to return it
        filename = text_premade_class().generate(**parameters)

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