import pytest

from uk_post_validator import exceptions
from uk_post_validator.outward_code import OutwardCode
from uk_post_validator.parsers import outward_parser
from uk_post_validator.exceptions import OutwardCodeParsingError
from uk_post_validator.validators import outward_validators


class TestOutwardParsers:
    @pytest.mark.parametrize(
        "complete_code, expected_area, expected_district", [
            ('EC1A', 'EC', '1A'),
            ('W1A', 'W', '1A'),
            ('M1', 'M', '1'),
            ('B33', 'B', '33'),
            ('CR2', 'CR', '2'),
            ('DN55', 'DN', '55'),
            ('DN55AAA55', 'DN', '55AAA55'),
        ]
    )
    def test_outward_code_is_divided_into_components_correctly(
            self,
            complete_code,
            expected_area,
            expected_district
    ):
        area, district = outward_parser.divide_outward_code_in_components(
            complete_code
        )

        assert expected_area == area
        assert expected_district == district

    @pytest.mark.parametrize(
        "complete_code", [
            '1AA', 'AAAA', '1111', '',
        ]
    )
    def test_outward_code_raises_exception_when_tries_parsing_incorrect_values(
            self,
            complete_code
    ):
        with pytest.raises(OutwardCodeParsingError):
            outward_parser.divide_outward_code_in_components(complete_code)


class TestOutwardValidators:
    @pytest.mark.parametrize("area", [
        'A',
        'a',
        'AA',
        'aa',
    ])
    def test_area_validators_for_correct_values(self, area):
        assert outward_validators.validate_area(area) is True

    @pytest.mark.parametrize("area", [
        '',
        None,
        object,
        [],
        '1',
        'A1',
        '*',
        '11',
        'aaa'
    ])
    def test_area_validators_for_invalid_values(self, area):
        with pytest.raises(exceptions.InvalidAreaValueError):
            outward_validators.validate_area(area)

    @pytest.mark.parametrize("district", [
        '0',
        '9',
        '10',
        '99',
        '9A',
        '9a',
    ])
    def test_district_for_correct_values(self, district):
        assert outward_validators.validate_district(district) is True

    @pytest.mark.parametrize("district", [
        '00',
        '01',
        '990',
        '999',
        'A9',
        'AA',
        'A',
        '',
        None,
        object,
        [],
    ])
    def test_district_validator_for_incorrect_values_raises_exception(self, district):
        with pytest.raises(exceptions.InvalidDistrictValueError):
            outward_validators.validate_district(district)

    @pytest.mark.parametrize("outward_code", [
        'A9',
        'A0',
        'A99',
        'A10',
        'A9A',
        'A0A',
        'AA9',
        'AA0',
        'AA99',
        'AA90',
        'AA9A',
        'AA0A',
    ])
    def test_complete_outward_code_validator_for_correct_values(self, outward_code):
        assert outward_validators.validate_outward_code(outward_code) is True

    @pytest.mark.parametrize("outward_code", [
        '9',
        '9A',
        '9AA',
        '9AAA',
        '9AAA',
        '99',
        '99A',
        '99AA',
        '99AA',
        '999A',
        'A999',
        'A111',
        'A00',
        'A01',
        'A09',
        'AA00',
        'AA01',
        'AA09',
        'AAA0',
        'A0A0',
        'A1A1'
    ])
    def test_outward_code_validator_raises_exception_for_incorrect_values(
            self,
            outward_code
    ):
        with pytest.raises(exceptions.InvalidOutwardCodeFormatError):
            outward_validators.validate_outward_code(outward_code)


class TestOutwardCodeObject:
    @pytest.mark.parametrize(
        "area, district, expected_area, expected_district, expected_code", [
            ('A', '9', 'A', '9', 'A9'),
            ('A', '99', 'A', '99', 'A99'),
            ('A', '9A', 'A', '9A', 'A9A'),
            ('AA', '9', 'AA', '9', 'AA9'),
            ('AA', '99', 'AA', '99', 'AA99'),
            ('AA', '9A', 'AA', '9A', 'AA9A'),
            ('a', 9, 'A', '9', 'A9'),
        ]
    )
    def test_creation_of_outward_code_for_valid_entry_values(
            self,
            area,
            district,
            expected_area,
            expected_district,
            expected_code
    ):
        outward_code = OutwardCode(area=area, district=district)
        assert expected_area == outward_code.area
        assert expected_district == outward_code.district
        assert expected_code == outward_code.code

    @pytest.mark.parametrize(
        "area, district, expected_exception", [
            ('', '', exceptions.InvalidAreaValueError),
            ('', '9A', exceptions.InvalidAreaValueError),
            (None, '', exceptions.InvalidAreaValueError),
            (object, '', exceptions.InvalidAreaValueError),
            ('1A', '', exceptions.InvalidAreaValueError),
            ('11', '', exceptions.InvalidAreaValueError),
            ('A1', '', exceptions.InvalidAreaValueError),
            ('AAA', '', exceptions.InvalidAreaValueError),
            ('AA', '', exceptions.InvalidDistrictValueError),
            ('AA', None, exceptions.InvalidDistrictValueError),
            ('AA', object, exceptions.InvalidDistrictValueError),
            ('AA', 'A9', exceptions.InvalidDistrictValueError),
            ('AA', 'AA', exceptions.InvalidDistrictValueError),
            ('AA', 'A', exceptions.InvalidDistrictValueError),
        ]
    )
    def test_creation_of_outward_code_for_invalid_values(
            self,
            area,
            district,
            expected_exception
    ):
        with pytest.raises(expected_exception):
            OutwardCode(area=area, district=district)

    @pytest.mark.parametrize("area, district, expected_string", [
        ('AA', '9A', 'AA9A'),
        ('AA', '99', 'AA99'),
        ('A', '9A', 'A9A'),
        ('A', '99', 'A99'),
        ('AA', '9', 'AA9'),
        ('A', '9', 'A9'),

    ])
    def test_string_representation_outward_code(self, area, district, expected_string):
        assert expected_string == str(OutwardCode(area=area, district=district))

    @pytest.mark.parametrize(
        "expected_area, expected_district, complete_outward_code", [
            ('AA', '9A', 'AA9A'),
            ('AA', '99', 'AA99'),
            ('A', '9A', 'A9A'),
            ('A', '99', 'A99'),
            ('AA', '9', 'AA9'),
            ('A', '9', 'A9'),
        ]
    )
    def test_inward_class_object_creation_by_complete_code(
            self,
            expected_area,
            expected_district,
            complete_outward_code
    ):
        outward_code: OutwardCode = OutwardCode.create_from_complete_outward_code(
            complete_outward_code
        )
        assert expected_area == outward_code.area
        assert expected_district == outward_code.district
        assert complete_outward_code == outward_code.code


