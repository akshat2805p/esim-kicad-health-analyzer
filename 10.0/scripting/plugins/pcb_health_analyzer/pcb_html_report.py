import os


def generate_html_report(
    report_path,
    health_score,
    grade,
    board_status,
    tracks,
    vias,
    footprints,
    total_nets,
    min_track_width,
    max_track_width,
    avg_track_width,
    complexity_score,
    warnings_text
):

    warnings_html = "<br>".join([line for line in warnings_text.strip().split("\n")])

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>PCB Health Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
        }}

        h1, h2 {{
            color: #2c3e50;
        }}

        table {{
            border-collapse: collapse;
            width: 70%;
            margin-bottom: 20px;
        }}

        th, td {{
            border: 1px solid black;
            padding: 10px;
            text-align: left;
        }}

        th {{
            background-color: #f2f2f2;
        }}
        
        .warnings {{
            color: #d35400;
            font-weight: bold;
        }}
    </style>
</head>
<body>

<h1>PCB HEALTH REPORT</h1>

<p><strong>Health Score:</strong> {health_score}/100</p>
<p><strong>Grade:</strong> {grade}</p>

<h2>Design Quality Analysis</h2>
<hr style="width:70%; text-align:left; margin-left:0">
<p>Min Track Width: {min_track_width} mm</p>
<p>Max Track Width: {max_track_width} mm</p>
<p>Average Track Width: {avg_track_width} mm</p>

<p>Via Count: {vias}</p>
<p>Complexity Score: {complexity_score}/100</p>

<h3>Warnings:</h3>
<p class="warnings">
{warnings_html}
</p>

<h2>General Statistics</h2>
<table>
<tr>
    <th>Metric</th>
    <th>Value</th>
</tr>
<tr>
    <td>Board Status</td>
    <td>{board_status}</td>
</tr>
<tr>
    <td>Total Tracks</td>
    <td>{tracks}</td>
</tr>
<tr>
    <td>Total Components</td>
    <td>{footprints}</td>
</tr>
<tr>
    <td>Total Nets</td>
    <td>{total_nets}</td>
</tr>
</table>

</body>
</html>
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
