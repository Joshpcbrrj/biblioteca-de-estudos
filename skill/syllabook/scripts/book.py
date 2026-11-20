#!/usr/bin/env python3
"""The book's contract and memory: validate book.yaml, brief a chapter, record progress.

Usage:
  python scripts/book.py validate <book.yaml>     check fields and the concept graph; selects the book
  python scripts/book.py brief <n> [--book B]     create the chapter skeleton and print its brief
  python scripts/book.py done <n> --summary "..." [--book B]   record the chapter as done
  python scripts/book.py status [--book B]        where the book stopped and the next step

Prints JSON. Exit code 1 when something blocks the next step.
"""
import argparse
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (chapter_numbers, chapter_path, fail, find_book, labels, load_yaml, out,
                    remember, save_yaml, slugify)

REQUIRED = ['title', 'slug', 'origin', 'language', 'profiles', 'level', 'audience', 'goal',
            'sources', 'approved_on', 'concepts', 'chapters']
PROFILES = {'stem', 'languages', 'skills', 'knowledge'}
CHOICES = {'images': {'svg', 'illustrations', 'paid-api'}, 'reading': {'large', 'small'}}
LABEL_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
# goals must be checkable (references/SYLLABUS.md); these openings are not
WEAK_GOALS = re.compile(r'^(understand|know|learn about|be familiar|entender|compreender|conhecer|saber|'
                        r'aprender sobre|comprender|conocer)\b', re.I)
TODO = '<!-- TODO'


def validate(path):
    if not os.path.exists(path):
        fail(f'file not found: {path}')
    data = load_yaml(path)
    errors, warnings = [], []
    for key in REQUIRED:
        if key not in data:
            errors.append(f'missing field: {key}')
    if errors:
        return data, errors, warnings

    if not LABEL_RE.match(str(data['slug'])):
        errors.append('slug: use lowercase ASCII letters, digits and hyphens')
    if data['origin'] not in ('created', 'improved'):
        errors.append('origin: must be "created" or "improved"')
    profiles = data['profiles'] or []
    if not profiles or not set(profiles) <= PROFILES or len(profiles) > 2:
        errors.append(f'profiles: 1 or 2 of {sorted(PROFILES)}')
    if not isinstance(data['level'], dict) or not {'start', 'end'} <= set(data['level']):
        errors.append('level: needs start and end')
    for key, allowed in CHOICES.items():
        value = (data.get('choices') or {}).get(key)
        if value is not None and value not in allowed:
            errors.append(f'choices.{key}: must be one of {sorted(allowed)}')

    if not data['sources']:
        warnings.append('sources: empty')
    for i, s in enumerate(data['sources'] or [], 1):
        if not isinstance(s, dict) or not s.get('title') or not s.get('url'):
            errors.append(f'sources[{i}]: needs title and url')
        elif not DATE_RE.match(str(s.get('checked', ''))):
            errors.append(f'sources[{i}] "{s["title"]}": checked must be a YYYY-MM-DD date')

    chapters = data['chapters'] or []
    numbers = chapter_numbers(data)
    if numbers != list(range(1, len(chapters) + 1)):
        errors.append('chapters: n must go 1, 2, 3... in order, with no gaps')
    for ch in chapters:
        n = ch.get('n', '?')
        for key in ('title', 'goal'):
            if not ch.get(key):
                errors.append(f'chapter {n}: missing {key}')
        if ch.get('goal') and WEAK_GOALS.match(str(ch['goal']).strip()):
            warnings.append(f'chapter {n}: goal starts with a verb that cannot be checked ("{ch["goal"]}")')
        if not ch.get('topics'):
            warnings.append(f'chapter {n}: no topics')
        if not isinstance(ch.get('minutes'), int) or ch['minutes'] <= 0:
            warnings.append(f'chapter {n}: minutes missing (needed for the study schedule)')
        if data['origin'] == 'improved' and not ch.get('sources_original'):
            warnings.append(f'chapter {n}: sources_original empty (where it comes from in the original)')

    concepts = data['concepts'] or []
    taught = {}
    for c in concepts:
        cid = c.get('id', '')
        if not LABEL_RE.match(str(cid)):
            errors.append(f'concept "{cid}": id must be lowercase ASCII with hyphens')
        elif cid in taught:
            errors.append(f'concept "{cid}": listed twice')
        if c.get('chapter') not in numbers:
            errors.append(f'concept "{cid}": chapter {c.get("chapter")} does not exist')
        taught[cid] = c.get('chapter')
    for c in concepts:
        for dep in c.get('depends') or []:
            if dep not in taught:
                errors.append(f'concept "{c.get("id")}": depends on unknown concept "{dep}"')
            elif isinstance(taught[dep], int) and isinstance(c.get('chapter'), int) and taught[dep] > c['chapter']:
                errors.append(f'concept "{c["id"]}" (ch. {c["chapter"]}) depends on "{dep}", '
                              f'taught later (ch. {taught[dep]})')
    for n in numbers:
        if n not in taught.values():
            warnings.append(f'chapter {n}: teaches no concept in the concept graph')

    if data['origin'] == 'improved':
        if not data.get('original'):
            errors.append('improved book: missing original (what the material was)')
        promise = data.get('promise') or {}
        if not {'goal', 'audience', 'level', 'sequence'} <= set(promise):
            errors.append('improved book: promise needs goal, audience, level and sequence')
        pct = data.get('new_content_pct')
        if isinstance(pct, (int, float)) and pct > 20:
            warnings.append(f'new content at {pct}%: above the ~20% limit, say why in the plan')
    if data.get('translation_of') and not data.get('glossary'):
        errors.append('translation: missing glossary')
    if data['approved_on'] and not DATE_RE.match(str(data['approved_on'])):
        errors.append('approved_on: must be empty or a YYYY-MM-DD date')
    return data, errors, warnings


def cmd_validate(args):
    data, errors, warnings = validate(args.path)
    result = {'ok': not errors, 'errors': errors, 'warnings': warnings}
    if not errors:
        result['book'] = {'title': data['title'], 'chapters': len(data['chapters']),
                          'concepts': len(data['concepts']), 'approved': bool(data['approved_on'])}
        remember(args.path)
        result['selected'] = os.path.abspath(args.path)
    out(result, 0 if not errors else 1)


def chapter(data, n):
    for ch in data['chapters']:
        if ch.get('n') == n:
            return ch
    fail(f'chapter {n} is not in book.yaml')


def summaries(data):
    return {p['n']: p.get('summary', '') for p in data.get('progress') or [] if 'n' in p}


def skeleton(data, ch, lab, review):
    n = ch['n']
    lines = [f'# {n}. {ch["title"]}', '',
             f'> 🗺️ **{lab["In this chapter"]}:** <!-- TODO: 1–2 sentences --> · ⏱️ ~{ch.get("minutes", "?")} min', '']
    if n > 1:
        lines += [f'> 🔥 **{lab["Warm-up"]}:** <!-- TODO: 1–2 questions on earlier chapters, answers hidden -->', '',
                  f'## {lab["Where we left off"]}', '', '<!-- TODO: 2–3 sentences -->', '']
    topic_todo = ('<!-- TODO: why → definition → example → code/procedure with real output '
                  '→ diagram → common mistake -->')
    for topic in ch.get('topics') or ['<!-- TODO: topic -->']:
        lines += [f'## {topic}', '', topic_todo, '']
    lines += [f'## 🏋️ {lab["Practice"]}', '',
              '<!-- TODO: worked example → complete it → on your own → challenge -->', '',
              f'## 🧠 {lab["Quick review"]}', '',
              '<!-- TODO: 3–5 questions, at least one from an earlier chapter -->', '',
              f'## 🤖 {lab["Study with an AI tutor"]}', '', '<!-- TODO: 2 ready-to-copy prompts -->', '',
              f'> ➡️ **{lab["Next"]}:** <!-- TODO -->', '',
              f'## 📌 {lab["Summary"]}', '', '<!-- TODO: table: item | one sentence -->', '',
              f'## 📚 {lab["Sources"]}', '', '<!-- TODO: links with the date checked -->', '']
    if review:
        lines += [f'> 🔁 **{lab["Review today"]}:** ' + ', '.join(str(r) for r in review), '']
    return '\n'.join(lines)


def cmd_brief(args):
    book_dir, path = find_book(args.book)
    data = load_yaml(path)
    n = args.n
    ch = chapter(data, n)
    lab = labels(data.get('language', 'en'))
    # spaced review: 1, 3, 7 and 15 chapters back
    review = sorted({n - k for k in (1, 3, 7, 15) if n - k >= 1})
    file = chapter_path(book_dir, n)
    created = False
    if not file:
        file = os.path.join(book_dir, 'chapters', f'{n:02d}-{slugify(ch["title"])}.md')
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(skeleton(data, ch, lab, review))
        created = True
    done = summaries(data)
    others = {c['n']: c for c in data['chapters']}
    brief = {
        'chapter': {k: ch.get(k) for k in ('n', 'title', 'goal', 'topics', 'minutes')},
        'file': os.path.relpath(file, book_dir).replace(os.sep, '/'),
        'skeleton_created': created,
        'language': data.get('language'), 'profiles': data.get('profiles'), 'choices': data.get('choices'),
        'previous': {'n': n - 1, 'title': others[n - 1]['title'], 'summary': done.get(n - 1, '')} if n > 1 else None,
        'next': {'n': n + 1, 'title': others[n + 1]['title']} if n + 1 in others else None,
        'concepts_you_may_use': [c['name'] for c in data['concepts'] if c.get('chapter', n) < n],
        'concepts_to_teach': [c['name'] for c in data['concepts'] if c.get('chapter') == n],
        'warm_up_from': [k for k in (n - 1, n - 2) if k >= 1],
        'review_today': review,
        'sources': [{'title': s['title'], 'url': s['url']} for s in data.get('sources') or []],
    }
    if ch.get('sources_original'):
        brief['original_sections'] = ch['sources_original']
    if data.get('translation_of'):
        original = os.path.join(os.path.dirname(book_dir), data['translation_of'])
        source = chapter_path(original, n) or original
        brief['original_chapter'] = os.path.relpath(source, book_dir).replace(os.sep, '/')
        brief['glossary'] = data.get('glossary')
    out(brief)


def cmd_done(args):
    book_dir, path = find_book(args.book)
    data = load_yaml(path)
    chapter(data, args.n)
    file = chapter_path(book_dir, args.n)
    if not file:
        fail(f'chapter {args.n} has no file yet: run "book.py brief {args.n}" first')
    left = open(file, encoding='utf-8').read().count(TODO)
    if left:
        fail(f'chapter {args.n} still has {left} TODO placeholder(s): finish it and run audit.py {args.n}')
    summary = (args.summary or '').strip()
    if not summary:
        fail('--summary is required (3 to 5 lines: what it taught, terms, examples used)')
    progress = [p for p in data.get('progress') or [] if p.get('n') != args.n]
    progress.append({'n': args.n, 'done': datetime.date.today().isoformat(), 'summary': summary[:800]})
    data['progress'] = sorted(progress, key=lambda p: p['n'])
    save_yaml(path, data)
    total = len(data['chapters'])
    pending = [c['n'] for c in data['chapters'] if c['n'] not in {p['n'] for p in data['progress']}]
    out({'saved': True, 'progress': f'{total - len(pending)}/{total}',
         'next': f'book.py brief {pending[0]}' if pending else 'fixed parts (references/BOOK.md), then audit.py'})


def cmd_status(args):
    book_dir, path = find_book(args.book)
    data = load_yaml(path)
    lab = labels(data.get('language', 'en'))
    done = sorted(summaries(data))
    pending = [n for n in chapter_numbers(data) if n not in done]
    files = os.listdir(os.path.join(book_dir, 'chapters')) if os.path.isdir(os.path.join(book_dir, 'chapters')) else []
    fixed = {'chapter 0': any(f.startswith('00-') for f in files),
             'mock exam': any(slugify(lab['Final mock exam']) in f for f in files),
             'glossary': any(slugify(lab['Glossary']) in f for f in files)}
    if not data.get('approved_on'):
        step = 'syllabus not approved yet'
    elif not data.get('choices'):
        step = 'ask the choices (images, reading) and save them in book.yaml'
    elif pending:
        step = f'book.py brief {pending[0]}'
    elif not all(fixed.values()):
        step = 'write the fixed parts: ' + ', '.join(k for k, v in fixed.items() if not v)
    else:
        step = 'audit.py (whole book), then build.py'
    out({'title': data.get('title'), 'slug': data.get('slug'), 'language': data.get('language'),
         'approved': bool(data.get('approved_on')), 'chapters_done': f'{len(done)}/{len(chapter_numbers(data))}',
         'pending_chapters': pending, 'fixed_parts': fixed, 'next_step': step})


def main():
    p = argparse.ArgumentParser(description='Validate the book, brief chapters and record progress.')
    sub = p.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('validate')
    v.add_argument('path')
    b = sub.add_parser('brief')
    b.add_argument('n', type=int)
    d = sub.add_parser('done')
    d.add_argument('n', type=int)
    d.add_argument('--summary')
    s = sub.add_parser('status')
    for q in (b, d, s):
        q.add_argument('--book')
    args = p.parse_args()
    {'validate': cmd_validate, 'brief': cmd_brief, 'done': cmd_done, 'status': cmd_status}[args.cmd](args)


if __name__ == '__main__':
    main()
