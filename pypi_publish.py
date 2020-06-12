from more_termcolor import util
import re
import semver
import sys
from pathlib import Path
import subprocess
import shlex

DRY_RUN_RE = re.compile('^[-]+dry[-_]?run$')


def is_dry_run():
    # -n, [-]+dry[-_]?run
    for arg in sys.argv[1:]:
        if arg == '-n' or DRY_RUN_RE.fullmatch(arg):
            sys.argv.remove(arg)
            return True
    return False


def main():
    if subprocess.check_output(shlex.split('git status -s')):
        print('some uncommitted changes:')
        subprocess.run(shlex.split('git status'))
        if not util.confirm('publish regardless?'):
            sys.exit()
    with open('./setup.py') as f:
        data = f.read()
    VERSION_RE = re.compile(r"\s*version='(?P<ver>\d+(?:\.\d+)+)',")
    version = VERSION_RE.search(data).groupdict()['ver']
    parsed = semver.VersionInfo.parse(version)
    bumped = parsed.bump_patch()
    if bumped.patch == 10:
        bumped = parsed.bump_minor()
    if util.confirm(f'current version is {version}, bump to {bumped}?'):
        bump_version(data, version, bumped)
    
    if Path('./dist').is_dir() or Path('./build').is_dir():
        cmd = 'rm -rf dist build'
        if util.confirm(f"run '{cmd}'?"):
            run(shlex.split(cmd))
    else:
        print("dist and/or build dirs don't exist")
    cmds = ['./env/bin/python setup.py sdist bdist_wheel',
            './env/bin/python -m twine upload dist/*']
    for cmd in cmds:
        if util.confirm(f"run '{cmd}'?"):
            ok = run(shlex.split(cmd))
            if not ok:
                sys.exit(1)


def run(cmd):
    if dry_run:
        print('dry_run, not actually running anything')
        return
    try:
        subprocess.run(cmd, stderr=subprocess.PIPE)
    except Exception as e:
        print(f'FAILED cmd: {cmd}', repr(e))
        return False
    else:
        print('success')
        return True


def bump_version(data, version, bumped):
    replaced = data.replace(version, str(bumped), 1)
    before, after = map(str.strip, set(data.splitlines()).symmetric_difference(set(replaced.splitlines())))
    if dry_run:
        print('dry run: would have made the following changes to setup.py;', 'before:', before, 'after:', after, sep='\n')
        return
    with open('./setup.py', 'w') as f:
        f.write(replaced)
    print(f'replaced "{before}" with "{after}" successfully')


if __name__ == '__main__':
    dry_run = is_dry_run()
    main()
