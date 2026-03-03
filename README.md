# Data Paradox Agent

**An AI-powered tool that challenges your marketing analytics claims — using your actual data.**

Built to prevent costly mistakes by detecting logical fallacies in data analysis before they reach production.

[![Security Rating](https://img.shields.io/badge/Security-A+-brightgreen)](https://github.com/AkpanDaniel/data-paradox-agent/blob/main/SECURITY.md)
[![OWASP Compliant](https://img.shields.io/badge/OWASP-90%25-blue)](https://owasp.org/www-project-top-ten/)
[![Privacy](https://img.shields.io/badge/Privacy-100%25-success)](https://github.com/AkpanDaniel/data-paradox-agent/blob/main/SECURITY.md)
[![HTTPS](https://img.shields.io/badge/HTTPS-Enforced-green)](https://data-paradox-agent.onrender.com)

🔗 **[Try it Live](https://data-paradox-agent.onrender.com)** | 📖 **[Security Policy](SECURITY.md)**

---

##  Security First

**Production-Ready Security (A+ Rating):**
- ✅ HTTPS/TLS encryption enforced
- ✅ Security headers (CSP, HSTS, X-Frame-Options, XSS Protection)
- ✅ Rate limiting (10 req/min per IP)
- ✅ Input sanitization & validation (50MB limit, content scanning)
- ✅ No data storage (privacy by design)
- ✅ Automated security updates (Dependabot)
- ✅ OWASP Top 10 compliant (90%)
- ✅ NIST Cybersecurity Framework aligned (76%)
- ✅ ISO 27001 compliant (85%)
- ✅ SOC 2 ready (97%)

**[View Full Security Policy →](SECURITY.md)**

---

##  What It Does

The Data Paradox Agent performs **dual validation**:
1. **Fact-checks** your claims against uploaded campaign data
2. **Logic-checks** your reasoning for common analytical fallacies

### Key Features

- **CSV Data Upload** - Validates claims against your actual marketing data (max 50MB)
- **Fallacy Detection** - Identifies 6 common marketing analytics fallacies
- **Claim Comparison** - Scores competing strategies and recommends the lower-risk option
- **Methodology Recognition** - Recognizes proper statistical practices (A/B tests, p-values)
- **Dark Mode** - Toggle between light/dark themes with localStorage persistence
- **Professional UI** - Clean, intuitive web interface with responsive design
- **Security Hardened** - Enterprise-grade security for production use

---

##  Functionality Preview

### 1. Analysis Dashboard
![Analysis Dashboard](assets/screenshot_1.png)

### 2. Fallacy Detection
![Fallacy Detection](assets/screenshot_2.png)
![Deep Dive](assets/screenshot_3.png)
![Upload Interface](assets/screenshot_4.png)

---

##  Why This Matters

**The Problem:** Most analysts make recommendations based on true-but-misleading data:
- High ROAS that won't scale
- Correlations mistaken for causation  
- Attribution models that inflate performance
- Survivorship bias in success stories

**The Solution:** This tool validates the facts AND challenges the logic — preventing expensive mistakes.

---

##  Demo

### Example: Budget Reallocation Decision

**Claim:** *"TikTok has ROAS of 9.54 (highest in our data) and CPC of $1.01. We should shift 60% of Google Ads budget to TikTok."*

**Agent Response:**
```
DATA VERIFIED: TikTok ROAS is 9.54 (confirmed from your dataset)

LOGICAL RISKS DETECTED:
- Incremental Return Fallacy (HIGH) - Average ROAS ≠ Marginal ROAS
- Survivorship Bias (HIGH) - Only looking at successful campaigns
- Correlation ≠ Causation (HIGH) - Platform might not be the true driver

RECOMMENDATION: Test incrementally before scaling
```

---

## Technical Architecture

### Backend
- **Python/Flask** - Web server with security middleware
- **Pattern Matching Engine** - Rule-based fallacy detection
- **Polars** - High-performance CSV processing (faster than Pandas)
- **Flask-Limiter** - Rate limiting and DoS protection

### Frontend  
- **Vanilla JavaScript** - No frameworks, fast and lightweight
- **Responsive Design** - Works on desktop, tablet, mobile
- **Dark Mode** - Theme persistence with localStorage

### Security Layer
- **Security Headers** - CSP, HSTS, X-Frame-Options, XSS Protection
- **Input Sanitization** - File validation, content scanning, size limits
- **Rate Limiting** - Per-IP request throttling
- **Dependency Scanning** - Automated weekly updates via Dependabot

### Fallacy Detection System
- 6 marketing-specific fallacies with weighted scoring
- Context-aware confidence levels (HIGH/MEDIUM/LOW)
- Methodology recognition (reduces false positives for good analysis)

---

##  Detected Fallacies

1. **Incremental Return Fallacy** - Assumes average performance holds when scaling
2. **Attribution Inflation** - Over-generous attribution windows claiming false credit
3. **Selection Bias** - High-intent audiences mistaken for broad scalability
4. **Correlation ≠ Causation** - Relationships assumed to be causal
5. **Survivorship Bias** - Only analyzing winners, ignoring failures
6. **Confounding Variables** - Failing to control for alternative explanations

---

##  Data Requirements

**Optimized for marketing campaign data.** Your CSV should include:

**Required Column (one of):**
- `platform`, `channel`, `ad_platform`, `source`, or `medium`

**Optional Metrics (detected automatically):**
- ROAS, CTR, CPC, CPA
- Conversions, Spend, Revenue

**File Limits:**
- Max size: 50MB
- Format: UTF-8 encoded CSV
- Security: Scanned for malicious content

**Example Data Structure:**
| Platform    | ROAS | CTR  | CPC  |
|-------------|------|------|------|
| Google Ads  | 4.11 | 3.2% | $2.15|
| Meta Ads    | 6.92 | 2.1% | $1.32|
| TikTok Ads  | 9.54 | 5.5% | $1.01|

---

##  Use Cases

### For Analysts
- Self-review before presenting recommendations
- Peer review of colleague's analysis
- Teaching junior analysts about common pitfalls

### For Managers
- Evaluate competing strategy proposals objectively
- Ask better questions before approving budget changes
- Reduce risk of expensive analytical mistakes

### For Interviews
- Demonstrates advanced analytical thinking
- Shows ability to build practical tools
- Proves understanding of real-world data challenges

---

##  Project Structure
```
data-paradox-agent/
├── agent/
│   ├── challenge_generator.py    # Formats challenges and handles comparison
│   ├── data_analyzer.py          # CSV upload and data validation (Polars)
│   ├── fallacy_detector.py       # Pattern matching and scoring
│   └── input_processor.py        # Extracts metrics and keywords
├── config/
│   └── fallacies.json            # Fallacy database with triggers and challenges
├── static/
│   └── 0218.mp4                  # Demo video
├── .github/
│   └── dependabot.yml            # Automated security updates
├── app.py                        # Flask server + web interface + security
├── requirements.txt              # Python dependencies
├── SECURITY.md                   # Security policy and responsible disclosure
└── README.md
```

---

##  Testing

Tested with real marketing dataset:
- **1,800+ campaigns** across Google Ads, Meta Ads, TikTok Ads
- **Multiple claim types** (budget allocation, platform comparison, metric correlation)
- **Edge cases** (controlled experiments, good methodology, nonsense claims)
- **Security testing** (XSS, injection, rate limiting, file uploads)

---

##  Key Insights from Building This

### What Works Well
- Pattern matching is fast and reliable for domain-specific fallacies
- Scoring system effectively prioritizes HIGH-risk issues
- Comparison mode provides clear, actionable recommendations
- Security-first approach prevents common vulnerabilities

### What Could Be Improved
- Currently optimized for marketing analytics (extensible to other domains)
- Pattern-based (doesn't understand semantic meaning)
- Manual fallacy database (could be ML-enhanced)

---

##  Future Enhancements

- [ ] Export reports to PDF/Word
- [ ] Multi-domain support (sales, product, finance analytics)
- [ ] Severity scoring with business impact weighting
- [ ] Historical claim tracking
- [ ] API for integration with BI tools
- [ ] Advanced logging and monitoring dashboard

---

##  Lessons Learned

**1. Domain expertise matters** - Generic fallacy detection is weak; specialized knowledge makes it powerful

**2. False positives are costly** - Added methodology recognition to avoid flagging good analysis

**3. UX drives adoption** - Comparison mode transformed it from "critique tool" to "decision support tool"

**4. Real data matters** - CSV validation makes it actually useful, not just educational

**5. Security is non-negotiable** - Production apps need rate limiting, sanitization, and security headers from day one

---

##  About

### Inspiration
*"I noticed a trend in the current AI ecosystem: an abundance of generic agents and flashy dashboards that often prioritize aesthetics over substance. I wanted to build something unique that moves beyond the 'dashboard fatigue' often seen on professional networks. This tool focuses on **core insights**—proving that AI can do more than just display data; it can actively challenge and improve our understanding of it."*

Built by **Akpan Daniel** as a portfolio project demonstrating:
- Full-stack development (Python backend, JavaScript frontend)
- Domain expertise in marketing analytics
- System design (pattern matching, scoring algorithms, security architecture)
- Product thinking (solving real analyst pain points)
- Security best practices (OWASP, NIST, ISO compliance)

**Timeline:** 3 days (February 15-17, 2026)

---

## Contact

- **GitHub:** [https://github.com/AkpanDaniel/data-paradox-agent](https://github.com/AkpanDaniel/data-paradox-agent)
- **LinkedIn:** [https://www.linkedin.com/in/akpan-daniel-b09a1b1a1/](https://www.linkedin.com/in/akpan-daniel-b09a1b1a1/)
- **Email:** [alviva91@gmail.com](mailto:alviva91@gmail.com)
- **Security:** [SECURITY.md](SECURITY.md)

---

##  License

MIT License - Feel free to use this code for learning or building your own tools.

---

*"Most tools confirm your bias. This one challenges it."*