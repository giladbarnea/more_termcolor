# env/bin/python3
from more_termcolor import util
import re
import semver


def main():
    with open('./setup.py') as f:
        data = f.read()
    version = re.fullmatch(r"\s*version='(?P<ver>\d(?:\.\d)+)',", data).groupdict()['ver']
    parsed = semver.VersionInfo.parse(version)
    bumped = parsed.bump_patch()
    if bumped.patch == 10:
        bumped = parsed.bump_minor()
    if util.confirm(f'current version is {version}, bump to {bumped}?'):
        with open('./setup.py', 'w'):
            pass
    pass


if __name__ == '__main__':
    main()
