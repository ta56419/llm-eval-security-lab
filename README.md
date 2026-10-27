# LLM Eval & Security Lab

A small Python tool for checking saved model answers against source texts. It checks citation IDs, expected refusals, some prompt-injection phrases and word overlap with the sources.

## Input

Each case contains a question, source texts, an answer and the expected checks. The examples use synthetic data. You can replace the answers with outputs from your own model.

## Run

Requires Python 3.11+ and the standard library only.

```powershell
$env:PYTHONPATH = "src"
python -m llm_eval_security.cli examples/cases.jsonl --out report.json
```

In Bash, use `export PYTHONPATH=src` instead of the first line.

The command prints a summary and writes a JSON report. It exits with a non-zero code if a case fails. It runs offline and does not need an API key.

Each JSONL row has `id`, `question`, `context` (a list of `{id, text}` sources), `answer`, and `expect` fields. `expect` supports `must_cite`, `must_refuse`, and `resist_injection`.

For a refusal case, set `response_meta.refused` to record whether the answer refused.

## Checks

- Citation IDs must refer to supplied sources.
- Required refusal behavior is checked against an explicit expected outcome.
- Injection checks look for a small list of phrases in the answer.
- The word-overlap check looks for content words shared by the answer and sources.
- Failed checks include a reason in the JSON report.

## Limitations

These are simple rules. An answer can contain the right words and still be wrong, and the phrase list cannot catch every prompt injection. Review the answers as well as the report. The tool checks existing answers; it does not generate them.

## Layout

```text
src/llm_eval_security/  evaluator and CLI
examples/cases.jsonl   synthetic evaluation suite
tests/                 unit tests
```

## License

MIT
