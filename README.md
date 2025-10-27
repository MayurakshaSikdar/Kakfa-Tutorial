<p align="center">
    <img src="https://svn.apache.org/repos/asf/kafka/site/logos/originals/png/WIDE%20-%20White%20on%20Transparent.png" align="center" width="40%">
    <img src="https://d2mkz4zdclmlek.cloudfront.net/blog/wp-content/uploads/2023/05/postgresql_original_wordmark_logo_icon_146392.png" align="center" width="20%">
</p>
<p align="center">
	<em><code>❯ Real-Time Financial Transaction Monitoring System</code></em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/MayurakshaSikdar/Kakfa-Tutorial?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/MayurakshaSikdar/Kakfa-Tutorial?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/MayurakshaSikdar/Kakfa-Tutorial?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/MayurakshaSikdar/Kakfa-Tutorial?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<br>

# ⚡ Real-Time Financial Transaction Monitoring System

A **Kafka + KRaft-based real-time streaming system** for simulating financial transactions, detecting fraud, and storing results in PostgreSQL.  
Built using **Confluent Kafka (no Zookeeper)**, **async PostgreSQL**, and **Python producers/consumers**.

---

## About the Author

### **Mayuraksha Sikdar**  
*AI & Data Engineer | AWS & GCP Certified | HackerRank 5-Star | Python API-Backend Developer | ETL Glue Spark Developer | GEN-AI Enabler | DevOps | Docker/Kubernetes | CI/CD | Apache Airflow*

- 📧 **Email:** mayurakshasikdar@gmail.com  |  adataguy.in@gmail.com
- 📱 **Phone:** +353 0894370260  |  +91 8100132483
- 📍 **Location:** Dublin, Ireland  |  ✈ India
- 🌐 **Website:** <a href="https://adataguy.in/" target="_blank">A Data Guy</a>
- 🔗 **Profiles:** <a href="https://www.linkedin.com/in/mayuraksha-sikdar/" target="_blank">LinkedIn</a> | <a href="https://github.com/MayurakshaSikdar" target="_blank">GitHub</a> | <a href="https://medium.com/@mayurakshasikdar" target="_blank">Medium</a> | <a href="https://topmate.io/mayuraksha_sikdar" target="_blank">Topmate</a>


---


## 🧩 Project Overview

This project simulates a real-time financial transaction pipeline similar to what a bank (e.g., JPMorgan, Goldman Sachs, SBI) might use to detect fraudulent activity.  
It features:

- 🧠 **Kafka with KRaft Mode** (no Zookeeper dependency)  
- 🧾 **Producer** generating random transactions with Faker  
- 🚦 **Consumer** performing async fraud detection and batch inserts into Postgres  
- 🧍 **Kafka UI** for topic and message inspection  
- 💾 **Postgres** for persistent transaction storage

> ⚡️ Note: `confluent_kafka` automatically creates the topic if it doesn't exist  
> (as long as `auto.create.topics.enable=true` in Kafka broker, which is default).

---

## 🗂️ Project Structure

```txt
Kafka-Tutorial
├── config/
│   └── config.json
├── db/
│   └── init.sql
├── producer/
│   └── app.py
├── consumer/
│   └── app.py
├── pgdata/         # Local Postgres data (persistent)
├── docker-compose.yml
├── .env
└── README.md
```

---

## 🚀 Quick Start

### 1️⃣ Start Services

```bash
docker-compose up -d --build
```

This will spin up:
- **Kafka** (KRaft mode)
- **Kafka UI** → [http://localhost:8080](http://localhost:8080)
- **Postgres** on port `5432`

---

### 2️⃣ Create Kafka Topic (optional)

Inside the Kafka container:

```bash
docker exec -it kafka bash
kafka-topics.sh --create --topic transactions --bootstrap-server kafka:9093
```

Verify the topic:

```bash
kafka-topics.sh --list --bootstrap-server kafka:9093
```

---

### 3️⃣ Run Producer

```bash
python producer/app.py
```

Produces random transactions every 5 seconds.

---

### 4️⃣ Run Consumer

```bash
python consumer/app.py
```

🆘 Consumes messages, flags fraud (amount > 3000), and stores results in Postgres.

---

### 5️⃣ View Data

**Option 1:** Via `psql`
```bash
docker exec -it postgres psql -U kafka -d transactions
SELECT * FROM transactions;
```

**Option 2:** Using Kafka UI  
👉 [http://localhost:8080](http://localhost:8080)

---

## 🧮 Environment Variables

| Variable | Description | Example |
|-----------|-------------|----------|
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap server | `kafka:9092` |
| `TOPIC` | Kafka topic name | `transactions` |
| `POSTGRES_DSN` | Postgres connection string | `postgresql://kafka:12345@localhost:5432/transactions` |
| `TIMER` | Delay (seconds) between produced messages | `5` |

---

## ⚙️ Tech Stack

- **Apache Kafka (Native KRaft)** – Event streaming backbone  
- **Confluent Kafka Python Client** – Producer & Consumer SDK  
- **PostgreSQL 15** – Transaction storage  
- **AsyncPG + SQLAlchemy** – Async data ingestion  
- **Docker Compose** – Orchestration  
- **Kafka UI** – Topic monitoring

---

## 🔍 Fraud Logic

Simple rule-based check:

```python
is_fraud = amount > 3000.0
```

💡 You can extend this with ML-based anomaly detection later.

---

## 🧹 Clean Up

To stop and remove everything:

```bash
docker-compose down -v
```

---

### ✅ Summary

| Component | Role |
|------------|------|
| **Producer** | Publishes fake transaction data |
| **Consumer** | Detects fraud & saves to Postgres |
| **Kafka (KRaft)** | Message broker without Zookeeper |
| **Postgres** | Persistent transaction store |
| **Kafka UI** | Visual inspection and debugging |

---

🧠 *Fast, containerized, and KRaft-enabled real-time transaction pipeline for financial event streaming.*
