Act as a Senior DevOps and Security Engineer.
Conduct a Production Readiness Review (PRR) for my Django application www.harada.global

**Stack:** Linux VPS, Nginx, Gunicorn, PostgreSQL
**User for deployments**: deploy 
**Paths:**
- App root: /srv/harada
- Git bare repo: /srv/git/harada.git
- Database: harada_db, user: harada_user
- Nginx config: /etc/nginx/sites-available/harada.global
- Gunicorn service: /etc/systemd/system/harada.service

Perform the following checks. 

---

### 1. Django App Layer
1.1 Confirm DEBUG=False in the running environment
1.2 Confirm SECRET_KEY is loaded from environment (not hardcoded in settings.py)
1.3 Validate ALLOWED_HOSTS is explicit (not '*')
1.4 Confirm SECURE_SSL_REDIRECT, SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE, SECURE_HSTS_SECONDS are set
1.4 Run `pip audit` or `safety check` to identify packages with known CVEs
1.5 Check file permissions: .env and settings.py should not be world-readable (target: 600)
1.6 Check whether the admin url is the default `/admin/`. Suggest to change it to something unique 

### 2. Web Server Layer (Nginx)
2.1 Verify SSL certificate validity and expiry date (Certbot/LetsEncrypt)
2.2 Check TLS version — TLS 1.0 and 1.1 must be disabled; only TLS 1.2+ allowed
2.3 Confirm security headers: HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy
2.4 Verify Nginx correctly serves /static/ and /media/ with the app server bypassed
2.5 Confirm Nginx blocks access to /.git/, /.env, /settings.py, and any dotfiles
2.6 Verify Nginx rate-limiting on authentication endpoints:
    - Confirm limit_req_zone is defined globally (e.g., in http block or before server block)
    - Verify location blocks for /(sign-in|login|accounts/login) include BOTH:
      a) limit_req directive (e.g., limit_req zone=login_limit burst=10 nodelay;)
      b) proxy_pass directive forwarding to Gunicorn (e.g., proxy_pass http://127.0.0.1:8000;)
      c) proxy headers: Host, X-Real-IP, X-Forwarded-For, X-Forwarded-Proto
    - Example of CORRECT pattern:
      location ~ ^/(sign-in|login|accounts/login) {
          limit_req zone=login_limit burst=10 nodelay;
          proxy_pass http://127.0.0.1:8000;
          proxy_set_header Host $http_host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }
    - Confirm the proxy destination matches actual Gunicorn binding (check gunicorn_config.py)
2.7 Confirm Nginx is not exposing server version (server_tokens off)
2.8 Verify NO location blocks exist that have limit_req WITHOUT proxy_pass (indicates misconfigured rate-limiting)


### 3. Database Layer (PostgreSQL)
3.1 Confirm PostgreSQL listener is bound to localhost only (127.0.0.1), not 0.0.0.0
3.2 Verify harada_user is NOT a superuser and does NOT have CREATEDB privilege
3.3 Confirm harada_user privileges are scoped to harada_db only
3.4 Check pg_hba.conf — ensure no 'trust' authentication method is in use
3.5 Verify automated backups exist and the most recent backup file is less than 24 hours old
3.6 Check PostgreSQL version for known CVEs

### 4. OS / SSH Layer
4.1 Check UFW/iptables: only ports 80, 443, and the configured non-standard SSH port should be open
4.2 Confirm SSH PasswordAuthentication is disabled (keys only)
4.3 Confirm SSH root login is disabled (PermitRootLogin no)
4.4 Verify fail2ban is installed, running, and has an active jail for sshd
4.5 Check for unattended-upgrades or equivalent for automatic OS security patches

### 5. Process & Service Management
5.1 Confirm Gunicorn is managed by systemd and set to Restart=on-failure
5.2 Confirm Gunicorn binds to a Unix socket (not 0.0.0.0 or 127.0.0.1:PORT)
5.3 Validate worker count is appropriate for available CPU cores
5.4 Confirm --timeout flag is set (recommended: 30s) to kill hanging workers
5.5 Check Nginx and Gunicorn log rotation is configured
5.6 Check that gunicorn has a restart policy

### 6. File & Directory Permissions (Least Privilege Audit)
6.1 Secrets Protection: Verify /srv/harada/.env is set to 600 (Owner: deploy, Group: deploy).
6.2 Application Code: Verify /srv/harada/ code files are owned by deploy:deploy and NOT writable by www-data.
6.3 Static/Media Ownership: Verify /srv/harada/static and /srv/harada/media are owned by deploy:www-data.
6.4 Write Permissions: Verify media/ and logs/ directories have 775 (or 2775) permissions to allow Gunicorn to write uploads/logs.
6.5 Socket Access: Verify the Gunicorn socket file has group permissions (660 or 664) allowing Nginx to read/write.

---



### Output Format
Produce a report named: production_report_YYYY-MM-DD.md

Structure:
- **Overall Verdict:** GO / NO-GO
- **Summary Table** (Check | Status | Severity)
- **Findings** grouped by severity:
  - 🔴 HIGH — must fix before go-live
  - 🟡 MEDIUM — fix within 7 days
  - 🟢 LOW — best practice improvements
- For each finding: exact command or config change to remediate it