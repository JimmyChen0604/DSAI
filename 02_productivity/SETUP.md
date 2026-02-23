# 🚀 Setup & Run Guide

This guide walks you through **installing dependencies**, **setting up API keys**, and **running** the NYT reporter software: the **Shiny app** (web UI for browsing popular articles) and **DataReport_NYT.py** (pipeline that fetches articles, extracts content, summarizes with Ollama, and generates a Word report with OpenAI).

---

## 📋 Quick overview

| Software | What it does | Where it lives |
|----------|--------------|-----------------|
| **Shiny app** | Web app to search and view NYT Most Popular articles (viewed/emailed/shared). | `02_productivity/shiny_app/` |
| **DataReport_NYT.py** | Fetches NYT articles → extracts full text (Zyte) → summarizes with Ollama → writes a trend report with OpenAI → saves `data_report.docx`. | Project root |

Both read API keys from a **single `.env` file** in the **project root** (the folder that contains `query_nyapi.py` and `DataReport_NYT.py`).

---

## 🔧 Step 1: Install dependencies

### For the Shiny app

From your project root:

```bash
cd 02_productivity/shiny_app
pip install -r requirements.txt
```

This installs: `shiny`, `pandas`, and `requests`.

### For DataReport_NYT.py

From your project root:

```bash
pip install requests pandas openai zyte-api python-docx
```

- **requests**, **pandas** — HTTP and data handling  
- **openai** — OpenAI API for report generation  
- **zyte-api** — Zyte API for full article text extraction  
- **python-docx** — Writing the Word report  

**Ollama (optional but used by default):** The script uses a local Ollama model (`newsanalyst:latest`) to summarize article content. If you don’t have Ollama, you’d need to change the script to skip or replace that step. To use it:

1. Install [Ollama](https://ollama.com/) and run it locally.
2. Create/use a model that returns JSON with a `key_insights` field (e.g. a custom model built from a Modelfile in this project).

---

## 🔑 Step 2: Set up API keys

Create a file named **`.env`** in the **project root** (same folder as `DataReport_NYT.py` and `query_nyapi.py`). Do **not** commit this file (it should be in `.gitignore`).

### Keys used by each piece of software

| Key | Used by | Where to get it |
|-----|---------|------------------|
| **TEST_API_KEY** | Shiny app, DataReport_NYT.py, query_nyapi.py | [NYT Developer](https://developer.nytimes.com/) — Most Popular API |
| **ZYTE_API_KEY** | DataReport_NYT.py only | [Zyte](https://www.zyte.com/) — for article extraction |
| **OPENAI_API_KEY** | DataReport_NYT.py only | [OpenAI](https://platform.openai.com/) — for report generation |

### Example `.env` file

Create `.env` in the project root with:

```env
# NYT Most Popular API (required for Shiny app and DataReport_NYT)
TEST_API_KEY=your_nyt_api_key_here

# Zyte – full article text extraction (required for DataReport_NYT)
ZYTE_API_KEY=your_zyte_api_key_here

# OpenAI – report generation (required for DataReport_NYT)
OPENAI_API_KEY=your_openai_api_key_here
```

Replace the placeholder values with your real keys. You can use comments (lines starting with `#`) and leave out keys you don’t need for the part you’re running:

- **Only running the Shiny app?** You only need `TEST_API_KEY`.
- **Running DataReport_NYT.py?** You need all three keys (and optionally Ollama).

---

## ▶️ Step 3: Run the software

### Run the Shiny app

1. Open a terminal.
2. Go to the Shiny app folder and start the app:

```bash
cd 02_productivity/shiny_app
python app.py
```

Or, if you use the Shiny CLI:

```bash
cd 02_productivity/shiny_app
shiny run app.py
```

3. Open a browser at **http://localhost:8080** (or the port shown in the terminal).
4. Use the sidebar to choose article type (Viewed/Emailed/Shared), period, number of articles, and date range, then click **Search**.

The app reads `TEST_API_KEY` from the **project root** `.env` (it looks three folders up from `shiny_app`).

### Run DataReport_NYT.py

1. Open a terminal.
2. Go to the **project root** (where `DataReport_NYT.py` and `.env` are):

```bash
cd path/to/DSAI
```

3. Run the script:

```bash
python DataReport_NYT.py
```

4. The script will:
   - Load `.env` from the current directory
   - Fetch NYT most-viewed articles (endpoint and count are set in `main()`)
   - Extract full article text via Zyte
   - Summarize with Ollama (if running and model is available)
   - Generate a trend report with OpenAI
   - Save **`data_report.docx`** in the same folder

Make sure **Ollama** is running locally if you use the default summarization step.

---

## ⚠️ Troubleshooting

| Problem | What to check |
|--------|----------------|
| **"TEST_API_KEY not found in .env"** | Create `.env` in the **project root** (not inside `shiny_app`). Add a line: `TEST_API_KEY=your_key`. |
| **Shiny app: "API key not found"** | The app expects `.env` at project root. Run the app after `cd 02_productivity/shiny_app`; it will look up from there. |
| **DataReport: "ZYTE_API_KEY" / "OPENAI_API_KEY" not found** | Add both keys to the same `.env` in the project root. |
| **Ollama errors or no summaries** | Install Ollama, start it, and ensure the script’s model name (e.g. `newsanalyst:latest`) exists. Or change the script to skip/use another summarization method. |
| **Import errors (e.g. `zyte_api`, `docx`)** | From project root run: `pip install zyte-api python-docx`. Use the same Python you use to run the script. |
| **Port 8080 already in use** | Set another port, e.g. `set PORT=8888` (Windows) or `export PORT=8888` (Mac/Linux), then run the Shiny app again. |

---

## 📁 Where things live

```
DSAI/
├── .env                    ← Create this: TEST_API_KEY, ZYTE_API_KEY, OPENAI_API_KEY
├── DataReport_NYT.py       ← Run from here: python DataReport_NYT.py
├── query_nyapi.py
├── data_report.docx        ← Created by DataReport_NYT.py
└── 02_productivity/
    └── shiny_app/
        ├── app.py          ← Run from here: python app.py
        ├── nyt_api.py
        └── requirements.txt
```

---

## 📝 Summary checklist

**Shiny app**

- [ ] `pip install -r requirements.txt` in `02_productivity/shiny_app`
- [ ] `.env` in **project root** with `TEST_API_KEY`
- [ ] `cd 02_productivity/shiny_app` then `python app.py`
- [ ] Open http://localhost:8080

**DataReport_NYT.py**

- [ ] `pip install requests pandas openai zyte-api python-docx`
- [ ] `.env` in **project root** with `TEST_API_KEY`, `ZYTE_API_KEY`, `OPENAI_API_KEY`
- [ ] Ollama installed and running (if using default summarization)
- [ ] From project root: `python DataReport_NYT.py`
- [ ] Report saved as `data_report.docx`

Once these are done, installation, API keys, and run steps are all set.
