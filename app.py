from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os

sys.path.insert(0, 'agent')

from challenge_generator import ChallengeGenerator

# Try to import DataAnalyzer (now uses Polars)
try:
    from data_analyzer import DataAnalyzer
    analyzer = DataAnalyzer()
    DATA_UPLOAD_ENABLED = True
except ImportError:
    analyzer = None
    DATA_UPLOAD_ENABLED = False

app = Flask(__name__, static_folder='static')
CORS(app)

generator = ChallengeGenerator()

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/')
def home():
    """Serve the HTML interface with comparison and CSV upload."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Paradox Agent - Challenge Your Marketing Analytics</title>
        <style>
            /* Theme Variables */
            :root {
                --bg-gradient-start: #667eea;
                --bg-gradient-end: #764ba2;
                --card-bg: white;
                --text-primary: #333;
                --text-secondary: #666;
                --border-color: #e0e0e0;
                --shadow: rgba(0,0,0,0.1);
                --input-bg: white;
                --upload-bg: #f8f9fa;
                --upload-border: #667eea;
            }

            [data-theme="dark"] {
                --bg-gradient-start: #1a1a2e;
                --bg-gradient-end: #16213e;
                --card-bg: #0f3460;
                --text-primary: #eee;
                --text-secondary: #bbb;
                --border-color: #2a2a40;
                --shadow: rgba(0,0,0,0.3);
                --input-bg: #1a2332;
                --upload-bg: #1a2332;
                --upload-border: #667eea;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            
            .theme-toggle {
                position: fixed;
                top: 20px;
                right: 20px;
                background: rgba(255,255,255,0.2);
                backdrop-filter: blur(10px);
                border: none;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                cursor: pointer;
                font-size: 1.5em;
                transition: all 0.3s;
                z-index: 1000;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .theme-toggle:hover {
                transform: scale(1.1);
                background: rgba(255,255,255,0.3);
            }
            
            .header {
                text-align: center;
                color: white;
                margin-bottom: 30px;
                padding: 40px 20px 20px 20px;
            }
            
            .header h1 {
                font-size: 3.5em;
                margin-bottom: 15px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                font-weight: 800;
            }
            
            .header .tagline {
                font-size: 1.4em;
                opacity: 0.95;
                margin-bottom: 25px;
                font-weight: 500;
            }
            
            .explainer {
                background: rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 20px 30px;
                margin: 0 auto 20px auto;
                max-width: 700px;
                color: white;
            }
            
            .explainer-list {
                list-style: none;
                padding: 0;
            }
            
            .explainer-list li {
                padding: 8px 0;
                padding-left: 30px;
                position: relative;
                font-size: 1.05em;
                line-height: 1.5;
            }
            
            .explainer-list li::before {
                content: '✓';
                position: absolute;
                left: 0;
                font-weight: bold;
                font-size: 1.3em;
                color: #4ade80;
            }
            
            .value-prop {
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 20px;
                margin: 15px auto 30px auto;
                max-width: 800px;
                color: white;
                line-height: 1.6;
                font-size: 1em;
                text-align: center;
            }
            
            .badges {
                display: flex;
                justify-content: center;
                gap: 15px;
                margin-top: 15px;
                flex-wrap: wrap;
            }
            
            .badge {
                background: white;
                color: #667eea;
                padding: 8px 15px;
                border-radius: 20px;
                font-weight: 600;
                font-size: 0.9em;
                text-decoration: none;
                transition: transform 0.2s;
            }
            
            .badge:hover {
                transform: translateY(-2px);
            }
            
            .demo-section {
                max-width: 900px;
                margin: 30px auto;
                background: var(--card-bg);
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 10px 30px var(--shadow);
            }
            
            .demo-section h3 {
                text-align: center;
                color: #667eea;
                margin-bottom: 15px;
            }
            
            .demo-section video {
                width: 100%;
                border-radius: 10px;
            }
            
            .how-it-works {
                max-width: 900px;
                margin: 20px auto;
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 25px;
                color: white;
            }
            
            .how-it-works h3 {
                text-align: center;
                margin-bottom: 20px;
                font-size: 1.4em;
            }
            
            .steps-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
            }
            
            .step {
                text-align: center;
            }
            
            .step-number {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .step-desc {
                opacity: 0.9;
                font-size: 0.9em;
            }
            
            .mode-toggle {
                display: flex;
                justify-content: center;
                gap: 10px;
                margin-bottom: 30px;
            }
            
            .mode-btn {
                padding: 12px 30px;
                background: white;
                border: none;
                border-radius: 25px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
                color: #667eea;
            }
            
            .mode-btn.active {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }
            
            .main-card {
                background: var(--card-bg);
                border-radius: 20px;
                box-shadow: 0 20px 60px var(--shadow);
                padding: 40px;
                margin-bottom: 30px;
            }
            
            .upload-section {
                background: var(--upload-bg);
                border: 2px dashed var(--upload-border);
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 30px;
                text-align: center;
                transition: all 0.3s;
                box-shadow: 0 5px 15px var(--shadow);
            }
            
            .upload-section:hover {
                border-color: #764ba2;
                transform: translateY(-2px);
                box-shadow: 0 8px 20px var(--shadow);
            }
            
            .upload-section h3 {
                color: var(--text-primary);
                margin-bottom: 15px;
                font-size: 1.3em;
            }
            
            .upload-section p {
                color: var(--text-secondary);
                margin-bottom: 20px;
            }
            
            .file-input-wrapper {
                position: relative;
                display: inline-block;
            }
            
            .file-input-wrapper input[type=file] {
                position: absolute;
                opacity: 0.01;
                width: 100%;
                height: 100%;
                cursor: pointer;
                z-index: 10;
                left: 0;
                top: 0;
            }
            
            .upload-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 40px;
                border-radius: 10px;
                font-weight: 600;
                font-size: 1.1em;
                cursor: pointer;
                display: inline-block;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            
            .upload-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            .data-summary {
                background: #e8f5e9;
                border-left: 4px solid #4caf50;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 10px;
                display: none;
                box-shadow: 0 3px 10px var(--shadow);
            }
            
            .data-summary.active {
                display: block;
            }
            
            .data-summary h4 {
                color: #2e7d32;
                margin-bottom: 10px;
            }
            
            .platform-stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 15px;
            }
            
            .platform-card {
                background: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 5px var(--shadow);
            }
            
            .platform-card h5 {
                color: #667eea;
                margin-bottom: 8px;
            }
            
            .platform-card p {
                color: #666;
                font-size: 0.9em;
                margin: 3px 0;
            }
            
            .comparison-grid {
                display: none;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }
            
            .comparison-grid.active {
                display: grid;
            }
            
            .claim-column {
                display: flex;
                flex-direction: column;
            }
            
            .claim-column h3 {
                color: #667eea;
                margin-bottom: 10px;
                text-align: center;
            }
            
            .single-mode {
                display: block;
            }
            
            .single-mode.hidden {
                display: none;
            }
            
            label {
                display: block;
                font-size: 1.1em;
                font-weight: 600;
                margin-bottom: 10px;
                color: var(--text-primary);
            }
            
            textarea {
                width: 100%;
                min-height: 150px;
                padding: 15px;
                border: 2px solid var(--border-color);
                border-radius: 10px;
                font-size: 1em;
                font-family: inherit;
                resize: vertical;
                transition: border-color 0.3s, box-shadow 0.3s;
                background: var(--input-bg);
                color: var(--text-primary);
            }
            
            textarea:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .button-container {
                display: flex;
                gap: 15px;
                margin-top: 20px;
            }
            
            button {
                flex: 1;
                padding: 15px 30px;
                font-size: 1.1em;
                font-weight: 600;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .analyze-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            
            .analyze-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            }
            
            .analyze-btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            
            .clear-btn {
                background: #f5f5f5;
                color: #666;
            }
            
            .clear-btn:hover {
                background: #e0e0e0;
            }
            
            [data-theme="dark"] .clear-btn {
                background: #2a2a40;
                color: #bbb;
            }
            
            [data-theme="dark"] .clear-btn:hover {
                background: #3a3a50;
            }
            
            .examples {
                margin-top: 30px;
                padding: 25px;
                background: var(--upload-bg);
                border-radius: 15px;
                box-shadow: 0 3px 10px var(--shadow);
            }
            
            .examples h3 {
                margin-bottom: 20px;
                color: var(--text-primary);
                text-align: center;
                font-size: 1.2em;
            }
            
            .examples-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 15px;
            }
            
            .example-card {
                background: var(--card-bg);
                border: 2px solid #667eea;
                border-radius: 12px;
                padding: 20px;
                cursor: pointer;
                transition: all 0.3s;
                box-shadow: 0 3px 10px var(--shadow);
            }
            
            .example-card:hover {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
            }
            
            .example-card:hover .example-icon {
                transform: scale(1.1);
            }
            
            .example-card:hover .example-title,
            .example-card:hover .example-desc {
                color: white;
            }
            
            .example-icon {
                font-size: 2em;
                margin-bottom: 10px;
                transition: transform 0.3s;
            }
            
            .example-title {
                font-weight: 700;
                font-size: 1.1em;
                margin-bottom: 8px;
                color: var(--text-primary);
            }
            
            .example-desc {
                font-size: 0.9em;
                color: var(--text-secondary);
                line-height: 1.4;
            }
            
            .verification-badge {
                display: inline-block;
                padding: 8px 15px;
                background: #e8f5e9;
                color: #2e7d32;
                border-radius: 5px;
                font-weight: 600;
                margin-bottom: 15px;
            }
            
            #results {
                margin-top: 30px;
            }
            
            .comparison-results {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-top: 20px;
            }
            
            .recommendation-banner {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 30px;
                text-align: center;
            }
            
            .recommendation-banner h2 {
                font-size: 2em;
                margin-bottom: 10px;
            }
            
            .recommendation-banner p {
                font-size: 1.2em;
                opacity: 0.95;
            }
            
            .risk-comparison {
                background: var(--card-bg);
                padding: 25px;
                border-radius: 15px;
                margin-bottom: 20px;
                box-shadow: 0 5px 15px var(--shadow);
            }
            
            .risk-comparison h3 {
                color: var(--text-primary);
                margin-bottom: 15px;
                text-align: center;
            }
            
            .risk-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }
            
            .risk-card {
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            
            .risk-card.winner {
                background: #e8f5e9;
                border: 2px solid #4caf50;
            }
            
            .risk-card.loser {
                background: #ffebee;
                border: 2px solid #ef5350;
            }
            
            .risk-card h4 {
                margin-bottom: 10px;
            }
            
            .risk-score {
                font-size: 2.5em;
                font-weight: bold;
                margin: 10px 0;
            }
            
            .risk-breakdown {
                font-size: 0.9em;
                color: #666;
            }
            
            .challenge-card {
                background: var(--card-bg);
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 20px;
                box-shadow: 0 5px 15px var(--shadow);
                border-left: 5px solid #667eea;
            }
            
            .challenge-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid var(--border-color);
            }
            
            .challenge-title {
                font-size: 1.5em;
                color: var(--text-primary);
                font-weight: 700;
            }
            
            .confidence-badge {
                padding: 8px 15px;
                border-radius: 20px;
                font-weight: 600;
                font-size: 0.9em;
            }
            
            .confidence-high {
                background: #fee;
                color: #c33;
            }
            
            .confidence-medium {
                background: #ffeaa7;
                color: #d63031;
            }
            
            .confidence-low {
                background: #dfe6e9;
                color: #636e72;
            }
            
            .section {
                margin: 20px 0;
            }
            
            .section-title {
                font-size: 1.1em;
                font-weight: 600;
                margin-bottom: 10px;
                color: var(--text-primary);
            }
            
            .section-title::before {
                content: '';
                display: inline-block;
                width: 4px;
                height: 20px;
                background: #667eea;
                margin-right: 10px;
                vertical-align: middle;
            }
            
            .challenge-list {
                list-style: none;
            }
            
            .challenge-list li {
                padding: 10px 0;
                padding-left: 25px;
                position: relative;
                line-height: 1.6;
                color: var(--text-secondary);
            }
            
            .challenge-list li::before {
                content: '•';
                position: absolute;
                left: 0;
                color: #667eea;
                font-size: 1.5em;
                line-height: 1;
            }
            
            .loading {
                text-align: center;
                padding: 40px;
                color: white;
                font-size: 1.2em;
            }
            
            .spinner {
                border: 4px solid rgba(255,255,255,0.3);
                border-top: 4px solid white;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 20px auto;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .summary {
                background: var(--upload-bg);
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            
            .summary h2 {
                color: var(--text-primary);
                margin-bottom: 10px;
            }
            
            .footer {
                text-align: center;
                color: white;
                padding: 30px 20px;
                margin-top: 50px;
                opacity: 0.9;
            }
            
            .footer a {
                color: white;
                text-decoration: none;
                font-weight: 600;
                border-bottom: 2px solid rgba(255,255,255,0.3);
            }
            
            .footer a:hover {
                border-bottom-color: white;
            }
            
            .toast {
                position: fixed;
                top: 20px;
                right: 80px;
                background: white;
                padding: 15px 25px;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.2);
                z-index: 1000;
                animation: slideIn 0.3s ease-out;
                max-width: 400px;
            }
            
            [data-theme="dark"] .toast {
                background: var(--card-bg);
                color: var(--text-primary);
            }
            
            .toast.error {
                border-left: 4px solid #ef5350;
            }
            
            .toast.success {
                border-left: 4px solid #4caf50;
            }
            
            .toast.info {
                border-left: 4px solid #2196F3;
            }
            
            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            /* Mobile Responsiveness */
            @media (max-width: 768px) {
                .header h1 {
                    font-size: 2.5em;
                }
                
                .comparison-grid {
                    grid-template-columns: 1fr;
                }
                
                .comparison-results {
                    grid-template-columns: 1fr;
                }
                
                .risk-grid {
                    grid-template-columns: 1fr;
                }
                
                .steps-grid {
                    grid-template-columns: 1fr;
                }
                
                .examples-grid {
                    grid-template-columns: 1fr;
                }
                
                .button-container {
                    flex-direction: column;
                }
                
                button {
                    width: 100%;
                }
                
                .theme-toggle {
                    top: 10px;
                    right: 10px;
                    width: 40px;
                    height: 40px;
                    font-size: 1.2em;
                }
            }
        </style>
    </head>
    <body>
        <button class="theme-toggle" onclick="toggleTheme()" id="themeToggle">🌙</button>
        
        <div class="container">
            <div class="header">
                <h1>🔍 Data Paradox Agent</h1>
                <p class="tagline">Challenge your marketing analytics — with your actual data</p>
                
                <div class="explainer">
                    <ul class="explainer-list">
                        <li>Upload CSV → Test claims → Get instant fallacy flags</li>
                        <li>Compare two strategies with risk scoring</li>
                        <li>No signup, no BS — built for performance marketers</li>
                    </ul>
                </div>
                
                <div class="value-prop">
                    <em>Most analytics tools confirm your bias. This one challenges it.</em>
                </div>
                
                <div class="badges">
                    <a href="https://github.com/AkpanDaniel/data-paradox-agent" target="_blank" class="badge">
                        ⭐ View on GitHub
                    </a>
                    <a href="https://github.com/AkpanDaniel/data-paradox-agent" target="_blank" class="badge">
                        📖 Read Documentation
                    </a>
                    <span class="badge">🚀 100% Free & Open Source</span>
                </div>
            </div>
            
            <div class="demo-section">
                <h3>📺 See It In Action (20 seconds)</h3>
                <video autoplay loop muted playsinline>
                    <source src="/static/0218.mp4" type="video/mp4">
                    Your browser doesn't support video.
                </video>
            </div>
            
            <div class="how-it-works">
                <h3>⚡ How It Works</h3>
                <div class="steps-grid">
                    <div class="step">
                        <div class="step-number">1️⃣</div>
                        <strong>Upload Your CSV</strong><br>
                        <span class="step-desc">Or try without data</span>
                    </div>
                    <div class="step">
                        <div class="step-number">2️⃣</div>
                        <strong>Make a Claim</strong><br>
                        <span class="step-desc">Or click an example</span>
                    </div>
                    <div class="step">
                        <div class="step-number">3️⃣</div>
                        <strong>Get Challenged</strong><br>
                        <span class="step-desc">See logical risks instantly</span>
                    </div>
                </div>
            </div>
            
            <div class="mode-toggle">
                <button class="mode-btn active" onclick="switchMode('single')">Single Analysis</button>
                <button class="mode-btn" onclick="switchMode('compare')">Compare Two Claims</button>
            </div>
            
            <div class="main-card">
                <div class="upload-section">
                    <h3>📊 Upload Your Dataset (Optional but Recommended)</h3>
                    <p>Best with: date, platform, spend, revenue, clicks, impressions, conversions</p>
                    <div class="file-input-wrapper">
                        <div class="upload-btn">📁 Choose CSV File</div>
                        <input type="file" id="csvFile" accept=".csv" onchange="handleFileUpload(event)">
                    </div>
                </div>
                
                <div id="dataSummary" class="data-summary">
                    <h4>✅ Dataset Loaded Successfully</h4>
                    <div id="summaryContent"></div>
                </div>
                
                <div id="singleMode" class="single-mode">
                    <label for="claim">Paste Your Analytical Claim:</label>
                    <textarea 
                        id="claim" 
                        placeholder="Example: TikTok has ROAS of 9.54, highest in my dataset. We should reallocate 60% of budget..."
                    ></textarea>
                    
                    <div class="button-container">
                        <button class="analyze-btn" onclick="analyzeClaim()">🚀 Analyze Claim</button>
                        <button class="clear-btn" onclick="clearAll()">🗑️ Clear</button>
                    </div>
                </div>
                
                <div id="compareMode" class="comparison-grid">
                    <div class="claim-column">
                        <h3>📝 Claim A</h3>
                        <textarea 
                            id="claimA" 
                            placeholder="First strategy or recommendation..."
                        ></textarea>
                    </div>
                    
                    <div class="claim-column">
                        <h3>📝 Claim B</h3>
                        <textarea 
                            id="claimB" 
                            placeholder="Alternative strategy or recommendation..."
                        ></textarea>
                    </div>
                    
                    <div style="grid-column: 1 / -1;">
                        <div class="button-container">
                            <button class="analyze-btn" onclick="compareClaimsFn()">⚖️ Compare Both Claims</button>
                            <button class="clear-btn" onclick="clearAll()">🗑️ Clear All</button>
                        </div>
                    </div>
                </div>
                
                <div class="examples">
                    <h3>📝 Try These Examples (Click to Auto-Analyze)</h3>
                    <div class="examples-grid">
                        <div class="example-card" onclick="loadExampleAndAnalyze(1)">
                            <div class="example-icon">🚀</div>
                            <div class="example-title">ROAS Reallocation</div>
                            <div class="example-desc">Shifting budget to highest-ROAS channel boosts total profit?</div>
                        </div>
                        
                        <div class="example-card" onclick="loadExampleAndAnalyze(2)">
                            <div class="example-icon">📈</div>
                            <div class="example-title">CTR-CPA Correlation</div>
                            <div class="example-desc">Higher CTR always means better CPA performance?</div>
                        </div>
                        
                        <div class="example-card" onclick="loadExampleAndAnalyze(3)">
                            <div class="example-icon">🎯</div>
                            <div class="example-title">Platform Attribution</div>
                            <div class="example-desc">View-through windows accurately show channel contribution?</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div id="results"></div>
            
            <div class="footer">
                Built with 💜 by <a href="https://github.com/AkpanDaniel" target="_blank">Akpan Daniel</a><br>
                © 2026 Data Paradox Agent | <a href="https://github.com/AkpanDaniel/data-paradox-agent" target="_blank">Open Source on GitHub</a>
            </div>
        </div>
        
        <script>
            const examples = {
                1: "Since campaigns with a ROAS above 4.0 represent our most efficient spend, we should immediately reallocate 30% of the budget from underperforming Brand campaigns (ROAS < 2.0) to these high-performers to maximize total profit.",
                2: "Our analysis shows that campaigns with a Click-Through Rate (CTR) above 5% consistently yield a 20% lower Cost Per Acquisition (CPA), suggesting that creative optimization is the primary lever for solving the Google Tax problem.",
                3: "Across the 1,800 campaigns, we found that YouTube and Display ads have a significantly higher ROAS than Search ads when using a 30-day view-through attribution window. Therefore, we should transition the majority of the Search budget to Video to avoid the high competition tax on Search."
            };
            
            let datasetLoaded = false;
            let currentMode = 'single';
            
            // Dark Mode Toggle
            function toggleTheme() {
                const html = document.documentElement;
                const currentTheme = html.getAttribute('data-theme');
                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                
                html.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
                
                document.getElementById('themeToggle').textContent = newTheme === 'dark' ? '☀️' : '🌙';
            }
            
            // Load saved theme on page load
            (function() {
                const savedTheme = localStorage.getItem('theme') || 'light';
                document.documentElement.setAttribute('data-theme', savedTheme);
                if (document.getElementById('themeToggle')) {
                    document.getElementById('themeToggle').textContent = savedTheme === 'dark' ? '☀️' : '🌙';
                }
            })();
            
            function showToast(message, type = 'info') {
                const toast = document.createElement('div');
                toast.className = `toast ${type}`;
                toast.textContent = message;
                document.body.appendChild(toast);
                
                setTimeout(() => {
                    toast.style.animation = 'slideIn 0.3s ease-out reverse';
                    setTimeout(() => toast.remove(), 300);
                }, 3000);
            }
            
            function switchMode(mode) {
                currentMode = mode;
                
                document.querySelectorAll('.mode-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                event.target.classList.add('active');
                
                const singleMode = document.getElementById('singleMode');
                const compareMode = document.getElementById('compareMode');
                
                if (mode === 'single') {
                    singleMode.classList.remove('hidden');
                    compareMode.classList.remove('active');
                } else {
                    singleMode.classList.add('hidden');
                    compareMode.classList.add('active');
                }
                
                document.getElementById('results').innerHTML = '';
            }
            
            function loadExample(num) {
                if (currentMode === 'single') {
                    document.getElementById('claim').value = examples[num];
                } else {
                    document.getElementById('claimA').value = examples[num];
                }
            }
            
            function loadExampleAndAnalyze(num) {
                loadExample(num);
                showToast('Example loaded! Analyzing...', 'info');
                setTimeout(() => analyzeClaim(), 100);
            }
            
            function clearAll() {
                if (currentMode === 'single') {
                    document.getElementById('claim').value = '';
                } else {
                    document.getElementById('claimA').value = '';
                    document.getElementById('claimB').value = '';
                }
                document.getElementById('results').innerHTML = '';
            }
            
            async function handleFileUpload(event) {
                const file = event.target.files[0];
                if (!file) return;
                
                if (!file.name.endsWith('.csv')) {
                    showToast('Please upload a CSV file', 'error');
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', file);
                
                const summaryDiv = document.getElementById('dataSummary');
                const summaryContent = document.getElementById('summaryContent');
                summaryDiv.classList.add('active');
                summaryContent.innerHTML = '<p>⏳ Loading and analyzing your data...</p>';
                
                try {
                    const response = await fetch('/api/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        datasetLoaded = true;
                        displayDataSummary(data);
                        showToast('Dataset loaded successfully!', 'success');
                    } else {
                        summaryContent.innerHTML = `<p style="color: red;">❌ ${data.error}</p>`;
                        showToast(data.error, 'error');
                    }
                } catch (error) {
                    summaryContent.innerHTML = `<p style="color: red;">❌ Error: ${error.message}</p>`;
                    showToast('Failed to upload file', 'error');
                }
            }
            
            function displayDataSummary(data) {
                const summaryContent = document.getElementById('summaryContent');
                
                let html = `
                    <p><strong>Rows:</strong> ${data.rows} campaigns</p>
                    <p><strong>Platforms:</strong> ${Object.keys(data.summary.by_platform).join(', ')}</p>
                    <div class="platform-stats">
                `;
                
                for (const [platform, stats] of Object.entries(data.summary.by_platform)) {
                    html += `
                        <div class="platform-card">
                            <h5>${platform}</h5>
                            <p><strong>${stats.count}</strong> campaigns</p>
                    `;
                    
                    if (stats.roas) html += `<p>ROAS: ${stats.roas.mean} avg</p>`;
                    if (stats.ctr) html += `<p>CTR: ${stats.ctr.mean}% avg</p>`;
                    if (stats.cpc) html += `<p>CPC: $${stats.cpc.mean} avg</p>`;
                    
                    html += `</div>`;
                }
                
                html += `</div>`;
                summaryContent.innerHTML = html;
            }
            
            async function analyzeClaim() {
                const claim = document.getElementById('claim').value.trim();
                
                if (!claim) {
                    showToast('Please paste a claim to analyze (or try an example above)', 'error');
                    return;
                }
                
                const resultsDiv = document.getElementById('results');
                resultsDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Analyzing...</div>';
                
                const analyzeBtn = document.querySelector('.analyze-btn');
                analyzeBtn.disabled = true;
                
                try {
                    const response = await fetch('/api/analyze', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ 
                            claim: claim,
                            validate_data: datasetLoaded
                        })
                    });
                    
                    const data = await response.json();
                    displayResults(data);
                    
                    if (!datasetLoaded) {
                        showToast('💡 Tip: Upload your CSV for data verification too!', 'info');
                    }
                } catch (error) {
                    resultsDiv.innerHTML = `<div class="main-card"><p style="color: red;">Error: ${error.message}</p></div>`;
                    showToast('Analysis failed. Please try again.', 'error');
                } finally {
                    analyzeBtn.disabled = false;
                }
            }
            
            async function compareClaimsFn() {
                const claimA = document.getElementById('claimA').value.trim();
                const claimB = document.getElementById('claimB').value.trim();
                
                if (!claimA || !claimB) {
                    showToast('Please enter both claims to compare', 'error');
                    return;
                }
                
                const resultsDiv = document.getElementById('results');
                resultsDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Comparing claims...</div>';
                
                const analyzeBtn = document.querySelector('.analyze-btn');
                analyzeBtn.disabled = true;
                
                try {
                    const response = await fetch('/api/compare', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ 
                            claim_a: claimA,
                            claim_b: claimB,
                            validate_data: datasetLoaded
                        })
                    });
                    
                    const data = await response.json();
                    displayComparisonResults(data);
                } catch (error) {
                    resultsDiv.innerHTML = `<div class="main-card"><p style="color: red;">Error: ${error.message}</p></div>`;
                    showToast('Comparison failed. Please try again.', 'error');
                } finally {
                    analyzeBtn.disabled = false;
                }
            }
            
            function displayResults(data) {
                const resultsDiv = document.getElementById('results');
                let html = '';
                
                if (data.data_verification && data.data_verification.verified) {
                    html += '<div class="main-card"><div class="verification-badge">✅ DATA VERIFIED</div>';
                    
                    for (const v of data.data_verification.verifications) {
                        if (v.type === 'metric_claim' && v.matching_platforms.length > 0) {
                            const match = v.matching_platforms[0];
                            html += `<p><strong>${v.metric.toUpperCase()}:</strong> You claimed ${v.claimed_value}. Found ${match.actual_value} ${match.match_type} for ${match.platform}. ✅</p>`;
                        }
                    }
                    html += '</div>';
                }
                
                if (data.status === 'no_issues') {
                    html += '<div class="main-card"><h2 style="color: #27ae60;">✅ No Obvious Issues</h2><p>' + data.message + '</p></div>';
                } else {
                    html += '<div class="summary"><h2>📊 Analysis Summary</h2><p><strong>Issues Found:</strong> ' + data.fallacies_detected + '</p></div>';
                    
                    data.challenges.forEach(challenge => {
                        html += `
                            <div class="challenge-card">
                                <div class="challenge-header">
                                    <div class="challenge-title">🚨 ${challenge.fallacy_name}</div>
                                    <div class="confidence-badge confidence-${challenge.confidence.toLowerCase()}">${challenge.confidence}</div>
                                </div>
                                <div class="section">
                                    <div class="section-title">📝 What This Means</div>
                                    <p style="color: var(--text-secondary);">${challenge.description}</p>
                                </div>
                                <div class="section">
                                    <div class="section-title">🟡 Constructive Questions</div>
                                    <ul class="challenge-list">${challenge.constructive_questions.map(q => '<li>' + q + '</li>').join('')}</ul>
                                </div>
                                <div class="section">
                                    <div class="section-title">🔴 Direct Challenges</div>
                                    <ul class="challenge-list">${challenge.direct_challenges.map(c => '<li>' + c + '</li>').join('')}</ul>
                                </div>
                                <div class="section">
                                    <div class="section-title">📊 Missing Data</div>
                                    <ul class="challenge-list">${challenge.missing_data.map(m => '<li>' + m + '</li>').join('')}</ul>
                                </div>
                                <div class="section">
                                    <div class="section-title">💡 Alternative Explanations</div>
                                    <ul class="challenge-list">${challenge.alternative_explanations.map(a => '<li>' + a + '</li>').join('')}</ul>
                                </div>
                            </div>
                        `;
                    });
                }
                
                resultsDiv.innerHTML = html;
                resultsDiv.scrollIntoView({ behavior: 'smooth' });
            }
            
            function displayComparisonResults(data) {
                const resultsDiv = document.getElementById('results');
                
                const rec = data.recommendation;
                let winnerText = rec.winner === 'claim_a' ? 'Claim A' : rec.winner === 'claim_b' ? 'Claim B' : 'Both Claims';
                
                let html = `
                    <div class="recommendation-banner">
                        <h2>🏆 Recommendation: ${winnerText}</h2>
                        <p>${rec.message}</p>
                        <p style="font-size: 1em; margin-top: 10px; opacity: 0.9;">${rec.reasoning}</p>
                    </div>
                    
                    <div class="risk-comparison">
                        <h3>⚖️ Risk Comparison</h3>
                        <div class="risk-grid">
                            <div class="risk-card ${rec.winner === 'claim_a' || rec.winner === 'both' ? 'winner' : 'loser'}">
                                <h4>Claim A</h4>
                                <div class="risk-score">${data.claim_a.risk_score.total}</div>
                                <div class="risk-breakdown">
                                    Risk Level: <strong>${data.claim_a.risk_score.level}</strong><br>
                                    HIGH: ${data.claim_a.risk_score.high} | 
                                    MEDIUM: ${data.claim_a.risk_score.medium} | 
                                    LOW: ${data.claim_a.risk_score.low}
                                </div>
                            </div>
                            
                            <div class="risk-card ${rec.winner === 'claim_b' || rec.winner === 'both' ? 'winner' : 'loser'}">
                                <h4>Claim B</h4>
                                <div class="risk-score">${data.claim_b.risk_score.total}</div>
                                <div class="risk-breakdown">
                                    Risk Level: <strong>${data.claim_b.risk_score.level}</strong><br>
                                    HIGH: ${data.claim_b.risk_score.high} | 
                                    MEDIUM: ${data.claim_b.risk_score.medium} | 
                                    LOW: ${data.claim_b.risk_score.low}
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <h2 style="color: white; margin: 30px 0 20px 0; text-align: center;">📋 Detailed Analysis</h2>
                    
                    <div class="comparison-results">
                        <div>
                            <h3 style="color: white; text-align: center; margin-bottom: 15px;">Claim A Analysis</h3>
                `;
                
                if (data.claim_a.analysis.status === 'no_issues') {
                    html += '<div class="challenge-card"><h3 style="color: #27ae60;">✅ No Issues Detected</h3></div>';
                } else {
                    data.claim_a.analysis.challenges.forEach(challenge => {
                        html += `
                            <div class="challenge-card">
                                <div class="challenge-header">
                                    <div class="challenge-title">${challenge.fallacy_name}</div>
                                    <div class="confidence-badge confidence-${challenge.confidence.toLowerCase()}">${challenge.confidence}</div>
                                </div>
                                <div class="section">
                                    <p style="color: var(--text-secondary);">${challenge.description}</p>
                                </div>
                            </div>
                        `;
                    });
                }
                
                html += '</div><div><h3 style="color: white; text-align: center; margin-bottom: 15px;">Claim B Analysis</h3>';
                
                if (data.claim_b.analysis.status === 'no_issues') {
                    html += '<div class="challenge-card"><h3 style="color: #27ae60;">✅ No Issues Detected</h3></div>';
                } else {
                    data.claim_b.analysis.challenges.forEach(challenge => {
                        html += `
                            <div class="challenge-card">
                                <div class="challenge-header">
                                    <div class="challenge-title">${challenge.fallacy_name}</div>
                                    <div class="confidence-badge confidence-${challenge.confidence.toLowerCase()}">${challenge.confidence}</div>
                                </div>
                                <div class="section">
                                    <p style="color: var(--text-secondary);">${challenge.description}</p>
                                </div>
                            </div>
                        `;
                    });
                }
                
                html += '</div></div>';
                
                resultsDiv.innerHTML = html;
                resultsDiv.scrollIntoView({ behavior: 'smooth' });
            }
        </script>
    </body>
    </html>
    """

@app.route('/api/upload', methods=['POST'])
def upload_csv():
    """Handle CSV file upload."""
    if not DATA_UPLOAD_ENABLED:
        return jsonify({'success': False, 'error': 'CSV upload not available'}), 503
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'success': False, 'error': 'File must be a CSV'}), 400
    
    csv_content = file.read()
    result = analyzer.load_csv(csv_content)
    
    return jsonify(result)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint to analyze claims."""
    data = request.get_json()
    claim = data.get('claim', '')
    validate_data = data.get('validate_data', False)
    
    if not claim:
        return jsonify({'error': 'No claim provided'}), 400
    
    response = generator.generate_challenges(claim)
    
    if validate_data and analyzer and analyzer.df is not None:
        validation = analyzer.validate_claim(claim)
        response['data_verification'] = validation
    
    return jsonify(response)

@app.route('/api/compare', methods=['POST'])
def compare():
    """API endpoint to compare two claims."""
    data = request.get_json()
    claim_a = data.get('claim_a', '')
    claim_b = data.get('claim_b', '')
    validate_data = data.get('validate_data', False)
    
    if not claim_a or not claim_b:
        return jsonify({'error': 'Both claims required'}), 400
    
    comparison = generator.compare_claims(claim_a, claim_b)
    
    if validate_data and analyzer and analyzer.df is not None:
        comparison['claim_a']['data_verification'] = analyzer.validate_claim(claim_a)
        comparison['claim_b']['data_verification'] = analyzer.validate_claim(claim_b)
    
    return jsonify(comparison)

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy', 'version': '1.0.0'}), 200

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 DATA PARADOX AGENT - Web Interface")
    print("=" * 60)
    print("\n✅ Server starting...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("\n💡 CSV Upload & Comparison Enabled!")
    print("\n Press Ctrl+C to stop the server\n")
    print("=" * 60 + "\n")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)