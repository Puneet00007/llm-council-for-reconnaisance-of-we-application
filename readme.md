# 🛡️ LLM Council for Reconnaissance & Website Penetration Testing

**A fully automated, multi-agent AI security auditor that moves beyond simple scanning to deep, adversarial analysis.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Ollama](https://img.shields.io/badge/AI-Ollama-orange?style=for-the-badge)
![WSL2](https://img.shields.io/badge/Platform-WSL2-lightgrey?style=for-the-badge&logo=linux)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## 📋 Table of Contents
- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [The Architecture](#-the-architecture)
- [Tech Stack & Tool Arsenal](#-tech-stack--tool-arsenal)
- [Installation Guide](#-installation-guide)
- [Usage](#-usage)
- [The Council Logic](#-the-council-logic)
- [Troubleshooting](#-troubleshooting)
- [Disclaimer](#-disclaimer)
- [Acknowledgements](#-acknowledgements)

---

## 📖 About the Project

The **LLM Council for Reconnaissance** is a next-generation security tool designed to solve the problem of "log fatigue" in penetration testing. Traditional scanners generate thousands of lines of output, often filled with false positives.

This project bridges the gap between raw command-line tools and modern Large Language Models (LLMs). It automates the execution of **25+ industry-standard reconnaissance tools** and feeds the data into a local "Council" of specialized AI agents. These agents debate, analyze code, and verify findings to produce a high-fidelity, CISO-level security report.

**Developed as a Final Year Project at Sri Sairam Engineering College.**

---

## ✨ Key Features

* **Full-Spectrum Automation:** Moves seamlessly from Passive OSINT to Active Scanning without human intervention.
* **Multi-Agent AI Debate:** Utilizing **DeepSeek**, **Qwen**, and **Llama 3** to cross-verify findings.
* **Deep Code Analysis:** The AI doesn't just read logs; it analyzes response bodies and source code to confirm vulnerabilities.
* **Zero-Hallucination Protocol:** An "Auditor" agent is specifically tasked with disproving the "Strategist" agent to ensure accuracy.
* **Local Privacy:** Runs entirely on **WSL (Windows Subsystem for Linux)** using local LLMs. No sensitive target data is sent to the cloud.

---

## 🏗️ The Architecture

The system follows a strict three-phase pipeline:

1.  **Phase 1: Passive Recon (The Silent Phase)**
    * Gathers intelligence without directly engaging the target's infrastructure.
    * *Output:* Subdomains, DNS records, Tech Stacks, Leaked Emails.
2.  **Phase 2: Active Recon (The Intrusive Phase)**
    * Directly probes the target for open ports, hidden directories, and misconfigurations.
    * *Output:* Open Ports, Service Versions, CVEs, API Endpoints.
3.  **Phase 3: The Council Session (The Analysis Phase)**
    * The raw data is structured and fed into the AI Council for debate and report generation.

---

## 🛠️ Tech Stack & Tool Arsenal

This project integrates the following open-source tools into a unified Python orchestrator:

### 1. Infrastructure & Domain Assets
| Tool | Purpose |
| :--- | :--- |
| **Subfinder** | High-speed subdomain enumeration. |
| **Amass** | Deep-dive asset discovery (Passive Mode). |
| **DNSdumpster / Dig** | DNS record analysis and zone transfer checks. |
| **WhoisXML / bgp.he.net** | IP range and ASN mapping. |

### 2. Technology & OSINT
| Tool | Purpose |
| :--- | :--- |
| **Wappalyzer / BuiltWith** | Technology stack fingerprinting. |
| **CloudEnum** | Enumeration of public cloud assets (AWS/Azure/GCP). |
| **theHarvester / Hunter.io** | Email and employee pattern discovery. |
| **TruffleHog / GitLeaks** | Searching for secrets and credential leaks in repos. |
| **wafw00f** | Web Application Firewall detection. |

### 3. Active Scanning & Vulnerability Probing
| Tool | Purpose |
| :--- | :--- |
| **RustScan** | Ultra-fast port discovery (Adaptive). |
| **Nmap** | Service version detection (`-sV`) and OS fingerprinting (`-O`). |
| **FFUF / Gobuster** | Directory and parameter fuzzing. |
| **KiteRunner** | API endpoint discovery. |
| **Nuclei** | Template-based vulnerability scanning (CVEs, Misconfigurations). |
| **HTTPX** | Probing for security headers and status codes. |

---

## ⚙️ Installation Guide

### Prerequisites
* **OS:** Windows 10/11 with **WSL2** enabled.
* **Distro:** Ubuntu 22.04 LTS (Recommended).
* **Hardware:** NVIDIA GPU (6GB+ VRAM recommended) for AI inference.
* **Storage:** At least 20GB free space (preferably on a secondary drive like `A:` or `D:`).

### Step 1: System Setup
Update your WSL instance and install core dependencies:
```bash
sudo apt update && sudo apt upgrade -y

Step 2: Install the "Omega" Tool Suite
Run the provided setup script to fetch and install all 25+ tools:

Bash
chmod +x setup_omega.sh
./setup_omega.sh
Step 3: Install Ollama & The Council Models
Install the AI engine and pull the specific models required for the debate logic:

Bash
# 1. Install Ollama
curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh

# 2. Pull the Council Members
ollama pull deepseek-r1:7b   # The Strategist
ollama pull qwen2.5-coder:7b # The Auditor
ollama pull llama3.1:8b      # The Judge
🚀 Usage
1. Start the Engine
Navigate to your project directory and run the main mission script:

Bash
python3 mission_omega.py
2. Enter Target
When prompted, enter the URL of the website you are authorized to test:

Plaintext
🎯 Enter Target URL: [http://scanme.nmap.org](http://scanme.nmap.org)
3. Monitor & Report
The system will display real-time logs of the tools running.

Once complete, the Council Debate will begin in the terminal.

The final report is saved as a Markdown file:

Bash
/mnt/a/WSL/Reports/Omega/OMEGA_REPORT_[Target].md
🧠 The Council Logic
How the AI Agents work together to ensure accuracy:

🕵️‍♂️ The Strategist (DeepSeek-R1):

Role: Red Teamer / Attacker.

Task: Analyzes open ports and Nuclei logs to connect the dots. "If Port 8080 is open and running Jenkins, try these specific exploits."

🧐 The Auditor (Qwen2.5-Coder):

Role: Code Reviewer / Skeptic.

Task: Cross-references the Strategist's claims against the raw data. "The Strategist claims SQL Injection, but the WAF blocked the request (403 Forbidden). Finding rejected."

⚖️ The Judge (Llama 3.1):

Role: CISO / Report Writer.

Task: Reviews the debate, resolves conflicts, and writes the final report including Risk Scores (CVSS) and Remediation Steps.

🔧 Troubleshooting
Issue: The AI is slow / using CPU instead of GPU.

Fix: Ensure NVIDIA Container Toolkit is installed in WSL.

Bash
nvidia-smi
If this command works, restart Ollama to force GPU usage.

Issue: "Model not found" error.

Fix: Ensure you have pulled the exact tags used in the script.

Bash
ollama list
# Make sure qwen2.5-coder:7b is listed
⚖️ Disclaimer
⚠️ ETHICAL USE ONLY

This tool is designed for educational purposes and authorized security assessments (Bug Bounties, Penetration Tests with contracts).

DO NOT use this tool on targets you do not own or have explicit permission to test.

The developers are not responsible for any misuse or damage caused by this program.
sudo apt install -y git curl wget jq python3-pip golang-go nmap dnsutils whois libpcap-dev build-essential
