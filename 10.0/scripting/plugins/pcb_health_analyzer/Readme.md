# eSim KiCad Health Analyzer

A powerful KiCad Action Plugin developed for eSim/FOSSEE workflows that performs comprehensive PCB design quality analysis and generates detailed engineering health reports.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Module Documentation](#module-documentation)
- [Report Details](#report-details)
- [Technologies](#technologies)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The PCB Health Analyzer is a specialized KiCad plugin that automatically analyzes PCB designs and generates comprehensive health reports. It evaluates multiple aspects of PCB quality including track routing, via placement, component distribution, and design rule compliance.

**Developed for:** eSim/FOSSEE educational and professional workflows

## ✨ Features

### Core Analysis Capabilities

- **PCB Statistics Analysis**
  - Track count and layer-wise distribution
  - Via analysis and placement
  - Footprint and component tracking
  - Net connectivity analysis
  - Copper layer information

- **Design Quality Inspection**
  - Unconnected pad detection
  - Track overlap detection
  - Component placement analysis
  - Layer distribution validation

- **Health Scoring System**
  - Automated health score calculation (0-100)
  - Board status classification (EXCELLENT, GOOD, NEEDS REVIEW, CRITICAL)
  - Penalty-based scoring system

- **Report Generation**
  - Formatted text reports
  - JSON export capability
  - Automatic file generation
  - DRC summary integration

### Advanced Features

- **Layer-wise PCB Statistics**
  - Top layer (F.Cu) track analysis
  - Bottom layer (B.Cu) track analysis
  - Multi-layer copper tracking

- **Component Analysis**
  - Top-side component count
  - Bottom-side component count
  - Component distribution analysis

- **DRC Integration**
  - DRC summary generation
  - Overlap detection
  - Unconnected pad tracking

- **Modular Plugin Architecture**
  - Separable analysis engines
  - Extensible report generation
  - Clean plugin entry point

## 🔧 Installation

### Prerequisites

- KiCad 6.0 or later
- Python 3.6+
- wxPython library

### Installation Steps

1. **Locate KiCad Scripting Plugins Directory**
   ```
   Windows: %APPDATA%/KiCad/scripting/plugins
   Linux: ~/.config/kicad/scripting/plugins
   macOS: ~/Library/Application Support/KiCad/scripting/plugins
   ```

2. **Copy Plugin Files**
   ```bash
   cp -r pcb_health_analyzer <kicad_plugins_directory>/
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   The plugin requires:
   - wxPython (for GUI components)
   - KiCad pcbnew API (bundled with KiCad)

4. **Restart KiCad**
   Launch KiCad PCB Editor for the plugin to be recognized.

## 📖 Usage

### Running the Plugin

1. **Open a PCB file** in KiCad's PCB Editor (pcbnew)
2. **Access the plugin:**
   - Go to `Tools → External Plugins → OPCB Health Analyzer`
   - Or use the plugin menu in the toolbar

3. **View the Report**
   - A popup dialog shows the health score and status
   - A detailed text report is generated in the same directory as the PCB file
   - Report filename: `pcb_health_report.txt`

### Report Output Example

```
================================
      PCB HEALTH REPORT
================================

Board File: /path/to/design.kicad_pcb

-------------------------------
GENERAL STATISTICS
-------------------------------
Total Tracks       : 156
Total Vias         : 42
Total Footprints   : 48
Copper Layers      : 2

-------------------------------
LAYER STATISTICS
-------------------------------
Top Layer Tracks   : 98
Bottom Layer Tracks: 58

-------------------------------
NET ANALYSIS
-------------------------------
Total Nets         : 45

-------------------------------
COMPONENT ANALYSIS
-------------------------------
Total Components   : 48
Top Components     : 32
Bottom Components  : 16

-------------------------------
DRC SUMMARY
-------------------------------
Unconnected Pads   : 0
Possible Overlaps  : 1

-------------------------------
HEALTH ANALYSIS
-------------------------------
Health Score       : 85/100
Board Status       : GOOD

================================
```

## 🏗️ Architecture

The plugin follows a modular, layered architecture:

```
KiCad PCB Editor
    ↓
Plugin Entry Layer (__init__.py)
    ↓
Analysis Engine (health_analyzer.py)
    ↓
Core Analyzers (analyzer_core.py, drc_summary.py)
    ↓
Report Generation (report_generator.py)
    ↓
GUI Layer (gui.py)
    ↓
Output (Text & JSON Reports)
```

## 📦 Module Documentation

### `health_analyzer.py` - Main Plugin Entry
**Class:** `OPCBHealthAnalyzer` (extends `pcbnew.ActionPlugin`)

**Key Methods:**
- `defaults()` - Sets plugin metadata
- `analyze_board()` - Main analysis engine
- `calculate_health_score()` - Scoring algorithm
- `Run()` - Plugin execution entry point

**Functionality:**
- Comprehensive board analysis
- Track and via enumeration
- Layer-wise statistics collection
- Component distribution analysis
- DRC metrics calculation
- Health score generation
- Report generation and export

### `analyzer_core.py` - Statistics Engine
**Class:** `PCBStatistics`

**Methods:**
- `get_statistics()` - Gathers PCB statistics

**Returns Dictionary:**
```python
{
    "Tracks": int,
    "Footprints": int,
    "Drawings": int,
    "Vias": int,
    "Nets": int
}
```

### `drc_summary.py` - Design Rule Check Analysis
**Class:** `DRCSummary`

**Methods:**
- `count_tracks()` - Returns total track count
- `count_vias()` - Returns total via count
- `count_unconnected_pads()` - Identifies floating pads
- `detect_overlaps()` - Finds track overlaps
- `generate_report()` - Creates DRC summary report

### `report_generator.py` - Report Export
**Function:** `generate_report(stats)`

**Features:**
- JSON report generation
- Structured data export
- Report file management
- Output validation

### `gui.py` - User Interface Layer
**Status:** Framework for future development

**Planned Features:**
- Health score visualization
- Interactive PCB inspection
- Export options dialog
- Risk highlighting
- Statistical dashboard

### `__init__.py` - Plugin Registration
Registers the `OPCBHealthAnalyzer` plugin with KiCad on import.

## 📊 Report Details

### Health Score Calculation

The health score is calculated using a penalty-based system:

```
Initial Score: 100

Penalties Applied:
- Tracks < 20              : -20 points
- Vias > 50                : -10 points
- Each unconnected pad     : -5 points
- Each detected overlap    : -5 points

Final Score: Maximum of (calculated, 0)
Range: 0-100
```

### Board Status Classification

| Score Range | Status | Meaning |
|-------------|--------|---------|
| 90-100 | EXCELLENT | Design meets all best practices |
| 70-89 | GOOD | Design is solid with minor issues |
| 50-69 | NEEDS REVIEW | Design has significant issues |
| 0-49 | CRITICAL | Design requires immediate attention |

### Report Content

Each generated report includes:

1. **General Statistics** - Track, via, footprint, and layer counts
2. **Layer Statistics** - Top and bottom layer track distribution
3. **Net Analysis** - Total connected nets
4. **Component Analysis** - Component distribution across layers
5. **DRC Summary** - Design rule violations
6. **Health Analysis** - Score and board status

## 🛠️ Technologies

- **Python 3.6+** - Core programming language
- **KiCad pcbnew API** - PCB data access and manipulation
- **wxPython** - GUI toolkit for dialogs and notifications
- **JSON** - Structured data export
- **Git/GitHub** - Version control

## 🚀 Future Enhancements

### Planned Features

- **Advanced Scoring System**
  - Electromagnetic analysis weighting
  - Thermal distribution assessment
  - Signal integrity checks

- **Enhanced GUI Dashboard**
  - Real-time visualization of health metrics
  - Interactive PCB layer viewer
  - Comparative analysis tools

- **DRC Enhancement**
  - Trace width validation
  - Spacing rule checking
  - Via size optimization

- **AI-Assisted Suggestions**
  - Machine learning-based recommendations
  - Design pattern recognition
  - Automatic routing suggestions

- **Export Formats**
  - HTML report generation
  - PDF export with charts
  - CSV data export

- **Integration Features**
  - Automated CI/CD pipeline integration
  - Git commit hooks
  - Cloud-based report storage

## 👥 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review the architecture guide in `/docs`

