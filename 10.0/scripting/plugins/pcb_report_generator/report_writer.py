def generate_report(results):
    report = []

    report.append("PCB DESIGN REPORT")
    report.append("=" * 30)
    report.append("")

    report.append(f"Total Components: {results['total']}")
    report.append("")

    report.append(f"Resistors: {results['resistors']}")
    report.append(f"Capacitors: {results['capacitors']}")
    report.append(f"ICs: {results['ics']}")
    report.append("")

    report.append("Duplicate Components:")

    if results["duplicates"]:
        for item in results["duplicates"]:
            report.append(f"- {item}")
    else:
        report.append("None")

    report.append("")

    report.append("Missing Values:")

    if results["missing"]:
        for item in results["missing"]:
            report.append(f"- {item}")
    else:
        report.append("None")

    report.append("")
    report.append("STATUS:")

    if results["duplicates"] or results["missing"]:
        report.append("Design needs review.")
    else:
        report.append("Design verified successfully.")

    return "\n".join(report)