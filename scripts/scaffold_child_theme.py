#!/usr/bin/env python3
"""Create a safe WordPress child-theme skeleton for a known parent theme."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


CHILD_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PARENT_SLUG = re.compile(r"^[A-Za-z0-9._-]+$")
VERSION = re.compile(r"^[0-9]+(?:\.[0-9A-Za-z-]+)*$")


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"Error: {message}")


def clean_header(value: str, label: str) -> str:
    cleaned = " ".join(value.split())
    if not cleaned or "*/" in cleaned:
        fail(f"{label} is empty or contains an unsafe comment terminator")
    return cleaned


def php_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def style_css(args: argparse.Namespace) -> str:
    return f"""/*
Theme Name: {clean_header(args.child_name, 'child name')}
Description: {clean_header(args.description, 'description')}
Author: {clean_header(args.author, 'author')}
Template: {args.parent_slug}
Version: {args.version}
Text Domain: {args.text_domain}
*/

/* Keep only small WordPress-level overrides here. Put approved design CSS in assets/css/site.css. */
"""


def functions_php(args: argparse.Namespace) -> str:
    prefix = args.child_slug.replace("-", "_")
    parent_enqueue = ""
    child_dependencies = "array()"
    if args.enqueue_parent_style:
        parent_enqueue = f"""
    $parent_theme = wp_get_theme( get_template() );
    wp_enqueue_style(
        '{args.child_slug}-parent',
        get_template_directory_uri() . '/style.css',
        array(),
        $parent_theme->get( 'Version' ) ?: null
    );
"""
        child_dependencies = f"array( '{args.child_slug}-parent' )"

    classic_setup = ""
    if args.mode == "classic":
        classic_setup = f"""
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'custom-logo' );
    add_theme_support(
        'html5',
        array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script' )
    );
    register_nav_menus(
        array(
            'primary' => __( 'Primary Menu', '{php_string(args.text_domain)}' ),
            'footer'  => __( 'Footer Menu', '{php_string(args.text_domain)}' ),
        )
    );
"""

    return f"""<?php
/**
 * Child theme setup and assets.
 *
 * @package {clean_header(args.child_name, 'child name')}
 */

defined( 'ABSPATH' ) || exit;

function {prefix}_setup() {{
    load_child_theme_textdomain( '{php_string(args.text_domain)}', get_stylesheet_directory() . '/languages' );{classic_setup}
}}
add_action( 'after_setup_theme', '{prefix}_setup' );

function {prefix}_asset_version( $relative_path ) {{
    $absolute_path = get_stylesheet_directory() . $relative_path;
    return file_exists( $absolute_path ) ? (string) filemtime( $absolute_path ) : wp_get_theme()->get( 'Version' );
}}

function {prefix}_enqueue_assets() {{{parent_enqueue}
    wp_enqueue_style(
        '{args.child_slug}-style',
        get_stylesheet_uri(),
        {child_dependencies},
        wp_get_theme()->get( 'Version' )
    );

    wp_enqueue_style(
        '{args.child_slug}-site',
        get_stylesheet_directory_uri() . '/assets/css/site.css',
        array( '{args.child_slug}-style' ),
        {prefix}_asset_version( '/assets/css/site.css' )
    );

    wp_enqueue_script(
        '{args.child_slug}-site',
        get_stylesheet_directory_uri() . '/assets/js/site.js',
        array(),
        {prefix}_asset_version( '/assets/js/site.js' ),
        true
    );
}}
add_action( 'wp_enqueue_scripts', '{prefix}_enqueue_assets', 20 );
"""


def hybrid_template(args: argparse.Namespace) -> str:
    return f"""<?php
/**
 * Template Name: Approved HTML Design
 * Template Post Type: page
 *
 * Replace the content region with the approved, WordPress-mapped page markup.
 * Preserve get_header(), get_footer(), and the parent theme's global assignments.
 *
 * @package {clean_header(args.child_name, 'child name')}
 */

defined( 'ABSPATH' ) || exit;

get_header();
?>
<main id="primary" class="{args.child_slug}-page" tabindex="-1">
    <?php
    while ( have_posts() ) :
        the_post();
        the_content();
    endwhile;
    ?>
</main>
<?php
get_footer();
"""


def classic_files(args: argparse.Namespace) -> dict[str, str]:
    package = clean_header(args.child_name, "child name")
    return {
        "header.php": f"""<?php
/** @package {package} */
defined( 'ABSPATH' ) || exit;
?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<header class="site-header">
    <div class="{args.child_slug}-container">
        <?php if ( has_custom_logo() ) : ?>
            <?php the_custom_logo(); ?>
        <?php else : ?>
            <a class="site-title" href="<?php echo esc_url( home_url( '/' ) ); ?>">
                <?php echo esc_html( get_bloginfo( 'name' ) ); ?>
            </a>
        <?php endif; ?>
        <nav class="primary-navigation" aria-label="<?php esc_attr_e( 'Primary menu', '{php_string(args.text_domain)}' ); ?>">
            <?php
            wp_nav_menu(
                array(
                    'theme_location' => 'primary',
                    'container'      => false,
                    'fallback_cb'   => false,
                )
            );
            ?>
        </nav>
    </div>
</header>
""",
        "footer.php": f"""<?php
/** @package {package} */
defined( 'ABSPATH' ) || exit;
?>
<footer class="site-footer">
    <div class="{args.child_slug}-container">
        <?php
        wp_nav_menu(
            array(
                'theme_location' => 'footer',
                'container'      => false,
                'fallback_cb'   => false,
            )
        );
        ?>
    </div>
</footer>
<?php wp_footer(); ?>
</body>
</html>
""",
        "front-page.php": f"""<?php
/** @package {package} */
defined( 'ABSPATH' ) || exit;
get_header();
?>
<main id="primary" class="{args.child_slug}-front-page" tabindex="-1">
    <?php
    while ( have_posts() ) :
        the_post();
        the_content();
    endwhile;
    ?>
</main>
<?php get_footer(); ?>
""",
        "page.php": f"""<?php
/** @package {package} */
defined( 'ABSPATH' ) || exit;
get_header();
?>
<main id="primary" class="{args.child_slug}-content" tabindex="-1">
    <?php
    while ( have_posts() ) :
        the_post();
        ?>
        <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
            <h1><?php the_title(); ?></h1>
            <?php the_content(); ?>
        </article>
        <?php
    endwhile;
    ?>
</main>
<?php get_footer(); ?>
""",
        "index.php": f"""<?php
/** @package {package} */
defined( 'ABSPATH' ) || exit;
get_header();
?>
<main id="primary" class="{args.child_slug}-content" tabindex="-1">
    <?php if ( have_posts() ) : ?>
        <?php while ( have_posts() ) : the_post(); ?>
            <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
                <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
                <?php the_excerpt(); ?>
            </article>
        <?php endwhile; ?>
        <?php the_posts_navigation(); ?>
    <?php else : ?>
        <p><?php esc_html_e( 'No content found.', '{php_string(args.text_domain)}' ); ?></p>
    <?php endif; ?>
</main>
<?php get_footer(); ?>
""",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-name", required=True)
    parser.add_argument("--parent-slug", required=True)
    parser.add_argument("--child-name", required=True)
    parser.add_argument("--child-slug", required=True)
    parser.add_argument("--output", type=Path, required=True, help="Directory that will receive the child folder")
    parser.add_argument("--mode", choices=("builder", "hybrid", "classic"), default="builder")
    parser.add_argument("--version", default="1.0.0")
    parser.add_argument("--author", default="Site Team")
    parser.add_argument("--description", default="Production child theme generated from an approved HTML design.")
    parser.add_argument("--text-domain")
    parser.add_argument(
        "--enqueue-parent-style",
        action="store_true",
        help="Use only after confirming the parent does not enqueue its own stylesheet",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not CHILD_SLUG.fullmatch(args.child_slug):
        fail("child slug must contain lowercase letters, digits, and single hyphens only")
    if not PARENT_SLUG.fullmatch(args.parent_slug):
        fail("parent slug must be an exact safe theme directory name")
    if not VERSION.fullmatch(args.version):
        fail("version must start with a number and contain dot-separated safe segments")
    args.text_domain = args.text_domain or args.child_slug
    if not CHILD_SLUG.fullmatch(args.text_domain):
        fail("text domain must use lowercase letters, digits, and single hyphens only")
    clean_header(args.parent_name, "parent name")

    target = args.output.resolve() / args.child_slug
    if target.exists():
        fail(f"target already exists; refusing to overwrite: {target}")

    write(target / "style.css", style_css(args))
    write(target / "functions.php", functions_php(args))
    write(
        target / "assets/css/site.css",
        f"""/* Approved design styles belong here, scoped to .{args.child_slug}-page or a specific body class. */

.{args.child_slug}-container {{
    width: min(1180px, calc(100% - 32px));
    margin-inline: auto;
}}
""",
    )
    write(
        target / "assets/js/site.js",
        """/* Keep interactions accessible, bounded, and dependency-light. */
document.documentElement.classList.add('js');
""",
    )
    (target / "languages").mkdir(parents=True, exist_ok=True)

    if args.mode == "hybrid":
        write(target / "template-approved-html.php", hybrid_template(args))
    elif args.mode == "classic":
        for relative, content in classic_files(args).items():
            write(target / relative, content)

    summary = {
        "child_theme": str(target),
        "parent_name": args.parent_name,
        "parent_slug": args.parent_slug,
        "mode": args.mode,
        "enqueue_parent_style": args.enqueue_parent_style,
        "files": sorted(path.relative_to(target).as_posix() for path in target.rglob("*") if path.is_file()),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
