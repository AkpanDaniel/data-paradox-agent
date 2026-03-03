# Security Policy

## 🔒 Our Security Commitment

Data Paradox Agent is committed to ensuring the security and privacy of our users. We implement industry-standard security practices and welcome responsible disclosure of any security vulnerabilities.

## 📋 Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅ Yes            |
| < 1.0   | ❌ No             |

## 🛡️ Security Measures Implemented

### Infrastructure Security
- ✅ **HTTPS/SSL/TLS Encryption** - All traffic encrypted in transit
- ✅ **Secure Headers** - CSP, HSTS, X-Frame-Options, X-Content-Type-Options
- ✅ **Rate Limiting** - Protection against abuse and DoS attacks
  - Analysis: 10 requests/minute per IP
  - Upload: 20 requests/hour per IP
  - Overall: 50 requests/hour, 200/day per IP

### Application Security
- ✅ **Input Validation** - All user inputs sanitized and validated
- ✅ **File Upload Security** - Size limits (50MB), type checking, content scanning
- ✅ **XSS Protection** - Content Security Policy blocks malicious scripts
- ✅ **No Data Storage** - Privacy by design, no user data retention
- ✅ **Dependency Scanning** - Automated weekly security updates via Dependabot

### Code Security
- ✅ **Open Source** - Fully auditable codebase on GitHub
- ✅ **No Authentication Required** - No passwords to compromise
- ✅ **Minimal Dependencies** - Reduced attack surface
- ✅ **Error Handling** - No sensitive information in error messages

## 🐛 Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please follow responsible disclosure:

### How to Report

**Email:** alviva91@gmail.com

**Subject Line:** [SECURITY] Data Paradox Agent Vulnerability

**Please Include:**
1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)
5. Your contact information (optional)

### What to Expect

- **Acknowledgment:** Within 48 hours
- **Initial Assessment:** Within 5 business days
- **Updates:** Regular communication throughout investigation
- **Resolution:** Coordinated disclosure after fix is deployed

### Please DO NOT:
- ❌ Open a public GitHub issue for security vulnerabilities
- ❌ Exploit the vulnerability beyond proof-of-concept
- ❌ Share vulnerability details publicly before we've issued a fix

## 🏆 Recognition

We appreciate security researchers who help keep our users safe. With your permission, we will:
- Credit you in our security acknowledgments
- Publicly thank you after the fix is deployed (if you wish)

## 📊 Out of Scope

The following are **not** considered security vulnerabilities:
- Rate limiting triggering for legitimate heavy use
- CSV parsing errors for malformed files
- Fallacy detection false positives/negatives
- UI/UX issues without security impact
- Third-party dependencies (report directly to them)

## 🔐 Data Privacy

**What we DON'T collect:**
- ❌ No user accounts or authentication
- ❌ No personal information
- ❌ No tracking or analytics
- ❌ No cookies (except theme preference in localStorage)
- ❌ No uploaded CSV data retention

**What happens to your data:**
- CSV files are processed in memory only
- No data is written to disk
- All data is discarded after analysis
- No logs contain user data

## 📞 Security Contact

**Primary:** alviva91@gmail.com  
**GitHub:** https://github.com/AkpanDaniel/data-paradox-agent/security  

## 📅 Security Updates

Last Updated: March 2026  
Next Review: June 2026  

---

*This security policy is subject to change. Check back regularly for updates.*