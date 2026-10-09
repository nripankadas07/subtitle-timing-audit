"""Bounded SRT timing and delivery-policy audit. Caption text stays out of reports."""
import argparse
import json
import math
import re
from pathlib import Path

DEFAULT = dict(min_duration_ms=700, max_duration_ms=7000, max_cps=20,
               max_line_chars=42, min_gap_ms=0)
STAMP = r'(\d{2,}):([0-5]\d):([0-5]\d),(\d{3})'
TIMING = re.compile('^' + STAMP + r' --> ' + STAMP + '$')


def policy(value):
    if not isinstance(value, dict) or set(value) - set(DEFAULT):
        raise ValueError('unknown policy field or non-object policy')
    p = {**DEFAULT, **value}
    for k, v in p.items():
        if type(v) not in (int, float) or not math.isfinite(v) or v < 0:
            raise ValueError('policy values must be finite nonnegative numbers')
        if k != 'max_cps' and type(v) is not int:
            raise ValueError('timing and character limits must be integers')
    if p['min_duration_ms'] > p['max_duration_ms'] or p['max_cps'] == 0:
        raise ValueError('inconsistent policy limits')
    return p


def parse(text):
    if len(text.encode('utf-8')) > 2 * 1024 * 1024:
        raise ValueError('SRT exceeds 2 MiB')
    text = text.lstrip('\ufeff').replace('\r\n', '\n')
    if '\r' in text or not text.strip():
        raise ValueError('empty SRT or unsupported line endings')
    blocks = re.split(r'\n[ \t]*\n', text.strip('\n'))
    if len(blocks) > 10000:
        raise ValueError('more than 10000 cues')
    cues = []
    for n, block in enumerate(blocks, 1):
        lines = block.split('\n')
        if len(lines) < 3 or not re.fullmatch(r'[1-9]\d*', lines[0]):
            raise ValueError('cue %d requires positive index, timing and text' % n)
        m = TIMING.fullmatch(lines[1])
        if not m:
            raise ValueError('cue %d has invalid timing syntax' % n)
        v = list(map(int, m.groups()))
        start, end = [((v[i]*60 + v[i+1])*60+v[i+2])*1000+v[i+3] for i in (0, 4)]
        cues.append(dict(position=n, index=int(lines[0]), start=start, end=end, lines=lines[2:]))
    return cues


def audit(text, configuration=None):
    p = policy({} if configuration is None else configuration)
    cues = parse(text)
    findings = []
    def add(code, cue, **details):
        findings.append(dict(code=code, cue=cue['position'], **details))
    seen = set()
    for i, cue in enumerate(cues):
        if cue['index'] in seen:
            add('duplicate_index', cue)
        seen.add(cue['index'])
        if cue['index'] != i+1:
            add('nonsequential_index', cue, expected=i+1)
        if i and cue['start'] < cues[i-1]['start']:
            add('chronology', cue)
        duration = cue['end']-cue['start']
        if duration <= 0:
            add('nonpositive_duration', cue)
            continue
        if not p['min_duration_ms'] <= duration <= p['max_duration_ms']:
            add('duration', cue, duration_ms=duration)
        characters = len(' '.join(' '.join(cue['lines']).split()))
        cps = characters * 1000 / duration
        if cps > p['max_cps']:
            add('reading_rate', cue, cps=round(cps, 3))
        for line, content in enumerate(cue['lines'], 1):
            if len(content) > p['max_line_chars']:
                add('line_length', cue, line=line, characters=len(content))
    active = []
    overlaps = 0
    previous_end = None
    for cue in sorted(cues, key=lambda c: (c['start'], c['position'])):
        if cue['end'] <= cue['start']:
            continue
        active = [a for a in active if a['end'] > cue['start']]
        for a in active:
            if overlaps == 10000:
                add('overlap_report_limit', cue, limit=10000)
                return dict(cues=len(cues), policy=p, findings=findings, complete=False)
            add('overlap', cue, other_cue=a['position'], milliseconds=min(a['end'], cue['end'])-cue['start'])
            overlaps += 1
        if previous_end is not None and 0 <= cue['start']-previous_end < p['min_gap_ms']:
            add('short_gap', cue, gap_ms=cue['start']-previous_end)
        previous_end = max(previous_end or 0, cue['end'])
        active.append(cue)
    return dict(cues=len(cues), policy=p, findings=findings, complete=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('srt')
    ap.add_argument('policy', nargs='?')
    args = ap.parse_args()
    try:
        data = Path(args.srt).read_bytes()
        if len(data) > 2*1024*1024:
            raise ValueError('SRT exceeds 2 MiB')
        result = audit(data.decode('utf-8'), json.loads(Path(args.policy).read_text()) if args.policy else {})
        print(json.dumps(result, sort_keys=True))
        return int(bool(result['findings']))
    except (ValueError, OSError, UnicodeError) as e:
        print(json.dumps({'error': str(e)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
