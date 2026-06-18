import pcbnew
import os
import wx
import datetime
from .gui import SmartAssistantGUI

class SmartDesignAssistantPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Smart PCB Design Assistant"
        self.category = "Analysis"
        self.description = "AI-Based Smart PCB Design Rule Assistant"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')

    def Run(self):
        board = pcbnew.GetBoard()
        if not board:
            wx.MessageBox("No board open. Please open a PCB layout first.", "Error", wx.ICON_ERROR)
            return

        # Perform analysis
        warnings, score, grade, recommendations, report_path = self.analyze_board(board)
        
        # Display GUI
        gui = SmartAssistantGUI(None, warnings, score, grade, recommendations, report_path)
        gui.ShowModal()
        gui.Destroy()

    def analyze_board(self, board):
        warnings = []
        recommendations = []
        score = 100
        
        # 1. Tracks too thin (< 0.2mm)
        thin_track_threshold = pcbnew.FromMM(0.2)
        tracks = board.GetTracks()
        
        thin_tracks = 0
        vias_per_net = {}
        
        for track in tracks:
            if type(track) == pcbnew.PCB_TRACK:
                if track.GetWidth() < thin_track_threshold:
                    thin_tracks += 1
            elif type(track) == pcbnew.PCB_VIA:
                net_code = track.GetNetCode()
                if net_code > 0:
                    vias_per_net[net_code] = vias_per_net.get(net_code, 0) + 1
                    
        if thin_tracks > 0:
            warnings.append({"issue": f"{thin_tracks} tracks are too thin (< 0.2mm)", "severity": "Medium", "fix": "Increase track width for better manufacturability and lower impedance."})
            score -= min(15, thin_tracks * 2)
            recommendations.append(f"Widen {thin_tracks} thin tracks to at least 0.2mm.")

        # 2. Excessive vias on a signal path (> 10 vias per net)
        excessive_via_nets = 0
        for net_code, count in vias_per_net.items():
            if count > 10:
                excessive_via_nets += 1
                
        if excessive_via_nets > 0:
            warnings.append({"issue": f"{excessive_via_nets} nets have excessive vias (>10 vias)", "severity": "Medium", "fix": "Reroute nets to reduce via count, improving signal integrity."})
            score -= min(15, excessive_via_nets * 3)
            recommendations.append(f"Reduce via count on {excessive_via_nets} heavily routed nets.")

        # 3. Components placed too close together (< 0.1mm clearance)
        footprints = board.GetFootprints()
        close_components = 0
        
        inflation = pcbnew.FromMM(0.1)
        fps = []
        for fp in footprints:
            bb = fp.GetBoundingBox()
            bb.Inflate(inflation)
            fps.append(bb)
            
        for i in range(len(fps)):
            for j in range(i + 1, len(fps)):
                if fps[i].Intersects(fps[j]):
                    close_components += 1
                    
        if close_components > 0:
            warnings.append({"issue": f"{close_components} component pairs placed too close (< 0.1mm clearance)", "severity": "High", "fix": "Increase spacing between components to ensure reliable assembly."})
            score -= min(25, close_components * 4)
            recommendations.append(f"Reposition {close_components} closely packed component pairs.")

        # 4. Unconnected nets
        connectivity = board.GetConnectivity()
        unconnected_items = connectivity.GetUnconnectedEdges()
        num_unconnected = len(unconnected_items)
        
        if num_unconnected > 0:
            warnings.append({"issue": f"{num_unconnected} unconnected net edges found", "severity": "Critical", "fix": "Complete routing for all unconnected nets."})
            score -= min(30, num_unconnected * 5)
            recommendations.append(f"Route {num_unconnected} unconnected nets to complete the circuit.")

        # 5. Silkscreen overlapping pads
        pad_bboxes_top = []
        pad_bboxes_bot = []
        for fp in footprints:
            for pad in fp.Pads():
                if pad.IsOnLayer(pcbnew.F_Cu):
                    pad_bboxes_top.append(pad.GetBoundingBox())
                if pad.IsOnLayer(pcbnew.B_Cu):
                    pad_bboxes_bot.append(pad.GetBoundingBox())
                    
        drawings = board.GetDrawings()
        overlapping_silkscreen = 0
        for dwg in drawings:
            # PCB_TEXT and PCB_SHAPE check
            if type(dwg) in [pcbnew.PCB_TEXT, pcbnew.PCB_SHAPE]:
                layer = dwg.GetLayer()
                if layer == pcbnew.F_SilkS:
                    bb = dwg.GetBoundingBox()
                    for pbb in pad_bboxes_top:
                        if bb.Intersects(pbb):
                            overlapping_silkscreen += 1
                            break
                elif layer == pcbnew.B_SilkS:
                    bb = dwg.GetBoundingBox()
                    for pbb in pad_bboxes_bot:
                        if bb.Intersects(pbb):
                            overlapping_silkscreen += 1
                            break

        if overlapping_silkscreen > 0:
            warnings.append({"issue": f"{overlapping_silkscreen} silkscreen items overlapping pads", "severity": "Medium", "fix": "Move silkscreen text/shapes away from exposed copper pads."})
            score -= min(15, overlapping_silkscreen * 2)
            recommendations.append(f"Fix {overlapping_silkscreen} silkscreen items overlapping pads.")

        # Final Score & Grade
        score = max(0, score)
        if score >= 90:
            grade = "Excellent"
        elif score >= 70:
            grade = "Good"
        elif score >= 50:
            grade = "Needs Improvement"
        else:
            grade = "Critical"

        # Generate HTML Report
        board_path = board.GetFileName()
        if not board_path:
            report_path = os.path.join(os.path.expanduser("~"), "pcb_smart_assistant_report.html")
        else:
            report_dir = os.path.dirname(board_path)
            report_path = os.path.join(report_dir, "pcb_smart_assistant_report.html")

        self.generate_html_report(warnings, score, grade, recommendations, report_path)
        
        return warnings, score, grade, recommendations, report_path

    def generate_html_report(self, warnings, score, grade, recommendations, report_path):
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        color_map = {
            "Excellent": "#28a745",
            "Good": "#17a2b8",
            "Needs Improvement": "#ffc107",
            "Critical": "#dc3545"
        }
        score_color = color_map.get(grade, "#000")
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Intelligent PCB Design Recommendation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; color: #333; }}
        h1 {{ color: #0056b3; }}
        .summary-box {{ border: 1px solid #ccc; padding: 15px; border-radius: 5px; background: #f9f9f9; }}
        .score {{ font-size: 2em; font-weight: bold; color: {score_color}; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background-color: #0056b3; color: white; }}
        .severity-High {{ color: #dc3545; font-weight: bold; }}
        .severity-Medium {{ color: #ff8c00; font-weight: bold; }}
        .severity-Critical {{ color: #dc3545; font-weight: bold; text-transform: uppercase; }}
        .recommendation-list {{ font-size: 1.1em; }}
    </style>
</head>
<body>
    <h1>Intelligent PCB Design Recommendation Report</h1>
    <p><strong>Generated on:</strong> {date_str}</p>
    
    <div class="summary-box">
        <h2>PCB Warning Score</h2>
        <p class="score">{score} / 100 ({grade})</p>
        <p><strong>Total Issues Found:</strong> {len(warnings)}</p>
    </div>
    
    <h2>Top Recommendations</h2>
    <ul class="recommendation-list">
"""
        for rec in recommendations[:5]:
            html_content += f"        <li>{rec}</li>\n"
            
        if not recommendations:
            html_content += "        <li>No critical recommendations. Great job!</li>\n"

        html_content += """
    </ul>
    
    <h2>Detailed Warnings</h2>
"""
        if warnings:
            html_content += """
    <table>
        <tr>
            <th>Issue</th>
            <th>Severity</th>
            <th>Suggested Fix</th>
        </tr>
"""
            for w in warnings:
                html_content += f"""
        <tr>
            <td>{w['issue']}</td>
            <td class="severity-{w['severity']}">{w['severity']}</td>
            <td>{w['fix']}</td>
        </tr>"""
            html_content += "\n    </table>"
        else:
            html_content += "<p>No design warnings found.</p>"

        html_content += """
</body>
</html>
"""
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)
