# 🚀 MuseOS: Autonomous Multimodal Personal & Web Execution Agent
### Nebius Token Factory & NVIDIA NIM Edition

[![Nebius AI Builders Program: Approved Builder](https://img.shields.io/badge/Nebius_AI_Builders_Program-Approved_Builder-7B2CBF?style=for-the-badge&logo=nebius&logoColor=white)](https://tokenfactory.nebius.com)
[![Devpost Hackathon](https://img.shields.io/badge/Devpost-Nebius_x_NVIDIA_Hackathon-003E54?style=for-the-badge&logo=devpost&logoColor=white)](https://nebiusglobalaihackathon.devpost.com/)
[![Live Demo](https://img.shields.io/badge/Live_Demo-HuggingFace_ZeroGPU-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/spaces/MuseOS-Labs/museos-nebius-agent)
[![Telegram Bot](https://img.shields.io/badge/Telegram_Bot-@museos__nebius__agent__bot-24A1DE?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/museos_nebius_agent_bot)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Built for the [Nebius x NVIDIA Global AI Hackathon 2026](https://nebiusglobalaihackathon.devpost.com/) — Track: Personal AI / Best Apps & Agents**

**MuseOS** is an always-on, voice-and-web autonomous execution agent powered by **NVIDIA Nemotron open-weight models** running on **Nebius Token Factory**, combined with **Tavily Live Web Search**, persistent SQLite memory, a **Burnout Shield** time-blocking engine, a **Skill Recorder (`SKILL.md`)**, native `.ics` mobile alarms, and one-click `Excel/CSV` reporting via a live **4-Tab Gradio Command Center** and **24/7 Telegram Voice Bridge**.

---

## 🌟 Key Features & Architecture

1. **NVIDIA Nemotron Inference on Nebius Token Factory (`main.py`):**
   * Connects directly to the OpenAI-compatible **Nebius Token Factory endpoint** (`https://api.tokenfactory.nebius.com/v1/chat/completions`).
   * Uses an intelligent multi-model router across NVIDIA's open models:
     * `nvidia/Nemotron-3-Ultra-550b-a55b` (Deep multi-step agent planning & research)
     * `nvidia/nemotron-3-super-120b-a12b` (High-throughput multi-agent orchestration)
     * `nvidia/Nemotron-3.5-Super-VL` (Multimodal vision understanding)
     * `nvidia/Nemotron-3_5-Lightning` (Low-latency real-time interactive loops)

2. **Live Web Grounding via Tavily API (`Best Use of Tavily` Bonus Integration):**
   * Makes runtime calls to `https://api.tavily.com/search` (`search_depth="advanced"`, `include_answer=True`) so the agent autonomously researches live prices, vendors, documentation, and facts before generating executive deliverables with direct source links.

3. **Always-On Personal AI with Persistent Memory & Burnout Shield (`database.py` & `main.py`):**
   * **SQLite Persistent Memory (`agent_memory.db`):** Tracks multi-day conversation history, scheduled tasks, daily habits (`/habits`), and 7-day completion analytics (`/weekly`).
   * **Burnout Shield (`detect_burnout_or_deadline`):** Automatically detects overwork requests (>6 hours continuous work) and splits large deadlines into healthy 3-day deep-work roadmaps.

4. **Reusable Skill Recorder (`SKILL.md` Generator):**
   * Inspired by `microsoft/skill-recorder`, users can teach MuseOS any recurring workflow once via the Web UI or `/teach` command on Telegram, converting raw steps into a structured, reusable `.SKILL.md` automation file.

5. **One-Click Excel Exports & Native `.ics` Phone Alarms (`app.py`):**
   * Generates UTF-8 BOM `.csv` / Excel spreadsheets and RFC-5545 `.ics` calendar alarms (`VALARM`) directly from scheduled or executed tasks.

---

## 🛠️ Setup & Run Instructions

### 1. Clone the Repository & Install Dependencies
```bash
git clone https://github.com/ibrahimadel-ai/museos-nebius-agent.git
cd museos-nebius-agent
pip install -r requirements.txt
```

### 2. Configure Environment Variables (`Secrets` / `.env`)
Set the following environment variables (in Hugging Face `Settings -> Variables and secrets` or in a local `.env` file):
```bash
NEBIUS_API_KEY=your_nebius_token_factory_api_key
NEBIUS_BASE_URL=https://api.tokenfactory.nebius.com/v1
TAVILY_API_KEY=your_tavily_api_key
GEMINI_API_KEY=your_optional_groq_fallback_key
TELEGRAM_BOT_TOKEN=your_optional_dedicated_telegram_bot_token
```

### 3. Run the Application
```bash
python app.py
```
The **MuseOS 4-Tab Gradio Command Center** will launch at `http://0.0.0.0:7860`.

---

## 🌟 Acknowledgements & Open-Source Credits
* [**NVIDIA Nemotron**](https://huggingface.co/nvidia): For open-weights reasoning and instruction-tuned foundation models.
* [**Nebius Token Factory**](https://tokenfactory.nebius.com): For high-throughput, ultra-low latency serverless LLM infrastructure.
* [**Groq LPUs**](https://groq.com): For ultra-fast LPU inference acceleration and multi-model failover routing.
* [**OpenAI Whisper**](https://github.com/openai/whisper): For state-of-the-art voice transcription and audio processing.
* [**Tavily AI**](https://tavily.com): For real-time web search, grounding, and factual verification capabilities.
* [**Gradio**](https://gradio.app) & [**python-telegram-bot**](https://python-telegram-bot.org): For powering the web diagnostics control room and responsive mobile gateway.

---

## 📄 License
This project is licensed under the **MIT License**.