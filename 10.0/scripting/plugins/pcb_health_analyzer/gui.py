"""
PCB Design Copilot GUI Panel

Defines the wxPython panel/frame interface for live PCB metrics,
cost estimation, congestion analysis, recommendations, and
the AI chat assistant.
"""
import wx
import wx.html
import pcbnew
import os
import datetime


class ScorePanel(wx.Panel):
    """
    Subpanel for displaying the health score circle, grade, and board status.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour(wx.Colour("#FFFFFF"))
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Rounded/Colored panel for score
        self.score_box = wx.Panel(self, size=(80, 80))
        self.score_box.SetBackgroundColour(wx.Colour("#10B981"))
        
        box_sizer = wx.BoxSizer(wx.VERTICAL)
        box_sizer.AddStretchSpacer()
        self.score_lbl = wx.StaticText(self.score_box, label="--")
        font_score = wx.Font(26, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.score_lbl.SetFont(font_score)
        self.score_lbl.SetForegroundColour(wx.Colour("#FFFFFF"))
        box_sizer.Add(self.score_lbl, 0, wx.ALIGN_CENTER)
        box_sizer.AddStretchSpacer()
        self.score_box.SetSizer(box_sizer)
        
        text_sizer = wx.BoxSizer(wx.VERTICAL)
        self.grade_lbl = wx.StaticText(self, label="Grade: --")
        font_grade = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.grade_lbl.SetFont(font_grade)
        self.grade_lbl.SetForegroundColour(wx.Colour("#1F2937"))
        
        self.status_lbl = wx.StaticText(self, label="SCANNING BOARD...")
        font_status = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.status_lbl.SetFont(font_status)
        self.status_lbl.SetForegroundColour(wx.Colour("#6B7280"))
        
        text_sizer.Add(self.grade_lbl, 0, wx.BOTTOM, 4)
        text_sizer.Add(self.status_lbl, 0)
        
        sizer.Add(self.score_box, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        sizer.Add(text_sizer, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        self.SetSizer(sizer)


class CopilotFrame(wx.Frame):
    """
    Floating frame for the PCB Design Copilot panel.
    """
    def __init__(self, parent):
        super().__init__(
            parent,
            title="PCB Design Copilot",
            size=(480, 680),
            style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT,
            name="PCBDesignCopilotFrame"
        )
        
        self.current_stats = None
        self._last_board_sig = None
        
        # Setup fonts
        self.font_title = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.font_header = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.font_value = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.font_muted = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        
        self.InitUI()
        
        # Start background timer (updates every 3 seconds)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimerTick, self.timer)
        self.timer.Start(3000)
        
        # Bind close event to stop timer and cleanup
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        # Initial statistics update
        self.UpdateStats(force=True)
        
    def InitUI(self):
        # Base panel
        base_panel = wx.Panel(self)
        base_panel.SetBackgroundColour(wx.Colour("#F3F4F6")) # Light gray background
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Header card (Slate Blue theme)
        header_panel = wx.Panel(base_panel)
        header_panel.SetBackgroundColour(wx.Colour("#1E293B"))
        header_sizer = wx.BoxSizer(wx.VERTICAL)
        
        title_lbl = wx.StaticText(header_panel, label="PCB DESIGN COPILOT")
        font_title_large = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_lbl.SetFont(font_title_large)
        title_lbl.SetForegroundColour(wx.Colour("#FFFFFF"))
        
        subtitle_lbl = wx.StaticText(header_panel, label="Real-time Assistant for FOSSEE/eSim")
        subtitle_lbl.SetFont(self.font_muted)
        subtitle_lbl.SetForegroundColour(wx.Colour("#94A3B8"))
        
        header_sizer.Add(title_lbl, 0, wx.ALL | wx.ALIGN_LEFT, 8)
        header_sizer.Add(subtitle_lbl, 0, wx.LEFT | wx.BOTTOM | wx.ALIGN_LEFT, 8)
        header_panel.SetSizer(header_sizer)
        
        # Add header to main sizer
        main_sizer.Add(header_panel, 0, wx.EXPAND)
        
        # Notebook (Tabs)
        self.notebook = wx.Notebook(base_panel)
        
        # ---- TAB 1: DASHBOARD ----
        self.tab_dash = wx.ScrolledWindow(self.notebook, style=wx.VSCROLL)
        self.tab_dash.SetScrollRate(0, 10)
        self.tab_dash.SetBackgroundColour(wx.Colour("#F3F4F6"))
        dash_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Score banner (Card 1)
        self.score_panel = ScorePanel(self.tab_dash)
        dash_sizer.Add(self.score_panel, 0, wx.EXPAND | wx.ALL, 10)
        
        # Metrics Card (Card 2)
        metrics_box = wx.StaticBox(self.tab_dash, label="Board Metrics")
        metrics_box.SetFont(self.font_header)
        metrics_sizer = wx.StaticBoxSizer(metrics_box, wx.VERTICAL)
        
        self.metrics_grid = wx.FlexGridSizer(cols=2, vgap=8, hgap=20)
        self.metrics_grid.AddGrowableCol(1)
        
        self.add_metric_row("Tracks (F/B layer):", "tracks_val")
        self.add_metric_row("Vias (Thr/Mic/Bld):", "vias_val")
        self.add_metric_row("Total Nets:", "nets_val")
        self.add_metric_row("Board Area (W x H):", "area_val")
        self.add_metric_row("Copper Layers:", "layers_val")
        
        metrics_sizer.Add(self.metrics_grid, 1, wx.EXPAND | wx.ALL, 8)
        dash_sizer.Add(metrics_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        # Smart Insights Card (Card 3)
        insights_box = wx.StaticBox(self.tab_dash, label="Smart Assistant Insights")
        insights_box.SetFont(self.font_header)
        insights_sizer = wx.StaticBoxSizer(insights_box, wx.VERTICAL)
        
        self.insights_grid = wx.FlexGridSizer(cols=2, vgap=8, hgap=20)
        self.insights_grid.AddGrowableCol(1)
        
        self.add_insight_row("DRC Errors/Warnings:", "drc_val")
        self.add_insight_row("Congestion Level:", "congestion_val")
        self.add_insight_row("Estimated Cost (5 pcs):", "cost_val")
        
        insights_sizer.Add(self.insights_grid, 1, wx.EXPAND | wx.ALL, 8)
        dash_sizer.Add(insights_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        # Suggestions Card (Card 4)
        sugg_box = wx.StaticBox(self.tab_dash, label="AI Recommendations")
        sugg_box.SetFont(self.font_header)
        sugg_sizer = wx.StaticBoxSizer(sugg_box, wx.VERTICAL)
        
        self.suggestions_box = wx.TextCtrl(
            self.tab_dash,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.NO_BORDER,
            size=(-1, 100)
        )
        self.suggestions_box.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.suggestions_box.SetFont(self.font_muted)
        
        sugg_sizer.Add(self.suggestions_box, 1, wx.EXPAND | wx.ALL, 5)
        dash_sizer.Add(sugg_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        # Actions Panel (Buttons)
        actions_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_refresh = wx.Button(self.tab_dash, label="Refresh Now")
        self.btn_refresh.Bind(wx.EVT_BUTTON, self.OnRefreshClick)
        
        self.btn_export = wx.Button(self.tab_dash, label="Export PDF/HTML")
        self.btn_export.Bind(wx.EVT_BUTTON, self.OnExportClick)
        
        actions_sizer.Add(self.btn_refresh, 1, wx.RIGHT | wx.EXPAND, 5)
        actions_sizer.Add(self.btn_export, 1, wx.LEFT | wx.EXPAND, 5)
        
        dash_sizer.Add(actions_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        self.tab_dash.SetSizer(dash_sizer)
        
        # ---- TAB 2: AI CHAT ASSISTANT ----
        self.tab_chat = wx.Panel(self.notebook)
        self.tab_chat.SetBackgroundColour(wx.Colour("#F3F4F6"))
        chat_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Chat log window (HtmlWindow)
        self.chat_log = wx.html.HtmlWindow(self.tab_chat, style=wx.html.HW_SCROLLBAR_AUTO)
        self.chat_log.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.clear_chat_history()
        
        chat_sizer.Add(self.chat_log, 1, wx.EXPAND | wx.ALL, 10)
        
        # Predefined Quick Questions
        qq_box = wx.StaticBox(self.tab_chat, label="Quick Design Questions")
        qq_box.SetFont(self.font_header)
        qq_sizer = wx.StaticBoxSizer(qq_box, wx.VERTICAL)
        
        qq_grid = wx.FlexGridSizer(cols=2, vgap=5, hgap=5)
        qq_grid.AddGrowableCol(0)
        qq_grid.AddGrowableCol(1)
        
        self.btn_q1 = wx.Button(self.tab_chat, label="Why is my health score low?")
        self.btn_q2 = wx.Button(self.tab_chat, label="What are major issues?")
        self.btn_q3 = wx.Button(self.tab_chat, label="How can I improve?")
        self.btn_q4 = wx.Button(self.tab_chat, label="Is it fabrication ready?")
        
        self.btn_q1.Bind(wx.EVT_BUTTON, lambda e: self.ask_assistant("Why is my health score low?"))
        self.btn_q2.Bind(wx.EVT_BUTTON, lambda e: self.ask_assistant("What are the major issues?"))
        self.btn_q3.Bind(wx.EVT_BUTTON, lambda e: self.ask_assistant("How can I improve the board?"))
        self.btn_q4.Bind(wx.EVT_BUTTON, lambda e: self.ask_assistant("Is this board ready for fabrication?"))
        
        qq_grid.Add(self.btn_q1, 1, wx.EXPAND)
        qq_grid.Add(self.btn_q2, 1, wx.EXPAND)
        qq_grid.Add(self.btn_q3, 1, wx.EXPAND)
        qq_grid.Add(self.btn_q4, 1, wx.EXPAND)
        
        qq_sizer.Add(qq_grid, 1, wx.EXPAND | wx.ALL, 5)
        chat_sizer.Add(qq_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        # Custom input box
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.chat_input = wx.TextCtrl(self.tab_chat, style=wx.TE_PROCESS_ENTER)
        self.chat_input.Bind(wx.EVT_TEXT_ENTER, self.OnCustomAsk)
        
        self.btn_send = wx.Button(self.tab_chat, label="Ask AI")
        self.btn_send.Bind(wx.EVT_BUTTON, self.OnCustomAsk)
        
        self.btn_clear = wx.Button(self.tab_chat, label="Clear")
        self.btn_clear.Bind(wx.EVT_BUTTON, self.OnClearChat)
        
        input_sizer.Add(self.chat_input, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        input_sizer.Add(self.btn_send, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        input_sizer.Add(self.btn_clear, 0, wx.ALIGN_CENTER_VERTICAL)
        
        chat_sizer.Add(input_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        self.tab_chat.SetSizer(chat_sizer)
        
        # Add tabs to notebook
        self.notebook.AddPage(self.tab_dash, "Dashboard Monitor")
        self.notebook.AddPage(self.tab_chat, "AI Copilot Chat")
        
        main_sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
        base_panel.SetSizer(main_sizer)
        
        # Status Bar
        self.status_bar = self.CreateStatusBar(1)
        self.status_bar.SetStatusText("Initializing real-time scan...")
        
    def add_metric_row(self, label, attr_name):
        lbl = wx.StaticText(self.tab_dash, label=label)
        lbl.SetFont(self.font_muted)
        val = wx.StaticText(self.tab_dash, label="--")
        val.SetFont(self.font_value)
        val.SetForegroundColour(wx.Colour("#1F2937"))
        setattr(self, attr_name, val)
        self.metrics_grid.Add(lbl, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        self.metrics_grid.Add(val, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        
    def add_insight_row(self, label, attr_name):
        lbl = wx.StaticText(self.tab_dash, label=label)
        lbl.SetFont(self.font_muted)
        val = wx.StaticText(self.tab_dash, label="--")
        val.SetFont(self.font_value)
        setattr(self, attr_name, val)
        self.insights_grid.Add(lbl, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        self.insights_grid.Add(val, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        
    def clear_chat_history(self):
        self.chat_history = []
        welcome_html = (
            "<body bgcolor='#FFFFFF'>"
            "<font face='Segoe UI' color='#1E293B'>"
            "<h3>&#129302; PCB Design Copilot Chat Assistant</h3>"
            "<p>I can help you review design quality, analyze health score drops, suggest routing enhancements, and assess fabrication readiness.</p>"
            "<p>Select a quick question below or ask a custom question in the box.</p>"
            "<hr color='#E2E8F0'>"
            "</font></body>"
        )
        self.chat_log.SetPage(welcome_html)
        
    def OnClose(self, event):
        # Stop background timer before destroying window
        if self.timer.IsRunning():
            self.timer.Stop()
        event.Skip()
        
    def OnTimerTick(self, event):
        self.UpdateStats(force=False)
        
    def OnRefreshClick(self, event):
        self.UpdateStats(force=True)
        wx.MessageBox("Board statistics refreshed successfully!", "PCB Design Copilot", wx.OK | wx.ICON_INFORMATION)
        
    def OnExportClick(self, event):
        board = pcbnew.GetBoard()
        if board is None or self.current_stats is None:
            wx.MessageBox("No active board data to export!", "PCB Design Copilot", wx.OK | wx.ICON_ERROR)
            return
            
        from .health_analyzer import OPCBHealthAnalyzer
        analyzer = OPCBHealthAnalyzer()
        
        try:
            report_paths = analyzer.export_reports(board, self.current_stats)
            wx.MessageBox(
                f"PCB Health Reports generated successfully!\n\n"
                f"Files written:\n"
                f"  1. {os.path.basename(report_paths[0])} (HTML)\n"
                f"  2. {os.path.basename(report_paths[1])} (Text)\n"
                f"  3. {os.path.basename(report_paths[2])} (JSON Knowledge)\n\n"
                f"Location: {os.path.dirname(report_paths[0])}",
                "Export Complete",
                wx.OK | wx.ICON_INFORMATION
            )
        except Exception as e:
            wx.MessageBox(f"Failed to export reports: {str(e)}", "Export Failed", wx.OK | wx.ICON_ERROR)

    def UpdateStats(self, force=False):
        board = pcbnew.GetBoard()
        if board is None:
            self.status_bar.SetStatusText("No open PCB board found.")
            return
            
        try:
            filename = board.GetFileName()
            tracks = len(board.GetTracks())
            footprints = len(board.GetFootprints())
            nets = board.GetNetCount()
            bbox = board.GetBoardEdgesBoundingBox()
            bbox_sig = (bbox.GetX(), bbox.GetY(), bbox.GetWidth(), bbox.GetHeight())
        except Exception as e:
            # Safe ignore if board state is transient
            return
            
        current_sig = (filename, tracks, footprints, nets, bbox_sig)
        if not force and current_sig == self._last_board_sig:
            return
            
        self._last_board_sig = current_sig
        
        from .health_analyzer import OPCBHealthAnalyzer
        analyzer = OPCBHealthAnalyzer()
        try:
            stats = analyzer.analyze_board(board)
            self.current_stats = stats
            self.UpdateUI(stats)
        except Exception as e:
            self.status_bar.SetStatusText(f"Scan failed: {str(e)}")
            
    def UpdateUI(self, stats):
        # 1. Update score banner
        score = stats["health_score"]
        self.score_panel.score_lbl.SetLabel(str(score))
        self.score_panel.grade_lbl.SetLabel(f"Grade: {stats['grade']}")
        self.score_panel.status_lbl.SetLabel(stats['board_status'])
        
        # Color score box based on score
        if score >= 90:
            color = "#10B981" # Green
        elif score >= 75:
            color = "#F59E0B" # Amber
        else:
            color = "#EF4444" # Red
            
        self.score_panel.score_box.SetBackgroundColour(wx.Colour(color))
        self.score_panel.status_lbl.SetForegroundColour(wx.Colour(color))
        self.score_panel.score_box.Layout()
        
        # 2. Update metrics values
        top_tracks = stats.get("top_tracks", 0)
        bottom_tracks = stats.get("bottom_tracks", 0)
        self.tracks_val.SetLabel(f"{stats['tracks']} (F.Cu: {top_tracks}, B.Cu: {bottom_tracks})")
        
        through = stats.get("through_vias_count", 0)
        micro = stats.get("micro_vias_count", 0)
        blind = stats.get("blind_vias_count", 0)
        self.vias_val.SetLabel(f"{stats['vias']} (Thr: {through}, Mic: {micro}, Bld: {blind})")
        
        self.nets_val.SetLabel(str(stats["total_nets"]))
        
        w_mm = stats.get("board_width_mm", 0.0)
        h_mm = stats.get("board_height_mm", 0.0)
        area_cm2 = stats.get("board_area_cm2", 0.0)
        self.area_val.SetLabel(f"{area_cm2:.2f} cm² ({w_mm:.1f} x {h_mm:.1f} mm)")
        
        self.layers_val.SetLabel(f"{stats['copper_layers']} Layers")
        
        # 3. Update smart insights values
        unconnected = stats.get("unconnected_pads", 0)
        overlaps = stats.get("overlaps", 0)
        total_drc = unconnected + overlaps
        self.drc_val.SetLabel(str(total_drc))
        if total_drc > 0:
            self.drc_val.SetForegroundColour(wx.Colour("#EF4444"))
        else:
            self.drc_val.SetForegroundColour(wx.Colour("#10B981"))
            
        congestion = stats.get("congestion_score", 0.0)
        level = stats.get("congestion_level", "Low")
        self.congestion_val.SetLabel(f"{level} ({congestion:.1f} mm/cm²)")
        if level == "High":
            self.congestion_val.SetForegroundColour(wx.Colour("#EF4444"))
        elif level == "Moderate":
            self.congestion_val.SetForegroundColour(wx.Colour("#F59E0B"))
        else:
            self.congestion_val.SetForegroundColour(wx.Colour("#10B981"))
            
        cost = stats.get("estimated_cost", 5.0)
        self.cost_val.SetLabel(f"${cost:.2f}")
        self.cost_val.SetForegroundColour(wx.Colour("#3B82F6"))
        
        # 4. Update recommendations
        recs = stats.get("ai_review", {}).get("recommendations", [])
        if recs:
            recs_text = "\n".join(f"• {r}" for r in recs)
        else:
            recs_text = "• No recommendations. The design is in excellent shape!"
        self.suggestions_box.SetValue(recs_text)
        
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.status_bar.SetStatusText(f"Last sync: {now} | Live monitoring active")
        
        self.tab_dash.Layout()
        self.Layout()
        
    def ask_assistant(self, question):
        if self.current_stats is None:
            wx.MessageBox("Wait for a valid board scan first!", "PCB Design Copilot", wx.OK | wx.ICON_WARNING)
            return
            
        from .pcb_chat_assistant import PCBChatAssistant
        assistant = PCBChatAssistant()
        answer = assistant.answer_question(question, self.current_stats)
        
        # Append to log
        q_html = f"<div style='margin-bottom:10px;'><b><font face='Segoe UI' color='#3B82F6'>User Question:</font></b> {question}</div>"
        
        # Convert response text newlines to HTML paragraphs
        formatted_answer = answer.replace("\n", "<br>")
        a_html = f"<div style='margin-bottom:15px; background-color:#F8FAFC; padding:8px; border-radius:4px;'><b><font face='Segoe UI' color='#1E293B'>AI Copilot:</font></b><br><font face='Segoe UI' color='#334155'>{formatted_answer}</font></div>"
        
        self.chat_history.append(q_html + a_html)
        
        # Update html page
        full_page = (
            "<body bgcolor='#FFFFFF'>"
            "<font face='Segoe UI' color='#1E293B'>"
            "<h3>&#129302; PCB Design Copilot Chat Assistant</h3>"
            "<hr color='#E2E8F0'>"
            + "".join(self.chat_history) +
            "</font></body>"
        )
        self.chat_log.SetPage(full_page)
        
        # Scroll to bottom
        try:
            self.chat_log.Scroll(0, 10000)
        except:
            pass
            
    def OnCustomAsk(self, event):
        question = self.chat_input.GetValue().strip()
        if not question:
            return
            
        self.chat_input.SetValue("")
        
        # Map custom question keywords to predefined Qs
        q_lower = question.lower()
        matched_q = None
        if "health" in q_lower or "score" in q_lower:
            matched_q = "Why is my health score low?"
        elif "issue" in q_lower or "error" in q_lower or "drc" in q_lower or "overlap" in q_lower:
            matched_q = "What are the major issues?"
        elif "improve" in q_lower or "fix" in q_lower or "recommend" in q_lower or "tip" in q_lower or "suggest" in q_lower:
            matched_q = "How can I improve the board?"
        elif "fabrication" in q_lower or "fab" in q_lower or "ready" in q_lower or "manufactur" in q_lower:
            matched_q = "Is this board ready for fabrication?"
            
        if matched_q:
            self.ask_assistant(matched_q)
        else:
            # Fallback custom response explaining what to ask
            q_html = f"<div style='margin-bottom:10px;'><b><font face='Segoe UI' color='#3B82F6'>User Question:</font></b> {question}</div>"
            a_html = (
                "<div style='margin-bottom:15px; background-color:#F8FAFC; padding:8px; border-radius:4px;'>"
                "<b><font face='Segoe UI' color='#1E293B'>AI Copilot:</font></b><br>"
                "<font face='Segoe UI' color='#EF4444'>I'm sorry, I didn't recognize that question.</font><br>"
                "<font face='Segoe UI' color='#334155'>I can answer questions regarding health scores, design issues, improvements, or fabrication readiness. "
                "Try asking or clicking one of the predefined questions below!</font></div>"
            )
            self.chat_history.append(q_html + a_html)
            full_page = (
                "<body bgcolor='#FFFFFF'>"
                "<font face='Segoe UI' color='#1E293B'>"
                "<h3>&#129302; PCB Design Copilot Chat Assistant</h3>"
                "<hr color='#E2E8F0'>"
                + "".join(self.chat_history) +
                "</font></body>"
            )
            self.chat_log.SetPage(full_page)
            try:
                self.chat_log.Scroll(0, 10000)
            except:
                pass
                
    def OnClearChat(self, event):
        self.clear_chat_history()