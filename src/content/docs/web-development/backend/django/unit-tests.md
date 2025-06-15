---
title: Unit Tests with Built-in
description: Unit tests commands
---

Commands to run unit tests
```bash
# Execute all the unit tests
./manage.py test
# OR
# python manage.py test

# Run all the tests found within the <app_name> package
./manage.py test <app_name>
# Example
./manage.py test vbgf

# Run all the tests in the <app_name>.unit_test module
./manage.py test <app_name>.unit_test

# Run just one test case class
./manage.py test <app_name>.unit_test.<TestCaseClass>
# Example
./manage.py test vbgf.unit_test.test_vbgf_calculations.VbgfCalculationsTestCase

# Run just one test method
./manage.py test <app_name>.unit_test.<TestCaseClass>.<testcase_method>

# can also provide a path to a directory to discover tests below that directory
./manage.py test <app_name>/

# specify a custom filename pattern match using the -p (or --pattern) option, if your test files are named differently from the test*.py pattern
./manage.py test --pattern="tests_*.py"
```
