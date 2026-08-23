# Lightweight AI-Based Cybersecurity Digital Twin for Real-Time Threat Detection and Automatic Node Isolation

## Overview

This project presents a **Lightweight AI-Based Cybersecurity Digital Twin** designed for real-time cyber threat detection, anomaly analysis, and automatic node isolation in network environments.

The system creates a virtual representation (Digital Twin) of a computer network where incoming traffic, device behavior, and communication patterns are continuously monitored and analyzed using Machine Learning algorithms.

The primary goal of this project is to detect malicious activities such as:

* Distributed Denial of Service (DDoS)
* Network Intrusions
* Abnormal Traffic Patterns
* Unauthorized Access Attempts
* IoT Device Compromise
* Botnet Activities

Unlike traditional cybersecurity systems that rely on fixed rules and signatures, this project uses an adaptive AI-based anomaly detection mechanism with **dynamic thresholds** to improve detection accuracy and reduce false positives.

---

# Problem Statement

Modern organizations face several cybersecurity challenges:

* Traditional IDS systems rely heavily on predefined signatures.
* Attack patterns continuously evolve.
* Large-scale enterprise systems generate massive real-time traffic.
* Fixed anomaly thresholds fail under changing traffic conditions.
* Existing systems consume high computational resources.
* Delayed threat detection can damage the entire network.

This project addresses these limitations using:

* Lightweight AI models
* Dynamic anomaly thresholding
* Real-time stream processing
* Automatic malicious node isolation
* Digital twin-based monitoring

---

# What is a Digital Twin?

A **Digital Twin** is a virtual replica of a real-world system.

In this project:

* The real network acts as the physical environment.
* The digital twin simulates and monitors the behavior of the network.
* Incoming traffic data is continuously mirrored into the twin.
* The AI engine analyzes the mirrored data in real time.
* If malicious behavior is detected, the system isolates the compromised node.

The digital twin helps:

* Monitor network health
* Predict cyber attacks
* Detect anomalies earlier
* Test security strategies safely
* Reduce damage caused by attackers

---

# Project Objectives

## Primary Objectives

* Detect cyber threats in real time.
* Create a lightweight AI-powered cybersecurity system.
* Simulate network behavior using a digital twin.
* Automatically isolate suspicious nodes.
* Reduce false positives using dynamic thresholds.

## Secondary Objectives

* Support IoT and enterprise environments.
* Visualize network activities.
* Stream real-time traffic data.
* Compare anomaly detection methods.
* Build a scalable architecture.

---

# Key Features

## Real-Time Threat Detection

Continuously analyzes streaming network traffic.

## Digital Twin Environment

Maintains a virtual copy of network behavior.

## Lightweight Architecture

Designed to run efficiently with low CPU and memory usage.

## Dynamic Thresholding

Uses adaptive thresholds instead of fixed values.

## Automatic Node Isolation

Suspicious devices are isolated automatically.

## AI-Based Anomaly Detection

Uses machine learning algorithms for attack detection.

## Visualization Dashboard

Displays:

* Network nodes
* Attack alerts
* Threat scores
* Isolation status
* Live traffic graphs

## Multi-Dataset Support

Can work with:

* CICIDS2017
* UNSW-NB15
* NSL-KDD
* IoT datasets

---

# Why "Lightweight"?

The term lightweight means:

* Low memory consumption
* Fast execution speed
* Minimal computational overhead
* Suitable for IoT devices
* Can run on systems with limited hardware resources
* Faster detection response

Instead of using very large deep learning models, this project focuses on efficient machine learning algorithms such as:

* Isolation Forest
* One-Class SVM
* Local Outlier Factor
* Statistical thresholding methods

---

# Technologies Used

## Programming Language

* Python

## Libraries & Frameworks

* NumPy
* Pandas
* Scikit-learn
* Matplotlib
* Seaborn
* NetworkX
* Streamlit / Flask
* Joblib

## Development Tools

* VS Code
* GitHub
* Jupyter Notebook

## Visualization

* Node Graphs
* Traffic Flow Graphs
* Alert Dashboard

---

# Machine Learning Algorithms

## 1. Isolation Forest (Primary Algorithm)

Isolation Forest is used for anomaly detection.

### Working Principle

* Randomly partitions data.
* Anomalies get isolated faster.
* Produces anomaly scores.

### Advantages

* Fast
* Efficient
* Works well on large datasets
* Suitable for real-time detection

### Time Complexity

* Training: O(t × ψ × log ψ)
* Prediction: O(t × log ψ)

Where:

* t = number of trees
* ψ = sample size

---

## 2. Dynamic Thresholding

Instead of using a fixed anomaly threshold, the system calculates thresholds dynamically.

### Problem with Fixed Thresholds

Network traffic changes continuously.
A fixed threshold may:

* Miss attacks
* Produce false alarms
* Fail during traffic spikes

### Proposed Solution

Use adaptive statistical thresholds:

* Quartile Deviation (QD)
* Interquartile Range (IQR)
* Moving Average
* Z-score methods

### Example

If anomaly scores suddenly increase:

* Threshold automatically adjusts.
* System remains stable.

This significantly improves:

* Detection accuracy
* Adaptability
* Real-time performance

---

# Automatic Node Isolation

When a node is detected as malicious:

1. Threat score is generated.
2. Node is marked suspicious.
3. Isolation module disconnects the node.
4. Alert is generated.
5. Twin environment updates network status.

Isolation strategies may include:

* Blocking IP
* Disconnecting node
* Firewall rule updates
* VLAN isolation
* Quarantine mode

---

# System Architecture

## Workflow

### Step 1 — Data Collection

Traffic is collected from:

* Network packets
* IoT devices
* System logs
* Sensors

### Step 2 — Preprocessing

Data cleaning includes:

* Missing value handling
* Encoding
* Normalization
* Feature extraction

### Step 3 — Digital Twin Simulation

A virtual network model is created.

### Step 4 — AI-Based Detection

Isolation Forest analyzes behavior.

### Step 5 — Dynamic Threshold Calculation

Adaptive threshold is computed.

### Step 6 — Attack Detection

If anomaly score exceeds threshold:

* Alert generated
* Node isolated

### Step 7 — Visualization

Dashboard displays:

* Threat maps
* Node status
* Attack statistics

---

# Datasets Used

## CICIDS2017

Contains:

* DDoS
* Brute force
* Port scan
* Web attacks

## UNSW-NB15

Contains modern attack patterns.

## NSL-KDD

Benchmark intrusion detection dataset.

---

# Folder Structure

```bash
AI_Cybersecurity_Digital_Twin/
│
├── datasets/
│   ├── CICIDS2017/
│   ├── UNSW_NB15/
│   └── NSL_KDD/
│
├── preprocessing/
│   ├── load_datasets.py
│   ├── clean_data.py
│   └── feature_engineering.py
│
├── models/
│   ├── isolation_forest.py
│   ├── dynamic_threshold.py
│   └── node_isolation.py
│
├── visualization/
│   ├── network_graph.py
│   ├── dashboard.py
│   └── live_monitor.py
│
├── results/
│   ├── graphs/
│   ├── reports/
│   └── metrics/
│
├── app.py
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/AI_Cybersecurity_Digital_Twin.git
cd AI_Cybersecurity_Digital_Twin
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

## Run Main Application

```bash
python app.py
```

## Run Visualization Dashboard

```bash
streamlit run dashboard.py
```

---

# Expected Outputs

The system provides:

* Real-time anomaly detection
* Suspicious node identification
* Automatic node isolation
* Threat score generation
* Network visualization graphs
* Detection accuracy metrics
* Live monitoring dashboard

---

# Evaluation Metrics

The project evaluates performance using:

* Accuracy
* Precision
* Recall
* F1-score
* False Positive Rate
* Detection Time
* Resource Utilization

---

# Novelty of the Project

## Main Innovation

The major novelty of this project is:

### Dynamic Isolation Thresholding

Most existing systems use static thresholds.
This project dynamically adjusts thresholds based on live network behavior.

### Benefits

* Adapts to traffic fluctuations
* Reduces false alarms
* Improves attack detection
* Better for real-time systems

## Additional Novel Features

* Lightweight implementation
* AI-based adaptive security
* Real-time digital twin simulation
* Automatic attack response
* IoT compatibility

---

# Applications

This project can be used in:

* Smart Cities
* Enterprise Networks
* IoT Environments
* Industrial Systems
* Smart Agriculture
* Cloud Security
* Healthcare Networks
* Educational Institutions

---

# Future Enhancements

Future improvements may include:

* Deep Learning integration
* Federated Learning
* Blockchain-based security
* Reinforcement Learning for adaptive defense
* Cloud deployment
* Real packet sniffing using Scapy/Wireshark
* Kubernetes integration
* Advanced SIEM integration

---

# Research Contribution

This project contributes to cybersecurity research by:

* Combining Digital Twin and AI
* Improving anomaly detection adaptability
* Reducing computational cost
* Enhancing real-time threat response
* Supporting scalable cybersecurity architectures

---

# Conclusion

The Lightweight AI-Based Cybersecurity Digital Twin provides an intelligent and adaptive approach for modern cyber defense systems.

By integrating:

* Digital Twin Technology
* Machine Learning
* Dynamic Thresholding
* Automatic Node Isolation

The system enables:

* Faster threat detection
* Improved security response
* Better scalability
* Reduced resource consumption

This project demonstrates how lightweight AI systems can effectively secure modern networks and IoT environments in real time.

---

# Author

## Sumandeep Kaur

Computer Science Engineering Student
Chandigarh University

---

# License

This project is developed for academic and research purposes.
