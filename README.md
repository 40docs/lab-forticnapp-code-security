# 🔐 Code Security Demo: FortiCNAPP

This is an **educational security lab** designed to demonstrate common code vulnerabilities and how **Lacework FortiCNAPP** detects and helps remediate them. The repository contains intentionally vulnerable code that represents real-world security mistakes.

**⚠️ IMPORTANT**: This code contains deliberate security vulnerabilities for educational purposes only. **Never deploy this code to production environments.**

## What You'll Learn

Through hands-on experience with **Lacework FortiCNAPP**, you'll discover how to:

* **Detect vulnerabilities** across multiple security domains
* **Understand scan types**: IaC, SAST, SCA, and Secrets scanning
* **Remediate issues** using SmartFix automated suggestions
* **Integrate security** into CI/CD workflows and PR reviews
* **Prevent security debt** before code reaches production

## Vulnerability Categories

This lab demonstrates **4 key security domains** that FortiCNAPP addresses:

| Domain | Description | Examples in This Lab |
|--------|-------------|---------------------|
| **Secrets** | Hardcoded credentials and API keys | AWS credentials in config files |
| **SAST** | Application security flaws | SQL injection, command injection, weak crypto |
| **SCA** | Vulnerable dependencies | Outdated packages with known CVEs |
| **IaC** | Infrastructure misconfigurations | Public S3 buckets, insecure networking |

---

## 📁 Repository Structure

```txt
lab-forticnapp-code-security/
├── app/
│   ├── app.py              # Flask web application with vulnerable endpoints
│   ├── config.py           # ❌ Hardcoded AWS credentials (Secrets)
│   ├── vuln_app.py         # ❌ SQL injection, command injection (SAST)
│   ├── requirements.txt    # ❌ Vulnerable dependencies (SCA) 
│   └── Dockerfile          # ❌ Insecure container configuration
├── terraform/
│   ├── resource_aws_s3_bucket.tf    # ❌ Public S3 bucket (IaC)
│   └── resource_aws_subnet.tf       # ❌ Public subnet with auto-assign IPs (IaC)
├── CLAUDE.md              # Development guidance for Claude Code
└── README.md              # This file
```

## 🎯 Expected Scan Results

When you run FortiCNAPP scans, you should discover:

### Secrets Detection
- ✅ Hardcoded AWS access key in `app/config.py`
- ✅ Exposed credentials via Flask route responses

### SAST (Static Application Security Testing)
- ✅ **SQL Injection**: Direct string concatenation in database queries
- ✅ **Command Injection**: Unsanitized user input to `os.system()`
- ✅ **Weak Cryptography**: MD5 hashing for password storage
- ✅ **Missing Error Handling**: Potential information disclosure

### SCA (Software Composition Analysis)
- ✅ **8 vulnerable packages** with known CVEs:
  - Flask 1.0 (CVE-2018-1000656)
  - Django 1.11.27 (Multiple CVEs)
  - Requests 2.19.1 (CVE-2018-18074)
  - And 5 additional vulnerable dependencies

### IaC (Infrastructure as Code)
- ✅ **Public S3 Bucket**: Configured with public-read ACL
- ✅ **Public Subnet**: Auto-assigns public IPs to instances
- ✅ **Missing Encryption**: No server-side encryption configured

---

## 🚀 Getting Started

### Prerequisites
- **Visual Studio Code** with Lacework Security extension
- **GitHub account** with owner permissions (for GitHub integration)
- **Lacework FortiCNAPP account** (free trial available)

### Lab Setup

```bash
# Clone the vulnerable repository
git clone https://github.com/40docs/lab-forticnapp-code-security.git
cd lab-forticnapp-code-security

# Optional: Set up local Flask environment to see vulnerabilities in action
cd app/
pip install -r requirements.txt  # Installs vulnerable packages
python app.py                    # Runs insecure web application on port 5000
```

---

## 🔍 Scanning Methods

### Method 1: Local Scanning with VSCode Extension

**Setup Process**:
1. Open repository folder in **Visual Studio Code**
2. Install the **Lacework Security** extension from the marketplace
3. Click the **shield icon** in the VS Code sidebar
4. Sign in using **"Sign in with Lacework"** (OAuth authentication)

**Running Scans**:
- **Start all scans** - Comprehensive security analysis
- **Start IaC Scan** - Infrastructure misconfigurations only
- **Start SAST Scan** - Application security flaws only  
- **Start SCA Scan** - Vulnerable dependencies only

**Viewing Results**:
- Files with violations appear in the Lacework panel
- Click any finding to jump directly to the problematic code
- Hover over red-highlighted lines for detailed issue descriptions
- Review suggested fixes and remediation guidance

### Method 2: GitHub Integration (CI/CD Pipeline)

**Integration Setup**:
1. Access the **Lacework Console** (https://your-account.lacework.net)
2. Navigate to **Settings → Integrations → Code Security** 
3. Click **Add Integration** → **GitHub**
4. Authorize Lacework to access your GitHub organization
   > ⚠️ **Required**: Owner permissions in your GitHub organization

**Repository Configuration**:
- Choose **All repositories** or **Select specific repositories**
- Enable/disable scan types per repository: **IaC**, **SAST**, **SCA**, **Secrets**
- Configure PR commenting and blocking policies

**Automated Workflow**:
- FortiCNAPP automatically scans on every push to default branch
- Scan results appear in Lacework Console and GitHub PR comments
- SmartFix provides automated remediation suggestions
- Policy enforcement can block PRs with critical vulnerabilities

---

## 🔧 Testing SmartFix Automation

Experience automated vulnerability remediation by triggering a SmartFix suggestion:

```bash
# Add a new vulnerable dependency to trigger SmartFix
echo "paramiko==2.4.1" >> app/requirements.txt

# Create and push a pull request
git checkout -b trigger-smartfix
git add app/requirements.txt  
git commit -m "Add vulnerable paramiko dependency"
git push -u origin trigger-smartfix
gh pr create --title "Test SmartFix" --body "Adding vulnerable dependency to test SmartFix functionality"
```

**Expected Results**:
- Within 5-10 minutes, FortiCNAPP will scan your PR
- SmartFix Bot will comment with automated remediation suggestions
- Suggestions include specific version updates and security explanations
- You can apply suggestions directly from the GitHub interface

---

## 📊 Understanding Your Results

### Interpreting Scan Output

Each vulnerability finding includes:

**Severity Levels**:
- 🔴 **Critical** - Immediate remediation required
- 🟠 **High** - Fix within days  
- 🟡 **Medium** - Address in next sprint
- 🔵 **Low** - Fix when convenient
- ℹ️ **Info** - Best practice suggestions

**Finding Details**:
- **File location** and **line numbers** with vulnerable code
- **Vulnerability explanation** and **potential impact**
- **Remediation guidance** with specific fix recommendations
- **External references** to CVE databases and security documentation

### Sample Findings You'll See

| File | Vulnerability Type | Description | Fix |
|------|-------------------|-------------|-----|
| `config.py:1` | **Secrets** | Hardcoded AWS credentials | Use environment variables or secret management |
| `vuln_app.py:15` | **SAST - SQL Injection** | Direct string concatenation in query | Use parameterized queries |
| `vuln_app.py:9` | **SAST - Command Injection** | Unsanitized input to `os.system()` | Use subprocess with argument validation |
| `requirements.txt:1` | **SCA** | Flask 1.0 has CVE-2018-1000656 | Upgrade to Flask 2.3.3+ |
| `resource_aws_s3_bucket.tf:3` | **IaC** | S3 bucket is publicly readable | Remove public ACL, add bucket policies |

---

## 🎓 Learning Outcomes

By completing this lab, you will:

### Technical Skills
- **Master scan types** - Understand when to use IaC, SAST, SCA, and Secrets scanning
- **Read vulnerability reports** - Interpret findings, severity levels, and remediation guidance  
- **Apply security fixes** - Use SmartFix suggestions to remediate real vulnerabilities
- **Configure CI/CD security** - Integrate automated scanning into development workflows

### Security Knowledge  
- **Recognize common patterns** - Identify hardcoded secrets, injection flaws, and misconfigurations
- **Understand impact** - Learn how vulnerabilities can be exploited in production environments
- **Prevention strategies** - Implement secure coding practices and dependency management
- **DevSecOps integration** - Build security into every stage of development

### Best Practices
- **Shift-left security** - Catch vulnerabilities early in the development lifecycle
- **Automated remediation** - Leverage AI-powered fix suggestions for faster resolution
- **Risk-based prioritization** - Focus on critical and high-severity findings first
- **Continuous monitoring** - Establish ongoing security posture management

---

## 🔗 Additional Resources

### FortiCNAPP Documentation
- [Getting Started Guide](https://docs.lacework.net/onboarding/code-security)
- [VSCode Extension](https://marketplace.visualstudio.com/items?itemName=lacework.lacework-security)
- [GitHub Integration](https://docs.lacework.net/code-security/github-integration)
- [SmartFix Overview](https://docs.lacework.net/code-security/smart-fix)

### Security Learning Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Most critical web application security risks
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) - Industry security standards
- [CVE Database](https://cve.mitre.org/) - Common Vulnerabilities and Exposures
- [Secure Code Review](https://owasp.org/www-pdf-archive/OWASP_Code_Review_Guide_v2.pdf) - Manual security analysis techniques

---

## 🆘 Troubleshooting

### Common Issues

**VSCode Extension Not Working**
```bash
# Ensure you're signed into Lacework
# Check extension is enabled in VS Code
# Verify workspace folder contains vulnerable code files
```

**No Scan Results Appearing**  
- Confirm you have proper repository permissions
- Check that files contain the expected vulnerabilities
- Verify your Lacework account has active scanning credits

**SmartFix Not Triggering**
- Ensure GitHub integration is properly configured
- Confirm repository has FortiCNAPP scanning enabled
- Wait 5-10 minutes for scan completion after PR creation

**Questions or Need Help?**
This is an educational demo repository. For production use of Lacework FortiCNAPP, contact your Fortinet representative or visit [fortinet.com/products/cloud-security](https://www.fortinet.com/products/cloud-security).

---

**⚠️ REMINDER**: This repository contains intentional security vulnerabilities for educational purposes. Do not use any code patterns in production environments.