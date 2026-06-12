import pcbnew
import os
import webbrowser
import wx

from . import graph_builder
from . import html_exporter
from . import report_generator

class DependencyVisualizerPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Dependency Visualizer"
        self.category = "Analysis"
        self.description = "Generates an interactive dependency graph of components and nets"
        self.show_toolbar_button = True
        
        # Determine the path for the icon
        plugin_dir = os.path.dirname(__file__)
        self.icon_file_name = os.path.join(plugin_dir, 'icons', 'icon.png')

    def Run(self):
        board = pcbnew.GetBoard()
        if not board:
            wx.MessageBox("No board open", "Error", wx.OK | wx.ICON_ERROR)
            return

        plugin_dir = os.path.dirname(__file__)
        reports_dir = os.path.join(plugin_dir, 'reports')
        
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
            
        html_path = os.path.join(reports_dir, 'dependency_graph.html')
        json_path = os.path.join(reports_dir, 'dependency_report.json')

        try:
            # Build Graph
            G = graph_builder.build_dependency_graph(board)
            
            # Generate Report
            stats = report_generator.generate_report(G, json_path)
            
            # Export to HTML
            html_exporter.export_to_html(G, html_path)
            
            # Notify User
            msg = f"Analysis Complete!\n\nComponents: {stats['components']}\nNets: {stats['nets']}\nConnections: {stats['connections']}\nMost Connected: {stats['most_connected']}"
            wx.MessageBox(msg, "Dependency Visualizer", wx.OK | wx.ICON_INFORMATION)
            
            # Open the HTML report in default browser
            webbrowser.open(f"file://{html_path}")
            
        except Exception as e:
            wx.MessageBox(f"An error occurred: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

# Register the plugin
DependencyVisualizerPlugin().register()
