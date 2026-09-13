# Hardcore-Henry: Production-Grade MSP Triage Engine 🚀

Hardcore-Henry is a self-hosted, local AI triage assistant tailored specifically for MSP L1/L2 technicians. It automatically enforces a rigid, dual-pane breakdown for all technical queries: immediate **Remediation & Execution** steps followed by deep **Architectural Theory**.

This production guide walks you through setting up the AI engine, deploying the web interface, routing it securely through a free Cloudflare Tunnel, and automating the entire stack to launch silently on boot.

---

## 🏗️ Technical Architecture
* **Core Engine:** Ollama running local `qwen2.5vl:3b` vision base weights.
* **Web Interface:** Open WebUI deployed via Docker Bridge Network.
* **Secure Ingress:** Cloudflare Tunnel (`cloudflared`) bypassing local firewall restrictions.
* **OS Automation:** Native Linux Systemd Service configuration.

---

## 🚀 Step-by-Step Deployment

### 1. Build the AI Engine (Ollama)
First, make sure Ollama is installed on your host system. Create a file named `Modelfile` in your directory and compile the custom Hardcore-Henry framework:

```bash
ollama create hardcore-henry -f ./Modelfile
```

### 2. Configure Host Network Binding
By default, Ollama only listens on local loopback, which blocks Docker container traffic. We must force Ollama to accept internal bridge connections.
1. Run `sudo systemctl edit ollama`
2. Add the following lines at the very top of the file:
   ```text
   [Service]
   Environment="OLLAMA_HOST=0.0.0.0"
   ```
3. Save, exit, and reload the service engine:
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

## ⚡ Bulk Data Extraction & Documentation Ingestion (Admin Guide)

To make Henry instantly familiar with your specific MSP environments, you can bulk-export structural tracking tables from your management software instead of copying assets one by one.

### 🔐 1. KaseyaOne & IT Glue (Global Documentation Export)
If you possess Admin privileges, you can compile your entire IT Glue platform data structure into a unified, encrypted backup.
1. Log into your IT Glue portal, and click **Admin** in the top navigation bar.
2. Navigate to the left-hand sidebar and select **Export Data**.
3. Under *Export Options*, choose **Entire account** (or filter down to a specific customer layout under *Data for an organization*).
4. Check **Encrypt export with password** to secure credential and configuration files.
5. Click **Start Export**. IT Glue will email you a secure download link containing organized CSV and HTML tables of all your assets.

### 💻 2. Datto RMM (Global Device Asset Bulk Export)
To train Henry on your endpoints, software inventories, and monitor alerts, extract the complete device grid:
1. Log into your Datto RMM dashboard.
2. Navigate to **Devices** ➔ **All Devices**.
3. Click the **Export All Rows to CSV** button in the top right corner of the device list grid.
4. Save the compiled data spreadsheet directly to your computer.

### 📥 3. Uploading Bulk Data into Hardcore-Henry
Once you have your enterprise CSVs or HTML tables extracted, import them to Open WebUI all at once:
1. Log into your public **Open WebUI** dashboard as an Admin.
2. Go to **Workspace** ➔ **Documents**.
3. Click the **Upload Documents** button.
4. Drag and drop your bulk IT Glue asset CSV files and Datto RMM device tables directly into the browser.
5. In your chat prompt windows, simply type `#` followed by the file name (e.g., `#Datto_RMM_Devices`) to instruct Henry to reference entire enterprise configurations instantly!

---

## ⚠️ Critical Post-Installation Fixes (Error Prevention)

### Fix 1: Resolving "Ollama: Network Problem" in the UI
When you first log into your web interface at your public domain, go to **Settings ➔ Connections ➔ Ollama API**. 
* Ensure the target URL is explicitly mapped to: `http://docker.internal`
* Click the **Sync/Refresh icon** to pull down the models list and hit **Save**.

### Fix 2: Bypassing Empty UI Responses (Disabling Function Injection)
Open WebUI attempts to inject background tools into the model prompt string by default. Because `llama3` doesn't support native web extensions, this will crash the output bubble and return an empty response.
1. Navigate to **Workspace ➔ Models** or open the model properties menu.
2. Select **Edit** on `hardcore-henry:latest`.
3. Under the **Builtin Tools / Capabilities** section, **uncheck all active tool choices** (Web Search, Image Gen, etc.).
4. Click **Save & Update**.

### Fix 3: Handling High-Resolution Mobile Image Upload Crashes (Error 400)
When technicians upload raw smartphone photographs of error text or hardware layouts, the default 4,096 context block will instantly saturate, returning a HTTP 400 Context error.
1. Ensure your `Modelfile` has `PARAMETER num_ctx 16384` appended to expand the dynamic ceiling.
2. Log into the Open WebUI Admin Panel ➔ **Settings** ➔ **Models**.
3. Click **Edit** next to `hardcore-henry:latest`.
4. Under **Capabilities**, check the box for **Usage** and hit **Save**. This activates a live telemetry token counter beneath responses so technicians can monitor their active session utilization boundaries.
---

## 🔒 Cross-Platform & Dual-Boot Behavior (Windows / Linux)
* **When booting into Windows:** Your custom triage files live securely inside your encrypted Linux partitions. Henry remains completely dark, offline, and safe from outside intrusion while you game or run Windows apps.
* **When booting into Linux:** The moment your OS reaches the desktop environment, systemd instantly triggers Ollama, hooks up the Docker stack, establishes the Cloudflare network link, and brings Henry online entirely in the background.
