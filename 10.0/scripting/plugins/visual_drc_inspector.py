import pcbnew
import wx
import os

def to_mm(val):
    if hasattr(pcbnew, 'ToMM'):
        return getattr(pcbnew, 'ToMM')(val)
    return val / 1000000.0

def from_mm(val):
    if hasattr(pcbnew, 'FromMM'):
        return getattr(pcbnew, 'FromMM')(val)
    return int(val * 1000000.0)


def make_point(x, y):
    if hasattr(pcbnew, 'VECTOR2I'):
        return pcbnew.VECTOR2I(int(x), int(y))
    return pcbnew.wxPoint(int(x), int(y))

class VisualDRCInspector(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "OPCB Visual DRC Inspector"
        self.category = "Inspection"
        self.description = "Visually highlights potential PCB issues directly on the board"
        self.show_toolbar_button = True

    def Run(self):
        board = pcbnew.GetBoard()
        if not board:
            wx.MessageBox("No board found.", "Error", wx.OK | wx.ICON_ERROR)
            return

        issues = []
        
        bounding_box = board.GetBoardEdgesBoundingBox()
        track_threshold_nm = from_mm(0.2)
        short_track_threshold_nm = from_mm(0.1)

        vias = [t for t in board.GetTracks() if isinstance(t, pcbnew.PCB_VIA)]
        tracks = [t for t in board.GetTracks() if isinstance(t, pcbnew.PCB_TRACK)]

        # Collect all connection points
        points_map = {}
        for t in tracks:
            for p in (t.GetStart(), t.GetEnd()):
                key = (p.x, p.y)
                points_map[key] = points_map.get(key, 0) + 1
        
        for p in board.GetFootprints():
            for pad in p.Pads():
                pos = pad.GetPosition()
                key = (pos.x, pos.y)
                points_map[key] = points_map.get(key, 0) + 1

        for item in tracks:
            width = item.GetWidth()
            length = item.GetLength()
            start = item.GetStart()
            end = item.GetEnd()

            # Thin tracks
            if width < track_threshold_nm:
                issues.append({
                    "type": "Thin Track",
                    "pos": start,
                    "severity": "MEDIUM",
                    "fix": "Increase track width"
                })
            
            # Short tracks
            if length > 0 and length < short_track_threshold_nm:
                issues.append({
                    "type": "Very Short Track",
                    "pos": start,
                    "severity": "LOW",
                    "fix": "Remove or merge track segment"
                })

            # Outside Outline
            if bounding_box.GetWidth() > 0 and bounding_box.GetHeight() > 0:
                if not bounding_box.Contains(start) and not bounding_box.Contains(end):
                    issues.append({
                        "type": "Outside Outline",
                        "pos": start,
                        "severity": "CRITICAL",
                        "fix": "Move inside board outline"
                    })

            # Unconnected segments
            start_key = (start.x, start.y)
            end_key = (end.x, end.y)
            if points_map.get(start_key, 0) == 1 and points_map.get(end_key, 0) == 1:
                issues.append({
                    "type": "Unconnected Segment",
                    "pos": start,
                    "severity": "HIGH",
                    "fix": "Connect or remove track"
                })

        # Floating vias
        for via in vias:
            pos = via.GetPosition()
            key = (pos.x, pos.y)
            if points_map.get(key, 0) == 0:
                issues.append({
                    "type": "Floating Via",
                    "pos": pos,
                    "severity": "HIGH",
                    "fix": "Remove or connect via"
                })

        # Add visual markers
        for issue in issues:
            pos = issue['pos']
            
            # Draw circle
            circle = pcbnew.PCB_SHAPE(board)
            circle.SetShape(pcbnew.SHAPE_T_CIRCLE)
            circle.SetCenter(pos)
            # define radius by setting end point
            circle.SetEnd(make_point(pos.x + from_mm(2), pos.y))
            circle.SetLayer(pcbnew.Dwgs_User)
            circle.SetWidth(int(from_mm(0.2)))
            board.Add(circle)
            
            # Draw text label
            text = pcbnew.PCB_TEXT(board)
            text.SetText(f"⚠ {issue['type']}")
            text.SetPosition(make_point(pos.x + from_mm(3), pos.y))
            text.SetLayer(pcbnew.Dwgs_User)
            text.SetTextSize(make_point(from_mm(1.5), from_mm(1.5)))
            board.Add(text)

        # Output folder
        project_dir = os.path.dirname(board.GetFileName())
        if not project_dir:
            project_dir = os.path.expanduser("~")

        txt_path = os.path.join(project_dir, "visual_inspection_report.txt")
        html_path = os.path.join(project_dir, "visual_inspection_report.html")

        # AI Recommendations
        recommendations = []
        thin_tracks = sum(1 for i in issues if i["type"] == "Thin Track")
        floating_vias = sum(1 for i in issues if i["type"] == "Floating Via")
        unconnected = sum(1 for i in issues if i["type"] == "Unconnected Segment")
        
        if thin_tracks > 0:
            recommendations.append("• Increase track width near power net to reduce impedance.")
        if floating_vias > 0:
            recommendations.append("• Reduce via count in power section or remove isolated vias.")
        if unconnected > 0:
            recommendations.append("• Connect or remove floating track segments.")
        recommendations.append("• Route differential pairs together.")
        recommendations.append("• Improve copper balance on bottom layer.")

        counts = {}
        for issue in issues:
            counts[issue["type"]] = counts.get(issue["type"], 0) + 1

        # Generate txt
        report_txt = "PCB Visual Inspection Complete\n\n"
        for k, v in counts.items():
            report_txt += f"{k}s: {v}\n"
        report_txt += f"\nTotal Issues: {len(issues)}\n\nDetailed Issues:\n"
        for issue in issues:
            report_txt += f"- {issue['type']} at ({to_mm(issue['pos'].x):.2f}, {to_mm(issue['pos'].y):.2f}) mm. Severity: {issue['severity']}. Fix: {issue['fix']}\n"
        
        report_txt += "\nAI Recommendation:\n\n"
        for rec in recommendations:
            report_txt += f"{rec}\n"

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(report_txt)

        # Generate HTML
        html = f"<html><head><title>Visual Inspection Report</title></head><body style='font-family: sans-serif;'>"
        html += "<h1>PCB Visual Inspection Complete</h1><ul>"
        for k, v in counts.items():
            html += f"<li><b>{k}s:</b> {v}</li>"
        html += f"</ul><p><b>Total Issues:</b> {len(issues)}</p>"
        html += "<h2>Detailed Issues</h2><table border='1' cellpadding='5' style='border-collapse: collapse;'>"
        html += "<tr style='background-color: #f2f2f2;'><th>Type</th><th>X (mm)</th><th>Y (mm)</th><th>Severity</th><th>Suggested Fix</th></tr>"
        for issue in issues:
            html += f"<tr><td>{issue['type']}</td><td>{to_mm(issue['pos'].x):.2f}</td><td>{to_mm(issue['pos'].y):.2f}</td><td>{issue['severity']}</td><td>{issue['fix']}</td></tr>"
        html += "</table><h2>AI Recommendation</h2><ul>"
        for rec in recommendations:
            html += f"<li>{rec}</li>"
        html += "</ul></body></html>"

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        # Refresh board
        pcbnew.Refresh()

        # Popup msg
        msg = "PCB Visual Inspection Complete\n\n"
        for k, v in counts.items():
            msg += f"{k}s: {v}\n"
        msg += f"\nTotal Issues: {len(issues)}\n"
        
        wx.MessageBox(msg, "OPCB Visual DRC Inspector", wx.OK | wx.ICON_INFORMATION)

VisualDRCInspector().register()
