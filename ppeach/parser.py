"""
PPeach

This module contains logic related to extracting task and output dependencies from Luigi Tasks
"""

import datetime
import types

import luigi

from domain import Dependency
from domain import Param
from domain import Target
from domain import Task


def _default_param_value(param_obj):
    _defaults = {
        'datetime': datetime.datetime(2018, 01, 01, 00, 00, 00, 00),
        'str': 'hello-world',
        'list': ['a', 'b', 'c'],
        'tuple': ('a', 'b', 'c')
    }

    if isinstance(param_obj, luigi.DateParameter):
        return _defaults['datetime'].date()  # .strftime('%Y-%m-%d')
    elif isinstance(param_obj, luigi.DateHourParameter):
        return _defaults['datetime']  # .strftime('%Y-%m-%dT%H')
    elif isinstance(param_obj, luigi.DateMinuteParameter):
        return _defaults['datetime']  # .strftime('%Y-%m-%dT%H%M')
    elif isinstance(param_obj, luigi.DateSecondParameter):
        return _defaults['datetime']  # .strftime('%Y-%m-%dT%H%M%S')
    elif isinstance(param_obj, luigi.BoolParameter):
        return False
    elif isinstance(param_obj, luigi.IntParameter):
        return 1
    elif isinstance(param_obj, luigi.FloatParameter):
        return 1.
    elif isinstance(param_obj, luigi.ListParameter):
        return _defaults['list']
    elif isinstance(param_obj, luigi.TupleParameter):
        return _defaults['tuple']
    else:
        return _defaults['str']


def _param_type(param_obj):
    if isinstance(param_obj, luigi.DateParameter):
        return 'Date'
    elif isinstance(param_obj, luigi.DateHourParameter):
        return 'DateHour'
    elif isinstance(param_obj, luigi.DateMinuteParameter):
        return 'DateMinute'
    elif isinstance(param_obj, luigi.DateSecondParameter):
        return 'DateSecond'
    elif isinstance(param_obj, luigi.BoolParameter):
        return 'Bool'
    elif isinstance(param_obj, luigi.IntParameter):
        return 'Int'
    elif isinstance(param_obj, luigi.FloatParameter):
        return 'Float'
    elif isinstance(param_obj, luigi.ListParameter):
        return 'List'
    elif isinstance(param_obj, luigi.TupleParameter):
        return 'Tuple'
    else:
        return 'String'


def generate_params(cls):
    """
    Generates a list of parameters for a luigi task. It tries to use the default value, and if not provided,
    it tries to assign a sensible value based on the parameter type

    :param cls: A class of type `luigi.Task`
    :return: A dictionary with the name -> value for each parameter
    """

    if hasattr(cls, 'get_task_family'):
        task_family = cls.get_task_family()
    elif hasattr(cls, 'task_family'):
        task_family = cls.task_family
    else:
        raise RuntimeError('Class %s has no (get_task_family or task_family) attribute' % cls)

    values = {}

    for param_name, param_obj in cls.get_params():

        if not param_obj.has_task_value(task_family, param_name):
            values[param_name] = _default_param_value(param_obj)
        else:
            values[param_name] = param_obj.task_value(task_family, param_name)

    return values


def _get_properties(obj, property_names):
    values = {}

    if property_names:
        for attr in property_names:
            try:
                value = getattr(obj, attr)
                values[attr] = value
            except AttributeError:
                pass

    return values


def _call_methods(obj, func_names):
    values = {}

    if func_names:

        for func_name in func_names:
            try:
                value = getattr(obj, func_name)()
                values[func_name] = value
            except AttributeError:
                pass

    return values


def _extract_params(params):
    return [Param(name, _param_type(value)) for name, value in params]


def _extract_dependencies(deps):

    if not deps:
        return None

    if isinstance(deps, (list, tuple, types.GeneratorType)):

        dependencies = []
        for dep in deps:
            params = _extract_params(dep.get_params())
            dependencies.append(
                Dependency(name=type(dep).__name__, params=params)
            )

        return dependencies

    elif isinstance(deps, dict):

        dependencies = {}
        for name, dep in deps.iteritems():
            dependencies[name] = _extract_dependencies(dep)

        return dependencies

    else:

        if isinstance(deps, luigi.Task):
            params = _extract_params(deps.get_params())

            return Dependency(type(deps).__name__, params)
        else:
            raise RuntimeError('Unknown dependency: %s' % deps)


def _extract_targets(output, target_methods=None, target_properties=None):

    if not output:
        return None

    if isinstance(output, (list, tuple)):

        targets = []
        for out in output:
            fields = _get_properties(out, target_properties)
            fields.update(_call_methods(out, target_methods))

            target = Target(
                type=type(out).__name__,
                fields=fields
            )

            targets.append(target)

        return targets

    elif isinstance(output, dict):

        targets = {}
        for name, out in output.iteritems():
            fields = _get_properties(out, target_properties)
            fields.update(_call_methods(out, target_methods))

            target = Target(
                type=type(out).__name__,
                fields=fields
            )

            targets[name] = target

        return targets

    else:

        if isinstance(output, luigi.Target):
            fields = _get_properties(output, target_properties)
            fields.update(_call_methods(output, target_methods))

            target = Target(
                type=type(output).__name__,
                fields=fields
            )

            return target
        else:
            raise RuntimeError('Unknown target: %s' % output)


def parse_task(luigi_task, target_methods=None, target_properties=None):
    """
    Extracts task dependency and output information from a `luigi.Task`

    :param luigi_task: a luigi.Task to be converted to a ppeach.Task
    :param target_methods: names of zero-parameter methods to call from luigi.Target, if found
    :param target_properties names of properties to extract to luigi.Target, if found
    :return: A ppeach.Task
    """

    dependencies = _extract_dependencies(luigi_task.requires())
    params = _extract_params(luigi_task.get_params())
    targets = _extract_targets(luigi_task.output(),
                               target_methods=target_methods,
                               target_properties=target_properties)

    return Task(
        name=type(luigi_task).__name__,
        params=params,
        targets=targets,
        dependencies=dependencies
    )
