import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    # unittest.main(module='tests.src.test_employee', exit=False)
    # unittest.main(module='tests.src.test_calc', exit=False)

# We can now run the tests from the root of the project in three different ways
# without encountering a ModuleNotFoundError:

# The following is considered the best practice:
# python3 -m unittest discover tests/src/

# The following two will work if you have a __main__.py file in the tests/src/ directory:
# Running it this way will allow for granular control over the tests that are run:
# You can specify the module that you want to run the tests from in the __main__.py file.:

# python3 -m tests.src
# python3 tests/src/__main__.py