---
name: convert-html-to-wordpress-child-theme
description: Convert an approved static HTML, CSS, and JavaScript website design into a production-ready WordPress child theme compatible with the site's current parent theme and page builder. Use when turning an HTML preview into WordPress; creating or updating a Divi, Elementor/Hello, Astra, GeneratePress, block-theme, or classic child theme; building user-friendly section editors, header/footer controls, menus, forms, multiple-recipient email routing, or branded email templates; packaging a versioned installable ZIP; preserving editable WordPress content and existing integrations; or fixing a child-theme conversion. Identify the active parent theme and existing child-theme architecture before writing code; preserve design fidelity, responsiveness, WordPress data flow, SMTP ownership, and safe update behavior.
---

# Convert HTML to WordPress Child Theme

Turn an approved static design into a safe, editable, installable child theme without rebuilding the design or breaking the current WordPress architecture.

Read [references/conversion-playbook.md](references/conversion-playbook.md) before converting files. Read [references/parent-theme-modes.md](references/parent-theme-modes.md) after identifying the parent theme and builder. Read [references/admin-content-control-center.md](references/admin-content-control-center.md) when the site needs friendly editable fields, repeaters, menus, or global settings. Read [references/forms-and-email-routing.md](references/forms-and-email-routing.md) when the child theme owns form handling, recipients, or email presentation. Read [references/production-upgrade-catalog.md](references/production-upgrade-catalog.md) when planning optional improvements. Read [references/qa-and-deployment.md](references/qa-and-deployment.md) before packaging or delivering an update.

## Establish the Current Theme First

Inspect the site, repository, export, or supplied files for:

- active parent theme name, directory slug, version, and style handle;
- active child theme, if any, including its slug, version, hooks, templates, and asset pipeline;
- page builder or Theme Builder assignments;
- WordPress and PHP versions;
- editable content sources, menus, forms, plugins, tracking, custom fields, shortcodes, and widgets;
- current recipient routing, SMTP/mail plugin ownership, existing form storage, privacy requirements, and branded email behavior;
- which global elements and page sections need a friendly no-code editor, including add/remove/reorder requirements;
- whether the approved HTML represents one page, multiple pages, or the entire site.

If this information cannot be inspected, ask one focused question before generating the child theme:

> What is the active parent theme and folder slug, which builder is used, and are we creating a new child theme or updating an existing one?

Do not guess the `Template:` value in `style.css`. Do not create a child theme until the parent folder slug is known.

For a redesign on an established live site, preserve existing pages and the current homepage by default. Create new pages with non-conflicting slugs such as `-new` until the user explicitly approves replacement or reassignment.

## Choose the Conversion Mode

Select the smallest compatible mode:

1. **Builder-compatible:** Add styles, scripts, hooks, and bounded integrations while preserving builder-controlled pages, header, footer, and templates. Prefer this for established Divi or Elementor sites.
2. **Hybrid template:** Add one or more custom WordPress page templates that call the parent header and footer. Prefer this when the HTML page needs bespoke markup but global site chrome must remain editable.
3. **Classic templates:** Add child `header.php`, `footer.php`, `front-page.php`, `page.php`, `index.php`, and template parts. Use only when the child theme truly owns the complete frontend structure.

Never use Classic mode merely because the HTML contains `<header>` and `<footer>`. Confirm ownership first.

## Scaffold Safely

Use the bundled generator when starting a new child theme:

```bash
python3 scripts/scaffold_child_theme.py \
  --parent-name "Divi" \
  --parent-slug "Divi" \
  --child-name "Project Child" \
  --child-slug "project-child" \
  --mode builder \
  --output ./build
```

Use `--mode hybrid` or `--mode classic` only after selecting that architecture. Pass `--enqueue-parent-style` only when inspection confirms the parent does not enqueue its own stylesheet.

For an existing child theme, do not scaffold over it. Inspect and update the current files in place while preserving unrelated changes.

## Convert the Approved Design

Preserve the approved composition, content hierarchy, typography, imagery, interactions, and responsive behavior. Do not redesign unless the user asks for design changes.

During conversion:

- remove document-level wrappers that WordPress or the parent theme already owns;
- move reusable CSS and JavaScript into child-theme assets and enqueue them through WordPress;
- replace relative asset URLs with child-theme, uploads, attachment, or configured content URLs as appropriate;
- use `get_header()`, `get_footer()`, `wp_head()`, `wp_footer()`, `wp_body_open()`, and standard template loops where the selected mode requires them;
- preserve menus, logos, pages, Media Library assets, forms, maps, SMTP, analytics, SEO, and plugin data flows;
- keep client-editable content in WordPress, the page builder, core blocks, custom fields, menus, or theme settings instead of hardcoding every value;
- provide a data-driven Content Control Center when many bespoke sections must remain editable, following [references/admin-content-control-center.md](references/admin-content-control-center.md);
- keep header and footer markup reusable and independently editable when the architecture uses templates, hooks, blocks, or shortcodes;
- use native WordPress menu management or an equally clear add/remove/rename/reorder interface instead of hardcoded navigation arrays;
- scope CSS to the page or theme namespace and avoid leaking into builder modules or WordPress admin UI;
- remove duplicate libraries and unnecessary JavaScript;
- use semantic HTML, accessible controls, meaningful alt text, keyboard behavior, reduced-motion support, and safe responsive media;
- escape output, sanitize saved input, verify nonces, and check capabilities for state-changing WordPress actions;
- use translatable strings and the child text domain for user-facing theme text.

Do not copy `<html>`, `<head>`, `<body>`, external library tags, or hardcoded production URLs into a page template without proving they belong there.

## Build Friendly Editing Surfaces

When custom fields are required, make the editing experience resemble the page rather than exposing an unstructured key-value list. Use a section registry and render searchable, keyboard-accessible accordion cards with section shortcuts, concise instructions, item counts, and Open All/Close All controls. Support appropriate field types, WordPress Media Library pickers, repeaters, drag or button reordering, visible validation, and responsive admin layouts.

Keep global controls separate from page-specific content. Typical surfaces are:

- page editor: hero, counters, cards, products, services, about, team, gallery, news, map, CTAs, and forms;
- Appearance or a bounded top-level screen: header, footer, menus, contact details, sticky buttons, form routing, and email branding;
- native WordPress screens: posts, pages, Media Library, users, menus, forms, SEO, and SMTP whenever they already own the data.

Save through normal WordPress workflows. Verify nonces and capabilities, reject autosaves and revisions where appropriate, sanitize by field type, preserve omitted values intentionally, and confirm that clicking Update changes the correct frontend section. Do not create a beautiful admin screen whose fields are disconnected from template output.

Use [assets/content-control-schema-template.php](assets/content-control-schema-template.php) as a starting manifest when a custom schema helps. Adapt it to the project's real sections; do not ship sample labels or fields unchanged.

## Route Forms and Email Safely

Treat transport and routing as separate responsibilities:

- let the user's SMTP or transactional-mail plugin own credentials, authentication, provider choice, and delivery transport;
- let the child theme own form-specific To, Cc, Bcc, Reply-To, subject, template, confirmation, and fallback routing only when the existing form plugin does not already own them;
- never store SMTP passwords, API keys, or provider secrets in the theme or ZIP;
- normalize, validate, deduplicate, and safely display multiple recipient addresses;
- preserve the WordPress administration email as a configurable or required fallback according to the project contract;
- provide per-form routing when Contact, Partner, Careers, Quote, Appointment, or other forms need different teams;
- use a branded, responsive HTML notification plus a meaningful plain-text alternative;
- include Preview and Send Test Email controls, while explaining that an accepted send request does not prove inbox delivery.

Follow [references/forms-and-email-routing.md](references/forms-and-email-routing.md) and adapt [assets/branded-email-template.php](assets/branded-email-template.php) when building theme-owned notifications. Preserve existing Contact Form 7, Gravity Forms, Fluent Forms, Elementor Forms, Divi forms, or other plugin routing unless the user asks to replace it.

## Preserve Parent-Theme Behavior

Follow the matching adapter in [references/parent-theme-modes.md](references/parent-theme-modes.md).

For Divi in particular:

- keep the parent Divi installation in place;
- preserve existing Divi Theme Builder assignments and global header/footer templates;
- do not create duplicate assignments containing header or footer shortcodes;
- avoid loading libraries Divi already loads;
- keep existing pages, Media Library items, modules, forms, maps, logos, certificates, awards, and SMTP configuration intact;
- keep header/footer controls, recipient lists, form routing, and content-control metadata intact during code-only updates;
- clear Divi Static CSS after installation or update, then purge other caches.

## Validate and Package

Run the bundled structural validator:

```bash
python3 scripts/validate_child_theme.py ./build/project-child
```

When PHP is available, lint every PHP file:

```bash
find ./build/project-child -name '*.php' -print0 | xargs -0 -n1 php -l
```

Render or install in a safe WordPress environment and test the actual page at desktop, tablet, wide mobile, and narrow mobile widths. Verify navigation, menus, sliders, forms, links, focus, hover/touch states, template order, sticky controls, caching, console errors, and image paths. Exercise the admin editor: find a section, open and close accordions, add/remove/reorder an item, choose media, save, refresh, and confirm frontend output. Exercise every form route and branded email with test recipients before production use.

Package only after validation:

```bash
python3 scripts/package_child_theme.py \
  ./build/project-child \
  --output ./dist/project-child-v1.0.0.zip
```

Use a versioned ZIP filename. Do not include `.git`, caches, test artifacts, source maps, local configuration, secrets, or real environment files.

## Deliver the Result

Provide:

- versioned installable ZIP;
- source child-theme folder;
- conversion summary showing static-to-WordPress mappings;
- editable-content map;
- admin-surface map showing page, global, menu, form-routing, and email-branding ownership;
- form-routing matrix listing fallback and per-form recipients without exposing secrets;
- validation results and known limitations;
- bounded deployment and rollback steps based on [assets/deployment-guide-template.md](assets/deployment-guide-template.md).

For a safe update, instruct the user to back up the database and `wp-content/uploads`, upload through **Appearance → Themes → Add New → Upload Theme**, choose **Replace current with uploaded** when updating the same child theme, keep the correct child theme active, clear theme/plugin/server/browser caches, and verify in Incognito or with a hard refresh.

Do not instruct the user to re-import existing pages or media unless the conversion intentionally introduces new content and the import is required.

## Completion Standard

Complete only when the parent-theme relationship is correct, the child theme installs without errors, the approved design is faithfully converted, editable content and integrations remain intact, every custom field changes the intended frontend output, multiple-recipient routing and branded email tests pass where applicable, validation passes, responsive behavior is visually checked, and the ZIP can be safely installed or updated.
