from flask import Flask, render_template_string, request, jsonify
import numpy as np
import json
from scipy import stats
from scipy.stats import gaussian_kde
import logging

# Suppress werkzeug logs for cleaner output
logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__)

# Simulation configuration
WEIGHTS = {
    'Jurisdiction': 0.40,
    'Causation': 0.30,
    'Evidence': 0.10,
    'Precedent': 0.15,
    'Damages_Credibility': 0.05
}

TRIBUNAL_MULTIPLIERS = {
    'Pro-Investor': 1.10,
    'Neutral': 1.00,
    'Pro-State': 0.90
}

def run_monte_carlo_simulation(jurisdiction, causation, evidence, precedent, damages, tribunal_stance, iterations=5000):
    """Run Monte Carlo simulation with given parameters"""
    results = []
    
    for _ in range(iterations):
        # Generate random scores with uncertainty (std dev = 15)
        jurisdiction_score = np.clip(np.random.normal(jurisdiction, 15), 0, 100)
        causation_score = np.clip(np.random.normal(causation, 15), 0, 100)
        evidence_score = np.clip(np.random.normal(evidence, 15), 0, 100)
        precedent_score = np.clip(np.random.normal(precedent, 15), 0, 100)
        damages_score = np.clip(np.random.normal(damages, 15), 0, 100)
        
        # Calculate weighted score
        weighted_score = (
            jurisdiction_score * WEIGHTS['Jurisdiction'] +
            causation_score * WEIGHTS['Causation'] +
            evidence_score * WEIGHTS['Evidence'] +
            precedent_score * WEIGHTS['Precedent'] +
            damages_score * WEIGHTS['Damages_Credibility']
        )
        
        # Apply tribunal multiplier
        final_score = np.clip(weighted_score * TRIBUNAL_MULTIPLIERS[tribunal_stance], 0, 100)
        results.append(final_score)
    
    return np.array(results)

def calculate_metrics(results):
    """Calculate key metrics from simulation results"""
    median_score = np.percentile(results, 50)
    p25_score = np.percentile(results, 25)
    p75_score = np.percentile(results, 75)
    success_probability = (np.sum(results > 50) / len(results)) * 100
    
    return {
        'median': round(median_score, 1),
        'p25': round(p25_score, 1),
        'p75': round(p75_score, 1),
        'success_prob': round(success_probability, 1)
    }

def generate_density_data(results):
    """Generate kernel density estimation data for plotting"""
    # Create KDE
    kde = gaussian_kde(results)
    
    # Generate x values for smooth curve
    x_min, x_max = results.min(), results.max()
    x_range = np.linspace(max(0, x_min - 5), min(100, x_max + 5), 200)
    
    # Calculate density
    density = kde(x_range)
    
    return {
        'x': x_range.tolist(),
        'y': density.tolist(),
        'median': float(np.percentile(results, 50))
    }

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.json
        
        # Extract parameters
        jurisdiction = int(data['jurisdiction'])
        causation = int(data['causation'])
        evidence = int(data['evidence'])
        precedent = int(data['precedent'])
        damages = int(data['damages'])
        tribunal_stance = data['tribunal_stance']
        
        # Run simulation
        results = run_monte_carlo_simulation(
            jurisdiction, causation, evidence, precedent, damages, tribunal_stance
        )
        
        # Calculate metrics
        metrics = calculate_metrics(results)
        
        # Generate density data
        density_data = generate_density_data(results)
        
        return jsonify({
            'success': True,
            'metrics': metrics,
            'density_data': density_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Counterclaim Risk Simulator</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.26.0/plotly.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .container {
            display: grid;
            grid-template-columns: 400px 1fr;
            gap: 20px;
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
            min-height: 100vh;
        }

        .sidebar {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            height: fit-content;
            position: sticky;
            top: 20px;
        }

        .main-content {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #666;
            font-size: 1.1rem;
            margin-bottom: 30px;
            line-height: 1.4;
        }

        .control-group {
            margin-bottom: 25px;
        }

        .control-label {
            font-weight: 600;
            color: #444;
            margin-bottom: 8px;
            display: block;
            font-size: 0.95rem;
        }

        .slider-container {
            position: relative;
            margin-bottom: 15px;
        }

        .slider {
            width: 100%;
            height: 8px;
            border-radius: 5px;
            background: linear-gradient(to right, #ff6b6b, #feca57, #48ca8b);
            outline: none;
            -webkit-appearance: none;
            cursor: pointer;
        }

        .slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #fff;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            cursor: pointer;
            border: 3px solid #667eea;
            transition: all 0.2s ease;
        }

        .slider::-webkit-slider-thumb:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        }

        .slider::-moz-range-thumb {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #fff;
            cursor: pointer;
            border: 3px solid #667eea;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .slider-value {
            position: absolute;
            right: 0;
            top: -30px;
            background: #667eea;
            color: white;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .dropdown {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1rem;
            background: white;
            cursor: pointer;
            transition: border-color 0.3s ease;
        }

        .dropdown:focus {
            outline: none;
            border-color: #667eea;
        }

        .run-button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 20px;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }

        .run-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
        }

        .run-button:active {
            transform: translateY(0);
        }

        .run-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .metric-card {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
            transition: transform 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-5px);
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }

        .metric-label {
            color: #666;
            font-size: 0.9rem;
            font-weight: 500;
        }

        .chart-container {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
            min-height: 400px;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 40px;
            color: #667eea;
            font-size: 1.1rem;
        }

        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .results {
            display: none;
        }

        .initial-message {
            text-align: center;
            color: #999;
            font-size: 1.2rem;
            padding: 60px 20px;
        }

        .error-message {
            background: #ff6b6b;
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            display: none;
        }

        @media (max-width: 768px) {
            .container {
                grid-template-columns: 1fr;
                padding: 10px;
            }
            
            .sidebar {
                position: static;
            }
            
            h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <h1>Risk Simulator</h1>
            <p class="subtitle">Stress-test your strategy for the Fenoscadia v. Kronos counterclaim</p>
            
            <div class="control-group">
                <label class="control-label">Assumed Tribunal Stance</label>
                <select id="tribunalStance" class="dropdown">
                    <option value="Pro-Investor">Pro-Investor</option>
                    <option value="Neutral" selected>Neutral</option>
                    <option value="Pro-State">Pro-State</option>
                </select>
            </div>

            <div class="control-group">
                <label class="control-label">Strength of Jurisdictional Challenge</label>
                <div class="slider-container">
                    <input type="range" id="jurisdiction" class="slider" min="0" max="100" value="70">
                    <div class="slider-value" id="jurisdictionValue">70</div>
                </div>
            </div>

            <div class="control-group">
                <label class="control-label">Confidence in Disproving Causation Link</label>
                <div class="slider-container">
                    <input type="range" id="causation" class="slider" min="0" max="100" value="45">
                    <div class="slider-value" id="causationValue">45</div>
                </div>
            </div>

            <div class="control-group">
                <label class="control-label">Quality of Fenoscadia's Evidence</label>
                <div class="slider-container">
                    <input type="range" id="evidence" class="slider" min="0" max="100" value="60">
                    <div class="slider-value" id="evidenceValue">60</div>
                </div>
            </div>

            <div class="control-group">
                <label class="control-label">Strength of Favorable Precedent</label>
                <div class="slider-container">
                    <input type="range" id="precedent" class="slider" min="0" max="100" value="55">
                    <div class="slider-value" id="precedentValue">55</div>
                </div>
            </div>

            <div class="control-group">
                <label class="control-label">Credibility of Kronos's $150M Damage Claim</label>
                <div class="slider-container">
                    <input type="range" id="damages" class="slider" min="0" max="100" value="75">
                    <div class="slider-value" id="damagesValue">75</div>
                </div>
            </div>

            <button id="runSimulation" class="run-button">Run Simulation</button>
        </div>

        <div class="main-content">
            <div id="initialMessage" class="initial-message">
                <p>Adjust the parameters in the sidebar and click "Run Simulation" to analyze your legal strategy's risk profile.</p>
            </div>
            
            <div id="errorMessage" class="error-message"></div>
            
            <div id="loading" class="loading">
                <div class="spinner"></div>
                <p>Running Monte Carlo simulation with 5,000 iterations...</p>
            </div>

            <div id="results" class="results">
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value" id="medianScore">--</div>
                        <div class="metric-label">Most Likely Outcome<br>(Median Score)</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="successProbability">--</div>
                        <div class="metric-label">Probability of Success<br>(Score > 50)</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="pessimisticScore">--</div>
                        <div class="metric-label">Pessimistic Outcome<br>(25th Percentile)</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="optimisticScore">--</div>
                        <div class="metric-label">Optimistic Outcome<br>(75th Percentile)</div>
                    </div>
                </div>
                
                <div class="chart-container">
                    <div id="chart"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Initialize slider value displays
        function updateSliderValue(sliderId, valueId) {
            const slider = document.getElementById(sliderId);
            const valueDisplay = document.getElementById(valueId);
            
            slider.addEventListener('input', function() {
                valueDisplay.textContent = this.value;
            });
        }

        // Set up all sliders
        updateSliderValue('jurisdiction', 'jurisdictionValue');
        updateSliderValue('causation', 'causationValue');  
        updateSliderValue('evidence', 'evidenceValue');
        updateSliderValue('precedent', 'precedentValue');
        updateSliderValue('damages', 'damagesValue');

        // Update metrics display
        function updateMetrics(metrics) {
            document.getElementById('medianScore').textContent = metrics.median;
            document.getElementById('pessimisticScore').textContent = metrics.p25;
            document.getElementById('optimisticScore').textContent = metrics.p75;
            document.getElementById('successProbability').textContent = metrics.success_prob + '%';
        }

        // Create the density plot
        function createDensityPlot(densityData) {
            const trace = {
                x: densityData.x,
                y: densityData.y,
                type: 'scatter',
                mode: 'lines',
                fill: 'tonexty',
                fillcolor: 'rgba(102, 126, 234, 0.3)',
                line: {
                    color: 'rgba(102, 126, 234, 0.8)',
                    width: 3
                },
                name: 'Probability Density'
            };
            
            const maxY = Math.max(...densityData.y);
            const median = densityData.median;
            
            const shapes = [
                {
                    type: 'line',
                    x0: 50,
                    y0: 0,
                    x1: 50,
                    y1: maxY,
                    line: {
                        color: 'rgba(255, 107, 107, 0.8)',
                        width: 2,
                        dash: 'dash'
                    }
                },
                {
                    type: 'line',
                    x0: median,
                    y0: 0,
                    x1: median,
                    y1: maxY,
                    line: {
                        color: 'rgba(72, 202, 139, 0.8)',
                        width: 3
                    }
                }
            ];
            
            const annotations = [
                {
                    x: 50,
                    y: maxY * 0.9,
                    text: 'Success Threshold',
                    showarrow: true,
                    arrowhead: 2,
                    arrowcolor: 'rgba(255, 107, 107, 0.8)',
                    font: { color: 'rgba(255, 107, 107, 0.8)', size: 12 }
                },
                {
                    x: median,
                    y: maxY * 0.7,
                    text: `Median: ${median.toFixed(1)}`,
                    showarrow: true,
                    arrowhead: 2,
                    arrowcolor: 'rgba(72, 202, 139, 0.8)',
                    font: { color: 'rgba(72, 202, 139, 0.8)', size: 12 }
                }
            ];
            
            const layout = {
                title: {
                    text: 'Distribution of Potential Outcomes',
                    font: { size: 18, color: '#333' }
                },
                xaxis: {
                    title: 'Strategy Strength Score',
                    range: [0, 100],
                    gridcolor: 'rgba(0,0,0,0.1)'
                },
                yaxis: {
                    title: 'Likelihood',
                    gridcolor: 'rgba(0,0,0,0.1)'
                },
                shapes: shapes,
                annotations: annotations,
                showlegend: false,
                plot_bgcolor: 'rgba(0,0,0,0)',
                paper_bgcolor: 'rgba(0,0,0,0)',
                margin: { t: 60, r: 40, b: 60, l: 60 }
            };
            
            const config = {
                responsive: true,
                displayModeBar: false
            };
            
            Plotly.newPlot('chart', [trace], layout, config);
        }

        // Show error message
        function showError(message) {
            const errorDiv = document.getElementById('errorMessage');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            setTimeout(() => {
                errorDiv.style.display = 'none';
            }, 5000);
        }

        // Main execution function
        document.getElementById('runSimulation').addEventListener('click', function() {
            const button = this;
            button.disabled = true;
            button.textContent = 'Running...';
            
            // Show loading, hide other content
            document.getElementById('initialMessage').style.display = 'none';
            document.getElementById('results').style.display = 'none';
            document.getElementById('loading').style.display = 'block';
            
            // Prepare simulation data
            const data = {
                jurisdiction: parseInt(document.getElementById('jurisdiction').value),
                causation: parseInt(document.getElementById('causation').value),
                evidence: parseInt(document.getElementById('evidence').value), 
                precedent: parseInt(document.getElementById('precedent').value),
                damages: parseInt(document.getElementById('damages').value),
                tribunal_stance: document.getElementById('tribunalStance').value
            };
            
            // Call Flask backend
            fetch('/simulate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    updateMetrics(result.metrics);
                    createDensityPlot(result.density_data);
                    
                    // Show results, hide loading
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('results').style.display = 'block';
                } else {
                    showError('Simulation failed: ' + result.error);
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('initialMessage').style.display = 'block';
                }
            })
            .catch(error => {
                showError('Network error: ' + error.message);
                document.getElementById('loading').style.display = 'none';
                document.getElementById('initialMessage').style.display = 'block';
            })
            .finally(() => {
                button.disabled = false;
                button.textContent = 'Run Simulation';
            });
        });
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    print("🚀 Starting Counterclaim Risk Simulator...")
    print("📊 Navigate to http://localhost:5002 to use the simulator")
    print("⚖️  Based on Burlington, Perenco, and Rusoro case analysis")
    print("🎯 Optimized for Fenoscadia v. Kronos counterclaim strategy")
    app.run(debug=True, host='0.0.0.0', port=5002)