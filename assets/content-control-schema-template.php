<?php
/**
 * Content Control Center schema starter.
 *
 * Copy into the generated child theme, replace the sample text domain and
 * project namespace/prefix, and adapt every section and field to the approved
 * design. Do not ship sample content.
 *
 * @package ProjectChild
 */

defined( 'ABSPATH' ) || exit;

return array(
	'hero'    => array(
		'label'       => __( 'Hero Slider', 'project-child' ),
		'icon'        => 'format-gallery',
		'description' => __( 'Manage slides, images, headings, links, and accessible alternative text.', 'project-child' ),
		'fields'      => array(
			'eyebrow' => array(
				'type'  => 'text',
				'label' => __( 'Eyebrow', 'project-child' ),
			),
			'slides'  => array(
				'type'        => 'repeater',
				'label'       => __( 'Slides', 'project-child' ),
				'min_items'   => 1,
				'max_items'   => 7,
				'item_fields' => array(
					'image_id' => array(
						'type'  => 'image',
						'label' => __( 'Image', 'project-child' ),
					),
					'alt'      => array(
						'type'  => 'text',
						'label' => __( 'Alternative text', 'project-child' ),
					),
					'heading'  => array(
						'type'  => 'text',
						'label' => __( 'Heading', 'project-child' ),
					),
					'body'     => array(
						'type'  => 'textarea',
						'label' => __( 'Description', 'project-child' ),
					),
					'link'     => array(
						'type'  => 'link',
						'label' => __( 'Button', 'project-child' ),
					),
				),
			),
		),
	),
	'contact' => array(
		'label'       => __( 'Contact & Enquiry Form', 'project-child' ),
		'icon'        => 'email',
		'description' => __( 'Edit the section copy and select the existing form integration.', 'project-child' ),
		'fields'      => array(
			'heading' => array(
				'type'  => 'text',
				'label' => __( 'Heading', 'project-child' ),
			),
			'form_id' => array(
				'type'  => 'form_select',
				'label' => __( 'Form', 'project-child' ),
			),
		),
	),
);
