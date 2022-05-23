from unittest import TestCase, main
from enum import Enum
from rest_framework import status


# https://docs.python.org/3/library/enum.html
class Color(Enum):
    RED = 404
    GREEN = 2
    BLUE = 3


class SampleTest(TestCase):

    def test_sample(self):
        self.assertEquals(1, 1, "Is same number?")

    def test_get_pure_token(self):
        token_sample = "ff7cf2041ab98d61a1e797ffbcd36cd4d08cf177"
        header_value = f"Token {token_sample}"
        token = header_value.split(" ")[1]
        self.assertEquals(token, token_sample)
    
    def test_enum_obj(self):
        red = Color(404)
        classname = red.__class__.__name__
        self.assertEqual(classname, "Color")
        self.assertEqual(red.name, 'RED')
        self.assertEqual(red.value, 404)
    
    def test_get_status_items(self):
        first = True
        result: str
        for name, value in vars(status).items():
            if isinstance(value, int):
                if first:
                    result = name
                    first = False
        self.assertEqual(result, 'HTTP_100_CONTINUE')


if __name__ == '__main__':
    main()
