from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.insert(0, 'agent')

from challenge_generator import ChallengeGenerator

# Try to import DataAnalyzer (requires pandas)
try:
    from data_analyzer import DataAnalyzer
    analyzer = DataAnalyzer()
    DATA_UPLOAD_ENABLED = True
except ImportError:
    analyzer = None
    DATA_UPLOAD_ENABLED = False

app = Flask(__name__)
CORS(app)

generator = ChallengeGenerator()

@app.route('/')
def home():
    """Serve the HTML interface with comparison and CSV upload."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Paradox Agent</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            
            .header {
                text-align: center;
                color: white;
                margin-bottom: 40px;
                padding: 40px 20px;
            }
            
            .header h1 {
                font-size: 3em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }
            
            .header p {
                font-size: 1.2em;
                opacity: 0.9;
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
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                padding: 40px;
                margin-bottom: 30px;
            }
            
            .upload-section {
                background: #f8f9fa;
                border: 2px dashed #ccc;
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 30px;
                text-align: center;
                opacity: 0.5;
            }
            
            .upload-section h3 {
                color: #999;
                margin-bottom: 15px;
                font-size: 1.3em;
            }
            
            .upload-section p {
                color: #999;
                margin-bottom: 20px;
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
                color: #333;
            }
            
            textarea {
                width: 100%;
                min-height: 150px;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 1em;
                font-family: inherit;
                resize: vertical;
                transition: border-color 0.3s;
            }
            
            textarea:focus {
                outline: none;
                border-color: #667eea;
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
            
            .examples {
                margin-top: 20px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
            }
            
            .examples h3 {
                margin-bottom: 10px;
                color: #333;
            }
            
            .example-btn {
                display: inline-block;
                margin: 5px;
                padding: 8px 15px;
                background: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                cursor: pointer;
                font-size: 0.9em;
                transition: all 0.2s;
            }
            
            .example-btn:hover {
                background: #667eea;
                color: white;
                border-color: #667eea;
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
                background: white;
                padding: 25px;
                border-radius: 15px;
                margin-bottom: 20px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .risk-comparison h3 {
                color: #333;
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
                background: white;
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 20px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                border-left: 5px solid #667eea;
            }
            
            .challenge-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid #f0f0f0;
            }
            
            .challenge-title {
                font-size: 1.5em;
                color: #333;
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
                color: #555;
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
                color: #555;
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
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            
            .summary h2 {
                color: #333;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔍 Data Paradox Agent</h1>
                <p>Challenge your analysis — detect fallacies before they cost you</p>
            </div>
            
            <div class="mode-toggle">
                <button class="mode-btn active" onclick="switchMode('single')">Single Analysis</button>
                <button class="mode-btn" onclick="switchMode('compare')">Compare Two Claims</button>
            </div>
            
            <div class="main-card">
                <div class="upload-section">
                    <h3>📊 CSV Upload (Currently Unavailable)</h3>
                    <p>CSV validation disabled in this deployment. Core fallacy detection still works!</p>
                </div>
                
                <div id="singleMode" class="single-mode">
                    <label for="claim">Paste Your Analytical Claim:</label>
                    <textarea 
                        id="claim" 
                        placeholder="Example: TikTok has ROAS of 9.54, highest in dataset. We should reallocate 60% of budget..."
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
                    <h3>📝 Try Examples:</h3>
                    <button class="example-btn" onclick="loadExample(1)">ROAS Reallocation</button>
                    <button class="example-btn" onclick="loadExample(2)">CTR-CPA Correlation</button>
                    <button class="example-btn" onclick="loadExample(3)">Platform Attribution</button>
                </div>
            </div>
            
            <div id="results"></div>
        </div>
        
        <script>
            const examples = {
                1: "Since campaigns with a ROAS above 4.0 represent our most efficient spend, we should immediately reallocate 30% of the budget from underperforming Brand campaigns (ROAS < 2.0) to these high-performers to maximize total profit.",
                2: "Our analysis shows that campaigns with a Click-Through Rate (CTR) above 5% consistently yield a 20% lower Cost Per Acquisition (CPA), suggesting that creative optimization is the primary lever for solving the Google Tax problem.",
                3: "Across the 1,800 campaigns, we found that YouTube and Display ads have a significantly higher ROAS than Search ads when using a 30-day view-through attribution window. Therefore, we should transition the majority of the Search budget to Video to avoid the high competition tax on Search."
            };
            
            let currentMode = 'single';
            
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
            
            function clearAll() {
                if (currentMode === 'single') {
                    document.getElementById('claim').value = '';
                } else {
                    document.getElementById('claimA').value = '';
                    document.getElementById('claimB').value = '';
                }
                document.getElementById('results').innerHTML = '';
            }
            
            async function analyzeClaim() {
                const claim = document.getElementById('claim').value.trim();
                
                if (!claim) {
                    alert('Please enter a claim to analyze!');
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
                        body: JSON.stringify({ claim: claim })
                    });
                    
                    const data = await response.json();
                    displayResults(data);
                } catch (error) {
                    resultsDiv.innerHTML = `<div class="main-card"><p style="color: red;">Error: ${error.message}</p></div>`;
                } finally {
                    analyzeBtn.disabled = false;
                }
            }
            
            async function compareClaimsFn() {
                const claimA = document.getElementById('claimA').value.trim();
                const claimB = document.getElementById('claimB').value.trim();
                
                if (!claimA || !claimB) {
                    alert('Please enter both claims to compare!');
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
                        body: JSON.stringify({ claim_a: claimA, claim_b: claimB })
                    });
                    
                    const data = await response.json();
                    displayComparisonResults(data);
                } catch (error) {
                    resultsDiv.innerHTML = `<div class="main-card"><p style="color: red;">Error: ${error.message}</p></div>`;
                } finally {
                    analyzeBtn.disabled = false;
                }
            }
            
            function displayResults(data) {
                const resultsDiv = document.getElementById('results');
                let html = '';
                
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
                                    <p style="color: #666;">${challenge.description}</p>
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
                                    <p style="color: #666;">${challenge.description}</p>
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
                                    <p style="color: #666;">${challenge.description}</p>
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
        return jsonify({'success': False, 'error': 'CSV upload not available in this deployment'}), 503
    
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
    
    if not claim:
        return jsonify({'error': 'No claim provided'}), 400
    
    response = generator.generate_challenges(claim)
    return jsonify(response)

@app.route('/api/compare', methods=['POST'])
def compare():
    """API endpoint to compare two claims."""
    data = request.get_json()
    claim_a = data.get('claim_a', '')
    claim_b = data.get('claim_b', '')
    
    if not claim_a or not claim_b:
        return jsonify({'error': 'Both claims required'}), 400
    
    comparison = generator.compare_claims(claim_a, claim_b)
    return jsonify(comparison)

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 DATA PARADOX AGENT - Web Interface")
    print("=" * 60)
    print("\n✅ Server starting...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("\n💡 Fallacy Detection & Comparison Enabled!")
    print("\n Press Ctrl+C to stop the server\n")
    print("=" * 60 + "\n")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)