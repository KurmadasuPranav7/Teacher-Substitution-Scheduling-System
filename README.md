# 📚 Teacher Substitution Scheduling System

An intelligent scheduling system that automates teacher substitution in educational institutions using constraint-based optimization and fairness-aware allocation.

---

## 🚀 Features

- ⚙️ Constraint-based scheduling engine
- ⚖️ Fair workload distribution using historical substitution counts
- 📊 Multi-factor scoring (subject, class, availability, workload)
- 🔍 Explainable assignment decisions
- 🌐 REST API built with FastAPI
- 🖥️ Interactive UI using Streamlit

---

## 🧠 How It Works

1. Parse teacher timetables into structured JSON
2. Build availability map (day → period → teachers)
3. Identify classes requiring substitution
4. Score candidate teachers based on:
   - Same class
   - Same subject
   - Grade match
   - Daily load
   - Yearly fairness (`sub_counter`)
5. Assign best teacher (greedy approach)
6. Persist updated workload

---

## 🏗️ Tech Stack

- Python
- FastAPI
- Streamlit
- JSON (data storage)

---

## ▶️ Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
