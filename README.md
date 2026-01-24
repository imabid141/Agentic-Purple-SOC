# 🛡️ Agentic-Purple-SOC: Autonomous AI-Driven Defense

![Status](https://img.shields.io/badge/Status-Phase_1_Complete-green?style=for-the-badge&logo=checkmarx)
![OS](https://img.shields.io/badge/OS-Kali_Purple-black?style=for-the-badge&logo=kali-linux)
![AI](https://img.shields.io/badge/AI-Ollama--Llama3.2-orange?style=for-the-badge&logo=ollama)
![Framework](https://img.shields.io/badge/Framework-MITRE_ATT%26CK-red?style=for-the-badge)
![Security](https://img.shields.io/badge/Auth-mTLS-yellow?style=for-the-badge)
![Role](https://img.shields.io/badge/Role-SOC_Engineering-red?style=for-the-badge&logo=kali-linux)

**Agentic-Purple-SOC** is a privacy-first, local-only Security Operations Center. It proves that a sophisticated, AI-driven security architecture can run on a single laptop (16GB RAM) without relying on expensive cloud subscriptions and protects sensitive security data from third-party AI APIs.

---

## 📖 Project Vision

Security Operations Centers today face two major hurdles: **High Infrastructure Costs** and **Alert Fatigue**\
**Agentic-Purple-SOC** provides a proof-of-concept that enterprise-grade security monitoring can be:

1. **Cost-Effective:** $0 licensing using Open Source tools (Wazuh, Docker, Ollama).
2. **Privacy-Centric:** All telemetry and AI analysis stay on your local machine—zero data leakage.
3. **Autonomous:** Utilizing Agentic AI (LangGraph) for automated alert triage and reasoning.

---

## 🚀 Phase 1: The Sentinel Foundation

In this phase, I engineered the telemetry pipeline—the "Eyes" of the SOC. This involves a containerized Wazuh SIEM stack bridged with a physical **Kali Purple** host OS for deep system visibility.

### 🏗️ Technical Highlights

* **Deterministic Resource Allocation:** Custom-tuned JVM heap settings ($Xms1500m / Xmx1500m$) to ensure stability on a 16GB RAM host.
* **Hybrid Telemetry:** Unified monitoring of Kali Purple Host OS logs via Systemd Journald and Docker microservices.
* **Hardened Communication:** Mutual TLS (mTLS) certificate-based encryption for all internal traffic.
* **Loopback Handshake:** Engineered a stable `127.0.0.1` bridge to maintain SOC connectivity regardless of network changes.

---

## 📊 Phase 1 Milestones

| Milestone | Capability | Status |
| --- | --- | --- |
| **Agent Heartbeat** | Real-time monitoring of Kali Host OS | ✅ Active |
| **SCA Audit** | 180+ Security Configuration checks performed | ✅ Complete |
| **Log Orchestration** | Systemd Journald binary stream ingestion | ✅ Operational |
| **Threat Mapping** | Automated MITRE ATT&CK categorization | ✅ Enabled |
| **FIM** | File Integrity Monitoring for sensitive system files | ✅ Enabled |

---

## 🚦 Quick Start Guide

### Prerequisites

* Kali Linux / Ubuntu
* Docker & Docker Compose Installed
* 16GB RAM (Minimum)

### 1. Initialize Host Environment

The Wazuh Indexer requires the host's memory map limits to be increased, or the container will fail to start.

```bash
# Increase virtual memory limits for Indexer
sudo sysctl -w vm.max_map_count=262144

# Make the change permanent across reboots
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

### Step 2: Clone Repository and Navigate to the Directory

```bash
git clone https://github.com/imabid141/Agentic-Purple-SOC.git

cd Agentic-Purple-SOC/single-node
```

### Step 3: Generate Security Certificates

Initialize the SSL/TLS certificates for secure communication between the Indexer, Manager, and Dashboard.

```bash
docker compose -f generate-indexer-certs.yml run --rm generator
```

### Step 4: Launch the Microservices (The Brain)

Start the stack in detached mode.

```bash
docker compose up -d
```

### Step 5: Verification

Wait approximately 30 seconds (first time it took few mints) for the Microservices to initialize, then verify the containers health.

```bash
# Check container status
docker ps
```

---

## 🔮 Roadmap

* [x] **Phase 1:** Core SIEM Infrastructure & Host Monitoring. [View Deep-Dive]
* [ ] **Phase 2:** Local LLM Integration (Ollama & Llama 3.2).
* [ ] **Phase 3:** Agentic Reasoning with LangGraph.
* [ ] **Phase 4:** Autonomous Incident Response Playbooks.
