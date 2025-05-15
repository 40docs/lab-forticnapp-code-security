# 🔐 Code Security Demo: FortiCNAPP

In this lab, you'll explore a deliberately vulnerable codebase containing hardcoded secrets, outdated dependencies, insecure Docker configs, and misconfigured infrastructure-as-code. These represent common real-world mistakes.

You'll see how **Lacework FortiCNAPP** provides deep visibility into these risks through:

- Automated code scanning
- Detailed vulnerability findings
- Secrets detection
- SmartFix & AutoFix suggestions
- CI/CD policy enforcement (e.g., blocking PRs)

By the end, you’ll learn how to detect, remediate, and prevent security issues before they reach runtime.

---

## ✅ Repo Structure

```txt
forticnapp-demo/
├── app/
│   ├── app.py             # Flask app using secret from config
│   ├── config.py          # ❌ Hardcoded AWS secret
│   └── requirements.txt   # ❌ Known vulnerable package versions
├── Dockerfile             # ❌ Insecure container config
├── terraform/
│   └── s3-public.tf       # ❌ Public S3 bucket via IaC
├── README.md              # This file
```

---

### 📄 `app/app.py`

```python
from flask import Flask
from config import AWS_SECRET_KEY

app = Flask(__name__)

@app.route('/')
def home():
    return f"Secret: {AWS_SECRET_KEY}"  # ❌ Secret exposed in HTTP response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # ❌ No TLS, runs in dev mode
```

> **What FortiCNAPP detects**: Secret usage in code flow, use of insecure default server, lack of environment-based config.

---

### 📄 `app/config.py`

```python
AWS_SECRET_KEY = 'AKIAFAKEKEYEXAMPLE123456'  # ❌ Hardcoded AWS secret key
```

> **What FortiCNAPP detects**: Credential pattern match (high confidence), flagged as exposed secret.

---

### 📄 `app/requirements.txt`

```txt
flask==1.0            # ❌ CVE-2018-1000656
requests==2.19.1      # ❌ CVE-2018-18074
pyyaml==4.2b1         # ❌ CVE-2017-18342
django==1.11.27       # ❌ Multiple CVEs incl. RCE
urllib3==1.24.1       # ❌ CVE-2019-11324
jinja2==2.10          # ❌ CVE-2019-10906
pillow==6.2.1         # ❌ CVE-2020-10177
```

> **What FortiCNAPP detects**: Software Composition Analysis (SCA) matches against known CVEs. Provides CVSS scores, remediation paths (SmartFix), and upgrade suggestions.

---

### 📄 `Dockerfile`

```Dockerfile
FROM python:3.8

WORKDIR /app

COPY app/ .

RUN pip install -r requirements.txt  # ❌ Installs known-vulnerable packages

EXPOSE 5000

CMD ["python", "app.py"]
```

> ❌ No non-root user  
> ❌ No runtime user constraints  
> ❌ No multi-stage build or scan layers  
> ❌ No healthcheck  

> **What FortiCNAPP detects**: Insecure container build practices, base image risk (if known CVEs exist in `python:3.8`), missing best practices.

---

### 📄 `terraform/s3-public.tf`

```hcl
resource "aws_s3_bucket" "public_bucket" {
  bucket = "forticnapp-demo-bucket"
  acl    = "public-read"  # ❌ Publicly readable bucket
}
```

## 🧑‍💻 1. Local Scanning via VSCode: Lacework Security Extension

### ✅ Setup

Clone the lab repo `git clone https://github.com/40docs/lab_forticnapp_code_security.git`

Install the Lacework Security extension from the VSCode Marketplace.

Open the lab_forticnapp_code_security/ folder in VSCode.

Click the Lacework Shield icon in the sidebar.

Sign in using “Sign in with Lacework” (OAuth).

### 🧪 Running Scans

From the sidebar panel, choose one of:

Start all scans

Start IaC Scan

Start SAST Scan

Start SCA Scan

Scans run from the root of the open folder.

### 📌 Viewing Results

Violating files appear in the Lacework panel.

Click a file to view issues.

Red-highlighted code shows exact problem lines.

## 🧑‍💻 2. Lacework Github Integration:
