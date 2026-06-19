import pcbnew
import os
import wx

def to_mm(val):
    if hasattr(pcbnew, 'ToMM'):
        return getattr(pcbnew, 'ToMM')(val)
    return val / 1000000.0

def from_mm(val):
    if hasattr(pcbnew, 'FromMM'):
        return getattr(pcbnew, 'FromMM')(val)
    return int(val * 1000000.0)


class AdvancedPCBChecker(pcbnew.ActionPlugin):

    def defaults(self):
        self.name = "Advanced PCB Checker"
        self.category = "PCB Analysis"
        self.description = "Checks PCB for common issues and generates report"

    def Run(self):

        board = pcbnew.GetBoard()

        tracks = board.GetTracks()
        footprints = board.GetFootprints()

        total_tracks = 0
        total_vias = 0

        warnings = []

        # -------------------------
        # TRACK CHECKS
        # -------------------------
        for item in tracks:

            # Track count
            if isinstance(item, pcbnew.PCB_TRACK):
                total_tracks += 1

                width_mm = to_mm(item.GetWidth())

                # Thin track check
                if width_mm < 0.25:
                    pos = item.GetStart()
                    warnings.append(
                        f"Thin Track at X={to_mm(pos.x):.2f}, "
                        f"Y={to_mm(pos.y):.2f}"
                    )

            # Via count
            if isinstance(item, pcbnew.PCB_VIA):
                total_vias += 1

                drill_mm = to_mm(item.GetDrillValue())

                # Small drill check
                if drill_mm < 0.2:
                    pos = item.GetPosition()
                    warnings.append(
                        f"Small Via Drill at X={to_mm(pos.x):.2f}, "
                        f"Y={to_mm(pos.y):.2f}"
                    )

        # -------------------------
        # FOOTPRINT CHECKS
        # -------------------------
        board_box = board.GetBoardEdgesBoundingBox()

        for fp in footprints:

            fp_box = fp.GetBoundingBox()

            if not board_box.Contains(fp_box):
                warnings.append(
                    f"Footprint outside board: {fp.GetReference()}"
                )

        # -------------------------
        # REPORT GENERATION
        # -------------------------
        report = []
        report.append("PCB ANALYSIS REPORT")
        report.append("----------------------")
        report.append(f"Total Tracks: {total_tracks}")
        report.append(f"Total Vias: {total_vias}")
        report.append("")

        report.append("WARNINGS:")
        if warnings:
            for i, warning in enumerate(warnings, 1):
                report.append(f"{i}. {warning}")
        else:
            report.append("No issues found.")

        # Save report
        project_path = os.path.dirname(board.GetFileName())
        report_path = os.path.join(project_path, "pcb_report.txt")

        with open(report_path, "w") as file:
            file.write("\n".join(report))

        # Popup message
        wx.MessageBox(
            f"PCB Check Complete!\n\nReport saved at:\n{report_path}",
            "Advanced PCB Checker",
            wx.OK | wx.ICON_INFORMATION
)

AdvancedPCBChecker().register()