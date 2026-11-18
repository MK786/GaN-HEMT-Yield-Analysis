import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import re  

# =====================================================================
# PART 1: THE BLUEPRINT (GaN_Device Class)
# =====================================================================
class GaN_Device:
    """
    A professional class to represent a single GaN HEMT device, 
    extract its electrical parameters, coordinates, and visualize its characteristics.
    """
    
    def __init__(self, device_name, transfer_path=None, output_path=None):
        self.name = device_name
        self.transfer_path = transfer_path
        self.output_path = output_path
        
        # --- Extract X and Y coordinates from the device name ---
        match = re.search(r'x(\d+)y(\d+)', device_name)
        if match:
            self.x = int(match.group(1))
            self.y = int(match.group(2))
        else:
            self.x = None
            self.y = None
        
        # Automatically load data into the object's memory
        self.df_transfer = pd.read_csv(transfer_path) if transfer_path else None
        self.df_output = pd.read_csv(output_path) if output_path else None

    # --- EXTRACTION METHODS ---
    
    def get_vth(self):
        if self.df_transfer is None: return np.nan
        max_idx = self.df_transfer['Run4 Vg'].idxmax()
        df_fwd = self.df_transfer.iloc[:max_idx + 1]
        
        Vg = df_fwd['Run4 Vg'].values
        Id = df_fwd['Run4 Id'].values
        
        Gm = np.gradient(Id, Vg)
        max_gm_idx = np.argmax(Gm)
        return Vg[max_gm_idx] - (Id[max_gm_idx] / Gm[max_gm_idx])

    def get_ss(self):
        if self.df_transfer is None: return np.nan
        max_idx = self.df_transfer['Run4 Vg'].idxmax()
        df_fwd = self.df_transfer.iloc[:max_idx + 1]
        
        Vg = df_fwd['Run4 Vg'].values
        Id = df_fwd['Run4 Id'].values
        
        valid_idx = Id > 0
        dlogId_dVg = np.gradient(np.log10(Id[valid_idx]), Vg[valid_idx])
        positive_slopes = dlogId_dVg[dlogId_dVg > 0]
        
        return (1 / np.max(positive_slopes)) * 1000 if len(positive_slopes) > 0 else np.nan

    def get_on_off_ratio(self):
        if self.df_transfer is None: return np.nan
        Id = self.df_transfer['Run4 Id'].values
        return np.max(Id) / np.min(Id[Id > 0])

    def get_ron(self):
        if self.df_output is None: return np.nan
        Vd = self.df_output['Run3 Vd'].values
        Id = self.df_output['Run3 Id'].values
        
        Ron_array = np.gradient(Vd, Id)
        idx_linear = (np.abs(Vd - 0.1)).argmin()
        return Ron_array[idx_linear]

    def get_summary_dictionary(self):
        """Packages all extracted parameters and coordinates for reporting."""
        return {
            'Device Name': self.name,
            'Die X': self.x,
            'Die Y': self.y,
            'Vth (V)': self.get_vth(),
            'Ron (Ohms)': self.get_ron(),
            'SS (mV/dec)': self.get_ss(),
            'ON/OFF Ratio': self.get_on_off_ratio()
        }

    # --- VISUALIZATION METHODS ---
    
    def plot_transfer(self, save_dir=None):
        """Plots the transfer characteristics of the device."""
        if self.df_transfer is None:
            print(f"No transfer data available for {self.name}.")
            return
            
        fig, ax = plt.subplots(figsize=(8, 6))
        run_vg_cols = [col for col in self.df_transfer.columns if ' Vg' in col]
        
        for vg_col in run_vg_cols:
            run_prefix = vg_col.split(' ')[0]
            id_col = f"{run_prefix} Id"
            if id_col in self.df_transfer.columns:
                ax.plot(self.df_transfer[vg_col], self.df_transfer[id_col], linewidth=2, label=run_prefix)
                
        ax.set_yscale('log')
        ax.set_xlabel('Gate Voltage (V)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Drain Current (A)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.grid(True, which="both", linestyle="--", alpha=0.5)
        ax.legend(fontsize=12, title='Measurement Runs')
        ax.set_title(f'Transfer Characteristics: {self.name}', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        if save_dir:
            plt.savefig(os.path.join(save_dir, f"{self.name}_TransferCurve.png"), dpi=300)
        plt.show()

    def plot_gm(self, run_col='Run4 Vg', save_dir=None):
        """Plots Drain Current and Transconductance (Gm) on a dual-axis graph."""
        if self.df_transfer is None:
            print(f"No transfer data available for {self.name}.")
            return
            
        id_col = run_col.replace('Vg', 'Id')
        if run_col not in self.df_transfer.columns or id_col not in self.df_transfer.columns:
            print(f"Data for {run_col} not found in device {self.name}.")
            return

        max_idx = self.df_transfer[run_col].idxmax()
        df_fwd = self.df_transfer.iloc[:max_idx + 1]
        
        Vg = df_fwd[run_col].values
        Id = df_fwd[id_col].values
        Gm = np.gradient(Id, Vg)
        
        fig, ax1 = plt.subplots(figsize=(8, 6))
        
        ax1.plot(Vg, Id, color='blue', linewidth=2, label=f'Id ({run_col.split(" ")[0]})')
        ax1.set_xlabel('Gate Voltage (V)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Drain Current (A)', color='blue', fontsize=14, fontweight='bold')
        ax1.tick_params(axis='y', labelcolor='blue', labelsize=12)
        ax1.tick_params(axis='x', labelsize=12)
        ax1.set_yscale('log')
        ax1.grid(True, linestyle="--", alpha=0.5)
        
        ax2 = ax1.twinx()
        ax2.plot(Vg, Gm, color='red', linewidth=2, linestyle='--', label='Gm')
        ax2.set_ylabel('Transconductance, Gm (A/V)', color='red', fontsize=14, fontweight='bold')
        ax2.tick_params(axis='y', labelcolor='red', labelsize=12)
        
        plt.title(f'Transfer & Transconductance: {self.name}', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if save_dir:
            plt.savefig(os.path.join(save_dir, f"{self.name}_Gm_Curve.png"), dpi=300)
        plt.show()


# =====================================================================
# PART 2: THE AUTOMATION WORKFLOW
# =====================================================================
if __name__ == "__main__":
    folder_path = r"C:\Users\MKMRITUNJAY\OneDrive - Teknologian Tutkimuskeskus VTT\Silvaco\Wibase_TCAD\Experiemental_data"

    transfer_files = glob.glob(os.path.join(folder_path, "*transferCombined*.csv"))
    output_files = glob.glob(os.path.join(folder_path, "*outputCombined*.csv"))

    results_list = []

    for trans_file in transfer_files:
        base_name = os.path.basename(trans_file).split('_transferCombined')[0]
        
        matching_out = [f for f in output_files if base_name in f]
        out_file = matching_out[0] if matching_out else None
        
        try:
            # 1. Initialize the device object
            my_device = GaN_Device(device_name=base_name, 
                                   transfer_path=trans_file, 
                                   output_path=out_file)
            
            # 2. Extract parameters and add to summary
            results_list.append(my_device.get_summary_dictionary())
            
            # 3. Generate and save the plots (NEWLY ADDED)
            my_device.plot_transfer(save_dir=folder_path)
            my_device.plot_gm(save_dir=folder_path)
            
            print(f"Successfully processed: {my_device.name}")
            
        except Exception as e:
            print(f"Error processing {base_name}: {e}")

    # Export the final yield summary table to Excel
    summary_df = pd.DataFrame(results_list)
    output_excel = os.path.join(folder_path, "Device_Parameters_Summary.xlsx")
    summary_df.to_excel(output_excel, index=False)
    print(f"\nYield summary saved to: {output_excel}")