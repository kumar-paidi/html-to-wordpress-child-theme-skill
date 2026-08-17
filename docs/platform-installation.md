# Cross-platform installation

This repository follows the open [Agent Skills specification](https://agentskills.io/specification). A compatible agent discovers the `SKILL.md` file first and loads the supporting scripts, references and assets only when they are needed.

## OpenAI Codex

Install for one project from the project root:

```bash
git clone https://github.com/kumar-paidi/html-to-wordpress-child-theme-skill.git \
  .agents/skills/convert-html-to-wordpress-child-theme
```

Install for your user account:

```bash
git clone https://github.com/kumar-paidi/html-to-wordpress-child-theme-skill.git \
  "$HOME/.agents/skills/convert-html-to-wordpress-child-theme"
```

Restart or reload the agent if it does not discover the skill immediately. Invoke it explicitly with `$convert-html-to-wordpress-child-theme`.

Official guide: [Build skills for Codex and ChatGPT](https://learn.chatgpt.com/docs/build-skills)

## Claude Code

Install for one project from the project root:

```bash
git clone https://github.com/kumar-paidi/html-to-wordpress-child-theme-skill.git \
  .claude/skills/convert-html-to-wordpress-child-theme
```

Install globally:

```bash
git clone https://github.com/kumar-paidi/html-to-wordpress-child-theme-skill.git \
  "$HOME/.claude/skills/convert-html-to-wordpress-child-theme"
```

Invoke it with `/convert-html-to-wordpress-child-theme`, or describe a matching HTML-to-WordPress conversion task and allow Claude Code to select it automatically.

Official guide: [Extend Claude with skills](https://code.claude.com/docs/en/skills)

## Claude.ai

1. Download a versioned release ZIP whose top-level folder contains `SKILL.md`.
2. Open **Customize → Skills**.
3. Select **+ → Create skill → Upload a skill**.
4. Upload the ZIP and enable the skill.

Custom-skill availability can vary by plan, organization policy and product rollout. Uploaded custom skills are private to the account unless an organization administrator shares them.

Official guide: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)

## Google Antigravity

Install for one workspace from its root:

```bash
git clone https://github.com/kumar-paidi/html-to-wordpress-child-theme-skill.git \
  .agents/skills/convert-html-to-wordpress-child-theme
```

Install globally:

```bash
git clone https://github.com/kumar-paidi/html-to-wordpress-child-theme-skill.git \
  "$HOME/.gemini/config/skills/convert-html-to-wordpress-child-theme"
```

Official guide: [Antigravity skills](https://antigravity.google/docs/skills)

## ChatGPT

Use the [published ChatGPT skill](https://chatgpt.com/skills?skill_id=6a82a645ac34819198c2c8c1ae9cfc24). OpenAI plugins are the better distribution format when one package must work across more ChatGPT and Codex surfaces.

## Bolt, Lovable and other AI builders

Do not assume that an AI product supports Agent Skills merely because it can accept prompts or import a GitHub repository. Check its current official documentation for native `SKILL.md` discovery.

If the product does not support the standard, use an adapter:

1. Copy the essential workflow from `SKILL.md` into the product's project instructions or knowledge area.
2. Keep the repository available as reference material.
3. Run `scripts/scaffold_child_theme.py`, `scripts/validate_child_theme.py` and `scripts/package_child_theme.py` in a real shell or CI job.
4. Do not claim full compatibility when the host cannot read files, run commands or create a versioned ZIP.

## Verification prompt

After installation, ask:

```text
Use the convert-html-to-wordpress-child-theme skill. Before writing code,
list the parent-theme, builder, editable-content and email-routing details
you must discover.
```

The agent should begin with discovery and must not guess the active parent-theme folder slug.
