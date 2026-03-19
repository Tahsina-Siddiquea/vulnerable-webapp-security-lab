# Wulnerable Web App Security Lab

A hands-on cybersecurity lab that demonstrates common web application vulnerabilities and their secure mitigations.

This project contains two versions of the same web application:

* Vulnerable application (for learning attacks)
* Hardened application (for learning defenses)

It also includes an automated scanner and dynamic security report generator.

## Project Purpose

The goal of this lab is to understand:

* How real web attacks work
* How insecure coding leads to exploitation
* How proper security controls prevent attacks
* How automated security testing can be implemented

This project is designed for cybersecurity students, penetration testing beginners, and secure coding practice.


## Features

### Vulnerability Demonstrations

The vulnerable app intentionally contains:

* SQL Injection authentication bypass
* Cross-Site Scripting (XSS) in search functionality
* Insecure Direct Object Reference (IDOR) in profile access
* Cross-Site Request Forgery (CSRF) in email update

### Security Fixes in Hardened Version

The hardened app implements:

* Parameterized SQL queries
* Input sanitization / HTML escaping
* Session-based authorization checks
* CSRF token validation
* Secure authentication flow


## Automated Vulnerability Scanner

The scanner performs:

* SQL injection test
* XSS payload test
* IDOR access test
* CSRF forged request simulation

The scanner produces a dynamic security assessment.


## Dynamic Security Report

The report generator provides:

* Executive security summary
* Exploited vulnerabilities count
* Fixed vulnerabilities count
* Security rating before mitigation
* Security rating after mitigation
* Detailed vulnerability explanations
* Recommended fixes


## Project Structure
```
web-security-lab/
│
├── vulnerable_app/
│   ├── app.py
│   ├── init_db.py
│   ├── templates/
│   └── static/
│
├── hardened_app/
│   ├── app.py
│   ├── init_db.py
│   ├── templates/
│   └── static/
│
├── scanner.py
├── demo_test.py
├── report_generator.py
└── security_report.txt
```


## Installation

Clone repository
```
git clone https://github.com/Tahsina-Siddiquea/web-security-lab.git
cd web-security-lab
```

Install dependencies
```
pip install flask requests
```


## Running the Vulnerable App
```
cd vulnerable_app
python init_db.py
python app.py
```

Open in browser:
```
http://localhost:5000
```

## Running the Hardened App
```
cd hardened_app
python init_db.py
python app.py
```

## Running Automated Scanner

Make sure application is running.

Then execute:
```
python scanner.py
```


## Running Full Dynamic Test Suite
```
python demo_test.py
```
This will:

* Launch all attack simulations
* Generate a complete security report

## Example Output

After running the automated scanner and report generator:
```
===== Vulnerability Scanner =====

Testing SQL Injection
Result: Authentication bypass successful

Testing XSS
Result: Script executed in browser

Testing IDOR
Result: Private profile accessed

Testing CSRF
Result: Email changed via forged request

===== Generating Dynamic Security Report =====

Vulnerable Web App Security Report
Target: http://localhost:5000

Executive Summary
4 vulnerabilities discovered and exploited
4 vulnerabilities successfully mitigated

Overall security rating (before fixes): Critical
Overall security rating (after fixes): Secure

Detailed Findings
• SQL Injection – login endpoint vulnerable to authentication bypass
• XSS – search page reflects unsanitized user input
• IDOR – unauthorized access to user profile data
• CSRF – sensitive action allowed without verification

Conclusion
Hardened version mitigates all identified vulnerabilities.
```

## Educational Use Only

This project is created strictly for:

* Cybersecurity learning
* Secure coding practice
* Penetration testing lab simulation

## Performance Characteristics

* Lightweight Flask-based application
* Fast vulnerability scanning (typically < 3 seconds on localhost)
* Minimal memory usage (< 50 MB during execution)
* Multi-request testing using Python requests library
* Suitable for lab environments, virtual machines, and low-spec systems

Scanner complexity:

* SQLi test → O(1) request
* XSS test → O(1) request
* IDOR test → O(1) request
* CSRF test → O(1) request

Overall scan complexity: constant time for single target


## Security and Ethical Use

This project is developed strictly for:

* Cybersecurity education
* Ethical hacking practice
* Secure coding demonstration
* Penetration testing training labs

Important guidelines:

* Only test systems you own or have explicit permission to test
* Do not deploy vulnerable applications on public networks
* Do not use attack techniques for illegal activities
* Follow responsible disclosure practices

Misuse of this tool may violate laws and ethical standards.

## Author

Developed as part of an independent cybersecurity learning initiative focused on practical secure coding, vulnerability analysis, and defensive system design.
This project reflects hands-on exploration of real-world web security risks and mitigation techniques.

## License

This project is intended for educational and research purposes only.
Use responsibly and perform testing only on systems where you have proper authorization.
