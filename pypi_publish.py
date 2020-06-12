# env/bin/python3
from more_termcolor import util
import re
import semver
import sys


def is_dry_run():
    # -n, [-]+dry[-_]?run
    for arg in sys.argv[1:]:
        if arg == '-n' or re.fullmatch('^[-]+dry[-_]?run$', arg):
            sys.argv.remove(arg)
            return True
    return False


def main():
    with open('./setup.py') as f:
        data = f.read()
    VERSION_RE = re.compile(r"\s*version='(?P<ver>\d+(?:\.\d+)+)',")
    version = VERSION_RE.fullmatch(data).groupdict()['ver']
    parsed = semver.VersionInfo.parse(version)
    bumped = parsed.bump_patch()
    if bumped.patch == 10:
        bumped = parsed.bump_minor()
    if util.confirm(f'current version is {version}, bump to {bumped}?'):
        replaced = VERSION_RE.sub(str(bumped), version)
        if is_dry_run():
            diff = set(data).difference(set(replaced))
            print('dry run: would have made this changes to setup.py:\n', diff)
        
        else:
            with open('./setup.py', 'w'):
                pass


if __name__ == '__main__':
    main()
