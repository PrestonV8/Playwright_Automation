from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
import os
import subprocess
import threading
from datetime import datetime

app = FastAPI()

# simple in-memory run tracking (MVP)
RUNS = {}

def run_job(run_id: str, env: str, suite: str):
    RUNS[run_id]["status"] = "RUNNING"

    cmd = f'python run_playwright.py --env {env} --suite "{suite}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    RUNS[run_id]["stdout"] = result.stdout
    RUNS[run_id]["stderr"] = result.stderr
    RUNS[run_id]["exit code"] = result.returncode
    RUNS[run_id]["status"] = "PASSED" if result.returncode ==0 else "FAILED"



@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <body style="font-family: Arial; max-width: 760px; margin: 40px auto;">
        <h2>Playwright Runner</h2>
        <p>Click to run the smoke suite.</p>

        <label>Environment:</label>
        <select id="env">
          <option value="staging" selected>staging</option>
          <option value="qa">qa</option>
          <option value="prod">prod</option>
        </select>

        <label style="margin-left:10px;">Suite:</label>
        <input id="suite" value="smoke" />

        <button style="margin-left:10px;" onclick="startRun()">Run</button>

        <pre id="out" style="margin-top:16px; background:#f5f5f5; padding:12px;"></pre>

        <script>
          async function startRun() {
            const env = document.getElementById("env").value;
            const suite = document.getElementById("suite").value;

            document.getElementById("out").textContent = "Starting...";

            const res = await fetch("/runs", {
              method: "POST",
              headers: {"Content-Type":"application/json"},
              body: JSON.stringify({ env, suite })
            });

            const data = await res.json();
            document.getElementById("out").textContent =
              "Run started!\\nrun_id=" + data.run_id + "\\nOpening status page...";

            // Go to the live status page
            window.location.href = "/ui/runs/" + data.run_id;
          }
        </script>
      </body>
    </html>
    """




@app.post("/runs")
def create_run(payload: dict):
    env = payload.get("env", "staging")
    suite = payload.get("suite", "smoke")

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = f"reports/{env}/{run_id}"

    RUNS[run_id] = {"status": "QUEUED", 
                    "env": env, 
                    "suite": suite,
                    "report_dir": report_dir}

    t = threading.Thread(target=run_job, args=(run_id, env, suite), daemon=True)
    t.start()

    return {"run_id": run_id, "status": "QUEUED", "env": env, "suite": suite}


@app.get("/runs/{run_id}")
def get_run(run_id: str):
    if run_id not in RUNS:
        return JSONResponse({"error": "run_id not found"}, status_code=404)
    return RUNS[run_id]



@app.get("/ui/runs/{run_id}", response_class=HTMLResponse)
def run_details_ui(run_id: str):
    return f"""
    <html>
      <body style="font-family: Arial; max-width: 900px; margin: 40px auto;">
        <h2>Run Details</h2>
        <div><b>Run ID:</b> {run_id}</div>
        <div><b>Status:</b> <span id="status">Loading...</span></div>
        <pre id="logs" style="background:#f5f5f5; padding:12px; white-space:pre-wrap;"></pre>

        <script>
          async function refresh() {{
            const res = await fetch("/runs/{run_id}");
            if (res.status === 404) {{
              document.getElementById("status").textContent = "Waiting for run to register...";
              return;
            }}
            const data = await res.json();
            document.getElementById("status").textContent = data.status;
            document.getElementById("logs").textContent = ((data.stdout||"") + "\\n" + (data.stderr||"")).trim();
          }}
          refresh();
          setInterval(refresh, 1000);
        </script>
      </body>
    </html>
    """




from fastapi.staticfiles import StaticFiles

# Serve the reports folder at /reports/
app.mount("/reports", StaticFiles(directory="reports"), name="reports")