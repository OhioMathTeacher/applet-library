#!/usr/bin/env python3
"""Build the offline standards catalog from the Common Standards Project API.

Run once (needs internet); the output in ../standards/ is what the app ships with.
Each standards document (framework + content area + grade) becomes one small .js
file, loaded only when a teacher picks it, so the app works offline and from file://.

    python3 tools/build_standards.py
"""
import json
import os
import re
import urllib.request

API = 'https://api.commonstandardsproject.com/api/v1'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'standards')
CACHE = os.path.join(HERE, '.cache')

JURISDICTIONS = {
    'Common Core': '67810E9EF6944F9383DCC602A3484C23',
    'NGSS': '71E5AA409D894EB0B43A8CD82F727BFE',
    'Ohio': 'F4CB2B5DF6904071BBCC671A3AB783B8',
    'CSTA': 'C2D26B5D03E74C7B9AFFE6F592601728',
}

# (framework, CSP subject, label shown in the app, keep(set title) -> bool)
PICKS = [
    ('Common Core', 'Mathematics', 'Mathematics',
     lambda t: t.startswith('Grade ') or t.startswith('Grades 9, 10, 11, 12')),
    ('Common Core', 'English Language Arts & Literacy', 'English Language Arts', lambda t: True),
    ('NGSS', 'Science Performance Expectations (2013-)', 'Science', lambda t: True),
    ('Ohio', 'Mathematics (2017-)', 'Mathematics',
     lambda t: t.startswith('Grade ') or t == 'Grades 9, 10, 11, 12'),
    ('Ohio', 'English Language Arts (2017-)', 'English Language Arts', lambda t: True),
    ('Ohio', 'Science (2018-)', 'Science',
     lambda t: t.startswith('Grade ') or t.endswith('Content Statements: Grades 9-12')),
    ('Ohio', 'Social Studies (2018-)', 'Social Studies', lambda t: True),
    ('Ohio', 'Computer Science (2022-)', 'Computer Science', lambda t: True),
    ('CSTA', 'Computer Science (2017)', 'Computer Science', lambda t: not t.startswith('All Grades')),
]

# Headings, not things a puzzle would be aligned to.
SKIP_LABELS = {'Cluster', 'Disciplinary Core Idea', 'Topic', 'Domain', 'Strand', 'Course'}


def fetch(path):
    os.makedirs(CACHE, exist_ok=True)
    cached = os.path.join(CACHE, re.sub(r'[^A-Za-z0-9]', '_', path) + '.json')
    if not os.path.exists(cached):
        urllib.request.urlretrieve(API + path, cached)
    with open(cached) as f:
        return json.load(f)['data']


def grade_label(title):
    t = title.strip()
    m = re.match(r'^(.*) Content Statements: Grades 9-12$', t)
    if m:
        return f'High School — {m.group(1)}'
    if t in ('Grade K', 'Kindergarten'):
        return 'Kindergarten'
    if t.startswith('Grades 9, 10, 11, 12'):
        return 'High School'
    m = re.match(r'^Grades ([\d, ]+)$', t)
    if m:
        nums = [n.strip() for n in m.group(1).split(',')]
        return f'Grades {nums[0]}–{nums[-1]}'
    m = re.match(r'^Grades 9-12 (\w+)$', t)
    if m:
        return f'High School — {m.group(1)}'
    return t.replace('-', '–')


def grade_sort(levels, label):
    order = {'Pre-K': -1, 'K': 0}
    nums = [order[l] if l in order else int(l) if l.isdigit() else 99 for l in levels] or [99]
    return (min(nums), len(levels), label)


def slugify(*parts):
    return re.sub(r'[^a-z0-9]+', '-', ' '.join(parts).lower()).strip('-')


def build():
    os.makedirs(OUT, exist_ok=True)
    frameworks = {}
    for fw, subject, label, keep in PICKS:
        jur = fetch(f'/jurisdictions/{JURISDICTIONS[fw]}')
        docs = []
        for s in jur['standardSets']:
            if s['subject'].strip() != subject or not keep(s['title'].strip()):
                continue
            data = fetch(f"/standard_sets/{s['id']}")
            standards = sorted(data['standards'].values(), key=lambda x: x['position'])
            by_id = {x['id']: x for x in standards}
            items = []
            for x in standards:
                code = (x.get('statementNotation') or '').strip()
                if not code or x.get('statementLabel') in SKIP_LABELS:
                    continue
                ancestors = [by_id[a] for a in x.get('ancestorIds', []) if a in by_id]
                top = min(ancestors, key=lambda a: a['depth'], default=None)
                group = top['description'].strip() if top else ''
                sub = 1 if x.get('statementLabel') == 'Component' else 0
                items.append([code, re.sub(r'\s+', ' ', x['description']).strip(), group, sub])
            if not items:
                continue
            grade = grade_label(s['title'])
            slug = slugify(fw, label, grade)
            lic = data.get('license') or {}
            doc = {
                'id': slug, 'grade': grade,
                'source': (data.get('document') or {}).get('title', '').strip(),
                'license': lic.get('title', ''), 'rightsHolder': lic.get('rightsHolder', ''),
                'sort': grade_sort(s.get('educationLevels') or [], grade),
            }
            with open(os.path.join(OUT, slug + '.js'), 'w') as f:
                f.write('STANDARDS_LOADED(' + json.dumps(slug) + ', ' +
                        json.dumps(items, ensure_ascii=False, separators=(',', ':')) + ');\n')
            docs.append(doc)
        subjects = frameworks.setdefault(fw, {})
        subjects.setdefault(label, []).extend(docs)

    index = []
    for fw, subjects in frameworks.items():
        subj_list = []
        for label, docs in subjects.items():
            docs.sort(key=lambda d: d.pop('sort'))
            subj_list.append({'name': label, 'docs': docs})
        index.append({'name': fw, 'subjects': subj_list})
    with open(os.path.join(OUT, 'index.js'), 'w') as f:
        f.write('// Generated by tools/build_standards.py from the Common Standards Project\n')
        f.write('// (https://commonstandardsproject.com). Do not edit by hand.\n')
        f.write('window.STANDARDS_INDEX = ' + json.dumps(index, ensure_ascii=False, indent=1) + ';\n')

    total = sum(len(d['docs']) for fw in index for d in fw['subjects'])
    print(f'{total} documents written to {os.path.normpath(OUT)}')


if __name__ == '__main__':
    build()
