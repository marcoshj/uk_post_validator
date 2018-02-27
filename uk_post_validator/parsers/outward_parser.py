import re
from typing import Tuple

from uk_post_validator.exceptions import OutwardCodeParsingError


def divide_outward_code_in_components(outward_code: str) -> Tuple[str, str]:
    """
    Divide a string containing the full outward code
    into area and district.
    """

    try:
        area, district = re.split(r'(^[^\d]+)', outward_code)[1:]
    except (ValueError, TypeError):
        raise OutwardCodeParsingError(
            'Cannot find area and district for specified outward code'
        )

    if not all([area, district]):
        raise OutwardCodeParsingError('Nor area nor district can be empty')

    return area, district
