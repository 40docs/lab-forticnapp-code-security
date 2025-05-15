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

## 🧑‍💻 1. Local Scanning via VSCode: *Lacework Security Extension*

### 🛠️ Setup

```bash
git clone https://github.com/40docs/lab_forticnapp_code_security.git
cd lab_forticnapp_code_security
```

!!! info "Install the VSCode Extension"
\- Open the folder in **Visual Studio Code**
\- Install the **Lacework Security** extension from the VSCode Marketplace
\- Click the **shield icon** in the sidebar
\- Click **“Sign in with Lacework”** to authenticate using OAuth

---

### 🧪 Running Scans

From the Lacework panel in VSCode, you can choose:

* ✅ **Start all scans**
* 🛠️ **Start IaC Scan**
* 🔍 **Start SAST Scan**
* 📦 **Start SCA Scan**

!!! note
All scans run from the **root of the open workspace folder**.

---

### 📌 Viewing Results

* Files with violations appear in the Lacework panel
* Click a file to view its issues
* Red-highlighted code indicates exact problem lines

!!! tip "SmartFix Support"
Hover over red-highlighted code to view issue details and apply available **SmartFix** suggestions.

---

## 🔗 2. GitHub Integration: *Lacework FortiCNAPP*

### 🔧 Steps to Integrate with GitHub

1. Log in to the **Lacework Console**
2. Navigate to:
   `Settings → Integrations → Code Security`
3. Click **Add Integration**
4. Select:

   * Git provider: **GitHub**
5. Click **Go to GitHub** and log in

!!! warning "GitHub Permissions Required"
You must have **Owner** permissions in the GitHub organization to complete the integration.

6. Choose:

   * **All repositories**
     — or —
   * **Only select repositories** via dropdown
7. Click **Install & Authorize**

GitHub will redirect you back to the Lacework console to confirm the integration.

---

### 📊 Post-Integration Behavior

!!! info
Once integration is complete:
\- Lacework will automatically scan the **default branch** of connected repositories.
\- You can view scan results in the Lacework UI.

---

### 🔍 Available Tools After Integration

* **Infrastructure-as-Code Security**
* **SCA and SAST** vulnerability detection
* **Secrets detection** for exposed credentials or tokens

!!! tip
After integration, you can **enable/disable** specific tools per repository via the Lacework Console.
