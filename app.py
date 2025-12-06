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
        
        # Convert CrewOutput to string
        result_text = str(result)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in topic)
        safe_topic = safe_topic.replace(' ', '_').lower()[:50]
        
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        file_path = output_dir / f"{safe_topic}_{timestamp}.md"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(result_text)
        
        # Create workflow visualization data
        workflow = {
            "agents": [
                {
                    "name": "Research Agent",
                    "role": "Information Gathering",
                    "task": f"Searched and collected information about '{topic}' from credible sources",
                    "output": "Key facts, statistics, trends, examples, and source citations",
                    "icon": "📚"
                },
                {
                    "name": "Analyst Agent",
                    "role": "Data Synthesis & Validation",
                    "task": "Analyzed gathered information, validated accuracy, and identified patterns",
                    "output": "Synthesized insights, quality assessment, and key findings",
                    "icon": "🔍"
                },
                {
                    "name": "Writer Agent",
                    "role": "Report Creation",
                    "task": "Created professional report with clear structure and citations",
                    "output": "Final research report in markdown format",
                    "icon": "✍️"
                }
            ],
            "process": "Sequential collaboration: Research → Analysis → Writing"
        }
        
        yield f"data: {json.dumps({'status': 'complete', 'message': 'Report generated!', 'report': result_text, 'file_path': str(file_path), 'workflow': workflow})}\n\n"
    
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
        
        # Convert CrewOutput to string
        result_text = str(result)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in request.topic)
        safe_topic = safe_topic.replace(' ', '_').lower()[:50]
        
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        file_path = output_dir / f"{safe_topic}_{timestamp}.md"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(result_text)
        
        return ResearchResponse(
            status="success",
            report=result_text,
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
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #0f172a;
                min-height: 100vh;
                padding: 40px 20px;
                color: #e2e8f0;
                position: relative;
                overflow-x: hidden;
            }
            
            body::before {
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
                pointer-events: none;
                z-index: 0;
            }
            
            .container { 
                max-width: 1400px; 
                margin: 0 auto; 
                position: relative;
                z-index: 1;
            }
            
            .header {
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
                backdrop-filter: blur(20px);
                padding: 40px;
                border-radius: 24px;
                margin-bottom: 40px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 
                    0 20px 60px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
                animation: fadeInDown 0.6s ease-out;
            }
            
            @keyframes fadeInDown {
                from { opacity: 0; transform: translateY(-20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            h1 {
                background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 3rem;
                font-weight: 700;
                margin-bottom: 12px;
                letter-spacing: -0.02em;
            }
            
            .subtitle { 
                color: #94a3b8; 
                font-size: 1.1rem;
                font-weight: 400;
            }
            
            .main-content {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-bottom: 30px;
            }
            
            .card {
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
                backdrop-filter: blur(20px);
                padding: 32px;
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 
                    0 20px 60px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                animation: fadeIn 0.6s ease-out backwards;
            }
            
            .card:nth-child(1) { animation-delay: 0.1s; }
            .card:nth-child(2) { animation-delay: 0.2s; }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .card:hover {
                transform: translateY(-4px);
                box-shadow: 
                    0 30px 80px rgba(0, 0, 0, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
            }
            
            h2 {
                color: #f1f5f9;
                font-size: 1.5rem;
                margin-bottom: 24px;
                font-weight: 600;
            }
            
            .input-group {
                margin-bottom: 20px;
            }
            
            label {
                display: block;
                margin-bottom: 10px;
                color: #cbd5e1;
                font-weight: 500;
                font-size: 0.95rem;
            }
            
            input, select {
                width: 100%;
                padding: 14px 16px;
                background: rgba(15, 23, 42, 0.8);
                border: 2px solid rgba(148, 163, 184, 0.2);
                border-radius: 12px;
                font-size: 1rem;
                color: #e2e8f0;
                transition: all 0.3s ease;
                font-family: 'Inter', sans-serif;
            }
            
            input:focus, select:focus {
                outline: none;
                border-color: #60a5fa;
                box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.1);
                background: rgba(15, 23, 42, 1);
            }
            
            input::placeholder {
                color: #64748b;
            }
            
            button {
                background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                color: white;
                padding: 16px 28px;
                border: none;
                border-radius: 12px;
                font-size: 1.05rem;
                font-weight: 600;
                cursor: pointer;
                width: 100%;
                transition: all 0.3s ease;
                box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
                position: relative;
                overflow: hidden;
            }
            
            button::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
                transition: left 0.5s;
            }
            
            button:hover::before {
                left: 100%;
            }
            
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 30px rgba(59, 130, 246, 0.4);
            }
            
            button:active {
                transform: translateY(0);
            }
            
            button:disabled {
                background: linear-gradient(135deg, #475569 0%, #334155 100%);
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
            
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
                color: #60a5fa;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            .result {
                max-height: 600px;
                overflow-y: auto;
                padding: 24px;
                background: rgba(15, 23, 42, 0.6);
                border-radius: 12px;
                border: 1px solid rgba(148, 163, 184, 0.1);
                white-space: pre-wrap;
                font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
                font-size: 0.9rem;
                line-height: 1.7;
                color: #cbd5e1;
            }
            
            .result::-webkit-scrollbar {
                width: 8px;
            }
            
            .result::-webkit-scrollbar-track {
                background: rgba(15, 23, 42, 0.5);
                border-radius: 4px;
            }
            
            .result::-webkit-scrollbar-thumb {
                background: rgba(96, 165, 250, 0.3);
                border-radius: 4px;
            }
            
            .result::-webkit-scrollbar-thumb:hover {
                background: rgba(96, 165, 250, 0.5);
            }
            
            .reports-list {
                list-style: none;
            }
            
            .report-item {
                padding: 16px;
                border-bottom: 1px solid rgba(148, 163, 184, 0.1);
                cursor: pointer;
                transition: all 0.2s ease;
                border-radius: 8px;
                margin-bottom: 4px;
            }
            
            .report-item:hover {
                background: rgba(59, 130, 246, 0.1);
                border-color: rgba(96, 165, 250, 0.3);
                transform: translateX(4px);
            }
            
            .report-item strong {
                color: #f1f5f9;
                font-weight: 600;
            }
            
            .report-item small {
                color: #94a3b8;
            }
            
            @media (max-width: 968px) {
                .main-content {
                    grid-template-columns: 1fr;
                }
                h1 {
                    font-size: 2.2rem;
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
                        // Display report
                        resultDiv.innerHTML = `
                            <div style="color: #28a745; margin-bottom: 15px;">✅ ${data.message}</div>
                            <hr><pre style="white-space: pre-wrap; font-family: 'Courier New', monospace; max-height: 400px; overflow-y: auto;">${data.report}</pre>
                        `;
                        
                        // Display workflow visualization
                        if (data.workflow) {
                            const workflowHTML = `
                                <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
                                    <h3 style="margin-bottom: 15px; color: #333;">🔄 Research Workflow</h3>
                                    <p style="color: #666; margin-bottom: 20px;"><strong>Process:</strong> ${data.workflow.process}</p>
                                    ${data.workflow.agents.map((agent, index) => `
                                        <div style="margin-bottom: 20px; padding: 15px; background: white; border-left: 4px solid ${index === 0 ? '#28a745' : index === 1 ? '#ffc107' : '#17a2b8'}; border-radius: 4px;">
                                            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                                                <span style="font-size: 24px; margin-right: 10px;">${agent.icon}</span>
                                                <div>
                                                    <h4 style="margin: 0; color: #333;">${agent.name}</h4>
                                                    <p style="margin: 0; color: #666; font-size: 0.9rem;">${agent.role}</p>
                                                </div>
                                            </div>
                                            <p style="margin: 5px 0; color: #555;"><strong>Task:</strong> ${agent.task}</p>
                                            <p style="margin: 5px 0; color: #555;"><strong>Output:</strong> ${agent.output}</p>
                                        </div>
                                    `).join('')}
                                </div>
                            `;
                            resultDiv.innerHTML += workflowHTML;
                        }
                        
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
