from yta_multimedia.video.generation.google.google_search import GoogleSearch
from yta_multimedia.video.generation.google.youtube_search import YoutubeSearch
from yta_multimedia.video.generation.manim.classes.text.text_triplets_manim_animation import TextTripletsManimAnimation
from yta_multimedia.video.generation.manim.classes.text.text_word_by_word_manim_animation import TextWordByWordManimAnimation
from yta_multimedia.video.generation.manim.classes.text.simple_text_manim_animation import SimpleTextManimAnimation
from yta_multimedia.video.generation.manim.classes.text.rain_of_words_manim_animation import RainOfWordsManimAnimation
from yta_multimedia.video.generation.manim.classes.text.magazine_text_static_manim_animation import MagazineTextStaticManimAnimation
from yta_multimedia.video.generation.manim.classes.text.magazine_text_is_written_manim_animation import MagazineTextIsWrittenManimAnimation
from yta_multimedia.video.edition.effect.moviepy.black_and_white_moviepy_effect import BlackAndWhiteMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.blink_moviepy_effect import BlinkMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.blur_moviepy_effect import BlurMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.change_speed_moviepy_effect import ChangeSpeedMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.fade_in_moviepy_effect import FadeInMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.fade_out_moviepy_effect import FadeOutMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.flip_horizontally_moviepy_effect import FlipHorizontallyMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.flip_vertically_moviepy_effect import FlipVerticallyMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.multiplied_moviepy_effect import MultipliedMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.photo_moviepy_effect import PhotoMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.reversed_moviepy_effect import ReversedMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.sad_moment_moviepy_effect import SadMomentMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.scroll_moviepy_effect import ScrollMoviepyEffect
from yta_multimedia.video.edition.effect.zoom.linear_zoom_video_effect import LinearZoomVideoEffect
from yta_multimedia.video.edition.effect.stopmotion import StopMotionVideoEffect
from yta_multimedia.video.edition.effect.moviepy.position.slide_random_position_moviepy_effect import SlideRandomPositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.static.circles_at_position_moviepy_effect import CirclesAtPositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.static.stay_at_position_moviey_effect import StayAtPositionMoviepyEffect
from yta_general_utils.programming.enum import YTAEnum as Enum


class Premade(Enum):
    """
    Premade enum class to make our multimedia premades available for the
    app by matching the corresponding class with an Enum variable that is
    used and enabled here.

    This enums are pretended to be matched by their name ignoring cases,
    so feel free to use the 'get_valid_name' YTAEnum method to obtain the
    valid name to be able to intantiate it.
    """
    GOOGLE_SEARCH = GoogleSearch
    YOUTUBE_SEARCH = YoutubeSearch

class TextPremade(Enum):
    """
    Text premade enum class to make our multimedia text premades available
    for the app by matching the corresponding class with an Enum variable
    that is used and enabled here.

    This enums are pretended to be matched by their name ignoring cases,
    so feel free to use the 'get_valid_name' YTAEnum method to obtain the
    valid name to be able to intantiate it.
    """
    TRIPLETS = TextTripletsManimAnimation
    WORD_BY_WORD = TextWordByWordManimAnimation
    SIMPLE = SimpleTextManimAnimation
    RAIN_OF_WORDS = RainOfWordsManimAnimation
    MAGAZINE_STATIC = MagazineTextStaticManimAnimation
    MAGAZINE_IS_WRITTEN = MagazineTextIsWrittenManimAnimation

class EffectPremade(Enum):
    """
    Effect premade enum class to make our multimedia effects available for
    the app by matching the corresponding class with an Enum variable that
    is used and enabled here.

    This enums are pretended to be matched by their name ignoring cases,
    so feel free to use the 'get_valid_name' YTAEnum method to obtain the
    valid name to be able to intantiate it.
    """
    BLACK_AND_WHITE = BlackAndWhiteMoviepyEffect
    BLINK = BlinkMoviepyEffect
    BLUR = BlurMoviepyEffect
    CHANGE_SPEED = ChangeSpeedMoviepyEffect
    FADE_IN = FadeInMoviepyEffect
    FADE_OUT = FadeOutMoviepyEffect
    FLIP_HORIZONTALLY = FlipHorizontallyMoviepyEffect
    FLIP_VERTICALLY = FlipVerticallyMoviepyEffect
    MULTIPLIED = MultipliedMoviepyEffect
    PHOTO = PhotoMoviepyEffect
    REVERSED = ReversedMoviepyEffect
    SAD_MOMENT = SadMomentMoviepyEffect
    SCROLL = ScrollMoviepyEffect
    LINEAR_ZOOM = LinearZoomVideoEffect
    STOP_MOTION = StopMotionVideoEffect
    SLIDE_RANDOM = SlideRandomPositionMoviepyEffect
    # Positioned
    CIRCLES_AT_POSITION = CirclesAtPositionMoviepyEffect
    STAY_AT_POSITION = StayAtPositionMoviepyEffect
