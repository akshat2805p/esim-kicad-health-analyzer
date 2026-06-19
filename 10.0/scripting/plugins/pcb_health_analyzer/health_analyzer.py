"""
OPCB Health Analyzer — KiCad Action Plugin

Main entry point for the PCB Health Analyzer plugin.
Connects the KiCad interface to the PCB Design Copilot panel.
"""

import pcbnew
import wx
import os
from .pcb_html_report import generate_html_report
from . import report_generator
from .pcb_chat_assistant import PCBChatAssistant

def to_mm(val):
    if hasattr(pcbnew, 'ToMM'):
        return getattr(pcbnew, 'ToMM')(val)
    return val / 1000000.0

def from_mm(val):
    if hasattr(pcbnew, 'FromMM'):
        return getattr(pcbnew, 'FromMM')(val)
    return int(val * 1000000.0)



class OPCBHealthAnalyzer(pcbnew.ActionPlugin):

    def defaults(self):
        self.name = "PCB Design Copilot"
        self.category = "PCB Analysis"
        self.description = "Real-time AI-assisted PCB Design Copilot panel"

    def calculate_health_score(self, tracks, vias, unconnected_pads, overlaps):
        score = 100

        if tracks < 20:
            score -= 20

        if vias > 50:
            score -= 10

        score -= unconnected_pads * 5
        score -= overlaps * 5

        return max(score, 0)

    def analyze_board(self, board):
        """
        Extract all board statistics, run calculations, and evaluate
        quality assessment and AI review.
        """
        if board is None:
            return {}

        tracks = 0
        vias = 0
        top_tracks = 0
        bottom_tracks = 0
        unconnected_pads = 0
        overlaps = 0

        thin_tracks = 0
        small_vias = 0

        # Via type constants vary across KiCad versions — resolve safely
        _VIA_THROUGH = getattr(pcbnew, 'VIATYPE_THROUGH',
                        getattr(pcbnew, 'VIA_THROUGH', None))
        _VIA_BLIND   = getattr(pcbnew, 'VIATYPE_BLIND_BURIED',
                        getattr(pcbnew, 'VIA_BLIND_BURIED', None))
        _VIA_MICRO   = getattr(pcbnew, 'VIATYPE_MICROVIA',
                        getattr(pcbnew, 'VIA_MICROVIA', None))

        via_types = {}
        if _VIA_THROUGH is not None:
            via_types[_VIA_THROUGH] = 0
        if _VIA_BLIND is not None:
            via_types[_VIA_BLIND] = 0
        if _VIA_MICRO is not None:
            via_types[_VIA_MICRO] = 0

        through_vias_count = 0
        micro_vias_count = 0
        blind_vias_count = 0
        layer_tracks = {}

        track_widths = []
        via_sizes = []

        all_tracks = list(board.GetTracks())

        for item in all_tracks:
            if isinstance(item, pcbnew.PCB_VIA):
                vias += 1
                try:
                    width = round(to_mm(item.GetWidth()), 3)
                    via_sizes.append(width)
                    if width < 0.4:
                        small_vias += 1
                        
                    via_type = item.GetViaType()
                    if via_type in via_types:
                        via_types[via_type] += 1
                    if _VIA_THROUGH is not None and via_type == _VIA_THROUGH:
                        through_vias_count += 1
                    elif _VIA_MICRO is not None and via_type == _VIA_MICRO:
                        micro_vias_count += 1
                    elif _VIA_BLIND is not None and via_type == _VIA_BLIND:
                        blind_vias_count += 1
                except:
                    pass
            else:
                tracks += 1
                try:
                    width = round(to_mm(item.GetWidth()), 3)
                    track_widths.append(width)
                    if width < 0.25:
                        thin_tracks += 1
                except:
                    pass

                try:
                    layer = item.GetLayer()
                    layer_name = board.GetLayerName(layer)
                    layer_tracks[layer_name] = layer_tracks.get(layer_name, 0) + 1

                    if layer == pcbnew.F_Cu:
                        top_tracks += 1
                    elif layer == pcbnew.B_Cu:
                        bottom_tracks += 1
                except:
                    pass

        for footprint in board.GetFootprints():
            try:
                for pad in footprint.Pads():
                    if pad.GetNetCode() == 0:
                        unconnected_pads += 1
            except:
                pass

        for i in range(len(all_tracks)):
            for j in range(i + 1, len(all_tracks)):
                try:
                    if all_tracks[i].GetStart() == all_tracks[j].GetStart():
                        overlaps += 1
                except:
                    pass

        footprints = len(list(board.GetFootprints()))

        try:
            copper_layers = board.GetCopperLayerCount()
        except:
            copper_layers = 0

        try:
            total_nets = board.GetNetCount()
        except:
            total_nets = 0

        top_components = 0
        bottom_components = 0

        for fp in board.GetFootprints():
            try:
                if fp.GetLayer() == pcbnew.F_Cu:
                    top_components += 1
                else:
                    bottom_components += 1
            except:
                pass

        if track_widths:
            min_track_width = min(track_widths)
            max_track_width = max(track_widths)
            avg_track_width = round(sum(track_widths) / len(track_widths), 3)
        else:
            min_track_width = 0
            max_track_width = 0
            avg_track_width = 0

        if via_sizes:
            min_via_size = min(via_sizes)
            max_via_size = max(via_sizes)
        else:
            min_via_size = 0
            max_via_size = 0

        complexity_score_raw = (
            (tracks * 0.1) +
            (vias * 0.5) +
            (total_nets * 1.5) +
            (copper_layers * 5)
        )
        complexity_score = min(int(complexity_score_raw), 100)

        health_score = self.calculate_health_score(
            tracks,
            vias,
            unconnected_pads,
            overlaps
        )

        if health_score >= 90:
            grade = "A"
            board_status = "EXCELLENT"
        elif health_score >= 80:
            grade = "B"
            board_status = "GOOD"
        elif health_score >= 70:
            grade = "C"
            board_status = "FAIR"
        elif health_score >= 60:
            grade = "D"
            board_status = "NEEDS REVIEW"
        else:
            grade = "F"
            board_status = "CRITICAL"
            
        warnings_text = ""
        if thin_tracks > 0:
            warnings_text += f"- {thin_tracks} tracks below recommended width\n"
        if small_vias > 0:
            warnings_text += f"- {small_vias} very small vias detected\n"
        if not warnings_text:
            warnings_text = "- No warnings"

        # Board dimensions and area
        try:
            bbox = board.GetBoardEdgesBoundingBox()
            board_width_mm = to_mm(bbox.GetWidth())
            board_height_mm = to_mm(bbox.GetHeight())
            board_area_cm2 = (board_width_mm * board_height_mm) / 100.0
        except Exception:
            board_width_mm = 0.0
            board_height_mm = 0.0
            board_area_cm2 = 0.0

        # Congestion scoring
        total_track_length_mm = 0.0
        for item in board.GetTracks():
            if not isinstance(item, pcbnew.PCB_VIA):
                try:
                    length = item.GetLength()
                except AttributeError:
                    start = item.GetStart()
                    end = item.GetEnd()
                    length = ((start.x - end.x)**2 + (start.y - end.y)**2)**0.5
                total_track_length_mm += to_mm(length)

        layers_count = copper_layers if copper_layers > 0 else 2
        if board_area_cm2 > 0:
            congestion_score = total_track_length_mm / (board_area_cm2 * layers_count)
        else:
            congestion_score = 0.0

        if congestion_score > 50.0:
            congestion_level = "High"
        elif congestion_score > 20.0:
            congestion_level = "Moderate"
        else:
            congestion_level = "Low"

        # Cost estimation
        base_cost = 5.0
        area_surcharge = 0.0
        if board_area_cm2 > 100.0:
            area_surcharge = (board_area_cm2 - 100.0) * 0.15

        layer_surcharge = 0.0
        if copper_layers > 2:
            if copper_layers <= 4:
                layer_surcharge = 25.0
            else:
                layer_surcharge = 55.0

        via_surcharge = (micro_vias_count * 0.10) + (blind_vias_count * 0.15)
        if vias > 150:
            via_surcharge += (vias - 150) * 0.02

        thin_track_surcharge = 8.0 if thin_tracks > 0 else 0.0
        estimated_cost = base_cost + area_surcharge + layer_surcharge + via_surcharge + thin_track_surcharge

        # Build stats dict for the AI engine
        ai_stats = {
            "tracks": tracks,
            "vias": vias,
            "health_score": health_score,
            "unconnected_pads": unconnected_pads,
            "drc_errors": overlaps,
            "thin_tracks": thin_tracks,
            "small_vias": small_vias,
            "footprints": footprints,
            "total_nets": total_nets,
            "copper_layers": copper_layers,
            "complexity_score": complexity_score,
        }

        # Run AI analysis
        assistant = PCBChatAssistant()
        ai_review = assistant.get_ai_review(ai_stats)
        ai_summary = assistant.generate_response(ai_stats)

        # Merge all stats into a single dictionary
        stats = {
            "health_score": health_score,
            "grade": grade,
            "board_status": board_status,
            "tracks": tracks,
            "vias": vias,
            "top_tracks": top_tracks,
            "bottom_tracks": bottom_tracks,
            "layer_tracks": layer_tracks,
            "unconnected_pads": unconnected_pads,
            "overlaps": overlaps,
            "thin_tracks": thin_tracks,
            "small_vias": small_vias,
            "through_vias_count": through_vias_count,
            "micro_vias_count": micro_vias_count,
            "blind_vias_count": blind_vias_count,
            "footprints": footprints,
            "copper_layers": copper_layers,
            "total_nets": total_nets,
            "top_components": top_components,
            "bottom_components": bottom_components,
            "min_track_width": min_track_width,
            "max_track_width": max_track_width,
            "avg_track_width": avg_track_width,
            "min_via_size": min_via_size,
            "max_via_size": max_via_size,
            "complexity_score": complexity_score,
            "warnings_text": warnings_text,
            "board_width_mm": board_width_mm,
            "board_height_mm": board_height_mm,
            "board_area_cm2": board_area_cm2,
            "congestion_score": congestion_score,
            "congestion_level": congestion_level,
            "estimated_cost": estimated_cost,
            "ai_review": ai_review,
            "ai_summary": ai_summary,
            "board_file": board.GetFileName()
        }

        return stats

    def export_reports(self, board, stats):
        """
        Generate and write .txt, .html and reports/board_knowledge.json files.
        """
        # 1. Text report writing
        report = f"""
================================
      PCB HEALTH REPORT
================================

Board File:
{stats["board_file"]}

GENERAL STATISTICS
--------------------------------

Total Tracks       : {stats["tracks"]}
Total Vias         : {stats["vias"]}
Total Footprints   : {stats["footprints"]}
Copper Layers      : {stats["copper_layers"]}

LAYER STATISTICS
--------------------------------

Top Layer Tracks   : {stats["top_tracks"]}
Bottom Layer Tracks: {stats["bottom_tracks"]}
Other Layers       : {stats["layer_tracks"]}

NET ANALYSIS
--------------------------------

Total Nets         : {stats["total_nets"]}

COMPONENT ANALYSIS
--------------------------------

Top Components     : {stats["top_components"]}
Bottom Components  : {stats["bottom_components"]}

TRACK STATISTICS
--------------------------------

Minimum Width      : {stats["min_track_width"]} mm
Maximum Width      : {stats["max_track_width"]} mm
Average Width      : {stats["avg_track_width"]} mm

VIA STATISTICS
--------------------------------

Smallest Via       : {stats["min_via_size"]} mm
Largest Via        : {stats["max_via_size"]} mm
Through Vias       : {stats["through_vias_count"]}
Micro Vias         : {stats["micro_vias_count"]}
Blind/Buried Vias  : {stats["blind_vias_count"]}

DRC SUMMARY
--------------------------------

Unconnected Pads   : {stats["unconnected_pads"]}
Possible Overlaps  : {stats["overlaps"]}

DESIGN QUALITY ANALYSIS
--------------------------------
Min Track Width: {stats["min_track_width"]} mm
Max Track Width: {stats["max_track_width"]} mm
Average Track Width: {stats["avg_track_width"]} mm

Via Count: {stats["vias"]}
Complexity Score: {stats["complexity_score"]}/100

Warnings:
{stats["warnings_text"].strip()}

HEALTH ANALYSIS
--------------------------------

Health Score       : {stats["health_score"]}/100
Health Grade       : {stats["grade"]}
Board Status       : {stats["board_status"]}

================================

{stats["ai_summary"]}

================================
Analysis Complete
================================
"""

        board_file = stats["board_file"]
        if board_file:
            report_path = os.path.join(
                os.path.dirname(board_file),
                "pcb_health_report.txt"
            )
        else:
            report_path = "pcb_health_report.txt"

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
            
        # 2. JSON legacy report writing
        legacy_stats = {
            "health_score": stats["health_score"],
            "grade": stats["grade"],
            "board_status": stats["board_status"],
            "tracks": stats["tracks"],
            "vias": stats["vias"],
            "footprints": stats["footprints"],
            "total_nets": stats["total_nets"],
            "copper_layers": stats["copper_layers"],
            "complexity_score": stats["complexity_score"],
            "drc_summary": {
                "unconnected_pads": stats["unconnected_pads"],
                "possible_overlaps": stats["overlaps"],
                "thin_tracks_warning": stats["thin_tracks"],
                "small_vias_warning": stats["small_vias"]
            }
        }
        report_generator.generate_report(legacy_stats)

        # 3. HTML report writing
        html_report_path = os.path.join(
            os.path.dirname(report_path),
            "pcb_health_report.html"
        )
        generate_html_report(
            html_report_path,
            stats["health_score"],
            stats["grade"],
            stats["board_status"],
            stats["tracks"],
            stats["vias"],
            stats["footprints"],
            stats["total_nets"],
            stats["min_track_width"],
            stats["max_track_width"],
            stats["avg_track_width"],
            stats["complexity_score"],
            stats["warnings_text"],
            ai_review=stats["ai_review"],
        )

        # 4. Knowledge file export
        output_dir = os.path.dirname(report_path) if report_path else "."
        ai_stats = {
            "tracks": stats["tracks"],
            "vias": stats["vias"],
            "health_score": stats["health_score"],
            "unconnected_pads": stats["unconnected_pads"],
            "drc_errors": stats["overlaps"],
            "thin_tracks": stats["thin_tracks"],
            "small_vias": stats["small_vias"],
            "footprints": stats["footprints"],
            "total_nets": stats["total_nets"],
            "copper_layers": stats["copper_layers"],
            "complexity_score": stats["complexity_score"],
        }
        knowledge_path = report_generator.generate_knowledge_file(
            board_name=board_file,
            stats=ai_stats,
            ai_review=stats["ai_review"],
            output_dir=output_dir,
        )

        return html_report_path, report_path, knowledge_path

    def Run(self):
        # Prevent duplicate panels
        for win in wx.GetTopLevelWindows():
            if getattr(win, "Name", "") == "PCBDesignCopilotFrame":
                win.Raise()
                return

        # Find the active KiCad PCB editor frame as parent
        parent = None
        for win in wx.GetTopLevelWindows():
            title = win.GetTitle().lower()
            if "pcbnew" in title or "pcb editor" in title:
                parent = win
                break

        # Import locally inside Run to prevent circular dependency
        from .gui import CopilotFrame
        frame = CopilotFrame(parent)
        frame.Show()