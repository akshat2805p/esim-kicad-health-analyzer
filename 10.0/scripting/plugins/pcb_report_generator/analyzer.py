def analyze_components(data):
    components = []
    duplicates = []
    missing_values = []

    seen = set()

    resistor_count = 0
    capacitor_count = 0
    ic_count = 0

    for line in data:
        parts = line.strip().split(",")

        if len(parts) != 3:
            continue

        ref, comp_type, value = parts

        components.append(ref)

        if ref in seen:
            duplicates.append(ref)
        else:
            seen.add(ref)

        if value == "":
            missing_values.append(ref)

        if comp_type == "Resistor":
            resistor_count += 1
        elif comp_type == "Capacitor":
            capacitor_count += 1
        elif comp_type == "IC":
            ic_count += 1

    return {
        "total": len(components),
        "resistors": resistor_count,
        "capacitors": capacitor_count,
        "ics": ic_count,
        "duplicates": duplicates,
        "missing": missing_values
    }