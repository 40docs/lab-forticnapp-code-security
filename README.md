# 🔐 Code Security Demo: FortiCNAPP

In this lab, you'll explore a deliberately vulnerable codebase containing hardcoded secrets, outdated dependencies, insecure Docker configs, and misconfigured infrastructure-as-code. These represent common real-world mistakes.

You'll see how **Lacework FortiCNAPP** provides deep visibility into these risks through:

* Automated code scanning
* Detailed vulnerability findings
* Secrets detection
* SmartFix & AutoFix suggestions
* CI/CD policy enforcement (e.g., blocking PRs)

By the end, you’ll learn how to detect, remediate, and prevent security issues before they reach runtime.

---

## ✅ Repo Structure

```txt
lab_forticnapp_code_security/
├── app/
│   ├── app.py              # Flask app with all insecure routes
│   ├── config.py           # ❌ Hardcoded AWS secret
│   ├── Dockerfile          # ❌ Insecure container config
│   ├── requirements.txt    # ❌ Known vulnerable packages
│   └── vuln_app.py         # ❌ Insecure helper functions (SAST triggers)
├── terraform/
│   ├── resource_aws_s3_bucket.tf   # ❌ Public S3 bucket
│   └── resource_aws_subnet.tf      # ❌ Public subnet
├── README.md

```

## 🧑‍💻 1. Local Scanning with Lacework Security (VSCode Extension)

### Setup

```bash
git clone https://github.com/40docs/lab_forticnapp_code_security.git
cd lab_forticnapp_code_security
```

1. Open the folder in **Visual Studio Code**
2. Install the **Lacework Security** extension
3. Click the **shield icon** in the sidebar
4. Sign in using **“Sign in with Lacework”** (OAuth)

---

### Running Scans

From the Lacework panel:

* **Start all scans**
* **Start IaC Scan**
* **Start SAST Scan**
* **Start SCA Scan**

Scans run from the root of the open workspace folder.

---

### Viewing Results

* Files with violations appear in the panel
* Click to jump to flagged code
* Hover red-highlighted lines for issue details

---

## 🔗 2. GitHub Integration with Lacework FortiCNAPP

### How to Integrate

1. Log in to the **Lacework Console**
2. Go to **Settings → Integrations → Code Security**
3. Click **Add Integration**
4. Choose Git provider: **GitHub**
5. Click **Go to GitHub** and log in

> ⚠️ You must have **Owner** permissions in your GitHub org

6. Select:

   * **All repositories**, or
   * **Only select repositories** via dropdown
7. Click **Install & Authorize**

---

### After Integration

* FortiCNAPP automatically scans the **default branch**
* Results appear in the **Lacework UI** and optionally as **GitHub PR comments**
* You can enable or disable **IaC**, **SAST**, **SCA**, and **Secrets** scanning per repo

#### 💡 Trigger a SmartFix via PR

To see SmartFix in action:

```bash
echo "# trigger" >> app/requirements.txt && git checkout -b trigger-smartfix && git add app/requirements.txt && git commit -m "Trigger SmartFix" && git push -u origin trigger-smartfix && gh pr create --fill
```

Navigate to your Pull Request, after a few minutes a SmartFix comment will be left by the Lacework FortiCNAPP SmartFix Bot.