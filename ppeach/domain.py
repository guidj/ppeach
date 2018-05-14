"""
PPeach

This module contains domain classes
"""


class Param(object):

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return '%s(name=%s, type=%s)' \
               % (type(self).__name__, self.name, self.type)


class Target(object):

    def __init__(self, type, fields=None):
        self.type = type
        self.fields = fields

    def __repr__(self):
        return '%s(type=%s, fields=%s)' \
               % (type(self).__name__, self.type, self.fields)


class Dependency(object):

    def __init__(self, name, params):
        self.name = name
        self.params = params

    def __repr__(self):
        return '%s(name=%s, params=%s)' \
               % (type(self).__name__, self.name, self.params)


class Task(object):

    def __init__(self, name, params, targets, dependencies=None):
        self.name = name
        self.params = params
        self.targets = targets
        self.dependencies = dependencies

    def __repr__(self):
        return '%s(name=%s, params=%s, output=%s, dependencies=%s)' \
               % (type(self).__name__, self.name, self.params, self.targets, self.dependencies)
