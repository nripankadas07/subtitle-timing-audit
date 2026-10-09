# subtitle-timing-audit

Offline SRT timing, overlap and reading-policy checks without caption text in reports.

## Who and why

Caption delivery reviewers who need a reproducible batch gate before handing SRT files to another team. A long cue can overlap later nonadjacent cues; numeric caption lines can disappear in liberal parsing. Manual timeline review is expensive to repeat.

Strict indexed SRT parsing; duration, reading rate, line length, gaps, sequence and all overlapping pairs; machine-readable findings without caption text.

## Quickstart

Python 3.10+ and pip. Git source installation, no external-registry publication:

```sh
git clone https://github.com/nripankadas07/subtitle-timing-audit.git
cd subtitle-timing-audit
python -m venv .venv
# Unix: source .venv/bin/activate; Windows: .venv\Scripts\activate
python -m pip install .
subtitle-timing-audit sample.srt policy.json
python demo.py
python verify.py
```

CLI JSON on stdout. Exit **0** passes/claims, **1** policy findings or authentication/replay rejection, **2** malformed/unsupported input or IO errors. For automation, inspect the JSON and exit status together. Help: `subtitle-timing-audit --help`.

The fixture data is entirely synthetic. `demo.py` runs the example without installation and asserts a useful success and failure. `verify.py` additionally checks source tests, compilation and a fresh wheel installation in a temporary environment outside the source directory.

## Input and output

Read the checked-in fixture and policy JSON alongside `subtitle_timing_audit.py`. Policies reject unknown keys and invalid types rather than silently defaulting. See [DEMO.md](DEMO.md) for exact commands, expected outcome and schema notes; [VALIDATION.md](VALIDATION.md) for measured checks; [RESEARCH.md](RESEARCH.md) for dated comparable evidence and limits.

## Scope and limits

SRT only, indexed cues and comma milliseconds; no positioning fields, WebVTT, media-duration checks or rendered-font metrics. Reading rate counts normalized Unicode code points including markup; it is a declared delivery metric, not a visibility/accessibility certification. UTF-8, BOM and CRLF supported; bare CR unsupported. 2 MiB, 10,000 cues and 10,000 overlap pairs. Truncation is a finding and complete=false, never a clean result.

## Support

[Support, contribution and security](SUPPORT.md). MIT license. No performance or superiority claim; existing established tools are preferable when you need their broader workflows.
