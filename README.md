# PPeach


Crawls a python package to find definitions of [luigi](https://github.com/spotify/luigi) 
[Tasks](https://github.com/spotify/luigi/blob/master/luigi/task.py) to extract their parameters, dependencies, and output


Goodies:

  + Support for extracting properties and values of zero-parameter methods in Targets
  + Point-and-execute design (you can specify a path to any python package)
  + Save tasks to a file as JSON
  

## Usage

```
$ python -m ppeach.main --help

usage: main.py [-h] --pkg-path PKG_PATH
               [--target-method [TARGET_METHOD [TARGET_METHOD ...]]]
               [--target-property [TARGET_PROPERTY [TARGET_PROPERTY ...]]]
               [--env [ENV [ENV ...]]] [--to-json TO_JSON]

Extract luigi tasks, their dependencies and targets

optional arguments:
  -h, --help            show this help message and exit
  --pkg-path PKG_PATH   Path to python package
  --target-method [TARGET_METHOD [TARGET_METHOD ...]]
                        Name of a no-parameter to call in task's Targets, if
                        found. It will be used as a key in `fields` for the
                        return value
  --target-property [TARGET_PROPERTY [TARGET_PROPERTY ...]]
                        A property to get in each task's Targets, if found. It
                        will be used as a key in `fields` for the return value
  --env [ENV [ENV ...]]
                        Environment variables that your luigi modules may be
                        expecting when loaded
  --to-json TO_JSON     Path to a file to save output as json
```
