"""Optional args (all False by default):
-n, --dry-run       doesn't actually call setup()
-ok                 before calling setup(), pretty-prints args and prompts user to confirm"""
from setuptools import find_packages, setup
import sys
import re

from more_termcolor import util

with open("README.md", "r") as fh:
    long_description = fh.read()
packages = find_packages(exclude=["tests?", "*.tests*", "*.tests*.*", "tests*.*", 'pypi_publish.py'])
setup_args = dict(name='more_termcolor',
                  # https://packaging.python.org/tutorials/packaging-projects/
                  version='1.1.3',
                  description='All colors, with support for nested colors, convenience methods and full original termcolor compatability.',
                  long_description=long_description,
                  long_description_content_type="text/markdown",
                  license='MIT',
                  author='Gilad Barnea',
                  author_email='giladbrn@gmail.com',
                  url='https://github.com/giladbarnea/more_termcolor',
                  packages=packages,
                  keywords=["termcolor", "color", "colors", "terminal", "ansi", "formatting"],
                  # pip install -e .[dev]
                  extras_require={
                      'dev': ['pytest',
                              'ipdb',
                              'IPython',
                              'semver',
                              'birdseye'
                              ]
                      },
                  classifiers=[
                      # https://pypi.org/classifiers/
                      'Development Status :: 4 - Beta',
                      'Environment :: Console',
                      'Intended Audience :: Developers',
                      "License :: OSI Approved :: MIT License",
                      'Operating System :: OS Independent',
                      "Programming Language :: Python :: 3 :: Only",
                      'Topic :: Terminals',
    
                      ],
                  python_requires='>=3.7',
                  )

dry_run = False
confirm = False
DRY_RUN_RE = re.compile('^[-]+dry[-_]?run$')
CONFIRM_RE = re.compile('^[-]+ok$')
for arg in sys.argv[1:]:
    if arg == '-n' or DRY_RUN_RE.fullmatch(arg):
        dry_run = True
        sys.argv.remove(arg)
        continue
    if CONFIRM_RE.fullmatch(arg):
        confirm = True
        sys.argv.remove(arg)
        continue
print(f'sys.argv[1:]: {sys.argv[1:]}', f'dry_run: {dry_run}', f'confirm: {confirm}', sep='\n')
if confirm:
    from pprint import pprint
    
    print('setup args:')
    pprint(setup_args)
    if not util.confirm():
        print('aborting')
        sys.exit()

if dry_run:
    print('dry run: not calling setup(**setup_args). exiting')
    sys.exit()
setup(**setup_args)
