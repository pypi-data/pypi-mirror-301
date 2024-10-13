"""
All configurations for pycookie
"""
from pytconf import Config, ParamCreator


class ConfigDemo(Config):
    """
    Parameters to control ...
    """
    map_size = ParamCreator.create_int(
        help_string="Which size of mmap to use?",
        default=1000000000000,
    )
