import wx
import webbrowser
import os

class SmartAssistantGUI(wx.Dialog):
    def __init__(self, parent, warnings, score, grade, recommendations, report_path):
        super().__init__(parent, title="Smart PCB Design Assistant", size=(500, 450))
        
        self.report_path = report_path
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Header
        header = wx.StaticText(panel, label="PCB Health Analyzer Results")
        header.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        vbox.Add(header, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=15)
        
        # Score & Warnings Count
        score_box = wx.StaticBox(panel, label="Overall PCB Warning Score")
        score_sizer = wx.StaticBoxSizer(score_box, wx.VERTICAL)
        
        grade_color = wx.Colour(0, 0, 0)
        if grade == "Excellent": grade_color = wx.Colour(40, 167, 69)
        elif grade == "Good": grade_color = wx.Colour(23, 162, 184)
        elif grade == "Needs Improvement": grade_color = wx.Colour(255, 193, 7)
        elif grade == "Critical": grade_color = wx.Colour(220, 53, 69)
        
        score_text = wx.StaticText(panel, label=f"{score} / 100  ({grade})")
        score_text.SetForegroundColour(grade_color)
        score_text.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        warnings_text = wx.StaticText(panel, label=f"Total Issues Found: {len(warnings)}")
        warnings_text.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        score_sizer.Add(score_text, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        score_sizer.Add(warnings_text, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)
        vbox.Add(score_sizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=15)
        
        # Top Recommendations
        rec_box = wx.StaticBox(panel, label="Top Recommendations")
        rec_sizer = wx.StaticBoxSizer(rec_box, wx.VERTICAL)
        
        if recommendations:
            for rec in recommendations[:5]:
                txt = wx.StaticText(panel, label=f"• {rec}")
                txt.Wrap(440)
                rec_sizer.Add(txt, flag=wx.LEFT | wx.BOTTOM, border=5)
        else:
            txt = wx.StaticText(panel, label="No major recommendations. Layout looks solid!")
            rec_sizer.Add(txt, flag=wx.LEFT | wx.BOTTOM, border=5)
            
        vbox.Add(rec_sizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=15)
        
        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        view_btn = wx.Button(panel, label="View Full Report")
        view_btn.Bind(wx.EVT_BUTTON, self.on_view_report)
        btn_sizer.Add(view_btn, flag=wx.RIGHT, border=15)
        
        close_btn = wx.Button(panel, label="Close")
        close_btn.Bind(wx.EVT_BUTTON, self.on_close)
        btn_sizer.Add(close_btn)
        
        vbox.Add(btn_sizer, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=15)
        
        panel.SetSizer(vbox)
        self.Centre()

    def on_view_report(self, event):
        if os.path.exists(self.report_path):
            webbrowser.open(f"file://{self.report_path}")
        else:
            wx.MessageBox("Report file not found.", "Error", wx.ICON_ERROR)
            
    def on_close(self, event):
        self.Close()
