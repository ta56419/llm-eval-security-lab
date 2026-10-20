# LLM Eval & Security Lab

An offline evaluation harness for retrieval-augmented assistants. It checks whether responses cite supplied evidence, avoid unsupported claims, follow refusal expectations, and resist prompt injection embedded in retrieved documents.

## Why this project

The tool checks saved answers against their source texts and expected behavior. The examples use synthetic data.

## Run

Requires Python 3.11+ and the standard library only.

```bash
python -m llm_eval_security.cli examples/cases.jsonl --out report.json
```

The command prints a summary and writes a machine-readable report. Exit code is non-zero when any case fails. No API key or external model is required: provide your own model outputs in the JSONL file to evaluate a real system.

Each JSONL row has `id`, `question`, `context` (a list of `{id, text}` sources), `answer`, and `expect` fields. `expect` supports `must_cite`, `must_refuse`, and `resist_injection`.

## Checks

- Citation IDs must refer to supplied sources.
- Required refusal behavior is checked against an explicit expected outcome.
- Injection resistance cases fail if the response follows an instruction embedded in the retrieved text.
- Grounding uses a transparent lexical-support heuristic; it is a triage signal, not a semantic truth detector.
- Per-case results include reasons and a JSON summary suitable for CI.

## Limitations

This is a lightweight deterministic test harness, not a substitute for human review or model-based judging. It does not call an LLM, and lexical overlap cannot establish factual entailment. Add domain-specific cases and connect your model in a separate generation step before treating results as a release gate.

## Layout

```text
src/llm_eval_security/  evaluator and CLI
examples/cases.jsonl   synthetic evaluation suite
tests/                 unit tests
```

## License

MIT
