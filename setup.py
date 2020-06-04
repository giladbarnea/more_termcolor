"""Optional args (all False by default):
-n, --dry-run       doesn't actually call setup()
-ok                 before calling setup(), pretty-prints args and prompts user to confirm"""
from setuptools import find_packages, setup
import sys
import re

packages = find_packages()
setup_args = dict(name='more_termcolor',
                  version='1.0.0',
                  description='Literally more colors, with support for nested colors',
                  author='Gilad Barnea',
                  author_email='giladbrn@gmail.com',
                  url='https://github.com/giladbarnea/more_termcolor',
                  packages=packages,
                  # package_dir={'paint': 'more_termcolor'},
                  keywords=["termcolor", "color", "colors", "terminal", "ansi"],
                  # py_modules=[],
                  extras_require=dict(test=['pytest']))

dry_run = False  # -n, [-]+dry[-_]?run
confirm = False  # [-]+ok
for arg in sys.argv[1:]:
    if arg == '-n' or re.fullmatch('^[-]+dry[-_]?run$', arg):
        dry_run = True
        sys.argv.remove(arg)
        continue
    if re.fullmatch('^[-]+ok$', arg):
        confirm = True
        sys.argv.remove(arg)
        continue
print(f'sys.argv[1:]: ', sys.argv[1:])
print(f'dry_run: ', dry_run, '\nconfirm: ', confirm)
if confirm:
    from pprint import pprint
    
    print('setup args:')
    pprint(setup_args)
    if not ((answer := input('continue? y/n\t').lower()) == 'y' or answer == 'yes'):
        print('aborting')
        sys.exit()

if not dry_run:
    setup(**setup_args)
