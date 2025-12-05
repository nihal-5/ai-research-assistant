from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from pydantic import BaseModel
from pathlib import Path
import uvicorn
import asyncio
import json
from datetime import datetime
import os

app = FastAPI(title="AI Research Assistant")

class ResearchRequest(BaseModel):
    topic: str
    depth: str = "moderate"

class ResearchResponse(BaseModel):
    status: str
    report: str
    file_path: str = None
    error: str = None

async def research_stream(topic: str):
    try:
        yield f"data: {json.dumps({'status': 'starting', 'message': 'Initializing AI agents...'})}\n\n"
        await asyncio.sleep(0.5)
        
        yield f"data: {json.dumps({'status': 'research', 'agent': 'Research Agent', 'message': 'Gathering information on: ' + topic})}\n\n"
        await asyncio.sleep(1)
        
        yield f"data: {json.dumps({'status': 'analysis', 'agent': 'Analyst Agent', 'message': 'Analyzing and validating findings...'})}\n\n"
        await asyncio.sleep(1)
        
        yield f"data: {json.dumps({'status': 'writing', 'agent': 'Writer Agent', 'message': 'Creating professional report...'})}\n\n"
        await asyncio.sleep(1)
        
        from crew import ResearchCrew
        crew = ResearchCrew()
        result = crew.run(topic)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in topic)
        safe_topic = safe_topic.replace(' ', '_').lower()[:50]
        
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        file_path = output_dir / f"{safe_topic}_{timestamp}.md"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(result)
        
        yield f"data: {json.dumps({'status': 'complete', 'message': 'Report generated!', 'report': result, 'file_path': str(file_path)})}\n\n"
    
    except Exception as e:
        yield f"data: {json.dumps({'status': 'error', 'message': str(e)})}\n\n"

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content=get_default_html())

@app.get("/api/research/stream")
async def research_stream_endpoint(topic: str):
    return StreamingResponse(
        research_stream(topic),
        media_type="text/event-stream"
    )

@app.post("/api/research", response_model=ResearchResponse)
async def create_research(request: ResearchRequest):
    try:
        from crew import ResearchCrew
        crew = ResearchCrew()
        result = crew.run(request.topic)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in request.topic)
        safe_topic = safe_topic.replace(' ', '_').lower()[:50]
        
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        file_path = output_dir / f"{safe_topic}_{timestamp}.md"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(result)
        
        return ResearchResponse(
            status="success",
            report=result,
            file_path=str(file_path)
        )
    except Exception as e:
        return ResearchResponse(
            status="error",
            report="",
            error=str(e)
        )

@app.get("/api/reports")
async def list_reports():
    output_dir = Path("output")
    if not output_dir.exists():
        return {"reports": []}
    
    reports = []
    for file in sorted(output_dir.glob("*.md"), reverse=True):
        reports.append({
            "filename": file.name,
            "created": datetime.fromtimestamp(file.stat().st_mtime).isoformat(),
            "size": file.stat().st_size
        })
    return {"reports": reports}

@app.get("/api/reports/{filename}")
async def get_report(filename: str):
    file_path = Path("output") / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return {"content": content}

def get_default_html():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Research Assistant</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container { max-width: 1200px; margin: 0 auto; }
            .header {
                background: white;
                padding: 30px;
                border-radius: 12px;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                font-size: 2.5rem;
                margin-bottom: 10px;
            }
            .subtitle { color: #666; font-size: 1.1rem; }
            .main-content {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
            }
            .card {
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            .input-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: 500;
            }
            input, select, textarea {
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 1rem;
                transition: border 0.3s;
            }
            input:focus, select:focus, textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 14px 28px;
                border: none;
                border-radius: 8px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                width: 100%;
                transition: transform 0.2s;
            }
            button:hover { transform: translateY(-2px); }
            button:disabled {
                background: #ccc;
                cursor: not-allowed;
                transform: none;
            }
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
                color: #667eea;
            }
            .result {
                max-height: 600px;
                overflow-y: auto;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                white-space: pre-wrap;
                font-family: 'Courier New', monospace;
                font-size: 0.9rem;
                line-height: 1.6;
            }
            .reports-list {
                list-style: none;
            }
            .report-item {
                padding: 15px;
                border-bottom: 1px solid #e0e0e0;
                cursor: pointer;
                transition: background 0.2s;
            }
            .report-item:hover {
                background: #f8f9fa;
            }
            @media (max-width: 768px) {
                .main-content {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔍 AI Research Assistant</h1>
                <p class="subtitle">Multi-Agent research system powered by CrewAI</p>
            </div>
            
            <div class="main-content">
                <div class="card">
                    <h2>Create Research</h2>
                    <form id="researchForm">
                        <div class="input-group">
                            <label for="topic">Research Topic</label>
                            <input type="text" id="topic" placeholder="e.g., Latest developments in renewable energy" required>
                        </div>
                        <div class="input-group">
                            <label for="depth">Research Depth</label>
                            <select id="depth">
                                <option value="basic">Basic</option>
                                <option value="moderate" selected>Moderate</option>
                                <option value="comprehensive">Comprehensive</option>
                            </select>
                        </div>
                        <button type="submit" id="submitBtn">Generate Report</button>
                    </form>
                    <div class="loading" id="loading">
                        <p>🤖 Agents are working...</p>
                        <p style="font-size: 0.9rem; margin-top: 10px;">This may take 1-2 minutes</p>
                    </div>
                </div>
                
                <div class="card">
                    <h2>Research Result</h2>
                    <div class="result" id="result">
                        <p style="color: #999;">Results will appear here...</p>
                    </div>
                </div>
            </div>
            
            <div class="card" style="margin-top: 30px;">
                <h2>Recent Reports</h2>
                <ul class="reports-list" id="reportsList"></ul>
            </div>
        </div>
        
        <script>
            const form = document.getElementById('researchForm');
            const loading = document.getElementById('loading');
            const submitBtn = document.getElementById('submitBtn');
            const resultDiv = document.getElementById('result');
            
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const topic = document.getElementById('topic').value;
                
                loading.style.display = 'block';
                submitBtn.disabled = true;
                resultDiv.innerHTML = '<div style="color: #667eea; font-family: sans-serif;"><strong>Starting research...</strong></div>';
                
                const eventSource = new EventSource(`/api/research/stream?topic=${encodeURIComponent(topic)}`);
                
                eventSource.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    
                    if (data.status === 'starting') {
                        resultDiv.innerHTML = `<div style="color: #667eea;">🚀 ${data.message}</div>`;
                    }
                    else if (data.status === 'research') {
                        resultDiv.innerHTML += `<div style="color: #28a745; margin-top: 10px;">📚 <strong>${data.agent}:</strong> ${data.message}</div>`;
                    }
                    else if (data.status === 'analysis') {
                        resultDiv.innerHTML += `<div style="color: #ffc107; margin-top: 10px;">🔍 <strong>${data.agent}:</strong> ${data.message}</div>`;
                    }
                    else if (data.status === 'writing') {
                        resultDiv.innerHTML += `<div style="color: #17a2b8; margin-top: 10px;">✍️ <strong>${data.agent}:</strong> ${data.message}</div>`;
                    }
                    else if (data.status === 'complete') {
                        resultDiv.innerHTML = `<div style="color: #28a745; margin-bottom: 15px;">✅ ${data.message}</div><hr><pre style="white-space: pre-wrap; font-family: 'Courier New', monospace;">${data.report}</pre>`;
                        eventSource.close();
                        loading.style.display = 'none';
                        submitBtn.disabled = false;
                        loadReports();
                    }
                    else if (data.status === 'error') {
                        resultDiv.innerHTML = `<div style="color: #dc3545;">❌ Error: ${data.message}</div>`;
                        eventSource.close();
                        loading.style.display = 'none';
                        submitBtn.disabled = false;
                    }
                };
                
                eventSource.onerror = (error) => {
                    resultDiv.innerHTML = '<div style="color: #dc3545;">❌ Connection error. Please try again.</div>';
                    eventSource.close();
                    loading.style.display = 'none';
                    submitBtn.disabled = false;
                };
            });
            
            async function loadReports() {
                const response = await fetch('/api/reports');
                const data = await response.json();
                const list = document.getElementById('reportsList');
                list.innerHTML = data.reports.map(r => `
                    <li class="report-item" onclick="loadReport('${r.filename}')">
                        <strong>${r.filename}</strong><br>
                        <small>${new Date(r.created).toLocaleString()}</small>
                    </li>
                `).join('');
            }
            
            async function loadReport(filename) {
                const response = await fetch(`/api/reports/${filename}`);
                const data = await response.json();
                document.getElementById('result').textContent = data.content;
            }
            
            loadReports();
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
