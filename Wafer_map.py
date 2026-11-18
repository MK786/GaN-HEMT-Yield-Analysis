import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_wafer_map(excel_path, parameter='Vth (V)', cmap='coolwarm'):
    """
    Reads the device summary Excel file and generates a spatial Wafer Map.
    """
    # 1. Load the data
    df = pd.read_excel(excel_path)
    
    # Check if coordinate data exists
    if 'Die X' not in df.columns or df['Die X'].isnull().all():
        print("Error: No X/Y coordinate data found in the Excel file.")
        return
        
    # 2. Set up the Wafer Map canvas
    fig, ax = plt.subplots(figsize=(8, 7))
    
    # 3. Plot the dies (Scatter Plot)
    scatter = ax.scatter(df['Die X'], df['Die Y'], 
                         c=df[parameter], cmap=cmap, 
                         s=600, marker='s', edgecolors='black', linewidth=1.5)
    
    # 4. Add the color scale bar
    cbar = plt.colorbar(scatter)
    cbar.set_label(parameter, fontsize=12, fontweight='bold')
    
    # 5. Formatting to make it look like a physical wafer
    ax.set_title(f"Wafer Map: {parameter} Distribution", fontsize=16, fontweight='bold')
    ax.set_xlabel("Die X Coordinate", fontsize=12, fontweight='bold')
    ax.set_ylabel("Die Y Coordinate", fontsize=12, fontweight='bold')
    
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    # Optional: Draw a circle to represent the physical edge of the wafer
    center_x = df['Die X'].mean()
    center_y = df['Die Y'].mean()
    radius = max(df['Die X'].max() - center_x, df['Die Y'].max() - center_y) + 1
    wafer_edge = plt.Circle((center_x, center_y), radius, color='gray', fill=False, linestyle='--', linewidth=2)
    ax.add_patch(wafer_edge)
    
    ax.set_aspect('equal')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    
    # Save the map
    save_dir = os.path.dirname(excel_path)
    plt.savefig(os.path.join(save_dir, f"WaferMap_{parameter.split(' ')[0]}.png"), dpi=300)
    plt.show()

# =====================================================================
# RUN THE GENERATOR
# =====================================================================
if __name__ == "__main__":
    # Ensure this matches your actual folder path
    folder_path = r"C:\Users\MKMRITUNJAY\OneDrive - Teknologian Tutkimuskeskus VTT\Silvaco\Wibase_TCAD\Experiemental_data"
    
    # Update this to match the EXACT name of the latest Excel file you generated
    summary_file = os.path.join(folder_path, "Device_Parameters_Summary.xlsx") 
    
    # Generate the map for Threshold Voltage
    plot_wafer_map(summary_file, parameter='Vth (V)', cmap='coolwarm')