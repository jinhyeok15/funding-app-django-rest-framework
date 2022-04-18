from unittest import TestCase, main


class SampleTest(TestCase):
    def test_sample(self):
        self.assertEquals(1, 1, "Is same number?")


if __name__ == '__main__':
    main()
