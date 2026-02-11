🛡️ LLM Council for Reconnaissance & Penetration TestingA fully automated, multi-agent AI security auditor running locally on WSL.📖 OverviewThe LLM Council is a next-generation reconnaissance tool that bridges the gap between traditional command-line scanners and modern Large Language Models (LLMs). Instead of just generating raw logs, this tool feeds data from 25+ industry-standard tools into a "Council" of specialized AI agents that debate, analyze, and verify vulnerabilities in real-time.The Council Members:🧠 The Strategist (DeepSeek-R1): Analyzes attack surfaces and plans exploit chains.🧐 The Auditor (Qwen2.5-Coder): Verifies technical feasibility and code snippets.⚖️ The Judge (Llama 3.1): Synthesizes findings into a final, hallucinations-free CISO-level report.🏗️ ArchitectureThe system operates in three distinct phases:Passive Recon (OSINT): Silent gathering of subdomains, DNS records, and tech stacks.Active Recon (Intrusive): Port scanning, fuzzing, and vulnerability probing.The Council Debate: AI agents cross-reference findings to filter false positives.🛠️ The Arsenal (Integrated Tools)CategoryTools UsedInfrastructureSubfinder, Amass, DNSdumpster, Dig, WhoisXMLTech StackWappalyzer, BuiltWith, CloudEnum, wafw00fOSINTtheHarvester, Hunter.io, DeHashed, TruffleHog, GitLeaksActive ScanRustScan, Nmap, FFUF, KiteRunnerVulnerabilityNuclei, Nikto, HTTPX🚀 Installation GuidePrerequisitesOS: Windows 10/11 (running WSL2).Distro: Ubuntu 22.04 or later.Hardware: NVIDIA GPU (Recommended) for AI inference.1. System Setup (WSL)Update your system and install core dependencies:Bashsudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget jq python3-pip golang-go nmap dnsutils whois libpcap-dev build-essential
2. Install The Tool SuiteRun the included setup script to install all 25+ tools automatically:Bashchmod +x setup_omega.sh
./setup_omega.sh
3. Install Ollama & AI ModelsDownload and install Ollama, then pull the specific models required for the Council:Bash# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the Council Members
ollama pull deepseek-r1:7b
ollama pull qwen2.5-coder:7b
ollama pull llama3.1:8b
💻 Usage1. Run the Recon MissionStart the main engine. You will be prompted to enter a target URL (e.g., http://scanme.nmap.org).Bashpython3 mission_omega.py
2. Monitor the DebateWatch the terminal as the AI agents analyze the data in real-time:[PASSIVE] Tools gather initial intel.[ACTIVE] RustScan and Nuclei engage the target.[COUNCIL] The AI agents debate the findings.3. View the ReportThe final verified report is saved automatically:Bash# Reports are saved in your configured output directory
cd /mnt/a/WSL/Reports/Omega/
cat OMEGA_REPORT_target_com.md
🛡️ Disclaimer & EthicsThis tool is for educational and authorized testing purposes only.Do not use this tool on any network or website without explicit permission from the owner. The author is not responsible for any misuse or damage caused by this program.
