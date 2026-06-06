"""
OPCB Health Analyzer — KiCad Action Plugin

Main entry point for the PCB Health Analyzer plugin.
Collects board statistics, computes health scores, runs the
AI Review Engine and Chat Assistant, and generates all reports
(TXT, HTML, JSON, and knowledge file).
"""

import pcbnew
import wx
import os
from .pcb_html_report import generate_html_report
from . import report_generator
from .pcb_chat_assistant import PCBChatAssistant


class OPCBHealthAnalyzer(pcbnew.ActionPlugin):

    def defaults(self):
        self.name = "OPCB Health Analyzer"
        self.category = "PCB Analysis"
        self.description = "Analyzes PCB statistics and generates AI-assisted health report"

    def calculate_health_score(self, tracks, vias, unconnected_pads, overlaps):

        score = 100

        if tracks < 20:
            score -= 20

        if vias > 50:
            score -= 10

        score -= unconnected_pads * 5
        score -= overlaps * 5

        return max(score, 0)

    def Run(self):

        board = pcbnew.GetBoard()

        if board is None:
            wx.MessageBox(
                "No PCB Board Opened!",
                "OPCB Health Analyzer"
            )
            return

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
                    width = round(pcbnew.ToMM(item.GetWidth()), 3)
                    via_sizes.append(width)
                    if width < 0.4:
                        small_vias += 1
                        
                    via_type = item.GetViaType()
                    if via_type in via_types:
                        via_types[via_type] += 1
                    # Track counts by type using resolved constants
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
                    width = round(pcbnew.ToMM(item.GetWidth()), 3)
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

            avg_track_width = round(
                sum(track_widths) / len(track_widths),
                3
            )

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

        # ---------------------------------------------------------- #
        #  AI PCB Knowledge Assistant integration                      #
        # ---------------------------------------------------------- #

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

        # ---------------------------------------------------------- #
        #  Text report (original + AI summary appended)                #
        # ---------------------------------------------------------- #

        report = f"""
================================
      PCB HEALTH REPORT
================================

Board File:
{board.GetFileName()}

GENERAL STATISTICS
--------------------------------

Total Tracks       : {tracks}
Total Vias         : {vias}
Total Footprints   : {footprints}
Copper Layers      : {copper_layers}

LAYER STATISTICS
--------------------------------

Top Layer Tracks   : {top_tracks}
Bottom Layer Tracks: {bottom_tracks}
Other Layers       : {layer_tracks}

NET ANALYSIS
--------------------------------

Total Nets         : {total_nets}

COMPONENT ANALYSIS
--------------------------------

Top Components     : {top_components}
Bottom Components  : {bottom_components}

TRACK STATISTICS
--------------------------------

Minimum Width      : {min_track_width} mm
Maximum Width      : {max_track_width} mm
Average Width      : {avg_track_width} mm

VIA STATISTICS
--------------------------------

Smallest Via       : {min_via_size} mm
Largest Via        : {max_via_size} mm
Through Vias       : {through_vias_count}
Micro Vias         : {micro_vias_count}
Blind/Buried Vias  : {blind_vias_count}

DRC SUMMARY
--------------------------------

Unconnected Pads   : {unconnected_pads}
Possible Overlaps  : {overlaps}

DESIGN QUALITY ANALYSIS
--------------------------------
Min Track Width: {min_track_width} mm
Max Track Width: {max_track_width} mm
Average Track Width: {avg_track_width} mm

Via Count: {vias}
Complexity Score: {complexity_score}/100

Warnings:
{warnings_text.strip()}

HEALTH ANALYSIS
--------------------------------

Health Score       : {health_score}/100
Health Grade       : {grade}
Board Status       : {board_status}

================================

{ai_summary}

================================
Analysis Complete
================================
"""

        board_file = board.GetFileName()

        if board_file:

            report_path = os.path.join(
                os.path.dirname(board_file),
                "pcb_health_report.txt"
            )

        else:

            report_path = "pcb_health_report.txt"

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
            
        stats = {
            "health_score": health_score,
            "grade": grade,
            "board_status": board_status,
            "tracks": tracks,
            "vias": vias,
            "footprints": footprints,
            "total_nets": total_nets,
            "copper_layers": copper_layers,
            "complexity_score": complexity_score,
            "drc_summary": {
                "unconnected_pads": unconnected_pads,
                "possible_overlaps": overlaps,
                "thin_tracks_warning": thin_tracks,
                "small_vias_warning": small_vias
            }
        }
        report_generator.generate_report(stats)

        html_report_path = os.path.join(
            os.path.dirname(report_path),
            "pcb_health_report.html"
        )

        generate_html_report(
            html_report_path,
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
            ai_review=ai_review,
        )

        # ---------------------------------------------------------- #
        #  Knowledge file export (Task 6)                              #
        # ---------------------------------------------------------- #

        output_dir = os.path.dirname(report_path) if report_path else "."
        report_generator.generate_knowledge_file(
            board_name=board_file,
            stats=ai_stats,
            ai_review=ai_review,
            output_dir=output_dir,
        )

        # ---------------------------------------------------------- #
        #  Completion dialog                                           #
        # ---------------------------------------------------------- #

        fab_status = ai_review.get("fabrication_status", "UNKNOWN")
        quality_level = ai_review.get("quality_level", "")

        wx.MessageBox(
            f"PCB Health Report Generated Successfully!\n\n"
            f"Health Score : {health_score}/100\n"
            f"Grade        : {grade}\n"
            f"Status       : {board_status}\n"
            f"AI Quality   : {quality_level}\n"
            f"Fabrication  : {fab_status}\n\n"
            f"Generated Files:\n"
            f"  pcb_health_report.txt\n"
            f"  pcb_health_report.html\n"
            f"  reports/board_knowledge.json",
            "OPCB Health Analyzer"
        )