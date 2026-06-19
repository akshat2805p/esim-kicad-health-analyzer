import pcbnew
import os
import wx
from .report_generator import generate_text_report
from .html_generator import generate_html_report

def to_mm(val):
    if hasattr(pcbnew, 'ToMM'):
        return getattr(pcbnew, 'ToMM')(val)
    return val / 1000000.0

def from_mm(val):
    if hasattr(pcbnew, 'FromMM'):
        return getattr(pcbnew, 'FromMM')(val)
    return int(val * 1000000.0)


class OPCBDesignRuleChecker(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "OPCB Design Rule Checker"
        self.category = "Inspection"
        self.description = "Automatically detects common PCB design issues and generates a detailed report."
        self.show_toolbar_button = True 
        
    def Run(self):
        board = pcbnew.GetBoard()
        if not board:
            wx.MessageBox("No board loaded.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Settings for DRC
        track_min_width_mm = 0.2
        via_min_diameter_mm = 0.4
        
        report_data = {
            'track_threshold': track_min_width_mm,
            'via_threshold': via_min_diameter_mm,
            'board_width': 0.0,
            'board_height': 0.0,
            'board_area': 0.0,
            'total_tracks': 0,
            'total_vias': 0,
            'small_tracks': [],
            'small_vias': [],
            'layer_stats': {}
        }
        
        # 1. Board Dimension Analyzer
        try:
            bbox = board.GetBoardEdgesBoundingBox()
            width = to_mm(bbox.GetWidth())
            height = to_mm(bbox.GetHeight())
            report_data['board_width'] = width
            report_data['board_height'] = height
            report_data['board_area'] = width * height
        except Exception:
            report_data['board_width'] = 0.0
            report_data['board_height'] = 0.0
            report_data['board_area'] = 0.0

        # 2. Track & Via Analysis
        tracks = board.GetTracks()
        for track in tracks:
            item_type = track.Type()
            layer_id = track.GetLayer()
            
            if hasattr(board, 'GetLayerName'):
                layer_name = board.GetLayerName(layer_id)
            else:
                layer_name = pcbnew.Board_GetLayerName(board, layer_id)
            
            # Update Layer Usage
            if board.IsCopperLayer(layer_id):
                report_data['layer_stats'][layer_name] = report_data['layer_stats'].get(layer_name, 0) + 1

            if item_type == pcbnew.PCB_TRACE_T:
                report_data['total_tracks'] += 1
                width_mm = to_mm(track.GetWidth())
                if width_mm < track_min_width_mm:
                    pos = track.GetPosition()
                    report_data['small_tracks'].append({
                        'x': to_mm(pos.x),
                        'y': to_mm(pos.y),
                        'width': width_mm
                    })
            elif item_type == pcbnew.PCB_VIA_T:
                report_data['total_vias'] += 1
                width_mm = to_mm(track.GetWidth())
                if width_mm < via_min_diameter_mm:
                    pos = track.GetPosition()
                    report_data['small_vias'].append({
                        'x': to_mm(pos.x),
                        'y': to_mm(pos.y),
                        'width': width_mm
                    })

        # Add other objects (e.g. pads) to layer usage if desired
        for footprint in board.GetFootprints():
            for pad in footprint.Pads():
                for layer_id in pad.GetLayerSet().Seq():
                    if board.IsCopperLayer(layer_id):
                        if hasattr(board, 'GetLayerName'):
                            layer_name = board.GetLayerName(layer_id)
                        else:
                            layer_name = pcbnew.Board_GetLayerName(board, layer_id)
                        report_data['layer_stats'][layer_name] = report_data['layer_stats'].get(layer_name, 0) + 1

        # Generate Reports
        board_path = board.GetFileName()
        if not board_path:
            # Fallback to home dir if board is unsaved
            board_dir = os.path.expanduser("~")
        else:
            board_dir = os.path.dirname(board_path)
            
        txt_output = os.path.join(board_dir, "drc_report.txt")
        html_output = os.path.join(board_dir, "drc_report.html")
        
        generate_text_report(report_data, txt_output)
        generate_html_report(report_data, html_output)
        
        wx.MessageBox(f"DRC Analysis Complete!\n\nReports saved to:\n- {txt_output}\n- {html_output}", 
                      "OPCB Design Rule Checker", wx.OK | wx.ICON_INFORMATION)
