"""
Report Generator for PCB Health Analyzer

Handles:
  1. JSON health report export  (existing functionality)
  2. Board knowledge file export (Task 6 — AI Knowledge Assistant)
"""

import json
import os


def generate_report(stats):
    """Write the standard pcb_health_report.json beside this module."""

    report_path = os.path.join(
        os.path.dirname(__file__),
        "pcb_health_report.json",
    )

    if "complexity_score" not in stats:
        stats["complexity_score"] = 0
    if "drc_summary" not in stats:
        stats["drc_summary"] = {}

    with open(report_path, "w") as report_file:
        json.dump(stats, report_file, indent=4)

    print(f"Report generated at: {report_path}")


def generate_knowledge_file(board_name, stats, ai_review, output_dir):
    """
    Generate a structured JSON knowledge file for future LLM integration.

    Creates ``reports/board_knowledge.json`` inside *output_dir*.

    Parameters
    ----------
    board_name : str
        Name / path of the PCB board file.
    stats : dict
        Raw board statistics.
    ai_review : dict
        Output of AIReviewEngine.analyze().
    output_dir : str
        Directory where the ``reports/`` folder will be created.
    """

    reports_dir = os.path.join(output_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    # Build issue tag list  (short machine-readable keys)
    issue_tags = []
    for issue in ai_review.get("issues", []):
        title = issue.get("title", "")
        tag = title.lower().replace(" ", "_")
        issue_tags.append(tag)

    # Build recommendation tag list
    rec_tags = []
    recs = ai_review.get("recommendations", [])
    tag_map = {
        "drc": "run_drc",
        "unconnected": "fix_unconnected_nets",
        "via": "reduce_vias",
        "layer transition": "reduce_layer_transitions",
        "track width": "increase_track_width",
        "drill": "increase_via_drill",
        "routing": "complete_routing",
        "power": "review_power_routing",
        "visual inspection": "final_visual_inspection",
        "gerber": "final_visual_inspection",
    }
    for rec in recs:
        rec_lower = rec.lower()
        for keyword, tag in tag_map.items():
            if keyword in rec_lower and tag not in rec_tags:
                rec_tags.append(tag)

    knowledge = {
        "board_name": os.path.basename(board_name) if board_name else "unknown.kicad_pcb",
        "health_score": stats.get("health_score", 0),
        "grade": stats.get("grade", ""),
        "board_status": stats.get("board_status", ""),
        "quality_level": ai_review.get("quality_level", ""),
        "fabrication_status": ai_review.get("fabrication_status", ""),
        "issues": issue_tags,
        "recommendations": rec_tags,
        "statistics": {
            "tracks": stats.get("tracks", 0),
            "vias": stats.get("vias", 0),
            "footprints": stats.get("footprints", 0),
            "total_nets": stats.get("total_nets", 0),
            "copper_layers": stats.get("copper_layers", 0),
            "complexity_score": stats.get("complexity_score", 0),
        },
        "ai_review": {
            "summary": ai_review.get("summary_text", ""),
            "issues_detail": ai_review.get("issues", []),
            "recommendations_detail": ai_review.get("recommendations", []),
            "fabrication_details": ai_review.get("fabrication_details", ""),
        },
    }

    knowledge_path = os.path.join(reports_dir, "board_knowledge.json")
    with open(knowledge_path, "w", encoding="utf-8") as f:
        json.dump(knowledge, f, indent=2, ensure_ascii=False)

    print(f"Knowledge file generated at: {knowledge_path}")
    return knowledge_path