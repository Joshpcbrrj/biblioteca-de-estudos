#!/usr/bin/env python3
"""Kit tests: the skill's structure, the documentation and the library skeleton.

Usage:  python tests/run.py

Needs PyYAML (`pip install pyyaml`). Prints OK or FAILED for each test and
exits with code 1 if any test fails. The "Kit tests" Action runs the same
on every push and pull request.
"""
import filecmp
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, 'skill', 'syllabook')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
failures = []


def test(name):
    def run(fn):
        try:
            note = fn()
            print(f'OK      {name}' + (f' ({note})' if note else ''))
        except AssertionError as e:
            failures.append(name)
            print(f'FAILED  {name}: {e}')
        return fn
    return run


def read(path):
    return open(path, encoding='utf-8').read()


def skill_docs():
    return [os.path.join(SKILL, 'SKILL.md')] + sorted(
        glob.glob(os.path.join(SKILL, 'modes', '*.md'))
        + glob.glob(os.path.join(SKILL, 'references', '**', '*.md'), recursive=True))


@test('SKILL.md frontmatter follows the Agent Skills rules')
def _():
    text = read(os.path.join(SKILL, 'SKILL.md'))
    m = re.match(r'---\nname: (.+)\ndescription: (.+?)\n---\n', text, re.S)
    assert m, 'frontmatter with name and description not found'
    name, desc = m.group(1), m.group(2)
    assert name == os.path.basename(SKILL), f'name "{name}" differs from the folder'
    assert re.fullmatch(r'[a-z0-9-]{1,64}', name), 'name must be lowercase letters, digits and hyphens, up to 64'
    assert not re.search(r'anthropic|claude', name), 'name uses a reserved word'
    assert 0 < len(desc) <= 1024, f'description has {len(desc)} characters (max 1024)'
    assert not re.search(r'<[a-zA-Z/]', desc), 'description contains an XML tag'
    lines = len(text.splitlines())
    assert lines <= 500, f'SKILL.md has {lines} lines (max 500)'
    return f'{lines} lines, description {len(desc)} characters'


# scripts cited by the skill but still being written (phase 3 of the rebuild);
# remove each name as soon as its script lands
PENDING_SCRIPTS = {'diagram.py', 'projects.py', 'ingest.py', 'notion.py', 'illustrate.py'}


@test('every path cited in the skill exists')
def _():
    missing = []
    scripts_written = os.path.isdir(os.path.join(SKILL, 'scripts'))
    for path in skill_docs():
        text = read(path)
        for ref in set(re.findall(r'`((?:modes|references|assets)/[\w./-]+)`', text)):
            if not os.path.exists(os.path.join(SKILL, ref)):
                missing.append(f'{os.path.relpath(path, SKILL)} -> {ref}')
        # scripts are checked once the scripts/ folder exists (phase 3 of the rebuild)
        if scripts_written:
            for ref in set(re.findall(r'scripts/([\w-]+\.py)', text)) - PENDING_SCRIPTS:
                if not os.path.exists(os.path.join(SKILL, 'scripts', ref)):
                    missing.append(f'{os.path.relpath(path, SKILL)} -> scripts/{ref}')
    assert not missing, missing
    landed = PENDING_SCRIPTS & set(os.listdir(os.path.join(SKILL, 'scripts')))
    assert not landed, f'remove from PENDING_SCRIPTS: {sorted(landed)}'
    return f'pending scripts: {", ".join(sorted(PENDING_SCRIPTS))}' if PENDING_SCRIPTS else None


@test('every mode and reference file is listed in SKILL.md (one level deep)')
def _():
    skill = read(os.path.join(SKILL, 'SKILL.md'))
    unlisted = []
    for path in skill_docs()[1:]:
        rel = os.path.relpath(path, SKILL).replace(os.sep, '/')
        folder, name = os.path.split(rel)
        # files in areas/ and style/ are listed by name or by the <placeholder> pattern
        if rel in skill or name in skill or f'{folder}/<' in skill:
            continue
        unlisted.append(rel)
    assert not unlisted, unlisted


@test('long skill files start with a table of contents')
def _():
    no_toc = []
    for path in skill_docs()[1:]:
        lines = read(path).splitlines()
        head = '\n'.join(lines[:12])
        if len(lines) > 100 and '## Contents' not in head and '- [ ] 1.' not in head:
            no_toc.append(f'{os.path.relpath(path, SKILL)} ({len(lines)} lines)')
    assert not no_toc, no_toc


@test('hidden answers in the examples use the exact <details> format')
def _():
    bad = []
    for path in skill_docs():
        lines = read(path).splitlines()
        for i, line in enumerate(lines):
            bare = line.lstrip('> ').strip()
            if bare.startswith('<summary>') and i + 1 < len(lines) and lines[i + 1].lstrip('> ').strip():
                bad.append(f'{os.path.relpath(path, SKILL)}:{i + 2} needs a blank line after <summary>')
            if bare == '</details>' and i > 0 and lines[i - 1].lstrip('> ').strip():
                bad.append(f'{os.path.relpath(path, SKILL)}:{i} needs a blank line before </details>')
    assert not bad, bad


@test('Portuguese translations exist and are up to date')
def _():
    import translation
    problems = translation.check()
    assert not problems, problems


@test('every documentation page has the language switcher')
def _():
    import translation
    missing = []
    for rel in translation.english_pages():
        for page in (rel, translation.translation_of(rel)):
            path = os.path.join(ROOT, page)
            # a missing translation is reported by the translation test
            if os.path.exists(path) and 'English' not in read(path)[:600]:
                missing.append(page)
    assert not missing, missing


@test('internal links in the documentation point to existing files')
def _():
    broken = []
    for path in glob.glob(os.path.join(ROOT, '**', '*.md'), recursive=True):
        rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
        if rel.startswith(('plano/', 'skill/syllabook/references/')):
            continue
        for target in re.findall(r'\]\(([^)#\s]+)(?:#[^)]*)?\)', read(path)):
            if target.startswith(('http://', 'https://', 'mailto:', '../../')):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), target))):
                broken.append(f'{rel} -> {target}')
    assert not broken, broken


@test('book folders at the root match the library skeleton')
def _():
    lib = os.path.join(SKILL, 'assets', 'library')
    different = []
    pairs = [f'{folder}/{name}' for folder in ('created-books', 'improved-materials')
             for name in ('README.md', 'README.pt-BR.md')]
    pairs += ['.github/workflows/epub.yml', '.github/workflows/site.yml']
    for rel in pairs:
        a, b = os.path.join(ROOT, rel), os.path.join(lib, rel)
        if not os.path.exists(a) or not os.path.exists(b) or not filecmp.cmp(a, b, shallow=False):
            different.append(rel)
    assert not different, f'root and assets/library differ: {different}'


@test('YAML files are valid and library.yaml has every key')
def _():
    import yaml
    keys = {'author', 'repository', 'branch', 'commit_name', 'commit_email', 'default_language',
            'content_license', 'code_license', 'epub_release', 'notion_page'}
    files = glob.glob(os.path.join(ROOT, '.github', '**', '*.yml'), recursive=True)
    for path in files + [os.path.join(ROOT, 'library.yaml'),
                         os.path.join(SKILL, 'assets', 'library', 'library.yaml')]:
        data = yaml.safe_load(read(path))
        if path.endswith('library.yaml'):
            assert keys <= set(data), f'{os.path.relpath(path, ROOT)} is missing {sorted(keys - set(data))}'
    return f'{len(files) + 2} files'


SCRIPTS = os.path.join(SKILL, 'scripts')
SAMPLE = os.path.join(ROOT, 'tests', 'fixtures', 'sample-book')
# keep the "current book" pointer out of the user's home folder
STATE = os.path.join(tempfile.gettempdir(), 'syllabook-tests-state')


def script(name, *args):
    env = dict(os.environ, SYLLABOOK_STATE=STATE, SYLLABOOK_BOOK='')
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, name), *args],
                       capture_output=True, text=True, encoding='utf-8', env=env)
    try:
        return r.returncode, json.loads(r.stdout)
    except json.JSONDecodeError:
        raise AssertionError(f'{name} {" ".join(args)} did not print JSON: {r.stdout[-300:]} {r.stderr[-500:]}')


def sample_copy():
    tmp = tempfile.mkdtemp()
    dest = os.path.join(tmp, 'book')
    shutil.copytree(SAMPLE, dest)
    return dest


@test('book.py validate accepts the sample book')
def _():
    code, r = script('book.py', 'validate', os.path.join(SAMPLE, 'book.yaml'))
    assert code == 0 and r['ok'], r


@test('book.py validate refuses a concept used before it is taught')
def _():
    import yaml
    book = sample_copy()
    path = os.path.join(book, 'book.yaml')
    data = yaml.safe_load(open(path, encoding='utf-8'))
    # "laço for" moves to chapter 1 but still depends on "lista", taught in chapter 2
    data['concepts'] = [{'id': 'lista', 'name': 'lista', 'chapter': 2, 'depends': []},
                        {'id': 'laco-for', 'name': 'laço for', 'chapter': 1, 'depends': ['lista']}]
    yaml.safe_dump(data, open(path, 'w', encoding='utf-8'), allow_unicode=True)
    code, r = script('book.py', 'validate', path)
    assert code == 1 and any('taught later' in e for e in r['errors']), r


@test('audit.py passes the whole sample book')
def _():
    code, r = script('audit.py', '--book', SAMPLE)
    assert code == 0 and r['ready'] and not r['warnings'], r


@test('audit.py reports each kind of defect')
def _():
    book = sample_copy()
    path = os.path.join(book, 'chapters', '01-listas.md')
    text = open(path, encoding='utf-8').read()
    # a 4-line block with no comment and one line over the 80-character limit
    block = ('```python\nnotas = [7.5, 8.0, 6.5]\nmaior = max(notas)\nmenor = min(notas)\n'
             'print("maior nota da turma:", maior, "menor nota da turma:", menor, "fim do relatorio")\n```\n')
    text = text.replace('## 🏋️ Pratique', block + '\n## 🏋️ Pratique')
    text = text.replace('](../img/c01-lista.svg)', '](../img/nao-existe.svg)')
    text = text.replace('<summary>Ver resposta</summary>\n\n4.', '<summary>Ver resposta</summary>\n4.')
    text = text.replace('## 🧠 Revisão rápida', '## Revisão')
    text += '\n![](../img/c01-lista.svg)\n'
    open(path, 'w', encoding='utf-8').write(text)
    code, r = script('audit.py', '1', '--book', book)
    found = '\n'.join(r['errors'])
    expected = ['no comment explaining why', 'characters (limit 80)', 'image not found',
                'blank line needed after <summary>', 'missing section "Revisão rápida"', 'image without alt text']
    missing = [e for e in expected if e not in found]
    assert code == 1 and not missing, f'not reported: {missing}; got {r["errors"]}'


@test('book.py brief creates the skeleton and done refuses an unfinished chapter')
def _():
    book = sample_copy()
    os.remove(os.path.join(book, 'chapters', '02-o-laco-for.md'))
    code, r = script('book.py', 'brief', '2', '--book', book)
    assert code == 0 and r['skeleton_created'] and r['concepts_you_may_use'] == ['lista'], r
    skeleton = open(os.path.join(book, r['file']), encoding='utf-8').read()
    assert '## De onde paramos' in skeleton and 'Revisão rápida' in skeleton, 'labels not in the book language'
    code, r = script('book.py', 'done', '2', '--summary', 'x', '--book', book)
    assert code == 1 and 'TODO' in r['error'], r
    code, r = script('book.py', 'done', '1', '--summary', 'Listas e len', '--book', book)
    assert code == 0 and r['progress'] == '1/2', r
    code, r = script('book.py', 'status', '--book', book)
    assert r['pending_chapters'] == [2] and r['next_step'] == 'book.py brief 2', r


@test('facts.py lists the dated sentence and skips headings, tables and source lists')
def _():
    code, r = script('facts.py', '2', '--book', SAMPLE)
    assert any('1991' in s['sentence'] for s in r['sentences']), r
    assert not any('Item' in s['sentence'] or 'Tutorial' in s['sentence'] for s in r['sentences']), r
    return f'{r["to_check"]} sentences'


def sample_library():
    """A library with the skeleton and the sample book, as a user's repository would be."""
    import yaml
    lib = os.path.join(tempfile.mkdtemp(), 'lib')
    shutil.copytree(os.path.join(SKILL, 'assets', 'library'), lib)
    shutil.copytree(SAMPLE, os.path.join(lib, 'created-books', 'python-do-zero-teste'))
    settings = yaml.safe_load(read(os.path.join(lib, 'library.yaml')))
    settings.update(author='Teste', repository='exemplo/minha-biblioteca', default_language='pt-BR')
    yaml.safe_dump(settings, open(os.path.join(lib, 'library.yaml'), 'w', encoding='utf-8'), allow_unicode=True)
    return lib


@test('build.py: EPUB with an answers appendix, navigation, map and zip in the repository layout')
def _():
    import zipfile
    lib = sample_library()
    book = os.path.join(lib, 'created-books', 'python-do-zero-teste')
    dist = os.path.join(lib, 'dist')
    code, r = script('build.py', '--book', book, '--out', dist)
    assert code == 0, r
    epub = zipfile.ZipFile(r['epub'])
    pages = '\n'.join(epub.read(n).decode('utf-8') for n in epub.namelist() if n.endswith('.xhtml'))
    assert '<details' not in pages, 'answers still inline in the EPUB'
    assert r['answers_in_appendix'] == 6 and len(re.findall(r'#q-\d+"', pages)) == 6, 'answer links missing'
    assert 'Voltar ao exercício' in pages and 'Respostas' in pages, 'appendix labels not in the book language'
    assert re.search(r'href="[^"]*#f-02-o-laco-for"', pages), 'link between chapters not resolved'
    chapter = read(os.path.join(book, 'chapters', '01-listas.md'))
    assert '<!-- nav:start -->' in chapter and 'Próximo capítulo' in chapter, 'navigation missing'
    assert '<!-- map:start -->' in read(os.path.join(book, 'README.md')), 'book map missing'
    names = zipfile.ZipFile(r['zips'][0]['zip']).namelist()
    assert all(n.startswith('created-books/python-do-zero-teste/') for n in names), names[:3]
    return f'{len(epub.namelist())} files in the EPUB'


@test('build.py: partial checkpoint, and zips split above 100 files')
def _():
    lib = sample_library()
    book = os.path.join(lib, 'created-books', 'python-do-zero-teste')
    code, r = script('build.py', '--book', book, '--out', os.path.join(lib, 'p'), '--partial')
    assert code == 0 and 'epub' not in r and r['zips'][0]['zip'].endswith('-partial.zip'), r
    for i in range(120):
        shutil.copy(os.path.join(book, 'img', 'c01-lista.svg'), os.path.join(book, 'img', f'extra-{i}.svg'))
    code, r = script('build.py', '--book', book, '--out', os.path.join(lib, 's'), '--no-epub')
    sizes = [z['files'] for z in r['zips']]
    assert code == 0 and len(sizes) == 2 and max(sizes) <= 100, sizes


@test('build.py lists and site: library lists and a website source that Zensical builds')
def _():
    lib = sample_library()
    code, r = script('build.py', 'lists', '--library', lib)
    assert code == 0 and 'created-books/README.pt-BR.md' in r['updated'], r
    listing = read(os.path.join(lib, 'created-books', 'README.pt-BR.md'))
    assert 'Baixar EPUB' in listing and 'releases/download/epubs/python-do-zero-teste.epub' in listing
    site = os.path.join(lib, '_site')
    code, r = script('build.py', 'site', '--library', lib, '--out', site)
    page = read(os.path.join(site, 'docs', 'created-books', 'python-do-zero-teste', 'chapters', '01-listas.md'))
    assert code == 0 and '??? success "Ver resposta"' in page and '<details>' not in page
    assert os.path.exists(os.path.join(site, 'mkdocs.yml'))
    zensical = shutil.which('zensical')
    if not zensical:
        return 'zensical not installed: site not built'
    built = subprocess.run([zensical, 'build', '--clean'], cwd=site, capture_output=True, text=True)
    assert built.returncode == 0, built.stderr[-500:]
    html = read(os.path.join(site, 'site', 'created-books', 'python-do-zero-teste', 'chapters', '01-listas', 'index.html'))
    assert '<details class="success"' in html, 'answers did not become collapsible blocks'
    return 'site built with Zensical'


@test('tools compile')
def _():
    paths = glob.glob(os.path.join(ROOT, 'tools', '*.py')) + glob.glob(os.path.join(SKILL, 'scripts', '**', '*.py'), recursive=True)
    for path in paths:
        compile(read(path), path, 'exec')
    return f'{len(paths)} files'


if __name__ == '__main__':
    print(f'\n{len(failures)} failure(s).' if failures else '\nAll tests passed.')
    sys.exit(1 if failures else 0)
