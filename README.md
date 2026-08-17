# HTML to WordPress Child Theme

> Convert an approved HTML/CSS/JavaScript design into a safe, editable and installable WordPress child theme—without breaking the current parent theme.

[![Tests](https://github.com/kumar-paidi/html-to-wordpress-child-theme-skill/actions/workflows/tests.yml/badge.svg)](https://github.com/kumar-paidi/html-to-wordpress-child-theme-skill/actions/workflows/tests.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-open%20standard-6f42c1)](https://agentskills.io/)

Static previews are easy to approve. Turning them into a maintainable WordPress site is where things usually go wrong: the wrong `Template:` slug, duplicate Divi headers, hardcoded URLs, broken assets, lost editability, confusing admin fields, unsafe mail routing, update ZIPs and mobile regressions.

This repository provides an open Agent Skill and dependency-free Python utilities that guide the complete conversion—from discovering the current theme to producing a validated, versioned child-theme ZIP.

## The skill asks the right question first

Before writing theme code, it identifies:

- the active parent theme name and exact folder slug;
- the current child theme, if one exists;
- Divi, Elementor or another builder and its template assignments;
- WordPress/PHP versions and asset-loading behavior;
- which content must remain editable;
- existing pages, menus, forms, media, SMTP, analytics and plugin flows;
- who owns recipient routing, branded email, storage and delivery transport;
- which sections need add/remove/reorder controls or global settings.

It never guesses the parent theme slug and never scaffolds over an existing child theme.

## Three conversion modes

| Mode | Best for | What it preserves |
|---|---|---|
| **Builder-compatible** | Established Divi or Elementor sites | Builder pages, global header/footer and Theme Builder assignments |
| **Hybrid template** | Bespoke approved page markup | Parent header/footer plus a custom WordPress page template |
| **Classic templates** | Child theme owns the full frontend | WordPress header, footer, loops, menus and complete template shell |

## What it handles

- HTML/CSS/JavaScript-to-WordPress mapping
- Safe asset enqueueing and cache-busting
- WordPress menus, logos, pages, posts, Media Library and editable content
- Searchable section-based Content Control Centers with accessible accordions
- Repeatable slides/cards, Media Library pickers, validation and frontend binding
- Independently editable header/footer controls and manageable menus
- Multiple To/Cc/Bcc recipients, per-form routing and safe fallback rules
- Branded responsive admin emails and optional user confirmations
- Clean separation between theme routing and SMTP plugin credentials
- Divi/Elementor/Astra/GeneratePress/block/classic-theme compatibility guidance
- Scoped responsive CSS and accessible interactions
- Output escaping, input sanitization, nonces and capability checks
- Structural validation and optional PHP linting
- Versioned installable ZIP packaging
- Deployment, rollback and cache-clearing instructions
- Desktop, tablet and mobile QA gates

## A better WordPress editing experience

The skill can turn bespoke template sections into a friendly control panel modeled after the page itself:

- section search, shortcut chips and **Open All / Close All**;
- clear accordion cards for Hero, Counters, Services, Team, Gallery, News, Map, Forms and any project-defined area;
- item counts, concise help text and responsive full-width fields;
- Add, Duplicate, Remove, Move Up/Down and drag ordering for repeaters;
- image preview, Replace, Remove, alt text and Media Library selection;
- normal WordPress Update behavior with nonce, capability and field-type validation;
- complete editor → save → reload → frontend QA.

It favors native posts, pages, menus, blocks, builders and specialist plugins when they already own the data. A custom editor is introduced only when it genuinely improves the editorial workflow.

## Email routing without SMTP lock-in

The theme may manage recipients and presentation while the site's chosen SMTP or transactional-mail plugin continues to manage credentials and transport.

The workflow supports global fallbacks, different teams per form, multiple recipients, Cc/Bcc, validated Reply-To, subject rules, preview/test actions, branded HTML templates, plain-text behavior and user confirmations. SMTP passwords and provider API keys never belong in the theme or release ZIP.

## Use as an Agent Skill

[Open the skill in ChatGPT](https://chatgpt.com/skills?skill_id=6a82a645ac34819198c2c8c1ae9cfc24) and ask:

```text
Use $convert-html-to-wordpress-child-theme to convert this approved HTML design.
```

The skill follows the open [Agent Skills specification](https://agentskills.io/specification), so the same folder can be used by compatible coding agents.

## Use the utilities directly

No third-party Python packages are required.

### 1. Scaffold

```bash
python3 scripts/scaffold_child_theme.py \
  --parent-name "Divi" \
  --parent-slug "Divi" \
  --child-name "Project Child" \
  --child-slug "project-child" \
  --mode builder \
  --output ./build
```

Use `--mode hybrid` or `--mode classic` after confirming the architecture. Add `--enqueue-parent-style` only when the parent does not enqueue its own stylesheet.

### 2. Validate

```bash
python3 scripts/validate_child_theme.py ./build/project-child --fail-on warning
```

### 3. Package

```bash
python3 scripts/package_child_theme.py \
  ./build/project-child \
  --output ./dist/project-child-v1.0.0.zip
```

The ZIP contains one correct top-level child-theme folder and excludes secrets, caches, tests, source maps, databases, logs and local environment files.

## Divi-safe by design

The workflow preserves the installed Divi parent and existing Theme Builder assignments. It avoids duplicate header/footer output and reminds the implementer to clear Divi Static CSS followed by plugin, server/CDN and browser caches after an update.

It also preserves existing pages, Media Library items, forms, maps, logos, certificates, SMTP and other WordPress data instead of asking users to re-import everything after a code-only theme update.

## Repository structure

```text
SKILL.md                         Agent workflow
scripts/scaffold_child_theme.py Safe child-theme generator
scripts/validate_child_theme.py Structural validator
scripts/package_child_theme.py  Installable ZIP packager
references/                     Conversion, parent-theme and QA guidance
assets/                         Admin schema, email, report and deployment starters
tests/                          Dependency-free automated tests
```

Key guidance includes:

- `references/admin-content-control-center.md`
- `references/forms-and-email-routing.md`
- `references/production-upgrade-catalog.md`
- `assets/content-control-schema-template.php`
- `assets/branded-email-template.php`

## Quality philosophy

The approved HTML design remains the source of visual truth. The conversion should preserve its content hierarchy, typography, imagery, interactions and responsive behavior while restoring WordPress editability and data flow.

A generated ZIP is not considered complete until the parent relationship is correct, the theme installs cleanly, integrations remain intact, editable fields change the intended frontend output, form routes reach only their intended recipients and the result has been checked at real desktop, tablet and mobile widths.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions are especially welcome for additional parent-theme adapters, stronger deterministic checks and safe WordPress packaging improvements.

## License

MIT
