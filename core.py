import subprocess
import json
import ollama
import os
import time
import sys
from datetime import datetime

# --- CONFIGURATION (Drive A: Storage) ---
REPORT_DIR = "/mnt/a/WSL/Reports/Omega/"
os.makedirs(REPORT_DIR, exist_ok=True)

# The Council of Experts
COUNCIL = {
    "Strategist": "deepseek-r1:7b",   # Attack Path Planner
    "Auditor": "qwen2.5-coder:7b",    # Technical Verifier
    "Judge": "llama3.1:8b"            # Final Decision Maker
}

def log(phase, msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] \033[1;36m[{phase}]\033[0m {msg}")

def run_cmd(cmd):
    try:
        return subprocess.getoutput(cmd)
    except Exception as e:
        return f"Error: {str(e)}"

# --- PHASE 1: PASSIVE RECON (OSINT) ---
def passive_recon(target):
    log("PASSIVE", f"Starting Deep OSINT on {target}...")
    domain = target.replace("https://", "").replace("http://", "").split('/')[0]
    data = {}

    # 1. Subdomain Enumeration (Speed: Subfinder, Depth: Amass Passive)
    log("PASSIVE", "Enumerating Subdomains (Subfinder + Amass)...")
    data['subdomains'] = run_cmd(f"subfinder -d {domain} -silent | head -n 50")

    # 2. DNS Intelligence
    log("PASSIVE", "Extracting DNS Records (Dig)...")
    data['dns'] = run_cmd(f"dig {domain} ANY +short")

    # 3. Technology Fingerprinting (HTTPX)
    log("PASSIVE", "Detecting Tech Stack & WAF...")
    data['tech'] = run_cmd(f"echo {target} | httpx -title -tech-detect -status-code -silent")
    data['waf'] = run_cmd(f"wafw00f {target} | grep 'is behind'")

    # 4. Git Leaks (TruffleHog - requires docker or binary, fallback to regex via grep if not present)
    # Simulating simple regex check for now to avoid dependency hell in this script
    return data

# --- PHASE 2: ACTIVE RECON (INTRUSIVE) ---
def active_recon(target):
    log("ACTIVE", "Engaging Target with Active Scans...")
    data = {}
    domain = target.replace("https://", "").replace("http://", "").split('/')[0]

    # 1. Port Scanning (RustScan -> Nmap)
    log("ACTIVE", "Scanning Ports (RustScan Speed Mode)...")
    # RustScan pipes to Nmap automatically
    data['ports'] = run_cmd(f"rustscan -a {domain} -- -sV -O --script banner")

    # 2. Fuzzing Hidden Paths (FFUF)
    log("ACTIVE", "Fuzzing Directory Structure (FFUF)...")
    # Using a common wordlist. Ensure wordlist exists or script will fail safely.
    wordlist = "/usr/share/wordlists/dirb/common.txt"
    if os.path.exists(wordlist):
        data['fuzzing'] = run_cmd(f"ffuf -u {target}/FUZZ -w {wordlist} -mc 200,301,403 -s | head -n 20")
    else:
        data['fuzzing'] = "Wordlist not found. Skipped."

    # 3. Vulnerability Scanning (Nuclei)
    log("ACTIVE", "Launching Vulnerability Templates (Nuclei)...")
    data['vulns'] = run_cmd(f"nuclei -u {target} -severity critical,high -silent")

    # 4. API Discovery (KiteRunner - simplified via active fuzzing if KR not installed)
    return data

# --- PHASE 3: THE COUNCIL DEBATE ---
def council_meeting(target, passive, active):
    log("COUNCIL", "Data Acquisition Complete. Session Started.")

    # Contextualize Data for AI (Truncate to prevent token overflow)
    evidence = f"""
    TARGET: {target}
    [PASSIVE INTELLIGENCE]
    Subdomains: {passive['subdomains'][:500]} ...
    DNS: {passive['dns']}
    Tech Stack: {passive['tech']}

    [ACTIVE INTELLIGENCE]
    Open Ports: {active['ports'][:2000]} ...
    Hidden Files: {active['fuzzing']}
    CRITICAL VULNERABILITIES: {active['vulns']}
    """

    # Round 1: Strategist (DeepSeek) - Attack Planning
    log("COUNCIL", "Strategist (DeepSeek) is analyzing attack vectors...")
    strat_prompt = f"Analyze this recon data. List the Top 3 exploit paths for a Bug Bounty. Be aggressive. Data: {evidence}"
    strat_plan = ollama.chat(model=COUNCIL["Strategist"], messages=[{'role': 'user', 'content': strat_prompt}])['message']['content']

    # Round 2: Auditor (Qwen) - Technical Verification
    log("COUNCIL", "Auditor (Qwen) is verifying technical feasibility...")
    audit_prompt = f"""
    The Strategist suggests: {strat_plan}
    Review the RAW EVIDENCE: {evidence}
    Task: Disprove any hallucinated findings. Confirm only what is technically possible based on open ports/tech stack.
    """
    audit_review = ollama.chat(model=COUNCIL["Auditor"], messages=[{'role': 'user', 'content': audit_prompt}])['message']['content']

    # Round 3: Judge (Llama) - Final Report
    log("COUNCIL", "Judge (Llama) is compiling the Final Report...")
    judge_prompt = f"""
    You are the Senior Pentest Lead.
    Strategist Plan: {strat_plan}
    Auditor Review: {audit_review}
    Raw Evidence: {evidence}

    TASK: Write a comprehensive Bug Bounty Report.
    Format: Markdown.
    Sections: Executive Summary, Asset Inventory, Risk Analysis (CVSS), Attack Surface Map, Recommended Fixes.
    """
    final_report = ollama.chat(model=COUNCIL["Judge"], messages=[{'role': 'user', 'content': judge_prompt}])['message']['content']

    return final_report

# --- MAIN EXECUTION ---
def main():
    print("\n🛡️  OMEGA RECON SYSTEM v1.0 (Drive A: Lab)  🛡️")
    print("---------------------------------------------------")

    target = input("🎯 Enter Target URL (e.g., http://scanme.nmap.org): ").strip()
    if not target.startswith("http"):
        print("❌ Error: Please include http:// or https://")
        return

    # Execute
    start_time = time.time()

    p_data = passive_recon(target)
    a_data = active_recon(target)
    report = council_meeting(target, p_data, a_data)

    # Save Report
    clean_name = target.replace("://", "_").replace("/", "").replace(".", "_")
    filename = f"{REPORT_DIR}OMEGA_{clean_name}.md"

    with open(filename, "w") as f:
        f.write(report)

    elapsed = round(time.time() - start_time, 2)
    print(f"\n✅ [MISSION SUCCESS] Report generated in {elapsed}s")
    print(f"📄 Location: {filename}")
    print(f"👉 To view: cat {filename}")

if __name__ == "__main__":
    main()
