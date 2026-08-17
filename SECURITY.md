# Security Policy

The included tools operate on local child-theme files and must not read credentials, real environment files, databases or WordPress uploads.

Report vulnerabilities privately through GitHub's security-advisory feature when available. Do not post credentials, private client files, exploit details or sensitive WordPress configuration in a public issue.

Changes that expand file discovery, packaging or WordPress action behavior require tests covering secret exclusion, overwrite protection and safe failure.
