import unittest


class TestArgParsing(unittest.TestCase):

    def test_env_parsing(self):

        from ppeach import util

        input = ['a=here_there_be_dragons.apk', 'b=/user/local/temp/']

        expected = {
            'a': 'here_there_be_dragons.apk',
            'b': '/user/local/temp/'
        }

        output, errors = util.parse_environment(input)

        self.assertEqual(output, expected)
        self.assertEqual(len(input), len(output.keys()))
        self.assertEqual(len(errors), 0)

    def test_failed_env_parsing(self):
        from ppeach import util

        input = ['a::here_there_be_dragons.apk', 'b::/user/local/temp/']

        output, errors = util.parse_environment(input)

        self.assertEqual(len(output), 0)
        self.assertEqual(len(input), len(errors))


if __name__ == '__main__':
    unittest.main()
