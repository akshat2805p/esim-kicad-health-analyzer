import os


def generate_html_report(
    report_path,
    health_score,
    grade,
    board_status,
    tracks,
    vias,
    footprints,
    total_nets
):

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

        h1 {{
            color: #2c3e50;
        }}

        table {{
            border-collapse: collapse;
            width: 70%;
        }}

        th, td {{
            border: 1px solid black;
            padding: 10px;
            text-align: left;
        }}

        th {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>

<h1>PCB Health Report</h1>

<table>
<tr>
    <th>Metric</th>
    <th>Value</th>
</tr>

<tr>
    <td>Health Score</td>
    <td>{health_score}</td>
</tr>

<tr>
    <td>Health Grade</td>
    <td>{grade}</td>
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
    <td>Total Vias</td>
    <td>{vias}</td>
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
        
