from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os
import base64
import json

from dotenv import load_dotenv
from groq import Groq

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

groq_api_key = os.getenv("GROQ_API_KEY")



@app.get("/analyze")
def analyze(repo_url: str):
   cleaned = repo_url.replace("https://github.com/", "")
   cleaned = cleaned.strip("/")
   parts = cleaned.split("/")
   owner = parts[0]
   repo = parts[1]
   print("Owner:", owner)
   print("Repo:", repo)
   
   
   import requests
   headers = {"Authorization": f"token {github_token}"}
   repo_info_url = f"https://api.github.com/repos/{owner}/{repo}"
   repo_info = requests.get(repo_info_url, headers =headers).json()
   if "default_branch" not in repo_info:
       return {"error": "Repository not found or is private. Check the URL and try again."}
   default_branch = repo_info["default_branch"]
   print("Default branch:", default_branch)
   tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
   tree_data = requests.get(tree_url, headers=headers).json()
   print("Total items found:", len(tree_data["tree"]))
   
   
   
   noisy_folders = ["node_modules", ".git", "venv", "__pycache__", "dist", "build"]
   noisy_extensions = [".png", ".jpg", ".jpeg", ".svg", ".ico", ".lock", ".min.js"]
   clean_files = []
   for item in tree_data["tree"]:
       if item["type"] != "blob":
           continue
       if any(folder in item["path"] for folder in noisy_folders):
           continue
       if any(item["path"].endswith(ext) for ext in noisy_extensions):
           continue
       clean_files.append(item["path"])
   print("Clean files found:", len(clean_files))
   for f in clean_files:
       print(f)
       
       
       
   signal_filenames = ["README.md", "package.json", "requirements.txt", "pom.xml", "main.py", "app.py", "index.js", "index.ts", "App.jsx", "App.tsx", "Cargo.toml", "go.mod", "index.html"]
   
   signal_files = []
   
   for path in clean_files:
       filename = path.split("/")[-1]
       if filename in signal_filenames:
           signal_files.append(path)
   
   print("Signal files found:", signal_files)
   
   file_contents = {}
   
   for path in signal_files:
       content_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"    
           
       response = requests.get(content_url, headers=headers).json()
   
       encoded_content = response["content"]
       decoded_content = base64.b64decode(encoded_content).decode("utf-8")
       file_contents[path] = decoded_content
   
   for path, content in file_contents.items():
       print(f"--- {path} ---")
       print(content[:200])
       print()
       
   combined_content = ""
   max_total_chars = 8000
   for path, content in file_contents.items():
    if len(combined_content) >= max_total_chars:
        break
    truncated = content[:1500]
    combined_content += f"\n--- FILE: {path} ---\n{truncated}\n"
   combined_content = combined_content[:max_total_chars]
   
   prompt = f"""
   You are analyzing a codebase to help a new developer understand it.
   
   Repository: {owner}/{repo}
   
   Here are the key files from this repository:
   {combined_content}
   
   Respond ONLY with valid JSON (no markdown, no code fences, no extra text) in exactly this structure:
   
   {{
     "summary": "short paragraph describing what this project does",
     "tech_stack": [
       {{"layer": "Frontend", "technology": "...", "notes": "..."}}
     ],
     "reading_order": [
       {{"order": 1, "file": "...", "why_it_matters": "..."}}
     ],
     "setup_instructions": ["step 1", "step 2"]
   }}
   """
   try:
       client = Groq(api_key=groq_api_key)
       response = client.chat.completions.create(
           model="openai/gpt-oss-120b",
           messages=[{"role": "user", "content": prompt}]
       )
   except Exception as e:
       return {"error": f"AI analysis failed: {str(e)}"}
   
   
   raw_output = response.choices[0].message.content
   parsed = json.loads(raw_output)
   
   with open("output.json", "w") as f:
       json.dump(parsed, f, indent=2)
   print("Saved to output.json")    
   return parsed    