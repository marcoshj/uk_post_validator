from typing import Tuple

from uk_post_validator import exceptions
from uk_post_validator.parsers import outward_parser, inward_parser


def divide_post_code_in_components(post_code: str) -> Tuple[str, str, int, str]:
    """
    Divide a string containing the full post code into
    outward and inward components (area, district, sector and unit).
    """
    try:
        post_code_formatted = post_code.strip()

        outward_components = outward_parser.divide_outward_code_in_components(
            post_code_formatted[:-3].strip()
        )

        inward_components = inward_parser.divide_inward_code_in_components(
            post_code_formatted[-3:]
        )
    except AttributeError:
        raise exceptions.PostCodeParsingError(
            'Post code cannot be parsed: post code value is not correct'
        )

    return outward_components + inward_components
