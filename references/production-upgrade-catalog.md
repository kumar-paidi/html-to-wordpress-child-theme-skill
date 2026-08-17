# Production Upgrade Catalog

Use this catalog to propose improvements after the core conversion is understood. Do not add every feature automatically. Select the smallest set that serves the site's real editors, visitors, maintenance model, privacy obligations, and budget.

## Core Upgrades

1. **Content Control Center** — searchable section accordions, repeaters, media pickers, help text, counts, validation, and reliable frontend binding.
2. **Global Header & Footer editor** — one authoritative source for logos, CTAs, contact details, social links, footer columns, legal text, and sticky buttons.
3. **Menu management** — native add/remove/rename/nest/reorder support with registered menu locations and one responsive source.
4. **Form routing and branded email** — multiple recipients, per-form teams, fallback rules, Reply-To, test mail, preview, and confirmation emails while SMTP stays plugin-owned.
5. **Non-destructive upgrades** — preserve the database, uploads, pages, builder templates, settings, and meta; use versioned ZIPs and rollback instructions.

## High-Value Optional Upgrades

- **Draft preview and revisions:** make content changes reviewable and restore promised revisions.
- **Role-based editing:** allow editors to change content without granting plugin/theme administration.
- **Form inbox:** store submissions with status, notes, search, export, retention, and privacy controls.
- **Import/export:** move field and global settings between staging and production without secrets or environment URLs.
- **Design tokens:** centralize approved colors, typography, spacing, radii, shadows, buttons, and container widths.
- **Conditional visibility and scheduling:** show approved campaigns or announcements by date, role, or page without hiding essential content from accessibility or search.
- **Media quality tools:** image size guidance, focal point, alt-text prompts, WebP/AVIF-compatible workflows, and deliberate crops.
- **SEO integration:** map editable content to the installed SEO plugin, Open Graph, canonical behavior, and structured data without duplicating plugin ownership.
- **Analytics continuity:** preserve consent-aware analytics, conversion events, and necessary UTM/GCLID fields without storing excess personal data.
- **Accessibility checks:** heading order, labels, alt text, keyboard operation, focus, motion, contrast, and error-summary review.
- **Performance budget:** prevent duplicate libraries, oversized media, unbounded repeaters, render-blocking assets, and cache-version mistakes.
- **Localization:** translatable interface strings, language-aware routes, locale-safe dates, and multilingual plugin compatibility.
- **Diagnostics panel:** show child/parent versions, active templates, missing dependencies, cache reminders, and mail test results without exposing secrets.
- **Migration layer:** map older meta/option keys to new schemas idempotently and record the installed data version.
- **Developer extension points:** namespaced filters/actions around schemas, rendering, recipients, subjects, and email templates.

## Selection Rules

- Add an upgrade only when its data owner is clear.
- Prefer existing WordPress or plugin capability over duplicating it in the theme.
- Keep operational features out of the theme when they must survive a theme switch, unless the project explicitly accepts theme ownership.
- Separate content, presentation, routing, transport, and credentials.
- Make migrations idempotent and reversible.
- Document permissions, defaults, empty states, retention, and failure behavior.
- Test the complete editor-to-frontend or form-to-inbox loop, not only the admin appearance.
