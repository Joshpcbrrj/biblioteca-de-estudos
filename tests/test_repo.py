"""The repository as a whole: the skill's structure, the documentation and the library skeleton."""
import filecmp
import glob
import os
import re

import pytest
import yaml
from conftest import ROOT, SKILL, read

# scripts cited by the skill but still being written (phase 3 of the rebuild);
# remove each name as soon as its script lands
PENDING_SCRIPTS = set()


def skill_docs():
    return [os.path.join(SKILL, 'SKILL.md')] + sorted(
        glob.glob(os.path.join(SKILL, 'modes', '*.md'))
        + glob.glob(os.path.join(SKILL, 'references', '**', '*.md'), recursive=True))


def rel(path, base=SKILL):
    return os.path.relpath(path, base).replace(os.sep, '/')


def test_skill_frontmatter_follows_the_agent_skills_rules():
    text = read(os.path.join(SKILL, 'SKILL.md'))
    m = re.match(r'---\nname: (.+)\ndescription: (.+?)\n---\n', text, re.S)
    assert m, 'frontmatter with name and description not found'
    name, desc = m.groups()
    assert name == os.path.basename(SKILL)
    assert re.fullmatch(r'[a-z0-9-]{1,64}', name) and not re.search(r'anthropic|claude', name)
    assert 0 < len(desc) <= 1024 and not re.search(r'<[a-zA-Z/]', desc)
    assert len(text.splitlines()) <= 500


def test_every_path_cited_in_the_skill_exists():
    missing = []
    for path in skill_docs():
        text = read(path)
        for ref in set(re.findall(r'`((?:modes|references|assets)/[\w./-]+)`', text)):
            if not os.path.exists(os.path.join(SKILL, ref)):
                missing.append(f'{rel(path)} -> {ref}')
        for ref in set(re.findall(r'scripts/([\w-]+\.py)', text)) - PENDING_SCRIPTS:
            if not os.path.exists(os.path.join(SKILL, 'scripts', ref)):
                missing.append(f'{rel(path)} -> scripts/{ref}')
    assert not missing


def test_pending_scripts_list_is_up_to_date():
    landed = PENDING_SCRIPTS & set(os.listdir(os.path.join(SKILL, 'scripts')))
    assert not landed, f'remove from PENDING_SCRIPTS: {sorted(landed)}'


def test_every_mode_and_reference_is_listed_in_skill_md():
    skill = read(os.path.join(SKILL, 'SKILL.md'))
    unlisted = []
    for path in skill_docs()[1:]:
        r = rel(path)
        folder, name = os.path.split(r)
        if r not in skill and name not in skill and f'{folder}/<' not in skill:
            unlisted.append(r)
    assert not unlisted


def test_long_skill_files_start_with_a_table_of_contents():
    for path in skill_docs()[1:]:
        lines = read(path).splitlines()
        head = '\n'.join(lines[:12])
        assert len(lines) <= 100 or '## Contents' in head or '- [ ] 1.' in head, rel(path)


def test_hidden_answers_in_the_skill_use_the_exact_details_format():
    bad = []
    for path in skill_docs():
        lines = read(path).splitlines()
        for i, line in enumerate(lines):
            bare = line.lstrip('> ').strip()
            if bare.startswith('<summary>') and i + 1 < len(lines) and lines[i + 1].lstrip('> ').strip():
                bad.append(f'{rel(path)}:{i + 2}')
            if bare == '</details>' and i > 0 and lines[i - 1].lstrip('> ').strip():
                bad.append(f'{rel(path)}:{i}')
    assert not bad


def test_every_documentation_page_has_the_language_switcher():
    import translation
    missing = [page for r in translation.english_pages() for page in (r, translation.translation_of(r))
               if os.path.exists(os.path.join(ROOT, page)) and 'English' not in read(os.path.join(ROOT, page))[:600]]
    assert not missing


def test_internal_links_point_to_existing_files():
    broken = []
    for path in glob.glob(os.path.join(ROOT, '**', '*.md'), recursive=True):
        r = rel(path, ROOT)
        if r.startswith(('plano/', 'skills/syllabook/references/')):
            continue
        for target in re.findall(r'\]\(([^)#\s]+)(?:#[^)]*)?\)', read(path)):
            if target.startswith(('http://', 'https://', 'mailto:', '../../')):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), target))):
                broken.append(f'{r} -> {target}')
    assert not broken


@pytest.mark.parametrize('relpath', ['LICENSE', 'LICENSE-CODIGO'])
def test_root_licenses_match_the_library_skeleton(relpath):
    copy = os.path.join(SKILL, 'assets', 'library', relpath)
    assert filecmp.cmp(os.path.join(ROOT, relpath), copy, shallow=False), f'{relpath} differs from assets/library'


def test_the_kit_repository_holds_no_library_folders():
    # books live in each user's own library (the syllabook-library template), never here
    leftovers = ['created-books', 'improved-materials', 'site', 'library.yaml',
                 '.github/workflows/epub.yml', '.github/workflows/site.yml']
    assert not [p for p in leftovers if os.path.exists(os.path.join(ROOT, p))]


def test_yaml_files_are_valid_and_library_yaml_has_every_key():
    keys = {'author', 'repository', 'branch', 'commit_name', 'commit_email', 'default_language',
            'content_license', 'code_license', 'epub_release', 'notion_page'}
    files = glob.glob(os.path.join(ROOT, '.github', '**', '*.yml'), recursive=True)
    files += glob.glob(os.path.join(SKILL, 'assets', '**', '*.yml'), recursive=True)
    for path in files:
        yaml.safe_load(read(path))
    assert keys <= set(yaml.safe_load(read(os.path.join(SKILL, 'assets', 'library', 'library.yaml'))))


def test_workflows_that_publish_run_only_in_the_kit_repository():
    for name in ('tests.yml', 'skill-release.yml'):
        assert "github.repository == 'Joshpcbrrj/syllabook'" in read(os.path.join(ROOT, '.github', 'workflows', name))
