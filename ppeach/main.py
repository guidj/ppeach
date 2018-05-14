"""
PPeach

Main module and cli for using PPeach
"""


import argparse
import inspect
import os
import sys
import importlib
import json

import luigi.task

from ppeach import parser
from ppeach import io
from ppeach import util
from ppeach import logger


def classes_in_module(module):
    md = module.__dict__
    return [
        attr for name, attr in md.iteritems() if (
            inspect.isclass(attr) and attr.__module__ == module.__name__
        )
    ]


def main(basepath, env, target_methods, target_properties, to_json):
    sys.path.append(os.path.abspath(basepath))
    sys.path.append(os.path.dirname(os.path.abspath(basepath)))

    for k, v in env.iteritems():
        os.environ[k] = v

    modules = {}
    tasks = []
    errors = {}

    for dirname, subdirs, files in os.walk(basepath):
        logger.info('Found directory: %s' % dirname)

        for fname in files:

            if not fname.endswith('.py') or '__init__' in fname:
                continue

            mpath = os.path.join(dirname, fname)
            mname = mpath.replace(os.sep, '.').rstrip('.py').lstrip('.')
            modules[mname] = mpath

    logger.info('Found the following modules: \n\t%s' % '\n\t'.join(modules.values()))

    for mname, mpath in modules.iteritems():

        name = os.path.splitext(os.path.basename(mpath))[0]

        try:

            module = importlib.import_module(name)

            classes = classes_in_module(module)

            for cls in classes:

                if issubclass(cls, (luigi.Task, luigi.task.Task)):
                    params = parser.generate_params(cls)
                    if params:
                        e = cls(**params)
                        peach_task = parser.parse_task(e,
                                                       target_methods=target_methods,
                                                       target_properties=target_properties)

                        tasks.append(peach_task)

        except ImportError as err:
            raise RuntimeError(err)
        except NotImplementedError as err:
            errors[mname] = err

    if tasks and to_json:
        with open(to_json, 'w') as fp:
            for task in tasks:
                json.dump(io.to_json(task), fp)
                fp.write('\n')
    elif tasks:
        for task in tasks:
            logger.info('ppeach.Task::%s' % task)


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser(description='Extract luigi tasks, their dependencies and targets')

    arg_parser.add_argument('--pkg-path', type=str, required=True,
                            help="Path to python package")
    arg_parser.add_argument('--target-method', type=str, nargs='*', default=[],
                            help="Name of a no-parameter to call in task's Targets, if found. " +
                                 "It will be used as a key in `fields` for the return value")
    arg_parser.add_argument('--target-property', type=str, nargs='*', default=[],
                            help="A property to get in each task's Targets, if found. " +
                                 "It will be used as a key in `fields` for the return value")
    arg_parser.add_argument('--env', type=str, nargs='*', default=[],
                            help="Environment variables that your luigi modules may be expecting when loaded")
    arg_parser.add_argument('--to-json', type=str, default=None,
                            help="Path to a file to save output as json")

    args = arg_parser.parse_args()

    environment, errors = util.parse_environment(args.env)

    if errors:
        raise RuntimeError('\n'.join(errors))

    main(basepath=args.pkg_path, env=environment,
         target_methods=args.target_method, target_properties=args.target_property,
         to_json=args.to_json)
