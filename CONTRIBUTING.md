# Contributing

Contributions should make HTML-to-WordPress conversion safer, more deterministic or easier to maintain.

## Good contributions

- a tested adapter or guardrail for a widely used parent theme or builder;
- a deterministic validation check with clear evidence and a low false-positive rate;
- safer asset, ZIP, cache or deployment behavior;
- improved WordPress accessibility, security or editability guidance;
- a focused bug fix with a regression test.

## Development

```bash
python -m unittest discover -s tests -v
```

Keep the utilities dependency-free unless a future major version establishes a compelling reason otherwise. Never add code that reads credentials, modifies a live WordPress site or overwrites an existing theme without explicit authorization.

## Pull requests

Explain the conversion problem, affected parent themes or modes, expected behavior, safety considerations and tests. Keep unrelated refactors separate.
