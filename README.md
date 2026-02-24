# Betterinfo 🔍 

v0.0.1

**Betterinfo** is an open-source reconnaissance tool for performing passive and active information gathering on domains you are authorized to audit. It produces a structured, color-coded terminal report covering a target's infrastructure, technology stack, and security posture.

> ⚠️ **Read the [Legal & Ethical Use](#️-legal--ethical-use) section before use.**

---

## 🚀 Features

### 📡 Passive Mode (Default)
No direct contact with the target server. All data is gathered from public records and third-party APIs, making it safe and non-intrusive.

- **Whois & Registry Data** — Domain registration details, expiration dates, and registrar information.
- **Subdomain Discovery** — Finds associated subdomains via passive scraping techniques.
- **Mail Infrastructure** — Extracts MX records (mail servers) and TXT records (SPF, DKIM, verification strings).
- **Security Flags** — Automatically warns about weak SPF policies (e.g., SoftFail `~all`).

### ⚡ Active Mode (`--active` / `-a`)
Makes direct HTTP requests to the target to gather live technical data. **Only use this on domains you own or have explicit written authorization to test.**

- **Technology Fingerprinting** — Detects the underlying tech stack (e.g., Astro, Tailwind CSS, Google Analytics).
- **Edge IP & Geolocation** — Resolves the server's live IP address with Country, City, and ISP details.
- **HTTP Security Header Audit** — Checks for the presence of critical security headers. Missing headers like `HSTS` or `X-Frame-Options` are flagged in red for fast identification.

---

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/JorgeRosbel/betterinfo
cd betterinfo
```

### 2. Set up the Virtual Environment
```bash
# Create the environment
python3 -m venv venv

# Activate it
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Create a System-wide Alias (Optional)
Run Betterinfo from any directory without manually activating the virtual environment:
```bash
# Add to ~/.bashrc or ~/.zshrc
# Replace the path with your actual clone location
alias betterinfo='/absolute/path/to/betterinfo/venv/bin/python3 /absolute/path/to/betterinfo/main.py'
```
Then reload your shell:
```bash
source ~/.bashrc
```

---

## 📖 Usage

| Goal | Command |
|---|---|
| Passive recon (safe, no direct contact) | `betterinfo domain.com` |
| Full active audit | `betterinfo domain.com -a` |
| Active audit with request delay | `betterinfo domain.com -a -r 3` |

### `-r` Flag — Rate Limiting
The `-r <seconds>` flag adds a delay between requests. This is strongly recommended during active scans to avoid triggering WAF (Web Application Firewall) rate limits and to reduce your footprint on the target server.

---

## 📋 Terminal Output Color Guide

| Color | Meaning |
|---|---|
| 🔵 Cyan | Field names and section labels |
| 🟡 Yellow | Detected values and active data |
| 🔴 Red | Missing security headers or errors |
| 🟣 Magenta | DNS and TXT record sections |

---

## ⚖️ Legal & Ethical Use

**Betterinfo is a dual-use tool.** Like any security tool (Nmap, Nikto, Burp Suite), its legality depends entirely on how and where it is used.

### ✅ Legal uses
- Auditing domains and infrastructure **you own**.
- Security testing with **explicit written authorization** from the domain owner (e.g., a signed scope-of-work agreement or bug bounty program rules).
- Educational use in **controlled lab environments** (local VMs, intentionally vulnerable apps like DVWA, HackTheBox, TryHackMe).
- Passive recon using **only public data** (Whois, DNS records) — this is universally legal.


### 📄 Disclaimer
The author provides this tool for **legitimate security research and education only**. By using Betterinfo, you agree that:

1. You take full legal responsibility for how you use this tool.
2. You will only perform active scans on systems you own or are explicitly authorized to test.
3. The author bears no liability for any damages, legal consequences, or misuse arising from use of this software.

**When in doubt: use passive mode, or don't run it at all.**e.