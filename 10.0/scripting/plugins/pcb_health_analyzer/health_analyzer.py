import pcbnew
import wx
import os
from .pcb_html_report import generate_html_report


class OPCBHealthAnalyzer(pcbnew.ActionPlugin):

    def defaults(self):
        self.name = "OPCB Health Analyzer"
        self.category = "PCB Analysis"
        self.description = "Analyzes PCB statistics and generates health report"

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

        track_widths = []
        via_sizes = []

        all_tracks = list(board.GetTracks())

        for item in all_tracks:

            if isinstance(item, pcbnew.PCB_VIA):

                vias += 1

                try:
                    via_sizes.append(
                        round(pcbnew.ToMM(item.GetWidth()), 3)
                    )
                except:
                    pass

            else:

                tracks += 1

                try:
                    track_widths.append(
                        round(pcbnew.ToMM(item.GetWidth()), 3)
                    )
                except:
                    pass

                try:
                    layer = item.GetLayer()

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

        complexity_score = (
            tracks +
            (vias * 2) +
            (total_nets * 3) +
            (footprints * 2)
        )

        complexity_score = min(complexity_score, 100)

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

DRC SUMMARY
--------------------------------

Unconnected Pads   : {unconnected_pads}
Possible Overlaps  : {overlaps}

ADVANCED ANALYSIS
--------------------------------

Complexity Score   : {complexity_score}/100

HEALTH ANALYSIS
--------------------------------

Health Score       : {health_score}/100
Health Grade       : {grade}
Board Status       : {board_status}

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
            total_nets
        )

        wx.MessageBox(
            f"PCB Health Report Generated Successfully!\n\n"
            f"Health Score : {health_score}/100\n"
            f"Grade        : {grade}\n"
            f"Status       : {board_status}\n\n"
            f"Generated Files:\n"
            f"pcb_health_report.txt\n"
            f"pcb_health_report.html",
            "OPCB Health Analyzer"
        )