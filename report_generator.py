from datetime import datetime
import os


def generate_report(results, target="http://localhost:5000"):

    exploited_count = sum(1 for v in results.values() if v["exploited"])
    fixed_count = sum(1 for v in results.values() if v["fixed"])

    rating_before = "Critical" if exploited_count > 0 else "Secure"
    rating_after = "Secure" if fixed_count == len(results) else "Vulnerable"

    # Dynamic conclusion
    if exploited_count > 0 and fixed_count == 0:
        conclusion = "Application is vulnerable. Exploits were successful."
    elif fixed_count == len(results):
        conclusion = "Hardened version mitigates all vulnerabilities."
    else:
        conclusion = "Some vulnerabilities remain unpatched."

    report = f"""
========================================
Vulnerable Web App Security Report
Generated: {datetime.now()}
Target: {target}
========================================

EXECUTIVE SUMMARY
-----------------
{exploited_count} vulnerabilities discovered and exploited
{fixed_count} vulnerabilities successfully patched
Overall security rating: {rating_before} (before fixes)
Overall security rating: {rating_after} (after fixes)

========================================
VULNERABILITY 1: SQL INJECTION
========================================
Severity: Critical
Location: /login endpoint
Parameter: username field

Attack:
  Payload used: admin'--
  Result: {"Authentication bypassed" if results["sqli"]["exploited"] else "Attack blocked"}
  Impact: Full admin access without valid credentials

Root Cause:
  User input passed directly into SQL query without sanitization
  Vulnerable code: "SELECT * FROM users WHERE username='" + username + "'"

Fix Applied:
  Parameterized queries implemented
  Fixed code: "SELECT * FROM users WHERE username=?"
  Result after fix: {"Attack blocked — invalid credentials returned" if results["sqli"]["fixed"] else "Still vulnerable"}

========================================
VULNERABILITY 2: CROSS SITE SCRIPTING
========================================
Severity: High
Location: /search endpoint
Parameter: search query field

Attack:
  Payload used: <script>alert('XSS')</script>
  Result: {"Script executed in victim browser" if results["xss"]["exploited"] else "Attack blocked"}
  Impact: Session hijacking, credential theft possible

Root Cause:
  User input rendered directly in HTML without encoding
  Vulnerable code: return "<p>Results for: " + query + "</p>"

Fix Applied:
  Input sanitization and output encoding implemented
  Fixed code: return "<p>Results for: " + escape(query) + "</p>"
  Result after fix: {"Attack blocked — script rendered as plain text" if results["xss"]["fixed"] else "Still vulnerable"}

========================================
VULNERABILITY 3: INSECURE DIRECT OBJECT REFERENCE
========================================
Severity: High
Location: /user/<id>/profile endpoint
Parameter: user ID in URL

Attack:
  Result: {"Another user's private data accessed" if results["idor"]["exploited"] else "Attack blocked"}
  Impact: Full account data of any user accessible

Root Cause:
  No authorization check verifying requesting user owns resource
  Vulnerable code: return get_user_profile(user_id)

Fix Applied:
  Authorization check added before returning data
  Fixed code: if current_user.id != user_id: return "Access denied"
  Result after fix: {"Attack blocked — access denied returned" if results["idor"]["fixed"] else "Still vulnerable"}

========================================
VULNERABILITY 4: CROSS SITE REQUEST FORGERY
========================================
Severity: High
Location: /contact endpoint
Parameter: email change form

Attack:
  Result: {"Forged request executed" if results["csrf"]["exploited"] else "Attack blocked"}
  Impact: Account takeover through email reset

Root Cause:
  No CSRF token validation on sensitive forms
  Vulnerable code: Form accepts any POST request without verification

Fix Applied:
  CSRF token validation implemented
  Fixed code: Verify csrf_token matches session token before processing
  Result after fix: {"Attack blocked — invalid token rejected" if results["csrf"]["fixed"] else "Still vulnerable"}

========================================
SUMMARY TABLE
========================================
Vulnerability    Severity    Exploited    Fixed
SQLi             Critical    {"Yes" if results["sqli"]["exploited"] else "No"}          {"Yes" if results["sqli"]["fixed"] else "No"}
XSS              High        {"Yes" if results["xss"]["exploited"] else "No"}          {"Yes" if results["xss"]["fixed"] else "No"}
IDOR             High        {"Yes" if results["idor"]["exploited"] else "No"}          {"Yes" if results["idor"]["fixed"] else "No"}
CSRF             High        {"Yes" if results["csrf"]["exploited"] else "No"}          {"Yes" if results["csrf"]["fixed"] else "No"}

========================================
CONCLUSION
========================================
{conclusion}

Full source code available in:
  /vulnerable_app/app.py
  /hardened_app/app.py
========================================
"""

    # Print report in terminal
    print("\n========================================")
    print("SECURITY REPORT OUTPUT")
    print("========================================\n")
    print(report)

    # Save report
    base_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(base_dir, "security_report.txt")

    with open(report_path, "w") as f:
        f.write(report)

    print("\nReport saved to:", report_path)
