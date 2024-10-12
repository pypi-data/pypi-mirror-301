
from youtube_autonomous.elements.validator.error_message import ErrorMessage
from youtube_autonomous.segments.enums import SegmentType, EnhancementType, SegmentStatus, ProjectStatus
from youtube_autonomous.segments.enhancement.edition_manual.enums import EditionManualTermContext, EditionManualTermMode
from youtube_autonomous.elements.validator import RULES_SUBCLASSES, BUILDER_SUBCLASSES
from yta_general_utils.programming.parameter_validator import ParameterValidator
from yta_general_utils.file.filename import FileType
from typing import Union


class ElementParameterValidator(ParameterValidator):
    """
    A validator that will raise an Exception if any of the used
    checkings is invalid, or will return the value if ok.
    """
    @classmethod
    def validate_keywords(cls, keywords: str):
        cls.validate_string_mandatory_parameter('keywords', keywords)

        return keywords

    @classmethod
    def validate_text(cls, text: str):
        cls.validate_string_mandatory_parameter('text', text)

        return text
    
    @classmethod
    def validate_premade_name(cls, premade_name: str):
        cls.validate_string_mandatory_parameter('premade_name', premade_name)
        # TODO: Maybe validate that is a key of a valid premade (?)

        return premade_name
    
    @classmethod
    def validate_text_class_name(cls, text_class_name: str):
        cls.validate_string_mandatory_parameter('text_class_name', text_class_name)
        # TODO: Maybe validate that is a key of a valid text_class (?)

        return text_class_name
    
    @classmethod
    def validate_duration(cls, duration: Union[int, float]):
        # TODO: Maybe validate that is a key of a valid text class (?)
        cls.validate_numeric_positive_mandatory_parameter('duration', duration)

        return duration
    
    @classmethod
    def validate_url(cls, url: str, is_mandatory: bool = True):
        """
        A mandatory 'url' must be not None, a valid string and also
        a valid url and accessible.

        A non mandatory 'url' can be None, 
        """
        if not is_mandatory and not url:
            return True
        
        cls.validate_mandatory_parameter('url', url)
        cls.validate_string_parameter('url', url)
        cls.validate_url_is_ok('url', url)
        # TODO: Validate 'url' file is some FileType

        return url

    @classmethod
    def validate_filename(cls, filename: str, file_type: FileType = FileType.IMAGE, is_mandatory: bool = True):
        """
        Validates the 'filename' parameter. If the 'filename' parameter has
        some value, all conditions will be checked. If there is not 'filename'
        and 'is_mandatory' is False, no Exceptions will be raised because it
        is valid.
        """
        if not is_mandatory and not filename:
            return True
        
        cls.validate_mandatory_parameter('filename', filename)
        cls.validate_string_parameter('filename', filename)
        cls.validate_file_exists('filename', filename)
        if file_type:
            cls.validate_filename_is_type('filename', filename, file_type)
            # TODO: Validate type trying to instantiate it

        return filename

    @classmethod
    def validate_rules(cls, rules: 'ElementRules'):
        if type(rules).__name__ not in RULES_SUBCLASSES:
            raise Exception(ErrorMessage.parameter_is_not_rules('rules'))
        
        return rules
        
    @classmethod
    def validate_builder(cls, builder: 'ElementBuilder'):
        if type(builder).__name__ not in BUILDER_SUBCLASSES:
            raise Exception(ErrorMessage.parameter_is_not_builder('builder'))
        
        return builder
        
    @classmethod
    def validate_segment_type(cls, type: Union[SegmentType, str]):
        """
        This method validates that the provided 'type' is not None
        and is a valid type and accepted for Segment building.

        This method raises an Exception if something is wrong
        and returns the type as a SegmentType enum if everything
        was ok.
        """
        return cls.validate_enum(type, SegmentType)

    @classmethod
    def validate_enhancement_type(cls, type: Union[EnhancementType, str]):
        """
        Validates that the provided 'type' is not None
        and is a valid type and accepted for Enhancement building.

        This method raises an Exception if something is wrong
        and returns the type as a EnhancementType enum if 
        everything was ok.
        """
        return cls.validate_enum(type, EnhancementType)
    
    @classmethod
    def validate_segment_or_enhancement_type(cls, type: Union[SegmentType, EnhancementType, str]):
        """
        Validates if the provided 'type' is a valid SegmentType or
        EnhancementType enum object, or a valid SegmentType or 
        EnhancementType enum value, raising an Exception if not.

        This method will return the type as the corresponding 
        enum if everything is ok.
        """
        enum_type = None
        try:
            enum_type = cls.validate_segment_type(type)
        except Exception:
            pass

        if not enum_type:
            try:
                enum_type = cls.validate_enhancement_type(type)
            except Exception:
                pass

        if not enum_type:
            raise Exception(f'The "type" parameter provided {type} is not a valid SegmentType or EnhancementType.')
        
        return enum_type

    @classmethod
    def validate_segment_status(cls, status: Union[SegmentStatus, str]):
        """
        Validates if the provided 'status' is not None and is
        a valid SegmentStatus Enum or string value.

        This method raises an Exception if something is wrong
        and returns the status as a SegmentStatus enum if 
        everything was ok.
        """
        return cls.validate_enum(status, SegmentStatus)
    
    @classmethod
    def validate_project_status(cls, status: Union[ProjectStatus, str]):
        """
        Validates if the provided 'status' is not None and is
        a valid SegmentStatus Enum or string value.

        This method raises an Exception if something is wrong
        and returns the status as a ProjectStatus enum if 
        everything was ok.
        """
        return cls.validate_enum(status, ProjectStatus)
    
    @classmethod
    def validate_edition_manual_term_mode(cls, mode: Union[EditionManualTermMode, str]):
        """
        Validates if the provided 'mode' is not None and is
        a valid EditionManualTermMode Enum or string value.

        This method raises an Exception if something is wrong
        and returns the mode as an EditionManualTermMode enum 
        if everything was ok.
        """
        return cls.validate_enum(mode, EditionManualTermMode)
        
    @classmethod
    def validate_edition_manual_term_context(cls, context: Union[EditionManualTermContext, str]):
        """
        Validates if the provided 'context' is not None and
        is a valid EditionManualTermContext Enum or string 
        value.

        This method raises an Exception if something is wrong
        and returns the mode as an EditionManualTermContext 
        enum if everything was ok.
        """
        return cls.validate_enum(context, EditionManualTermContext)
    
    @classmethod
    def validate_edition_manual_term(cls, edition_manual_term: dict):
        """
        This method verifies if the provided 'dict' has a valid
        structure for an EditionManualTerm, which has to be a key
        and a dict value containing all the required fields.

        This method will raise an Exception if something is wrong.
        """
        #_, dict = edition_manual_term
        term, term_content = next(iter(edition_manual_term.items()))

        # TODO: Apply Enums
        ElementParameterValidator.validate_edition_manual_term_mode(term_content.get('mode', None))
        ElementParameterValidator.validate_edition_manual_term_context(term_content.get('context', None))

        enhancements = term_content.get('enhancements', None)
        if enhancements is None:
            raise Exception('No "enhancements" field found in the provided "edition_manual_term".')
        
        if len(enhancements) == 0:
            raise Exception('The "enhancements" field is empty.')

        # TODO: Cyclic import error
        # for enhancement in enhancements:
        #     ElementParameterValidator.validate_segment_or_enhancement(enhancement)

    @classmethod
    def validate_transcription_parameter(cls, transcription: list[dict]):
        if any(key not in transcription_word for key in ['text', 'start', 'end'] for transcription_word in transcription):
            raise Exception('At least one term of the provided "transcription" parameter has no "text", "start" or "end" field.')