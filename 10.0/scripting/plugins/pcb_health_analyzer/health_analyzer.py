import pcbnew
import wx
import os


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

    def analyze_board(self, board):

        tracks = 0
        vias = 0
        top_tracks = 0
        bottom_tracks = 0
        unconnected_pads = 0
        overlaps = 0

        all_tracks = list(board.GetTracks())

        for item in all_tracks:

            if isinstance(item, pcbnew.PCB_TRACK):
                tracks += 1

                try:
                    layer_name = item.GetLayerName()

                    if layer_name == "F.Cu":
                        top_tracks += 1

                    elif layer_name == "B.Cu":
                        bottom_tracks += 1
                except:
                    pass

            if isinstance(item, pcbnew.PCB_VIA):
                vias += 1

        for footprint in board.GetFootprints():
            for pad in footprint.Pads():

                if pad.GetNetCode() == 0:
                    unconnected_pads += 1

        for i in range(len(all_tracks)):
            for j in range(i + 1, len(all_tracks)):

                try:
                    if all_tracks[i].GetStart() == all_tracks[j].GetStart():
                        overlaps += 1
                except:
                    pass

        footprints = len(list(board.GetFootprints()))
        copper_layers = board.GetCopperLayerCount()

        # NET ANALYSIS
        total_nets = 0

        try:
            nets = board.GetNetsByName()
            total_nets = len(nets)
        except:
            pass

        # COMPONENT ANALYSIS
        total_components = footprints

        top_components = 0
        bottom_components = 0

        for fp in board.GetFootprints():

            try:
                if fp.GetLayerName() == "F.Cu":
                    top_components += 1
                else:
                    bottom_components += 1
            except:
                pass

        health_score = self.calculate_health_score(
            tracks,
            vias,
            unconnected_pads,
            overlaps
        )

        if health_score >= 90:
            board_status = "EXCELLENT"
        elif health_score >= 70:
            board_status = "GOOD"
        elif health_score >= 50:
            board_status = "NEEDS REVIEW"
        else:
            board_status = "CRITICAL"

        report = f"""
================================
      PCB HEALTH REPORT
================================

Board File:
{board.GetFileName()}

-------------------------------
GENERAL STATISTICS
-------------------------------

Total Tracks       : {tracks}
Total Vias         : {vias}
Total Footprints   : {footprints}
Copper Layers      : {copper_layers}

-------------------------------
LAYER STATISTICS
-------------------------------

Top Layer Tracks   : {top_tracks}
Bottom Layer Tracks: {bottom_tracks}

-------------------------------
NET ANALYSIS
-------------------------------

Total Nets         : {total_nets}

-------------------------------
COMPONENT ANALYSIS
-------------------------------

Total Components   : {total_components}
Top Components     : {top_components}
Bottom Components  : {bottom_components}

-------------------------------
DRC SUMMARY
-------------------------------

Unconnected Pads   : {unconnected_pads}
Possible Overlaps  : {overlaps}

-------------------------------
HEALTH ANALYSIS
-------------------------------

Health Score       : {health_score}/100
Board Status       : {board_status}

================================
Analysis Complete
================================
"""

        report_path = os.path.join(
            os.path.dirname(board.GetFileName()),
            "pcb_health_report.txt"
        )

        with open(report_path, "w") as f:
            f.write(report)

        wx.MessageBox(
            f"PCB Health Report Generated Successfully!\n\n"
            f"Health Score: {health_score}/100\n"
            f"Status: {board_status}\n\n"
            f"Report saved as:\npcb_health_report.txt",
            "OPCB Health Analyzer"
        )

    def Run(self):

        board = pcbnew.GetBoard()

        if board is None:
            wx.MessageBox(
                "No PCB Board Opened!",
                "OPCB Health Analyzer"
            )
            return

        self.analyze_board(board)


OPCBHealthAnalyzer().register()