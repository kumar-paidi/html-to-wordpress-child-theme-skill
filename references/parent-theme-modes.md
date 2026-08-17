# Parent Theme Modes

## Select by Ownership

| Situation | Recommended mode |
|---|---|
| Divi/Elementor controls global header, footer, and pages | Builder-compatible |
| One approved custom page needs bespoke PHP markup | Hybrid template |
| Parent supplies features but child owns complete frontend templates | Classic templates |
| Existing child theme already works | Update in place; do not scaffold |

## Divi

- Use `Template: Divi` exactly when the parent directory is `Divi`.
- Let the existing Divi installation, Theme Builder, and page templates continue to supply their assigned header and footer.
- Do not create duplicate Divi Theme Builder assignments or duplicate `[ws_header]` / `[ws_footer]` output.
- Prefer builder-compatible or hybrid mode.
- Scope selectors so they do not alter unrelated Divi modules.
- Do not enqueue jQuery, icon fonts, or libraries Divi already supplies.
- After installation or replacement, clear **Divi → Theme Options → Builder → Advanced → Clear Static CSS File Generation**, then purge plugin, server/CDN, and browser caches.

## Elementor and Hello Elementor

- Preserve Elementor Pro Theme Builder header/footer assignments when present.
- Prefer builder-compatible mode for pages edited in Elementor.
- Use a hybrid page template only when bespoke PHP markup is required.
- Avoid forcing `the_content()` wrappers or container widths that fight the selected Elementor page layout.
- Do not load duplicate icon or animation libraries.

## Astra and GeneratePress

- Prefer hooks, filters, layout settings, and hybrid templates before overriding global templates.
- Preserve parent container, typography, WooCommerce, and accessibility behavior unless the approved design intentionally replaces it.
- Confirm the parent's stylesheet enqueue behavior before adding a parent-style enqueue.

## Block Themes

- Confirm whether a child theme with `theme.json`, templates, and template parts is appropriate instead of classic PHP templates.
- Preserve Site Editor templates and global styles when the user expects visual editing.
- Use block markup and valid template-part structure; do not mix classic template assumptions blindly.

## Classic Themes

- Use Classic mode only when ownership is clear.
- Include `wp_head()`, `wp_footer()`, `wp_body_open()`, body classes, semantic landmarks, template loops, and accessible navigation.
- Reuse parent hooks and helpers when they are part of the theme contract.

## Existing Child Themes

- Treat the current child theme as the source of truth for slug, text domain, versioning, hooks, and file structure.
- Preserve existing files and unrelated customizations.
- Update the version in `style.css` and use versioned ZIP names.
- Do not rename the theme folder during routine replacements; WordPress may treat it as a different theme.
