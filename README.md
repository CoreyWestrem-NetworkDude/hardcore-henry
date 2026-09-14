# Hardcore-Henry: Production-Grade MSP Triage Engine 🚀

Hardcore-Henry is a self-hosted, local AI triage assistant tailored specifically for MSP L1/L2 technicians. It automatically enforces a rigid, dual-pane breakdown for all technical queries: immediate **Remediation & Execution** steps followed by deep **Architectural Theory**.

This production guide walks you through setting up the AI engine, deploying the web interface, routing it securely through a free Cloudflare Tunnel, and automating the entire stack to launch silently on boot with real-time streaming telemetry counters.

---

## 🏗️ Technical Architecture
* **Core Engine:** Ollama running local `minicpm-v` multi-modal vision weights.
* **Web Interface:** Open WebUI deployed via Docker Bridge Network.
* **Secure Ingress:** Cloudflare Tunnel (`cloudflared`) bypassing local firewall restrictions.
* **OS Automation:** Native Linux Systemd Service configuration.
* **Telemetry Proxy:** Custom Open WebUI native Python `Pipe` middleware wrapper (v1.3.0 Streaming).

---

## 🚀 Step-by-Step Deployment

### 1. Build the AI Engine (Ollama)
First, make sure Ollama is installed on your host system. Create a file named `Modelfile` in your directory and compile the custom Hardcore-Henry framework:

```bash
ollama create hardcore-henry -f ./Modelfile
```

### 2. Configure Host Network Binding & Persistent VRAM Caching
By default, Ollama unloads models after 5 minutes of idling, which can cause early morning connection drops. We must force Ollama to accept internal bridge connections and cache the model permanently inside GPU VRAM.
1. Run `sudo systemctl edit ollama`
2. Add the following service rules at the very top of the drop-in override profile:
   ```text
   [Service]
   Environment="OLLAMA_HOST=0.0.0.0"
   Environment="OLLAMA_KEEP_ALIVE=-1"
   ```
3. Save, exit, and reload the background engine configurations:
   ```bash
   sudo systemctl daemon-reload && sudo systemctl restart ollama
   ```

### 3. Spin Up the Web Interface (Docker)
Use the included `docker-compose.yml` to launch Open WebUI. This configuration sets up a dedicated bridge and establishes a stable routing gateway back to your host hardware:

```bash
docker compose up -d
```
*Your web interface is now running locally on port `3000`.*

### 4. Create your Secure Cloudflare Tunnel
To access your triage engine securely from your phone or anywhere outside the office without opening dangerous firewall ports:
1. Create a free tunnel in your Cloudflare Zero Trust Dashboard named `msp-triage`.
2. Point your public hostname (e.g., `your-domain.com`) directly to **`http://127.0.0.1:3000`**.

### 5. Automate Tunnel & AI Launch on Boot (Linux Systemd)
To ensure Hardcore-Henry goes online the second your PC boots up—without needing to open a terminal—we create a system service file.
1. Create the automation profile: `sudo nano /etc/systemd/system/hardcore-henry-tunnel.service`
2. Paste the following configuration:
   ```text
   [Unit]
   Description=Cloudflare Tunnel for Hardcore-Henry MSP Triage
   After=network.target network-online.target
   Wants=network-online.target

   [Service]
   Type=simple
   User=YOUR_LINUX_USERNAME
   ExecStart=/usr/bin/cloudflared tunnel run --url http://127.0.0.1:3000 msp-triage
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```
3. Enable the startup routine:
   ```bash
   sudo systemctl daemon-reload && sudo systemctl enable --now hardcore-henry-tunnel.service
   ```

---

## 📊 Deploying the Real-Time Streaming Odometer (Pipe Proxy)
To give technicians instantaneous visual feedback alongside active transparency into their 16,384 token limits:
1. Navigate to Open WebUI **Admin Panel ➔ Functions**.
2. Click **Create Function (+)** and configure the ID as exactly: `hardcore_henry_triage`.
3. Paste the contents of your local `context_tracker_pipe.py` script file directly into the editor pane and click save. 

This introduces a custom model pipe mapping into the workspace layout. Select **`Hardcore-Henry (with Context Counter)`** from the chat model dropdown selector. Henry will stream responses word-by-word instantly upon hitting send, concluding each exchange with an isolated, dynamic filling-dot memory allocation odometer badge (`[⬢⬡⬡⬡⬡]`). This functionality applies automatically system-wide across all user accounts.

---

## ⚠️ Critical Post-Installation Fixes (Error Prevention)

### Fix 1: Resolving "Ollama: Network Problem" in the UI
When you first log into your web interface at your public domain, go to **Settings ➔ Connections ➔ Ollama API**. 
* Ensure the target URL is explicitly mapped to: `http://docker.internal`
* Click the **Sync/Refresh icon** to pull down the models list and hit **Save**.

### Fix 2: Bypassing Empty UI Responses (Disabling Function Injection)
Open WebUI attempts to inject background tools into the model prompt string by default. Because basic vision models don't support native web extensions, this will crash the output bubble and return an empty response.
1. Navigate to **Workspace ➔ Models** or open the model properties menu.
2. Select **Edit** on `hardcore-henry:latest`.
3. Under the **Builtin Tools / Capabilities** section, **uncheck all active tool choices** (Web Search, Image Gen, etc.).
4. Click **Save & Update**.

---

## 🔒 Cross-Platform & Dual-Boot Behavior (Windows / Linux)
* **When booting into Windows:** Your custom triage files live securely inside your encrypted Linux partitions. Henry remains completely dark, offline, and safe from outside intrusion while you game or run Windows apps.
* **When booting into Linux:** The moment your OS reaches the desktop environment, systemd instantly triggers Ollama, hooks up the Docker stack, establishes the Cloudflare network link, and brings Henry online entirely in the background.
