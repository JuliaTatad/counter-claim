import numpy as np
import plotly.graph_objects as go
import webbrowser
import os

def run_simulation(tribunal_stance, jurisdiction, causation, evidence, precedent, damages):
    """Runs the Monte Carlo simulation to assess counterclaim risk."""
    
    # Define weights and multipliers
    weights = {
        'Jurisdiction': 0.40,
        'Causation': 0.30,
        'Evidence': 0.10,
        'Precedent': 0.15,
        'Damages_Credibility': 0.05
    }

    tribunal_multipliers = {
        'Pro-Investor': 1.10,
        'Neutral': 1.00,
        'Pro-State': 0.90
    }

    tribunal_multiplier = tribunal_multipliers[tribunal_stance]
    N = 5000
    std_dev = 15
    
    # Run Monte Carlo simulation
    jurisdiction_scores = np.clip(np.random.normal(jurisdiction, std_dev, N), 0, 100)
    causation_scores = np.clip(np.random.normal(causation, std_dev, N), 0, 100)
    evidence_scores = np.clip(np.random.normal(evidence, std_dev, N), 0, 100)
    precedent_scores = np.clip(np.random.normal(precedent, std_dev, N), 0, 100)
    damages_scores = np.clip(np.random.normal(damages, std_dev, N), 0, 100)

    weighted_scores = (
        jurisdiction_scores * weights['Jurisdiction'] +
        causation_scores * weights['Causation'] +
        evidence_scores * weights['Evidence'] +
        precedent_scores * weights['Precedent'] +
        damages_scores * weights['Damages_Credibility']
    )

    final_scores = np.clip(weighted_scores * tribunal_multiplier, 0, 100)
    
    return final_scores

def get_metrics(results):
    """Calculates key metrics from the simulation results."""
    median_score = np.percentile(results, 50)
    pessimistic_score = np.percentile(results, 25)
    optimistic_score = np.percentile(results, 75)
    success_probability = np.mean(results > 50) * 100
    
    return {
        "median": median_score,
        "pessimistic": pessimistic_score,
        "optimistic": optimistic_score,
        "success_prob": success_probability
    }

def create_chart(results, metrics):
    """Creates a Plotly chart for the results."""
    
    # Create histogram data
    hist_data, bin_edges = np.histogram(results, bins=50, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    fig = go.Figure()

    # Add density plot
    fig.add_trace(go.Scatter(
        x=bin_centers,
        y=hist_data,
        mode='lines',
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.3)',
        line=dict(color='rgba(102, 126, 234, 0.8)', width=3),
        name='Probability Density'
    ))

    # Add lines for median and success threshold
    fig.add_shape(type="line",
        x0=50, y0=0, x1=50, y1=max(hist_data),
        line=dict(color="Red", width=2, dash="dash"),
        name="Success Threshold"
    )
    fig.add_shape(type="line",
        x0=metrics['median'], y0=0, x1=metrics['median'], y1=max(hist_data),
        line=dict(color="Green", width=2, dash="dot"),
        name="Median"
    )

    # Add annotations
    fig.add_annotation(x=50, y=max(hist_data) * 0.9, text="Success Threshold (50)", showarrow=False, font=dict(color="red"))
    fig.add_annotation(x=metrics['median'], y=max(hist_data) * 0.8, text=f"Median ({metrics['median']:.1f})", showarrow=False, font=dict(color="green"))

    # Update layout
    fig.update_layout(
        title_text='Distribution of Potential Outcomes',
        xaxis_title='Strategy Strength Score',
        yaxis_title='Likelihood',
        xaxis=dict(range=[0, 100]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Segoe UI, sans-serif', size=12, color='#333')
    )
    
    return fig

def generate_html_report(fig, metrics, tribunal_stance, jurisdiction_strength, causation_confidence, evidence_quality, precedent_strength, damages_credibility):
    """Generates an HTML report with the chart and metrics."""
    
    def get_metric_color(value, thresholds):
        if value > thresholds[0]: return 'success'
        if value > thresholds[1]: return 'warning'
        return 'danger'

    median_color = get_metric_color(metrics['median'], (60, 40))
    success_prob_color = get_metric_color(metrics['success_prob'], (70, 40))

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Python Simulation Report</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Roboto', sans-serif;
                background-color: #f0f2f5;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 1200px;
                margin: 50px auto;
                padding: 40px;
                background: #ffffff;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 40px;
                border-bottom: 1px solid #e0e0e0;
                padding-bottom: 20px;
            }}
            h1 {{
                font-size: 2.5rem;
                color: #1a237e;
                font-weight: 700;
                margin: 0;
            }}
            h2 {{
                font-size: 1.8rem;
                color: #3f51b5;
                margin-top: 0;
                margin-bottom: 20px;
                border-bottom: 2px solid #c5cae9;
                padding-bottom: 10px;
            }}
            .main-content {{
                display: flex;
                gap: 40px;
            }}
            .left-column {{
                flex: 1;
            }}
            .right-column {{
                flex: 1.5;
                display: flex;
                flex-direction: column;
            }}
            .metrics-grid, .inputs-grid {{
                display: grid;
                gap: 20px;
            }}
            .metrics-grid {{
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                margin-bottom: 40px;
            }}
            .inputs-grid {{
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            }}
            .metric-card, .input-card {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                border-left: 5px solid;
            }}
            .metric-card:hover, .input-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            }}
            .metric-label, .input-label {{
                font-size: 0.9rem;
                color: #555;
                margin-bottom: 10px;
                font-weight: 400;
            }}
            .metric-value {{
                font-size: 2.5rem;
                font-weight: 700;
            }}
            .input-value {{
                font-size: 1.8rem;
                font-weight: 700;
                color: #3f51b5;
            }}
            .metric-card.success {{ border-color: #4caf50; }}
            .metric-card.warning {{ border-color: #ff9800; }}
            .metric-card.danger {{ border-color: #f44336; }}
            .metric-value.success {{ color: #4caf50; }}
            .metric-value.warning {{ color: #ff9800; }}
            .metric-value.danger {{ color: #f44336; }}
            .input-card {{
                border-color: #c5cae9;
            }}
            #chart {{
                width: 100%;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            }}
            @media (max-width: 1024px) {{
                .main-content {{
                    flex-direction: column;
                }}
                .container {{
                    margin: 20px;
                    padding: 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Counterclaim Risk Simulation Report</h1>
            </div>
            <div class="main-content">
                <div class="left-column">
                    <h2>Simulation Outputs</h2>
                    <div class="metrics-grid">
                        <div class="metric-card {median_color}">
                            <div class="metric-label">Most Likely Outcome (Median)</div>
                            <div class="metric-value">{metrics['median']:.1f}</div>
                        </div>
                        <div class="metric-card {success_prob_color}">
                            <div class="metric-label">Probability of Success (>50)</div>
                            <div class="metric-value">{metrics['success_prob']:.1f}%</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Pessimistic Outcome (25th %)</div>
                            <div class="metric-value">{metrics['pessimistic']:.1f}</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Optimistic Outcome (75th %)</div>
                            <div class="metric-value">{metrics['optimistic']:.1f}</div>
                        </div>
                    </div>
        
                    <h2>Key Factors</h2>
                    <div class="inputs-grid">
                        <div class="input-card">
                            <div class="input-label">Tribunal Stance</div>
                            <div class="input-value">{tribunal_stance}</div>
                        </div>
                        <div class="input-card">
                            <div class="input-label">Jurisdiction Strength</div>
                            <div class="input-value">{jurisdiction_strength}</div>
                        </div>
                        <div class="input-card">
                            <div class="input-label">Causation Confidence</div>
                            <div class="input-value">{causation_confidence}</div>
                        </div>
                        <div class="input-card">
                            <div class="input-label">Evidence Quality</div>
                            <div class="input-value">{evidence_quality}</div>
                        </div>
                        <div class="input-card">
                            <div class="input-label">Precedent Strength</div>
                            <div class="input-value">{precedent_strength}</div>
                        </div>
                        <div class="input-card">
                            <div class="input-label">Damages Credibility</div>
                            <div class="input-value">{damages_credibility}</div>
                        </div>
                    </div>
                </div>
                <div class="right-column">
                    <h2>Distribution of Potential Outcomes</h2>
                    <div id="chart">
                        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open("python_report.html", "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    # --- Default Input Parameters ---
    # These can be modified or loaded from a config file/UI
    TRIBUNAL_STANCE = "Neutral"  # Options: "Pro-Investor", "Neutral", "Pro-State"
    JURISDICTION_STRENGTH = 70
    CAUSATION_CONFIDENCE = 45
    EVIDENCE_QUALITY = 60
    PRECEDENT_STRENGTH = 55
    DAMAGES_CREDIBILITY = 75
    # --------------------------------

    # Run the full process
    simulation_results = run_simulation(
        TRIBUNAL_STANCE,
        JURISDICTION_STRENGTH,
        CAUSATION_CONFIDENCE,
        EVIDENCE_QUALITY,
        PRECEDENT_STRENGTH,
        DAMAGES_CREDIBILITY
    )
    
    report_metrics = get_metrics(simulation_results)
    
    report_chart = create_chart(simulation_results, report_metrics)
    
    generate_html_report(
    report_chart,
    report_metrics,
    TRIBUNAL_STANCE,
    JURISDICTION_STRENGTH,
    CAUSATION_CONFIDENCE,
    EVIDENCE_QUALITY,
    PRECEDENT_STRENGTH,
    DAMAGES_CREDIBILITY
)

    print("Report 'python_report.html' generated successfully.")
    
    # Open the report in the default web browser
    webbrowser.open('file://' + os.path.realpath('python_report.html'))
