# Test suite developer notes

## Running the tests

Tests are run using the `pytest` command in the root of the project.

## Test teardown

`conftest.py` contains the code to delete the files and directories
created by the tests which need to be deleted at the end of the tests.

## WARNING

Do not delete or modify `tests/data` file as the test suite will start to fail!
