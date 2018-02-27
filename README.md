# UK POSTCODE VALIDATOR
A library that supports validating and formatting post codes for UK.

Supports only Python 3

## Development
Is highly recommended using a virtual environment to develop
on this project.

Python 3 is required.

To install development dependencies, run:
```
pip install -r requirements_dev.txt
```


### Run unit tests
Tests are being run under pytest, so, to run test suite just run:
```
pytest
```

### Run mutation tests
Mutation tests are being done using cosmic ray. Run the following
command to execute and run results:
```
cosmic-ray init mutation-test-config.yml mutation-test-result
cosmic-ray --verbose exec mutation-test-result.json
cosmic-ray dump mutation-test-result.json | cr-report
```
