# Forms and Email Routing

Use this guide only when the child theme must own form processing or extend routing not already owned by a form plugin.

## Separate Responsibilities

| Responsibility | Owner |
|---|---|
| Form display and validation | Existing form plugin or bounded theme handler |
| Recipient routing and subject rules | Existing form plugin first; theme only when required |
| SMTP credentials/provider/API keys | SMTP or transactional-mail plugin |
| Email branding | Plugin template or theme-owned renderer |
| Delivery logs | Mail plugin/provider; do not duplicate without a clear need |

Never embed SMTP credentials or provider secrets in theme files, options exported with the theme, logs, screenshots, documentation, or ZIP packages.

## Provide Friendly Settings

Create a bounded **Forms & Email** tab or settings screen with:

- global fallback recipients;
- per-form To recipients for Contact, Partner, Careers, Quote, Appointment, Newsletter, or project-specific forms;
- optional Cc and Bcc groups, clearly marked because Bcc recipients are hidden;
- sender display name and a domain-aligned From address when the transport plugin allows it;
- Reply-To behavior using the validated submitter address;
- subject prefix and per-form subject pattern;
- customer confirmation toggle and confirmation subject;
- logo, accent color, heading, footer, address, phone, website, and social links for branding;
- Preview Email and Send Test Email actions;
- brief SMTP ownership/status guidance without requesting credentials.

Accept comma, semicolon, newline, or one-address-per-row input if the UI promises it. Normalize separators, trim, sanitize, validate with `is_email()`, deduplicate case-insensitively, and show rejected values. Do not silently save invalid addresses.

Preserve a safe fallback. Unless the project explicitly requires different behavior, include the WordPress administration email when no valid route exists. If the contract requires the administration email on every notification, make that rule visible and test it.

## Define a Routing Matrix

Record routing before implementation:

| Form key | To | Cc/Bcc | Reply-To | Admin template | User confirmation |
|---|---|---|---|---|---|
| `contact` | Contact team + fallback rule | Optional | Submitter | Contact enquiry | Optional |
| `partner` | Partner team + fallback rule | Optional | Submitter | Partner application | Optional |

Use stable form keys rather than matching translated titles. Keep routing filterable so a deployment can override it without editing presentation templates.

## Process Submissions Safely

- Verify a nonce and capability where relevant; for public forms, combine the nonce with spam and rate controls rather than treating it as authentication.
- Validate required fields server-side and return field-specific errors.
- Prevent header injection by rejecting line breaks in email/header values.
- Sanitize stored values and escape rendered output according to context.
- Use a honeypot and bounded rate limiting; add CAPTCHA only when justified and privacy-reviewed.
- Restrict attachments by type, extension, size, count, and storage lifecycle.
- Preserve UTM or campaign fields only when needed and disclosed.
- Avoid collecting IP addresses, user agents, or extra personal data without a documented purpose and retention rule.
- Use a Post/Redirect/Get, REST, or AJAX flow that prevents accidental resubmission and exposes accessible success/error states.

If submissions are stored, create an inbox only when the project needs it. Include role-based access, status, notes, search, export, retention, deletion, and personal-data export/erase behavior. Do not promise a CRM.

## Build Branded Email

Start from [../assets/branded-email-template.php](../assets/branded-email-template.php) and adapt it to the site's brand. Use conservative table-based layout, inline presentation styles, a readable 600–640 px content width, strong text contrast, alt text, large tap targets, and a simple footer. Treat logo images as optional because some clients block remote images.

For admin notifications, include:

- clear form type and subject;
- submission fields in a readable label/value table;
- source page and timestamp when useful;
- a safe Reply-To address;
- an optional admin CTA to view the stored submission.

For user confirmations, acknowledge receipt without exposing internal recipients, notes, routing, or unrelated submitted data. Avoid promising a response time unless the business approved it.

Send HTML using a per-message `Content-Type: text/html` header or a carefully scoped content-type filter that is removed immediately afterward. Provide a meaningful plain-text alternative when the mail layer supports it. Escape untrusted fields before inserting them into HTML.

## Test Delivery

Test each form route with a non-production submission:

1. verify all intended To, Cc, and Bcc destinations;
2. verify no unintended recipient receives it;
3. verify Reply-To opens the submitter address;
4. inspect desktop, mobile, dark-mode-tolerant, and images-disabled rendering;
5. verify links, subject, sender name, plain-text behavior, and user confirmation;
6. inspect the SMTP/plugin/provider log for authentication or deliverability errors;
7. confirm spam controls, duplicate prevention, and accessible response messages.

A successful `wp_mail()` return means WordPress handed off the request; it does not prove inbox delivery. Report that distinction in QA results.
