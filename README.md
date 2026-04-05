# Log Analyzer Agent

A Claude-based AI agent that analyzes raw logs, identifies production incidents, and recommends debugging steps and fixes.

This project demonstrates how a prompt-driven agent can turn noisy logs into structured, actionable insights.

---

## 🚀 What This Does

The Log Analyzer Agent:

* analyzes raw logs from multiple systems
* prioritizes production-impacting issues
* groups related failures into incidents
* separates evidence from inference
* suggests root causes and debugging steps
* recommends practical engineering fixes

Supported log types include:

* Apache (access + error)
* Nginx (access + error)
* application logs
* system logs (syslog)
* Kubernetes logs

---

## 🧠 How It Works

This project is built as a prompt-based agent using Claude Projects.

### Core components

* **LOG_ANALYZER_AGENT.md**

  * defines the agent behavior
  * acts as the "brain" of the system

* **log files**

  * input data with realistic noise and injected incidents

* **tool layer (optional)**

  * simulates fetching and filtering logs
  * demonstrates how the agent could integrate with real systems

---

## ▶️ How to Run (Claude Project)

This agent runs inside Claude.

### Step 1: Create a Claude Project

* Open Claude
* Create a new Project (example: Log Analyzer Agent)

### Step 2: Load the Agent

* Open `LOG_ANALYZER_AGENT.md`
* Copy all contents
* Paste into the Project instructions

### Step 3: Provide Logs

Either:

* paste a log file directly into Claude

OR

* upload one of the generated log files

### Step 4: Run the Agent

Use a prompt like:

```
Analyze these logs and identify the most important incident, the likely root cause, and the best next debugging steps.
```

---

## 🧪 Example Output

The agent can detect:

* database connection pool exhaustion
* cascading API failures (HTTP 500)
* latency trends leading up to failure
* retry amplification issues
* suspicious authentication activity from external IPs
* secondary system degradation (Redis, etc.)

It also:

* cites supporting evidence
* distinguishes confirmed facts vs inference
* recommends concrete debugging steps

(Optional) Add a screenshot:

```
![Example Output](example.png)
```

---

## 🛠️ Fake Tool Interface (Optional)

This project includes a simple tool layer to simulate real-world agent capabilities:

* `get_recent_logs(...)`
* `get_service_logs(...)`
* `search_logs(...)`

These demonstrate how the agent could:

* fetch logs dynamically
* filter by service
* search for patterns

In a production system, these would connect to:

* logging platforms
* monitoring systems
* APIs

---

## 🧪 Generate Fake Logs

To create realistic test data:

```bash
python generate_fake_logs.py
```

This generates multiple log types in:

```
generated_logs/
```

Each file contains:

* normal background noise
* injected incidents (failures, attacks, timeouts)

---

## 💡 Why This Project Matters

This is not a generic chatbot.

It demonstrates:

* prompt-based agent design
* signal vs noise prioritization
* structured reasoning from unstructured data
* production-style debugging workflows
* extensibility via tool integration

---

## 🧠 Key Takeaways

* the `.md` file defines the agent behavior
* Claude executes the reasoning
* logs are the input data
* tools simulate real-world integrations

---

## 📌 Portfolio Summary

Built a Claude-based log analysis agent that triages noisy production logs, identifies incidents, separates evidence from inference, and recommends debugging steps and fixes. Designed with extensibility in mind via a simulated tool interface.

---

## 🔮 Future Improvements

* integrate with real log APIs
* add severity scoring
* support structured JSON output
* correlate logs with metrics
* auto-generate incident reports
