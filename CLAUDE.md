# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **deliberately vulnerable educational security lab** for demonstrating Lacework FortiCNAPP code security capabilities. The repository contains intentional security vulnerabilities including hardcoded secrets, outdated dependencies, insecure Docker configurations, and misconfigured infrastructure-as-code.

**⚠️ SECURITY NOTE**: This code contains intentional vulnerabilities for educational purposes. Never deploy this code to production environments.

## Common Development Commands

### Local Development
```bash
# Set up the vulnerable Flask application
cd app/
pip install -r requirements.txt
python app.py
```

### Security Scanning with Lacework
```bash
# Trigger SmartFix via PR (requires GitHub integration)
echo "paramiko==2.4.1" >> app/requirements.txt && \
git checkout -b trigger-smartfix && \
git add app/requirements.txt && \
git commit -m "Trigger SmartFix" && \
git push -u origin trigger-smartfix && \
gh pr create --fill
```

### Container Operations
```bash
# Build the vulnerable container
docker build -t forticnapp-demo .

# Run the container (insecure configuration)
docker run -p 5000:5000 forticnapp-demo
```

### Infrastructure Validation
```bash
# Validate Terraform configurations (will show security issues)
cd terraform/
terraform fmt
terraform validate
terraform plan  # Shows insecure resource configurations
```

## Architecture and Vulnerability Patterns

### Application Structure
- **Flask Application**: `app/app.py` - Main web application with vulnerable endpoints
- **Configuration**: `app/config.py` - Contains hardcoded AWS credentials (intentional)
- **Vulnerable Functions**: `app/vuln_app.py` - SQL injection, command injection, weak crypto
- **Dependencies**: `app/requirements.txt` - Outdated packages with known CVEs

### Intentional Vulnerabilities

#### Secrets Management
- Hardcoded AWS credentials in `config.py`
- Exposed secrets via Flask route responses

#### Application Security (SAST)
- **SQL Injection**: Direct string concatenation in database queries
- **Command Injection**: Unsanitized user input passed to `os.system()`
- **Weak Cryptography**: MD5 hashing for passwords
- **Unsafe Deserialization**: Missing `load_data()` function using pickle

#### Dependency Management (SCA)
- Flask 1.0 with CVE-2018-1000656
- Django 1.11.27 with multiple CVEs
- Requests 2.19.1 with CVE-2018-18074
- Multiple other outdated packages with known vulnerabilities

#### Container Security
- Running as root user (no USER directive)
- Using mutable base image tags
- Missing security configurations

#### Infrastructure as Code (IaC)
- **Public S3 Bucket**: `aws_s3_bucket` with `acl = "public-read"`
- **Public Subnet**: Auto-assigns public IPs with `map_public_ip_on_launch = true`
- Missing encryption and access controls

### Lacework FortiCNAPP Integration

The repository is designed to work with:
- **VSCode Extension**: Local scanning via Lacework Security extension
- **GitHub Integration**: Automated PR scanning and SmartFix suggestions
- **CI/CD Pipeline**: Policy enforcement and PR blocking capabilities

### Security Scan Types
- **IaC Scan**: Detects Terraform misconfigurations
- **SAST Scan**: Identifies application security flaws
- **SCA Scan**: Finds vulnerable dependencies
- **Secrets Scan**: Discovers hardcoded credentials

## Educational Use Only

This repository is strictly for educational purposes to demonstrate:
1. Common security vulnerabilities in modern applications
2. How security scanning tools detect these issues
3. Automated remediation suggestions via SmartFix
4. Integration of security scanning into development workflows

**Do not use any code patterns from this repository in production systems.**