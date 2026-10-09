import json
from pathlib import Path
import subtitle_timing_audit as m
good=m.audit(Path('sample.srt').read_text(),json.loads(Path('policy.json').read_text()));bad=m.audit(Path('bad.srt').read_text(),json.loads(Path('policy.json').read_text()))
assert not good['findings'] and bad['findings']
print(json.dumps({'good':good,'violation':bad},indent=2))
