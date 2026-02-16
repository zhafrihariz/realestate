# 🏙️ Agentic AI Real Estate Strategist (Malaysia)

A multi-agent feasibility engine that analyzes land development potential in Malaysia using **CrewAI**, **Streamlit**, and **Local LLMs (Ollama)**. This project transforms raw site parameters—location, acreage, and budget—into a structured investment proposal.

## 🚀 Overview
This system utilizes a "Crew" of AI agents to perform urban research and financial modeling. It features an interactive map interface with satellite view capabilities to help developers visualize the 5km demographic catchment area.

[Image of a multi-agent AI system architecture showing Researcher and Strategist agents collaborating]

## 🛠️ Tech Stack
- **Framework:** CrewAI (Agentic Orchestration)
- **Frontend:** Streamlit
- **LLM:** Llama 3.2 (1B/3B) via Ollama
- **Mapping:** Folium & OpenStreetMap (ESRI Satellite Tiles)
- **Geocoding:** GeoPy (Nominatim)

## 🏗️ Agent Architecture
The system employs a sequential process where data flows from research to strategy:

1. **Market Specialist:** Analyzes the location for commercial clusters and service gaps.
2. **Lead Strategist:** Synthesizes land size, budget, and market data to propose a specific building type and ROI logic.

[Image of a sequential workflow diagram for AI agents passing data from research to strategy]

## 📥 Installation & Setup

### 1. Prerequisites
Ensure you have [Ollama](https://ollama.com/) installed and the model downloaded:
```bash
ollama run llama3.2:1b
```
### 2.Clone this repo

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the Dashboard
```bash
streamlit run app.py
```
🗺️ Key Features
Interactive Map: Click-to-select site coordinates with a 5km radius circle.

Satellite Toggle: Switch between street maps and satellite imagery to inspect terrain.

Financial Safety Net: Handles local LLM output errors to ensure the UI stays stable.

PDF Export: Generate a professional feasibility report for stakeholders.

📝 Future Roadmap
[ ] Integration of Deep Learning Object Detection for tree crown analysis (PhD Research).

[ ] Real-time web search for latest population growth data.

[ ] Multi-plot comparison tools.

🎓 Author
Ahmad Zhafri PhD Researcher | Lecturer at UniKL MIIT

Focus: Deep Learning, Computer Vision, & AI-driven Urban Planning.
