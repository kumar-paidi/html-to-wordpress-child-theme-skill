# Admin Content Control Center

Use this pattern when bespoke templates need many editable sections but the current builder or block editor cannot expose them cleanly.

## Choose the Data Owner

Prefer existing WordPress ownership before creating fields:

| Content | Preferred owner |
|---|---|
| Page title and long-form copy | Page/block/builder content |
| Header and footer navigation | Registered WordPress menus or Navigation blocks |
| Logo and site identity | Custom Logo/site settings or parent-theme option |
| Blog, news, team, jobs, projects | Posts or justified custom post types |
| One page's bespoke sections | Page meta controlled by a section registry |
| Site-wide CTAs/contact details | Settings API or existing theme option |
| SEO, forms, SMTP, analytics | Existing specialist plugin |

Do not duplicate the same source in a builder module and custom meta. Record one authoritative owner for every editable value.

## Model the Screen from a Registry

Define each section once with a stable key, label, icon, description, item count, fields, constraints, and frontend renderer. Use [../assets/content-control-schema-template.php](../assets/content-control-schema-template.php) as a starting point.

Support only the field types the project needs:

- text, textarea, rich text, number, URL, email, telephone, select, toggle, color, date, and time;
- image, file, video, gallery, icon, or focal-point controls backed by Media Library attachment IDs;
- link groups with label, URL, target, and accessibility text;
- repeaters for slides, cards, counters, testimonials, locations, team members, FAQs, or rows;
- relationship selectors for pages, posts, taxonomies, menus, forms, or reusable blocks.

Keep storage predictable. Use page meta for page-specific values and options for global values. Prefer stable associative keys over positional-only storage so reordering does not corrupt data.

## Build the Editing Experience

Create a full-width content panel with:

1. a plain-language notice naming the page and explaining where edits appear;
2. a section search field that filters labels, descriptions, and field text;
3. Open All and Close All buttons;
4. section shortcut chips that focus and open their matching accordion;
5. accordion headers with icon, title, help text, item count, and expanded state;
6. well-spaced cards for repeated items with Add, Duplicate, Remove, Move Up, Move Down, or drag handles;
7. image preview, Replace, Remove, alt text, and optional focal-point controls;
8. inline validation and an error summary linked to invalid fields;
9. normal WordPress Update plus optional Save Section/Save All only when implemented without bypassing security or revisions;
10. success feedback that identifies what was saved.

Make the interface responsive and accessible. Use buttons for actions, unique labels and IDs, `aria-expanded`, keyboard-operable reordering, visible focus, sufficient contrast, and reduced-motion behavior. Do not rely on color or drag-and-drop alone.

## Manage Header, Footer, and Menus

Keep header and footer editing on a separate global screen when they are reused across pages. Allow editors to change logos, contact details, announcement bars, CTA labels/links, social links, footer columns, legal text, and sticky buttons when these are project-owned.

Use registered WordPress menu locations whenever possible. They already support add, remove, rename, nest, and reorder. If the project requires a custom menu editor, preserve those same capabilities and render through a single authoritative data source. Never maintain separate desktop and mobile arrays unless their content truly differs.

When reusable shortcodes supply header or footer output, keep their rendering functions independent and prevent Theme Builder assignments from outputting the same chrome twice.

## Save Securely

- Check the nonce before processing.
- Check the exact edit or settings capability.
- Ignore autosaves, revisions, and multisite-switched writes when applicable.
- Unslash request data before sanitizing it.
- Sanitize recursively by declared field type; do not run every value through one generic sanitizer.
- Validate URLs, emails, IDs, allowed choices, ranges, repeater limits, and attachment types.
- Escape late according to output context.
- Delete intentionally cleared values; do not accidentally erase fields absent from a partial request.
- Use namespaced or strongly prefixed functions, hooks, option keys, meta keys, handles, nonces, and DOM IDs.

Use `wp_enqueue_media()` only on relevant admin screens. Scope admin CSS and JavaScript to the control center so builder screens and unrelated WordPress pages are unaffected.

## Connect Data to the Frontend

Build a field-to-template map before coding. Every registry key must have:

- a storage location;
- a sanitizer and validator;
- a default or empty-state rule;
- a frontend output location;
- an escaping rule;
- a migration rule when an earlier version used a different key.

Render safe fallbacks for missing content. Do not repopulate deliberately cleared values from sample defaults after the first save.

## Verify the Complete Loop

For every section:

1. edit a text value and choose or replace media;
2. add, remove, duplicate, and reorder a repeated item;
3. update the page or settings;
4. reload the editor and confirm persistence;
5. load the frontend without cache and confirm the exact change;
6. test an empty value, maximum item count, invalid input, and insufficient permissions;
7. verify revisions or rollback behavior promised by the implementation.

Treat a disconnected field, silent save failure, or frontend cache mismatch as a release blocker.
