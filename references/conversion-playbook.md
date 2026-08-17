# Conversion Playbook

## 1. Inventory the Static Design

Map every HTML element to one of these destinations:

| Static element | WordPress destination |
|---|---|
| Document shell | Parent theme or child header/footer templates |
| Global navigation | `wp_nav_menu()`, Navigation block, or builder global header |
| Site logo | Custom Logo, theme option, or builder module |
| Page title/content | WordPress page fields, blocks, builder, or template loop |
| Repeated cards/items | Query loop, repeater field, custom post type, or builder module |
| Images | Media Library attachment or bundled theme asset |
| Contact/lead form | Existing form plugin or secure WordPress handler |
| Blog/news/events | Posts, custom post type, taxonomy, or query loop |
| Global CTA/settings | Options page, Customizer, builder global item, or reusable block |
| Bespoke page sections | Data-driven Content Control Center backed by page meta |
| Form recipient routing | Existing form plugin or theme settings without SMTP credentials |
| Branded notification email | Existing form plugin template or bounded theme email renderer |
| Decorative SVG/icon | Bundled asset or accessible inline SVG |
| CSS/JavaScript | Enqueued child-theme asset |

Record external fonts, libraries, icon sets, sliders, maps, tracking scripts, videos, forms, API calls, and hardcoded URLs. Remove duplicates already supplied by the parent theme or plugins.

## 2. Preserve Design Fidelity

- Keep the approved DOM order unless WordPress semantics require a bounded wrapper change.
- Extract design tokens for color, typography, spacing, containers, radius, border, shadow, and motion.
- Scope custom styles under a stable body class or page namespace.
- Replace fixed desktop values with deliberate responsive behavior, not generic shrinking.
- Preserve exact real content and relevant images. Do not introduce dummy copy or fake links.
- Keep heading length, line breaks, image crops, section rhythm, and mobile navigation aligned with the approved preview.

## 3. Make Content Editable Deliberately

Choose the least complex WordPress source that meets the editing need:

1. Existing builder modules or global items
2. Core page content or blocks
3. Menus, Custom Logo, featured image, excerpts, and native fields
4. Existing custom fields or custom post types
5. New fields or post types only when repetition or editorial workflow justifies them
6. Hardcoded theme content only for truly structural or non-editable elements

Do not add a large plugin dependency only to edit one string. Do not move working builder content into hardcoded PHP without approval.

When a custom editor is justified, follow [admin-content-control-center.md](admin-content-control-center.md). When the theme owns form routing or email presentation, follow [forms-and-email-routing.md](forms-and-email-routing.md). Keep data ownership unambiguous.

## 4. Split Files by Responsibility

- `style.css`: WordPress theme header plus minimal child overrides
- `functions.php`: setup, hooks, enqueueing, registrations, and includes
- `assets/css/site.css`: site design system and page styles
- `assets/js/site.js`: interaction only
- `template-*.php` or `page-*.php`: bespoke page composition
- `template-parts/`: repeated presentational fragments
- `inc/`: larger PHP helpers, registrations, or integration logic

Keep reusable PHP functions prefixed with a child-theme-specific namespace. Avoid anonymous global functions when maintainability matters.

## 5. Convert URLs Correctly

- Bundled asset: `get_stylesheet_directory_uri()`
- Parent asset: `get_template_directory_uri()` only when intentionally referencing the parent
- Home URL: `home_url()`
- Page URL: `get_permalink()` or resolved page/post link
- Upload: attachment functions or stored Media Library IDs
- REST/AJAX: `rest_url()` or `admin_url( 'admin-ajax.php' )`

Escape URLs with `esc_url()` at output. Do not bake staging or localhost domains into templates.

## 6. Convert JavaScript Safely

- Enqueue through `wp_enqueue_script()` and load in the footer when possible.
- Use dependencies already registered by WordPress or the parent theme.
- Pass dynamic values using a bounded data attribute, inline script helper, or localized script object as appropriate.
- Reinitialize only when the builder performs partial DOM updates and documentation requires it.
- Avoid global selectors, duplicate event handlers, console noise, and silent failures.

## 7. Preserve Existing Data

Theme ZIP replacement must not delete database content or uploads. Avoid activation routines that overwrite pages, menu assignments, options, Theme Builder templates, or plugin settings. If content creation is necessary, make it idempotent and user-authorized.
