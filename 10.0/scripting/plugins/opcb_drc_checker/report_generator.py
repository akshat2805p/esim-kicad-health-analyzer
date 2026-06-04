import os

def generate_text_report(report_data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write(" OPCB Design Rule Checker Report\n")
        f.write("=" * 50 + "\n\n")

        f.write("--- Board Dimensions ---\n")
        f.write(f"Width:  {report_data['board_width']:.2f} mm\n")
        f.write(f"Height: {report_data['board_height']:.2f} mm\n")
        f.write(f"Area:   {report_data['board_area']:.2f} mm^2\n\n")

        f.write("--- Design Rule Checks ---\n")
        f.write(f"Total Tracks: {report_data['total_tracks']}\n")
        f.write(f"Total Vias:   {report_data['total_vias']}\n")
        
        f.write("\nWarnings:\n")
        if not report_data['small_tracks'] and not report_data['small_vias']:
            f.write("  No small tracks or vias detected. DRC passed!\n")
        else:
            if report_data['small_tracks']:
                f.write(f"  Small Tracks Detected (< {report_data['track_threshold']} mm): {len(report_data['small_tracks'])}\n")
                for t in report_data['small_tracks']:
                    f.write(f"    - Track at ({t['x']:.2f}, {t['y']:.2f}) mm, Width: {t['width']:.3f} mm\n")
            
            if report_data['small_vias']:
                f.write(f"  Small Vias Detected (< {report_data['via_threshold']} mm): {len(report_data['small_vias'])}\n")
                for v in report_data['small_vias']:
                    f.write(f"    - Via at ({v['x']:.2f}, {v['y']:.2f}) mm, Diameter: {v['width']:.3f} mm\n")
        
        f.write("\n--- Layer Usage Statistics (Copper Layers) ---\n")
        if not report_data['layer_stats']:
            f.write("  No copper layers used or detected.\n")
        else:
            for layer, count in report_data['layer_stats'].items():
                f.write(f"  {layer}: {count} objects\n")

    return output_path
