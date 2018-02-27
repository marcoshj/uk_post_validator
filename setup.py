from distutils.core import setup


setup(
    name='uk_post_validator',
    version='1.0',
    description='A tool for validating and formatting UK Postcodes',
    author='Marcos Hernandez Juarez',
    author_email='marcos.hernandezjuarez@gmail.com',
    url='https://gitlab.com/marcoshj/uk-postcode-validator/',
    packages=['uk_post_validator', 'uk_post_validator.parsers', 'uk_post_validator.validators'],
)
