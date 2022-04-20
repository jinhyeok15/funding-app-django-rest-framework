from unittest import TestCase, main


class SampleTest(TestCase):

    def test_sample(self):
        self.assertEquals(1, 1, "Is same number?")

    def test_get_pure_token(self):
        token_sample = "ff7cf2041ab98d61a1e797ffbcd36cd4d08cf177"
        header_value = f"Token {token_sample}"
        token = header_value.split(" ")[1]
        self.assertEquals(token, token_sample)

if __name__ == '__main__':
    main()
