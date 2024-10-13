"""
All configurations for pyrelist
"""
from pytconf import Config, ParamCreator


class ConfigMatch(Config):
    """
    Config options for the match operation
    """
    patterns = ParamCreator.create_existing_file(
        help_string="Which file to load regexps from?",
        suffixes=[".json"]
    )
