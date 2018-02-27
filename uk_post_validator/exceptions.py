# Inward code exceptions
class InwardCodeError(ValueError):
    """ Generic inward code error. """
    pass


class InvalidInwardCodeFormatError(InwardCodeError):
    """ Inward code format is not correct. """
    pass


class InvalidSectorValueError(InwardCodeError):
    """ Sector value of inward code is not correct. """
    pass


class InvalidUnitValueError(InwardCodeError):
    """ Unit value of inward code is not correct. """
    pass


# Outward code exceptions
class OutwardCodeError(ValueError):
    """ Generic outward code error. """
    pass


class InvalidOutwardCodeFormatError(OutwardCodeError):
    """ Outward code format is not correct. """
    pass


class InvalidAreaValueError(OutwardCodeError):
    """ Area value of outward code is not correct. """
    pass


class InvalidDistrictValueError(OutwardCodeError):
    """ District value of outward code is not correct. """
    pass


# Post code exceptions
class PostCodeError(ValueError):
    """ Generic post code error. """
    pass


class InvalidPostCodeFormatError(PostCodeError):
    """ Post code format is not correct. """
    pass


class SingleDigitDistrictAreaFormatError(InvalidPostCodeFormatError):
    """ Area should have single digit district """
    pass


class DoubleDigitDistrictAreaFormatError(InvalidPostCodeFormatError):
    """ Area should have double digit district """
    pass


class NonZeroDistrictAreaFormatError(InvalidPostCodeFormatError):
    """ Area does not allow zero digit district """
    pass


class AreaCharacterNotAllowedError(InvalidPostCodeFormatError):
    """ Inappropriate character in area value """
    pass


class DistrictCharacterNotAllowedError(InvalidPostCodeFormatError):
    """ Inappropriate character in district value """
    pass


class UnitCharactersNotAllowedError(InvalidPostCodeFormatError):
    """ Inappropriate character in unit value """
    pass


# Parsing exceptions
class PostCodeParsingError(ValueError):
    """
    There was an error while trying to parse a post code.
    """
    pass


class OutwardCodeParsingError(ValueError):
    """
    There was an error while trying to parse an outward code.
    """
    pass


class InwardCodeParsingError(ValueError):
    """
    There was an error while trying to parse an inward code.
    """
    pass
