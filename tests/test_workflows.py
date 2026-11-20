"""The library workflows (epub.yml, site.yml), run step by step in a test library.

Each `run:` step of the real workflow file runs in bash, as on GitHub, with its `if:`
conditions, step outputs and GITHUB_ENV. `gh` and `pip` are fakes that only log what
they would do, so nothing is published; `actions/*` steps (Pages upload and deploy)
are skipped. What this cannot cover, the real release and Pages deploy, runs in the
public demo repository (syllabook-demo).
"""
import os
import re
import shutil
import stat
import subprocess
import sys

import package_skill
import pytest
import yaml
from conftest import SKILL

pytestmark = pytest.mark.skipif(os.name == 'nt' or not shutil.which('bash'),
                                reason='the workflow steps are bash scripts run by Linux runners')

WORKFLOWS = os.path.join(SKILL, 'assets', 'library', '.github', 'workflows')
FAKE_GH = '''#!/usr/bin/env bash
echo "gh $*" >> "$FAKE_LOG"
case "$1 $2" in
  "release view") exit 1 ;;
  "release download")
    while [ $# -gt 0 ]; do [ "$1" = "--dir" ] && dir="$2"; shift; done
    cp "$FAKE_SKILL_ZIP" "$dir/syllabook.zip" ;;
esac
'''


def executable(path, text):
    path.write_text(text)
    path.chmod(path.stat().st_mode | stat.S_IEXEC)


@pytest.fixture
def runner(tmp_path):
    """Fake tools on the PATH; returns a function that runs one workflow in a library."""
    bin_dir = tmp_path / 'fakebin'
    bin_dir.mkdir()
    log = tmp_path / 'calls.log'
    log.write_text('')
    executable(bin_dir / 'gh', FAKE_GH)
    # the test environment already has every dependency installed
    executable(bin_dir / 'pip', '#!/usr/bin/env bash\necho "pip $*" >> "$FAKE_LOG"\n')
    executable(bin_dir / 'python', f'#!/usr/bin/env bash\nexec "{sys.executable}" "$@"\n')
    skill_zip = package_skill.package(str(tmp_path / 'release'))

    def run(workflow, library):
        spec = yaml.safe_load(open(os.path.join(WORKFLOWS, workflow), encoding='utf-8'))
        env = dict(os.environ, PATH=f'{bin_dir}{os.pathsep}{os.environ["PATH"]}', FAKE_LOG=str(log),
                   FAKE_SKILL_ZIP=skill_zip, RUNNER_TEMP=str(tmp_path / 'runner'))
        os.makedirs(env['RUNNER_TEMP'], exist_ok=True)
        outputs = {}
        for job in spec['jobs'].values():
            for step in job.get('steps', []):
                if 'run' not in step or not condition(step.get('if'), outputs):
                    continue
                files = {k: tmp_path / f'{k.lower()}' for k in ('GITHUB_OUTPUT', 'GITHUB_ENV')}
                for f in files.values():
                    f.write_text('')
                step_env = {k: str(v).replace('${{ github.token }}', 'fake-token')
                            for k, v in (step.get('env') or {}).items()}
                result = subprocess.run(['bash', '--noprofile', '--norc', '-eo', 'pipefail', '-c', step['run']],
                                        cwd=library, env={**env, **step_env, **{k: str(v) for k, v in files.items()}},
                                        capture_output=True, text=True)
                assert result.returncode == 0, f'step "{step.get("name")}" failed:\n{result.stdout}\n{result.stderr}'
                outputs[step.get('id')] = dict(line.split('=', 1) for line in
                                               files['GITHUB_OUTPUT'].read_text().splitlines() if '=' in line)
                env.update(line.split('=', 1) for line in files['GITHUB_ENV'].read_text().splitlines() if '=' in line)
        return log.read_text().splitlines()
    return run


def condition(expression, outputs):
    """The only kind of `if:` these workflows use: steps.<id>.outputs.<key> != '<value>'."""
    if not expression:
        return True
    m = re.fullmatch(r"steps\.(\w+)\.outputs\.(\w+) != '(.*)'", expression.strip())
    assert m, f'unsupported condition in workflow: {expression}'
    return outputs.get(m.group(1), {}).get(m.group(2)) != m.group(3)


def test_epub_workflow_builds_and_publishes_every_book(runner, library):
    calls = runner('epub.yml', library)
    assert (library / 'dist' / 'python-do-zero-teste.epub').exists()
    assert 'gh release create epubs --title EPUBs --notes One EPUB per book, rebuilt on every change.' in calls
    assert 'gh release upload epubs dist/python-do-zero-teste.epub --clobber' in calls
    # the library has no copy of the skill, so the scripts come from the latest release
    assert any(c.startswith('gh release download --repo Joshpcbrrj/syllabook') for c in calls)


def test_epub_workflow_uses_the_skill_copy_in_the_repository_when_there_is_one(runner, library):
    shutil.copytree(os.path.dirname(SKILL), library / 'skills')
    calls = runner('epub.yml', library)
    assert (library / 'dist' / 'python-do-zero-teste.epub').exists()
    assert not any('release download' in c for c in calls)


def test_workflows_do_nothing_without_books(runner, library):
    shutil.rmtree(library / 'created-books' / 'python-do-zero-teste')
    assert runner('epub.yml', library) == []
    assert runner('site.yml', library) == []
    assert not (library / 'dist').exists() and not (library / '_site').exists()


@pytest.mark.slow
@pytest.mark.skipif(not shutil.which('zensical'), reason='zensical not installed')
def test_site_workflow_builds_the_website(runner, library):
    runner('site.yml', library)
    assert (library / '_site' / 'site' / 'index.html').exists()
    assert (library / '_site' / 'site' / 'search.json').exists()
