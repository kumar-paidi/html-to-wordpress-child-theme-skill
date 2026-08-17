<?php
/**
 * Responsive branded email template starter.
 *
 * Expected variables:
 * $brand  array{site_name:string,logo_url:string,accent:string,footer_html:string}
 * $title  string
 * $intro  string
 * $fields array<string,string>
 * $cta    array{label:string,url:string}|array{}
 *
 * Escape or allow-list every value before including this template.
 *
 * @package ProjectChild
 */

defined( 'ABSPATH' ) || exit;

$brand       = isset( $brand ) && is_array( $brand ) ? $brand : array();
$title       = isset( $title ) && is_scalar( $title ) ? (string) $title : '';
$intro       = isset( $intro ) && is_scalar( $intro ) ? (string) $intro : '';
$fields      = isset( $fields ) && is_array( $fields ) ? $fields : array();
$cta         = isset( $cta ) && is_array( $cta ) ? $cta : array();
$site_name   = isset( $brand['site_name'] ) && is_scalar( $brand['site_name'] ) ? (string) $brand['site_name'] : get_bloginfo( 'name' );
$logo_url    = isset( $brand['logo_url'] ) && is_scalar( $brand['logo_url'] ) ? (string) $brand['logo_url'] : '';
$accent      = isset( $brand['accent'] ) && is_string( $brand['accent'] ) && preg_match( '/^#[0-9a-fA-F]{6}$/', $brand['accent'] ) ? $brand['accent'] : '#165DFF';
$footer      = isset( $brand['footer_html'] ) && is_scalar( $brand['footer_html'] ) ? (string) $brand['footer_html'] : '';
$field_rows  = $fields;
$cta_data    = $cta;
?>
<!doctype html>
<html lang="<?php echo esc_attr( get_bloginfo( 'language' ) ); ?>">
<head>
	<meta charset="<?php echo esc_attr( get_bloginfo( 'charset' ) ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title><?php echo esc_html( $title ); ?></title>
</head>
<body style="margin:0;padding:0;background:#f4f7fb;color:#172033;font-family:Arial,Helvetica,sans-serif;">
	<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;background:#f4f7fb;">
		<tr>
			<td align="center" style="padding:32px 12px;">
				<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;max-width:640px;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 8px 28px rgba(23,32,51,.08);">
					<tr>
						<td style="height:6px;background:<?php echo esc_attr( $accent ); ?>;font-size:0;line-height:0;">&nbsp;</td>
					</tr>
					<tr>
						<td style="padding:30px 34px 18px;">
							<?php if ( $logo_url ) : ?>
								<img src="<?php echo esc_url( $logo_url ); ?>" width="160" alt="<?php echo esc_attr( $site_name ); ?>" style="display:block;max-width:160px;height:auto;border:0;margin:0 0 24px;">
							<?php else : ?>
								<p style="margin:0 0 24px;font-size:18px;font-weight:700;color:#172033;"><?php echo esc_html( $site_name ); ?></p>
							<?php endif; ?>
							<h1 style="margin:0 0 12px;font-size:27px;line-height:1.25;color:#172033;"><?php echo esc_html( $title ); ?></h1>
							<?php if ( $intro ) : ?>
								<p style="margin:0;font-size:16px;line-height:1.65;color:#526079;"><?php echo esc_html( $intro ); ?></p>
							<?php endif; ?>
						</td>
					</tr>
					<tr>
						<td style="padding:8px 34px 28px;">
							<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;border:1px solid #e6ebf2;border-radius:12px;border-collapse:separate;overflow:hidden;">
								<?php foreach ( $field_rows as $label => $value ) : ?>
									<?php $display_value = is_scalar( $value ) ? (string) $value : wp_json_encode( $value ); ?>
									<tr>
										<td valign="top" style="width:34%;padding:13px 15px;border-bottom:1px solid #e6ebf2;background:#f8fafc;font-size:13px;line-height:1.5;font-weight:700;color:#334155;"><?php echo esc_html( $label ); ?></td>
										<td valign="top" style="padding:13px 15px;border-bottom:1px solid #e6ebf2;font-size:14px;line-height:1.6;color:#172033;word-break:break-word;"><?php echo wp_kses_post( nl2br( esc_html( $display_value ) ) ); ?></td>
									</tr>
								<?php endforeach; ?>
							</table>
							<?php if ( ! empty( $cta_data['label'] ) && ! empty( $cta_data['url'] ) ) : ?>
								<p style="margin:26px 0 0;">
									<a href="<?php echo esc_url( $cta_data['url'] ); ?>" style="display:inline-block;padding:13px 20px;border-radius:8px;background:<?php echo esc_attr( $accent ); ?>;color:#ffffff;text-decoration:none;font-size:15px;font-weight:700;"><?php echo esc_html( $cta_data['label'] ); ?></a>
								</p>
							<?php endif; ?>
						</td>
					</tr>
					<tr>
						<td style="padding:22px 34px;background:#172033;color:#d8deea;font-size:12px;line-height:1.6;">
							<?php echo $footer ? wp_kses_post( $footer ) : esc_html( $site_name ); ?>
						</td>
					</tr>
				</table>
			</td>
		</tr>
	</table>
</body>
</html>
