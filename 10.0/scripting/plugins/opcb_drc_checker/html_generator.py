import os

def generate_html_report(report_data, output_path):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>OPCB Design Rule Checker Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
            h1 {{ color: #0056b3; }}
            h2 {{ color: #d9534f; border-bottom: 2px solid #eee; padding-bottom: 5px; }}
            h3 {{ color: #5bc0de; }}
            .summary {{ background: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            .warnings {{ background: #fff3cd; padding: 15px; border-left: 5px solid #ffecb5; margin-bottom: 20px; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 10px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>OPCB Design Rule Checker Report</h1>
        
        <div class="summary">
            <h2>Board Dimensions</h2>
            <p><strong>Width:</strong> {report_data['board_width']:.2f} mm</p>
            <p><strong>Height:</strong> {report_data['board_height']:.2f} mm</p>
            <p><strong>Area:</strong> {report_data['board_area']:.2f} mm&sup2;</p>
        </div>

        <div class="summary">
            <h2>Design Summary</h2>
            <p><strong>Total Tracks:</strong> {report_data['total_tracks']}</p>
            <p><strong>Total Vias:</strong> {report_data['total_vias']}</p>
        </div>
    """

    # Warnings section
    html_content += f"""
        <div class="warnings">
            <h2>Warnings / Violations</h2>
    """
    
    has_warnings = False
    if report_data['small_tracks']:
        has_warnings = True
        html_content += f"<h3>Small Tracks Detected (&lt; {report_data['track_threshold']} mm)</h3>"
        html_content += "<table><tr><th>Location (X, Y) mm</th><th>Width (mm)</th></tr>"
        for t in report_data['small_tracks']:
            html_content += f"<tr><td>({t['x']:.2f}, {t['y']:.2f})</td><td>{t['width']:.3f}</td></tr>"
        html_content += "</table>"
        
    if report_data['small_vias']:
        has_warnings = True
        html_content += f"<h3>Small Vias Detected (&lt; {report_data['via_threshold']} mm)</h3>"
        html_content += "<table><tr><th>Location (X, Y) mm</th><th>Diameter (mm)</th></tr>"
        for v in report_data['small_vias']:
            html_content += f"<tr><td>({v['x']:.2f}, {v['y']:.2f})</td><td>{v['width']:.3f}</td></tr>"
        html_content += "</table>"
        
    if not has_warnings:
        html_content += "<p style='color: green;'><strong>No small tracks or vias detected. DRC passed!</strong></p>"
        
    html_content += """
        </div>
    """
    
    # Layer statistics
    html_content += """
        <div class="summary">
            <h2>Layer Usage Statistics (Copper Layers)</h2>
    """
    if not report_data['layer_stats']:
        html_content += "<p>No copper layers used or detected.</p>"
    else:
        html_content += """
            <table>
                <tr><th>Layer</th><th>Object Count</th></tr>
        """
        for layer, count in report_data['layer_stats'].items():
            html_content += f"<tr><td>{layer}</td><td>{count}</td></tr>"
        html_content += """
            </table>
        """
        
    html_content += """
        </div>
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path
