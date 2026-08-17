# QA and Deployment

## Structural Gate

- `style.css` exists and contains valid `Theme Name`, `Template`, `Version`, and `Text Domain` headers.
- `functions.php` exists and guards direct access.
- Parent slug matches the installed parent directory exactly, including case.
- PHP files pass `php -l` when PHP is available.
- Enqueued asset paths exist and versions prevent stale caching.
- ZIP root contains the child-theme folder, not loose theme files.
- Package excludes secrets, real environment files, caches, logs, databases, uploads, and dependency folders.

## WordPress Gate

- Theme appears under Appearance → Themes without a broken-theme warning.
- Activation does not produce PHP warnings, fatal errors, or blank screens.
- Parent theme remains installed.
- Correct child theme remains active after an update.
- Existing pages, menus, Theme Builder assignments, forms, maps, Media Library items, SMTP, analytics, SEO metadata, and plugin settings remain present.
- Admin editing remains possible for the intended content.
- Content Control Center search, shortcut chips, accordions, repeaters, media selection, validation, permissions, saving, and persistence work.
- Header/footer and menu changes render once in the correct locations without duplicate builder output.
- Multiple recipient lists remain valid and deduplicated; each form reaches only its intended routing group.
- Branded admin notifications and user confirmations render correctly, and SMTP credentials remain plugin-owned.

## Visual Gate

Check narrow mobile, wide mobile, tablet, laptop, and large desktop plus intermediate widths.

- approved layout, content, typography, imagery, spacing, and section order match;
- no horizontal scrolling or clipped meaningful content;
- navigation and hamburger spacing, focus, labels, hit area, open/close behavior, and scroll locking work;
- headings do not create unintended three-or-more-line breaks where the approved design limits them;
- images use deliberate crops and cannot force overflow;
- sticky headers, back-to-top controls, chat buttons, cookies, and other fixed UI do not overlap;
- sliders, tabs, accordions, modals, forms, video, maps, hover, touch, keyboard, and reduced motion work;
- footer text remains readable.

## Cache Gate

After Divi or cached-theme updates:

1. Clear Divi Static CSS.
2. Purge optimization/cache plugin output.
3. Purge server, CDN, or Cloudways/Varnish cache when applicable.
4. Hard refresh or open an Incognito window.
5. Test on a real phone or remote device width.

Do not diagnose a conversion as broken from a stale cached page alone.

## Safe Update Procedure

1. Back up the database and `wp-content/uploads`; retain the previous child-theme ZIP or folder.
2. Confirm the parent theme is installed.
3. Upload the versioned ZIP through Appearance → Themes → Add New → Upload Theme.
4. For the same child folder, choose **Replace current with uploaded**.
5. Confirm the intended child theme is active.
6. Clear caches in the documented order.
7. Test critical pages, navigation, forms, tracking, and mobile behavior.
8. Roll back to the retained previous ZIP if a critical regression appears.

Do not re-import existing pages, media, certificates, awards, or editable content for a normal theme-code update.

## Form and Mail Gate

- Test every route with harmless staging data and approved test recipients.
- Confirm To, Cc, Bcc, Reply-To, fallback, subject, sender display name, admin template, and user confirmation behavior.
- Confirm invalid recipient settings show a useful error and cannot cause header injection.
- Confirm the HTML template remains readable on mobile and with remote images disabled.
- Inspect the SMTP/plugin/provider log; do not treat a successful `wp_mail()` return as proof of inbox delivery.
- Confirm spam controls, accessible error/success states, retention, and deletion behavior promised by the implementation.
