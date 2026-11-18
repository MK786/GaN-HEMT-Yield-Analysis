# Automated GaN HEMT Yield Analysis Pipeline
## Overview
This repository contains a production-grade, Object-Oriented Python suite designed to automate the extraction, statistical analysis, and spatial mapping of Wide Bandgap (GaN) semiconductor devices from raw SMU measurement data. 

## Key Features
* **Automated Parameter Extraction:** Calculates Threshold Voltage ($V_{th}$) via maximum transconductance ($G_m$) extrapolation, On-Resistance ($R_{on}$) via linear-region derivative, Subthreshold Swing (SS), and ON/OFF current ratios.
* **Hysteresis Error Handling:** Automatically isolates forward voltage sweeps in transfer characteristics to prevent divide-by-zero errors associated with dual-sweep measurement hysteresis.
* **Dual-Axis Visualization:** Generates publication-ready semi-logarithmic transfer curves ($I_d$-$V_g$) overlaid with linear transconductance.
* **Spatial Wafer Mapping:** Utilizes Regular Expressions (Regex) to extract die X/Y coordinates from test equipment file names, generating spatial heatmaps to diagnose process non-uniformities across the wafer.

## Technology Stack
* **Language:** Python 3
* **Libraries:** Pandas (Data manipulation), NumPy (Vectorized gradients/derivatives), Matplotlib & Seaborn (Statistical visualization).
* **Architecture:** Object-Oriented Programming (OOP) using a modular `GaN_Device` class for scalable yield analysis.

## Visual Outputs
*(Upload your images to the repository and link them here to show off the Transfer Curve and the Wafer Map)*
