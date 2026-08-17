# Child Theme Deployment Guide

## Package

- Parent theme:
- Child theme:
- Child version:
- ZIP filename:
- Conversion mode:

## Before Upload

- Back up the WordPress database.
- Back up `wp-content/uploads`.
- Retain the currently installed child-theme package for rollback.
- Confirm the required parent theme is installed.

## Install or Update

1. Open **Appearance → Themes → Add New → Upload Theme**.
2. Select the versioned ZIP.
3. Choose **Replace current with uploaded** when updating the same child theme.
4. Keep or activate the intended child theme.

## Clear Caches

1. [Theme-specific cache]
2. [Optimization/plugin cache]
3. [Server/CDN cache]
4. Browser hard refresh or Incognito

## Verify

- Header, footer, menus and page-template assignments
- Desktop, tablet and real-phone layouts
- Forms, maps, tracking and SMTP-dependent flows
- Images, icons, sliders and interactive elements
- Console/PHP errors

## Rollback

[Exact rollback package and steps]

## Content Preservation

[State which existing pages, media and settings must not be re-imported]
