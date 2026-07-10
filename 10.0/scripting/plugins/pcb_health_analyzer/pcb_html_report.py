"""
HTML Report Generator for PCB Health Analyzer

Generates a styled HTML report with board statistics, design quality
analysis, warnings, and the new AI PCB Assistant section including
issue explanations, recommendations, fabrication readiness, and
interactive Q&A.
"""

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
    warnings_text,
    ai_review=None,
):
    """
    Write a full HTML health report to *report_path*.

    Parameters
    ----------
    ai_review : dict or None
        Output of AIReviewEngine.analyze().  When provided, an
        "AI PCB Assistant" card is appended to the report.
    """

    warnings_html = "<br>".join(
        line for line in warnings_text.strip().split("\n") if line.strip()
    )

    # ---- build AI section HTML (Task 5) ------------------------------ #
    ai_section_html = ""
    if ai_review is not None:
        ai_section_html = _build_ai_section(ai_review)

    # ---- colour helpers ---------------------------------------------- #
    if health_score >= 90:
        score_colour = "#27ae60"
    elif health_score >= 75:
        score_colour = "#2ecc71"
    elif health_score >= 60:
        score_colour = "#f39c12"
    else:
        score_colour = "#e74c3c"

    fab_status = ""
    fab_colour = "#27ae60"
    if ai_review:
        fab_status = ai_review.get("fabrication_status", "")
        fab_colour = "#27ae60" if fab_status == "READY" else "#e74c3c"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PCB Health Report &mdash; AI-Assisted Analysis</title>
    <style>
        /* ---- Reset & base ---- */
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f2f5;
            color: #2c3e50;
            padding: 30px 40px;
            line-height: 1.6;
        }}

        /* ---- header ---- */
        .report-header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .report-header h1 {{
            font-size: 28px;
            color: #2c3e50;
            margin-bottom: 4px;
        }}
        .report-header p {{
            color: #7f8c8d;
            font-size: 14px;
        }}

        /* ---- cards ---- */
        .card {{
            background: #ffffff;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            padding: 24px 28px;
            margin-bottom: 24px;
        }}
        .card h2 {{
            font-size: 18px;
            color: #2c3e50;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
            margin-bottom: 16px;
        }}

        /* ---- score banner ---- */
        .score-banner {{
            display: flex;
            align-items: center;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px;
        }}
        .score-circle {{
            width: 120px; height: 120px;
            border-radius: 50%;
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            color: #fff; font-weight: bold;
            font-size: 32px;
            background: {score_colour};
        }}
        .score-circle small {{ font-size: 13px; font-weight: 400; }}
        .score-meta {{ text-align: center; }}
        .score-meta .grade {{ font-size: 38px; font-weight: 700; color: {score_colour}; }}
        .score-meta .status {{ font-size: 14px; color: #7f8c8d; }}

        /* ---- tables ---- */
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 8px;
        }}
        th, td {{
            border: 1px solid #ecf0f1;
            padding: 10px 14px;
            text-align: left;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            color: #7f8c8d;
        }}

        /* ---- warnings ---- */
        .warnings {{
            color: #d35400;
            font-weight: 600;
        }}

        /* ---- AI section ---- */
        .ai-card {{
            border-left: 4px solid #3498db;
        }}
        .ai-card h2 {{
            color: #2980b9;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            color: #fff;
        }}
        .badge-ready {{ background: #27ae60; }}
        .badge-warning {{ background: #e74c3c; }}
        .issue-item {{
            background: #fef9e7;
            border-left: 3px solid #f1c40f;
            padding: 10px 14px;
            margin-bottom: 10px;
            border-radius: 4px;
        }}
        .issue-item strong {{ color: #e67e22; }}
        .rec-list {{
            list-style: none;
            counter-reset: rec;
        }}
        .rec-list li {{
            counter-increment: rec;
            padding: 6px 0 6px 28px;
            position: relative;
        }}
        .rec-list li::before {{
            content: counter(rec);
            position: absolute;
            left: 0; top: 6px;
            width: 20px; height: 20px;
            background: #3498db;
            color: #fff;
            border-radius: 50%;
            font-size: 11px;
            text-align: center;
            line-height: 20px;
        }}

        /* ---- Q&A accordion ---- */
        details {{
            margin-bottom: 8px;
        }}
        details summary {{
            cursor: pointer;
            padding: 8px 12px;
            background: #eaf2f8;
            border-radius: 4px;
            font-weight: 600;
            color: #2980b9;
            list-style: none;
        }}
        details summary::-webkit-details-marker {{ display: none; }}
        details summary::before {{ content: "▸ "; }}
        details[open] summary::before {{ content: "▾ "; }}
        details .answer {{
            padding: 10px 14px;
            color: #555;
            border-left: 2px solid #3498db;
            margin-top: 4px;
        }}

        /* ---- fab banner ---- */
        .fab-banner {{
            text-align: center;
            padding: 18px;
            border-radius: 8px;
            margin-top: 12px;
            font-size: 20px;
            font-weight: 700;
            letter-spacing: 1px;
            color: #fff;
            background: {fab_colour};
        }}
    </style>
</head>
<body>

<!-- Header -->
<div class="report-header">
    <h1>&#128204; PCB HEALTH REPORT</h1>
    <p>AI-Assisted Analysis &bull; Generated by OPCB Health Analyzer</p>
</div>

<!-- Score card -->
<div class="card">
    <div class="score-banner">
        <div class="score-circle">
            {health_score}<small>/100</small>
        </div>
        <div class="score-meta">
            <div class="grade">{grade}</div>
            <div class="status">{board_status}</div>
        </div>
    </div>
</div>

<!-- Design Quality -->
<div class="card">
    <h2>&#128200; Design Quality Analysis</h2>
    <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Min Track Width</td><td>{min_track_width} mm</td></tr>
        <tr><td>Max Track Width</td><td>{max_track_width} mm</td></tr>
        <tr><td>Average Track Width</td><td>{avg_track_width} mm</td></tr>
        <tr><td>Via Count</td><td>{vias}</td></tr>
        <tr><td>Complexity Score</td><td>{complexity_score}/100</td></tr>
    </table>
    <h3 style="margin-top:14px;">Warnings</h3>
    <p class="warnings">{warnings_html if warnings_html else "No warnings"}</p>
</div>

<!-- General Statistics -->
<div class="card">
    <h2>&#128202; General Statistics</h2>
    <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Board Status</td><td>{board_status}</td></tr>
        <tr><td>Total Tracks</td><td>{tracks}</td></tr>
        <tr><td>Total Vias</td><td>{vias}</td></tr>
        <tr><td>Total Components</td><td>{footprints}</td></tr>
        <tr><td>Total Nets</td><td>{total_nets}</td></tr>
    </table>
</div>

<!-- AI PCB Assistant (Task 5) -->
{ai_section_html}

</body>
</html>
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)


# ---------------------------------------------------------------------- #
#  AI section builder                                                      #
# ---------------------------------------------------------------------- #

def _build_ai_section(ai_review):
    """Return an HTML string for the AI PCB Assistant card."""

    quality = ai_review.get("quality_level", "Unknown")
    issues = ai_review.get("issues", [])
    recommendations = ai_review.get("recommendations", [])
    fab_status = ai_review.get("fabrication_status", "UNKNOWN")
    fab_details = ai_review.get("fabrication_details", "")

    # Issues HTML
    if issues:
        issues_html = "\n".join(
            f'<div class="issue-item"><strong>{iss["title"]}</strong><br>'
            f'{iss["explanation"]}</div>'
            for iss in issues
        )
    else:
        issues_html = '<p style="color:#27ae60;font-weight:600;">No issues detected — excellent work!</p>'

    # Recommendations HTML
    if recommendations:
        recs_items = "\n".join(f"<li>{r}</li>" for r in recommendations)
        recs_html = f'<ol class="rec-list">{recs_items}</ol>'
    else:
        recs_html = "<p>No specific recommendations.</p>"

    # Fabrication badge
    badge_cls = "badge-ready" if fab_status == "READY" else "badge-warning"

    # Q&A section
    qa_html = _build_qa_section(ai_review)

    return f"""
<div class="card ai-card">
    <h2>&#129302; AI PCB Assistant</h2>

    <h3>Overall Assessment</h3>
    <p style="font-size:16px;font-weight:600;margin-bottom:14px;">{quality}</p>

    <h3>Major Issues</h3>
    {issues_html}

    <h3 style="margin-top:18px;">Recommendations</h3>
    {recs_html}

    <h3 style="margin-top:18px;">Fabrication Readiness</h3>
    <p><span class="badge {badge_cls}">{fab_status}</span></p>
    <p style="margin-top:6px;color:#555;">{fab_details}</p>

    <div class="fab-banner">{fab_status}</div>

    <h3 style="margin-top:24px;">&#128172; Interactive Q&amp;A</h3>
    {qa_html}
</div>
"""


def _build_qa_section(ai_review):
    """Build collapsible Q&A blocks."""

    issues = ai_review.get("issues", [])
    recommendations = ai_review.get("recommendations", [])
    fab_status = ai_review.get("fabrication_status", "")
    fab_details = ai_review.get("fabrication_details", "")

    # Q1: Why is my health score low?
    if issues:
        q1_body = "The score is reduced due to:<ul>" + "".join(
            f"<li>{i['title']}</li>" for i in issues
        ) + "</ul>"
    else:
        q1_body = "Your health score is not low — no significant issues detected."

    # Q2: What are the major issues?
    if issues:
        q2_body = "<ul>" + "".join(
            f"<li><strong>{i['title']}</strong> — {i['explanation']}</li>" for i in issues
        ) + "</ul>"
    else:
        q2_body = "No major issues found."

    # Q3: How can I improve the board?
    if recommendations:
        q3_body = "<ol>" + "".join(f"<li>{r}</li>" for r in recommendations) + "</ol>"
    else:
        q3_body = "No specific improvements needed."

    # Q4: Is this board ready for fabrication?
    q4_body = f"<strong>{fab_status}</strong><br>{fab_details}"

    pairs = [
        ("Why is my health score low?", q1_body),
        ("What are the major issues?", q2_body),
        ("How can I improve the board?", q3_body),
        ("Is this board ready for fabrication?", q4_body),
    ]

    return "\n".join(
        f'<details><summary>{q}</summary><div class="answer">{a}</div></details>'
        for q, a in pairs
    )
