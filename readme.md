# Codebase Onboarder
 
Paste any public GitHub repo URL and get an instant, AI-generated onboarding guide — a plain-language summary, tech stack breakdown, suggested reading order, and setup instructions. Built to make jumping into an unfamiliar codebase faster for new developers.
 
**Live demo:** https://codebaseonboarder.netlify.app
 
## How it works
 
1. **Repo ingestion** — fetches the full file tree of a public GitHub repository via the GitHub REST API
2. **Signal file detection** — identifies the files that actually explain the project (README, entry points, dependency manifests like `package.json` / `requirements.txt`)
3. **Content extraction** — pulls the contents of those signal files
4. **AI analysis** — sends the extracted content to an LLM (Groq, running `openai/gpt-oss-120b`), which returns a structured breakdown of the project
5. **Dashboard rendering** — displays the result as an interactive, readable page instead of a wall of text
## Tech stack
 
| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Repo access | GitHub REST API |
| AI analysis | Groq API |
| Frontend | HTML, CSS, JavaScript |
| Backend hosting | Render |
| Frontend hosting | Netlify |
 
## Features
 
- Live URL input — analyze any public GitHub repo on demand
- Structured output: project summary, tech stack table, numbered reading order with expandable explanations, and setup instructions
- Graceful error handling for invalid URLs, private/missing repos, and oversized repos that exceed AI token limits
- Clean, dark, card-based UI
 
## Project structure
 
```
codebase-onboarder/
├── main.py                 # FastAPI backend — repo parsing, AI analysis, /analyze endpoint
├── index.html               # Frontend dashboard
├── dashboard-style.css      # Dashboard styling
├── requirements.txt
├── Procfile                 # Render deployment config
└── .env                     # API keys (not committed)
```
 
## Author
 
**Rudra Narayan Paliwal**
B.Tech, AI DS — USAR, GGSIPU EDC
[GitHub](https://github.com/rudrapaliwal-1) · [LinkedIn](https://linkedin.com/in/rudra-narayan-paliwal)
 
