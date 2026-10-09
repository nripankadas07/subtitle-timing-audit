# Brief and comparable review — 9 October 2026

Observation: 9 October 2026, 06:34 UTC. Live connected GitHub queries `subtitle in:name sort:stars; subtitle lint sort:stars` sorted by stars, bounded result pages. Repository star counts fetched separately, with current default-branch code/docs/issues. Highest-star relevant comparable found: **SubtitleEdit/subtitleedit (14,482)**. This is not an exhaustive global ranking; HTML-only parsers, unrelated extractors, mobile-only release automation and report-only tools were distinguished by workflow relevance. Stars are discovery signals, not reliability/performance measurements.

Actual user: Caption delivery reviewers who need a reproducible batch gate before handing SRT files to another team.

Painful task: A long cue can overlap later nonadjacent cues; numeric caption lines can disappear in liberal parsing. Manual timeline review is expensive to repeat.

Smallest useful capability: Strict indexed SRT parsing; duration, reading rate, line length, gaps, sequence and all overlapping pairs; machine-readable findings without caption text.

Acceptance: good synthetic fixture passes; confirmed contract violation produces actionable JSON/exit 1; malformed input produces exit 2; installed quickstart works outside source; core boundary/concurrency/format regressions pass; remote Python matrix passes before LIVE.

Evidence and demand: Verified general bug evidence: [pysubs2 #119](https://github.com/tkarabela/pysubs2/issues/119), opened 30 September 2026, reports a numeric final caption line dropped by 1.9.0. Our strict indexed parser has a numeric-line regression; we did not rerun competitor versions or prove their current code defective. Need for this exact MVP is inferred, not an upstream request to build it.

Portfolio/distinctness: medialoom concerns media cataloguing; this tool checks exported caption timing and delivery policy. XML, DNS, releases and webhook authentication consume different data and serve different users. Compared all five briefs and 148 current owned repository descriptions and files where overlapping. No fork, rename or product subdivision counted as new.

Discovery: Search terms SRT overlap audit and subtitle CI; a runnable fixture and tagged topic metadata make the contract discoverable.

| Comparable | Stars | Last push UTC | License metadata | Observed workflow/capability tradeoff |
| --- | ---: | --- | --- | --- |
| [SubtitleEdit/subtitleedit](https://github.com/SubtitleEdit/subtitleedit) | 14482 | 2026-10-09T06:19:15Z | MIT | Desktop subtitle editing, timeline review and broad formats; heavier interactive workflow than an offline SRT JSON gate. |
| [Aegisub/Aegisub](https://github.com/Aegisub/Aegisub) | 3385 | 2025-01-01T21:42:03Z | NOASSERTION | Desktop subtitle editing and typesetting; source/build workflow, broader ASS features, not measured here. |
| [tkarabela/pysubs2](https://github.com/tkarabela/pysubs2) | 443 | 2026-09-27T19:08:28Z | MIT | pip-installable multi-format Python subtitle library and CLI; flexible reading/writing and examples. |

- [SubtitleEdit/subtitleedit source](https://github.com/SubtitleEdit/subtitleedit/blob/b1d3d2de31f86b8386a7a7eb76e76210a83e916f/src/libse/SubtitleFormats/SubRip.cs), head `b1d3d2de31f86b8386a7a7eb76e76210a83e916f`. README `README.md`, source and up to five current issue/PR entries read. Maintenance signal is the dated push, not a guarantee of support. Issue examples: Speech to text: visible progress for whisper.cpp (#15836), No progress display on Speech to text window
- [Aegisub/Aegisub source](https://github.com/Aegisub/Aegisub/blob/6f546951b4f004da16ce19ba638bf3eedefb9f31/src/subtitle_format_srt.cpp), head `6f546951b4f004da16ce19ba638bf3eedefb9f31`. README `README.md`, source and up to five current issue/PR entries read. Maintenance signal is the dated push, not a guarantee of support. Issue examples: Errors on startup on Debian Xfce (version 3.2.2), Can't Export Encore
- [tkarabela/pysubs2 source](https://github.com/tkarabela/pysubs2/blob/ae3c520a8aa13130f36d84df02ce15a843bc9bdb/pysubs2/formats/subrip.py), head `ae3c520a8aa13130f36d84df02ce15a843bc9bdb`. README `README.md`, source and up to five current issue/PR entries read. Maintenance signal is the dated push, not a guarantee of support. Issue examples: SRT reader drops last line when it is only a number, is there a way to fix words that are displayed at the same time (ass>srt)

Installability, time to first result, reliability and support comparison: README instructions, examples, current source and issues were reviewed. Competitor clean installations, workload timing, historical support response and demo reliability were **not measured**. Our own clean installation/demo proves only our behavior. NOASSERTION is incomplete license metadata, not a conclusion about permission. Licenses/attribution require actual upstream license review before reuse; no upstream code reused here.

No technical-performance benchmark or superiority claim. Workloads/hardware/versions were not measured equivalently, so stars and a successful example do not imply we outperform these tools. Broader tools already offer valuable workflows; this MVP chooses a small explicit contract with significant limits.
