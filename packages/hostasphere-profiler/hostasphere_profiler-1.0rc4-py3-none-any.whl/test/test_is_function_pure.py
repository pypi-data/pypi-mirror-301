##
## Hand-e project, 2024
## hostasphere python profiler api
## File description:
## test_is_function_pure.py
##

import unittest

from profiler.utils import is_function_pure

class TestIsFunctionPure(unittest.TestCase):
    def test_normal(self):
        source_code = """
def add(a, b):
    return a + b
        """
        self.assertTrue(is_function_pure(source_code))

    def test_with_internal_variable(self):
        source_code = """
def add(a, b):
    add = a + b
    return add
        """
        self.assertTrue(is_function_pure(source_code))

    def test_normal_openhosta_function_with_docstring(self):
        source_code = """
def translate(text:str, language:str)->str:
    \"\"\"
    This function translates the text in the “text” parameter into the language specified in the “language” parameter.
    \"\"\"
    return emulate()
        """
        self.assertTrue(is_function_pure(source_code))

    def test_normal_openhosta_function(self):
        source_code = """
def some_function():
    x = 5
    return emulate()
        """
        self.assertTrue(is_function_pure(source_code))

    def test_external_function_call_on_return(self):
        source_code = """
def some_function():
    x = 5
    return testest()
        """
        self.assertFalse(is_function_pure(source_code))

    def test_internal_function_call_on_return(self):
        source_code = """
def some_function():
    x = 5
    test = emulate()
    return x
        """
        self.assertTrue(is_function_pure(source_code))

    def test_external_function_call_on_assignment(self):
        source_code = """
def some_function():
    x = 5
    test = testest()
    return x
        """
        self.assertFalse(is_function_pure(source_code))

if __name__ == '__main__':
    unittest.main()