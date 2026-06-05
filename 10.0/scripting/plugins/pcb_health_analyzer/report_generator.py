import json
import os

def generate_report(stats):

    report_path = os.path.join(
        os.path.dirname(__file__),
        "pcb_health_report.json"
    )

    if "complexity_score" not in stats:
        stats["complexity_score"] = 0
    if "drc_summary" not in stats:
        stats["drc_summary"] = {}

    with open(report_path, "w") as report_file:
        json.dump(stats, report_file, indent=4)

    print(f"Report generated at: {report_path}")