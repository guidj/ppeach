"""
PPeach Util


Utility helper functions
"""


def parse_environment(env_args):
    """
    Parses environment variables to be set prior to crawling the python package for luigi Tasks.
    :param env_args: A list containing `k=v` pairs
    :return: A dictionary with k -> v pairs, and a list of errors encountered parsing the input
    """

    environment = {}
    errors = []

    for env_arg in env_args:

        if '=' not in env_arg:
            errors.append(
                'Error parsing `{}`. Each environment variable be formatted as key=value'.format(
                    env_arg
                )
            )
        else:
            k, v = env_arg.split('=')

            environment[k] = v

    return environment, errors