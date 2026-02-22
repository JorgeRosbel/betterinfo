# Betterinfo 🔍 v0.0.1

**Betterinfo** is a specialized reconnaissance tool designed to perform both passive and active information gathering on any given domain. It provides a structured, color-coded report of a target's infrastructure, technology stack, and security posture.

## 🚀 Features

The tool operates in two distinct modes based on your needs:

### 📡 Passive Mode (Default)
Safe and stealthy. It gathers data from public records and third-party APIs without interacting directly with the target server.
* **Whois & Registry Data:** Full domain registration details, expiration dates, and registrar info.
* **Subdomain Discovery:** Finds associated subdomains using passive scraping techniques.
* **Mail Infrastructure:** Extracts **MX Records** (Mail Servers) and **TXT Records** (SPF, verification strings).
* **Security Flags:** Automatically detects and warns about weak SPF policies (e.g., SoftFail `~all`).

### ⚡ Active Mode (using `--active` or `-a`)
Performs direct interaction with the target to extract "live" technical data.
* **Technology Analysis:** Detects the underlying tech stack (e.g., **Astro**, Tailwind CSS, Google Analytics).
* **Edge IP & Geolocation:** Resolves the server's IP and identifies the Country, City, and ISP.
* **HTTP Header Audit:** Checks for the presence of security headers. Missing headers like `HSTS` or `X-Frame-Options` are flagged in **red** for quick auditing.

---

## 🛠️ Installation & Setup

Follow these steps to get your environment ready:

### 1. Clone the repository
```bash
git clone https://github.com/JorgeRosbel/betterinfo
cd betterinfo

```

### 2. Prepare the Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies safely:

```bash
# Create the environment
python3 -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

### 3. Create a System Alias

To run **Betterinfo** from anywhere in your system without manually activating the environment, add this alias to your configuration file (e.g., `~/.bashrc` or `~/.zshrc`):

```bash
# Replace /absolute/path/to/betterinfo with the actual path where you cloned the repo
alias betterinfo='/absolute/path/to/betterinfo/venv/bin/python3 /absolute/path/to/betterinfo/main.py'

```

*After adding the line, restart your terminal or run `source ~/.bashrc`.*

---

## 📖 Usage Examples

### Stealth Reconnaissance (Passive)

```bash
betterinfo domain.com

```

### Full Infrastructure Audit (Active)

```bash
betterinfo domain.com -a

```

---

## 📋 Sample Output

The tool uses a clean terminal interface with progress bars and color coding:

* **Cyan:** Field names and categories.
* **Yellow:** Detected data and active values.
* **Red:** Critical missing security headers or "Not Found" errors.
* **Magenta:** DNS and TXT record sections.

## ⚖️ Legal Disclaimer

This tool is intended for educational purposes and authorized security auditing only. The author is not responsible for any misuse. Always obtain permission before performing **active** scans on third-party infrastructure.
