# Runnable example

Run `python demo.py`; it exercises the exact source API and fails if the intended positive/negative result changes. The installed CLI is separately exercised by `python verify.py` from outside the source directory.

Commands in `smoke.json` document the expected exit status for good, findings/replay and malformed-input cases. Snapshot files are synthetic and intentionally contain no credentials or private production data.

Strict indexed SRT parsing; duration, reading rate, line length, gaps, sequence and all overlapping pairs; machine-readable findings without caption text.

SRT only, indexed cues and comma milliseconds; no positioning fields, WebVTT, media-duration checks or rendered-font metrics. Reading rate counts normalized Unicode code points including markup; it is a declared delivery metric, not a visibility/accessibility certification. UTF-8, BOM and CRLF supported; bare CR unsupported. 2 MiB, 10,000 cues and 10,000 overlap pairs. Truncation is a finding and complete=false, never a clean result.
