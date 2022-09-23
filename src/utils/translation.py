import functools
import gettext
import typing


@functools.lru_cache(maxsize=64)
def get_translate_function(language: str = 'en_US') -> typing.Callable:
    gettext.bindtextdomain("app", "locales")
    gettext.textdomain("app")
    translation = gettext.translation('app', localedir='locales', languages=[language])
    translation.install()
    return translation.gettext


def translate(text: str, language_code: str):
    translate_function = get_translate_function(language_code)
    return translate_function(text)
