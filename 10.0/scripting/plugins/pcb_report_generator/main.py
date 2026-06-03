import pcbnew
import wx
import os

from .analyzer import analyze_components
from .report_writer import generate_report

class PCBReportGeneratorPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "PCB Report Generator"
        self.category = "PCB Analysis"
        self.description = "Generates a PCB design rule report from sample data"

    def Run(self):
        try:
            # Get the directory where this plugin is located
            plugin_dir = os.path.dirname(__file__)
            
            # Use absolute paths relative to the plugin directory
            sample_data_path = os.path.join(plugin_dir, "sample_data.txt")
            report_path = os.path.join(plugin_dir, "report.txt")
            
            if not os.path.exists(sample_data_path):
                wx.MessageBox(f"Data file not found:\n{sample_data_path}", "Error")
                return

            with open(sample_data_path, "r") as file:
                data = file.readlines()

            results = analyze_components(data)
            report = generate_report(results)

            with open(report_path, "w") as file:
                file.write(report)

            wx.MessageBox(f"Report generated successfully!\n\nSaved to:\n{report_path}", "PCB Report Generator")
            
        except Exception as e:
            wx.MessageBox(f"An error occurred:\n{str(e)}", "Error")