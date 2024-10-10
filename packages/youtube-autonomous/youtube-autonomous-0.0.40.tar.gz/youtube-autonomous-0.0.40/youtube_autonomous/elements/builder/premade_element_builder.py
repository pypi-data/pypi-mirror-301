from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from yta_multimedia.video.generation.google.google_search import GoogleSearch
from yta_multimedia.video.generation.google.youtube_search import YoutubeSearch
from yta_general_utils.programming.enum import YTAEnum as Enum
from typing import Union


# I don't know exactly how to manage this because I have
# classes and then the name that actually I make to be
# corresponding to that class
class Premade(Enum):
    GOOGLE_SEARCH = 'google_search'
    YOUTUBE_SEARCH = 'youtube_search'

class PremadeElementBuilder(ElementBuilder):
    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        premade_name = enhancement.keywords

        ElementParameterValidator.validate_premade_name(premade_name)

        parameters = super().extract_extra_params(enhancement, cls.premade_name_to_class(premade_name).__init__)

        return cls.build_custom_from_premade_name(premade_name, **parameters)

    @classmethod
    def build_from_segment(cls, segment: dict):
        premade_name = segment.keywords

        ElementParameterValidator.validate_premade_name(premade_name)

        parameters = super().extract_extra_params(segment, cls.premade_name_to_class(premade_name).__init__)

        return cls.build_custom_from_premade_name(premade_name, **parameters)

    @classmethod
    def premade_name_to_class(cls, premade_name: str):
        """
        Returns the corresponding premade class according to the
        provided 'premade_name'. If no premade class found, the
        return will be None.
        """
        premade_class = None

        if premade_name == Premade.GOOGLE_SEARCH.value:
            premade_class = GoogleSearch
        elif premade_name == Premade.YOUTUBE_SEARCH.value:
            premade_class = YoutubeSearch
        
        return premade_class

    @classmethod
    def build_custom_from_premade_name(cls, premade_name: str, **parameters):
        ElementParameterValidator.validate_premade_name(premade_name)

        premade_class = cls.premade_name_to_class(premade_name)
        if not premade_class:
            raise Exception(f'The provided "premade_name" parameter {premade_name} is not a valid premade name.')

        return cls.build_custom(premade_class, **parameters)

    @classmethod
    def build_custom(cls, premade, **parameters):
        # TODO: Make the premades implement an abstract class named
        # 'Premade' to be able to detect them as subclasses
        return premade(**parameters).generate()

    @classmethod
    def build(cls, text: str, duration: Union[float, int]):
        """
        Basic example to test that the building process and
        the class are working correctly.

        TODO: Remove this in the future when 'custom' is 
        working perfectly.
        """
        ElementParameterValidator.validate_text(text)
        ElementParameterValidator.validate_duration(duration)

        return GoogleSearch(text).generate()