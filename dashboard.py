import customtkinter as ctk
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----------------------------------------------------------------------
# Application Configuration & Theme Enforcement
# ----------------------------------------------------------------------
ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# ----------------------------------------------------------------------
# Simulated Data Service (Mock REST API Client)
# ----------------------------------------------------------------------

def fetch_edge_telemetry():
    """Returns static hardware metrics for UI layout purposes."""
    return {
        "cpu_usage": 45.2,
        "ram_usage": 68.9,
        "core_temp": 52.1
    }

def fetch_live_traffic_throughput(history_size=50):
    """Returns static pandas DataFrame for charting layout."""
    now = pd.Timestamp.now()
    times = pd.date_range(end=now, periods=history_size, freq='s')
    
    # Static placeholder data matching an initial realistic pattern
    https = np.linspace(800, 1200, history_size)
    vpn = np.linspace(250, 350, history_size)
    tor = np.linspace(10, 50, history_size)
    
    df = pd.DataFrame({
        'Timestamp': times,
        'HTTPS': https,
        'VPN Tunnel': vpn,
        'Tor Node': tor
    })
    return df

def fetch_active_threat_alerts():
    """Returns static list of dicts representing alert metadata with rich deep-dive data."""
    return [
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source_ip": "192.168.1.105",
            "dest_ip": "45.33.32.156",
            "confidence": 0.94, 
            "type": "[AWAITING AI: VPN Tunnel Detection]",
            "metadata": {
                "Flow IAT Max": 245030,
                "Fwd Packet Length Std": 125.4,
                "Flow Duration": 4500,
                "Total Fwd Packets": 24,
                "Protocol": "TCP (6)",
                "Src Port": 49152,
                "Dst Port": 443,
                "TCP Flags": "PSH, ACK"
            },
            "packets": [
                {"No": 1, "Time": "0.000000", "Src": "192.168.1.105", "Dst": "45.33.32.156", "Proto": "TCP", "Len": 74, "Info": "49152 -> 443 [SYN] Seq=0 Win=65535 Len=0 MSS=1460 SACK_PERM=1 TSval=1234567 TSecr=0 WS=128"},
                {"No": 2, "Time": "0.015231", "Src": "45.33.32.156", "Dst": "192.168.1.105", "Proto": "TCP", "Len": 74, "Info": "443 -> 49152 [SYN, ACK] Seq=0 Ack=1 Win=28960 Len=0 MSS=1460 SACK_PERM=1 TSval=8765432 TSecr=1234567 WS=128"},
                {"No": 3, "Time": "0.015302", "Src": "192.168.1.105", "Dst": "45.33.32.156", "Proto": "TCP", "Len": 66, "Info": "49152 -> 443 [ACK] Seq=1 Ack=1 Win=131328 Len=0 TSval=1234578 TSecr=8765432"},
                {"No": 4, "Time": "0.024101", "Src": "192.168.1.105", "Dst": "45.33.32.156", "Proto": "TLSv1.2", "Len": 254, "Info": "Client Hello"},
                {"No": 5, "Time": "0.051200", "Src": "45.33.32.156", "Dst": "192.168.1.105", "Proto": "TLSv1.2", "Len": 1460, "Info": "Server Hello, Certificate, Server Key Exchange, Server Hello Done"},
                {"No": 6, "Time": "0.080512", "Src": "192.168.1.105", "Dst": "45.33.32.156", "Proto": "TLSv1.2", "Len": 342, "Info": "Client Key Exchange, Change Cipher Spec, Encrypted Handshake Message"},
                {"No": 7, "Time": "0.150244", "Src": "45.33.32.156", "Dst": "192.168.1.105", "Proto": "TLSv1.2", "Len": 105, "Info": "Change Cipher Spec, Encrypted Handshake Message"},
                {"No": 8, "Time": "1.450211", "Src": "45.33.32.156", "Dst": "192.168.1.105", "Proto": "TLSv1.2", "Len": 1460, "Info": "Application Data [Suspected Payload chunk 1]"},
                {"No": 9, "Time": "1.450255", "Src": "45.33.32.156", "Dst": "192.168.1.105", "Proto": "TLSv1.2", "Len": 1460, "Info": "Application Data [Suspected Payload chunk 2]"},
                {"No": 10, "Time": "1.451002", "Src": "192.168.1.105", "Dst": "45.33.32.156", "Proto": "TCP", "Len": 66, "Info": "49152 -> 443 [ACK] Seq=423 Ack=2921 Win=131328 Len=0"}
            ],
            "hex_dump": "0000   45 00 05 dc 8a 22 40 00 40 06 db 0f 2d 21 20 9c   E....\"@.@...-! .\n0010   c0 a8 01 69 01 bb c0 00 12 34 56 78 87 65 43 21   ...i.....4Vx.eC!\n0020   80 18 01 c0 1c 46 00 00 01 01 08 0a 00 85 c5 c8   .....F..........\n0030   00 12 d6 87 17 03 03 05 a9 d0 eb b4 c7 a8 1b aa   ................\n0040   34 98 f1 d5 e6 72 8b 9c a0 b1 c2 d3 e4 f5 06 17   4....r..........\n0050   28 39 4a 5b 6c 7d 8e 9f b0 c1 d2 e3 f4 05 16 27   (9J[l}.........'\n0060   38 49 5a 6b 7c 8d 9e af c0 d1 e2 f3 04 15 26 37   8IZk|.........&7\n0070   48 59 6a 7b 8c 9d ae bf d0 e1 f2 03 14 25 36 47   HYj{.........%36G"
        },
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source_ip": "10.0.0.14",
            "dest_ip": "185.101.35.22",
            "confidence": 0.88, 
            "type": "[AWAITING AI: Tor Node Connection]",
            "metadata": {
                "Flow IAT Max": 100000,
                "Fwd Packet Length Std": 20.0,
                "Flow Duration": 500,
                "Total Fwd Packets": 5,
                "Protocol": "UDP (17)",
                "Src Port": 5353,
                "Dst Port": 53,
                "DNS Query": "update.windows-services-host.com"
            },
            "packets": [
                {"No": 1, "Time": "0.000000", "Src": "10.0.0.14", "Dst": "185.101.35.22", "Proto": "DNS", "Len": 82, "Info": "Standard query 0x1a2b A update.windows-services-host.com"},
                {"No": 2, "Time": "0.100201", "Src": "185.101.35.22", "Dst": "10.0.0.14", "Proto": "DNS", "Len": 98, "Info": "Standard query response 0x1a2b A update.windows-services-host.com A 185.101.35.22"},
                {"No": 3, "Time": "30.000122", "Src": "10.0.0.14", "Dst": "185.101.35.22", "Proto": "DNS", "Len": 82, "Info": "Standard query 0x2c4d A update.windows-services-host.com"},
                {"No": 4, "Time": "30.101033", "Src": "185.101.35.22", "Dst": "10.0.0.14", "Proto": "DNS", "Len": 98, "Info": "Standard query response 0x2c4d A update.windows-services-host.com A 185.101.35.22"}
            ],
            "hex_dump": "0000   45 00 00 52 1a 2b 00 00 80 11 00 00 0a 00 00 0e   E..R.+..........\n0010   b9 65 23 16 14 e9 00 35 00 3e 12 34 1a 2b 01 00   .e#....5.>.4.+..\n0020   00 01 00 00 00 00 00 00 06 75 70 64 61 74 65 10   .........update.\n0030   77 69 6e 64 6f 77 73 2d 73 65 72 76 69 63 65 73   windows-services\n0040   2d 68 6f 73 74 03 63 6f 6d 00 00 01 00 01         -host.com....."
        }
    ]

# ----------------------------------------------------------------------
# Pop-up Window for Deep Inspection
# ----------------------------------------------------------------------
class AlertDetailsWindow(ctk.CTkToplevel):
    def __init__(self, master, alert_data, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title(f"Flow Inspection: {alert_data['source_ip']} -> {alert_data.get('dest_ip', 'Unknown')}")
        self.geometry("900x700")
        
        # Make the popup transient to the main window
        self.transient(master)
        
        # Grid layout for the popup
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=3) # Packet List
        self.grid_rowconfigure(2, weight=2) # Hex Dump
        self.grid_rowconfigure(3, weight=1) # Metadata Bottom
        self.grid_columnconfigure(0, weight=1)

        # 1. Header
        header = ctk.CTkFrame(self, fg_color="#2b2b2b")
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        ctk.CTkLabel(header, text=f"Protocol Analyzer - Threat: {alert_data['type']}", font=ctk.CTkFont(size=16, weight="bold"), text_color="#ff7f0e").pack(pady=10)

        # 2. Packet List / Frame (Middle Top)
        list_frame = ctk.CTkScrollableFrame(self, label_text="Packet Capture (Mock PCAP)", label_anchor="w")
        list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Create a tiny pseudo-table for packets
        cols_frame = ctk.CTkFrame(list_frame, fg_color="#1e1e1e")
        cols_frame.pack(fill="x", pady=(0, 5))
        for col, width in [("No.", 40), ("Time", 80), ("Source", 120), ("Destination", 120), ("Protocol", 80), ("Length", 60), ("Info", 300)]:
            lbl = ctk.CTkLabel(cols_frame, text=col, width=width, anchor="w", font=ctk.CTkFont(weight="bold"))
            lbl.pack(side="left", padx=5)

        for pkt in alert_data.get("packets", []):
            row = ctk.CTkFrame(list_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=str(pkt["No"]), width=40, anchor="w", text_color="#aaaaaa").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=pkt["Time"], width=80, anchor="w", text_color="#aaaaaa").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=pkt["Src"], width=120, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=pkt["Dst"], width=120, anchor="w").pack(side="left", padx=5)
            
            # Color code protocols
            p_color = "#e0e0e0"
            if pkt["Proto"] == "TCP": p_color = "#5cae00"
            elif pkt["Proto"].startswith("TLS"): p_color = "#bf8f00"
            elif pkt["Proto"] == "DNS": p_color = "#008fbf"
            
            ctk.CTkLabel(row, text=pkt["Proto"], width=80, anchor="w", text_color=p_color).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=str(pkt["Len"]), width=60, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=pkt["Info"], anchor="w", justify="left").pack(side="left", fill="x", expand=True, padx=5)

        # 3. Hex Dump Frame (Bottom Middle)
        hex_frame = ctk.CTkFrame(self)
        hex_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        ctk.CTkLabel(hex_frame, text="Raw Payload (Hex Dump)", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x", padx=10, pady=5)
        
        textbox = ctk.CTkTextbox(hex_frame, font=ctk.CTkFont(family="Courier", size=12), text_color="#b3ecff", fg_color="#181818")
        textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        textbox.insert("1.0", alert_data.get("hex_dump", "No raw data available."))
        textbox.configure(state="disabled") # Read only

        # 4. Deep Metadata Frame (Bottom)
        meta_frame = ctk.CTkFrame(self, fg_color="#1e1e1e")
        meta_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        meta_str = " | ".join([f"{k}: {v}" for k, v in alert_data['metadata'].items()])
        ctk.CTkLabel(meta_frame, text="Extracted Flow Features:\n" + meta_str, justify="left", wraplength=850, text_color="#aaaaaa").pack(padx=15, pady=10, anchor="w")


# ----------------------------------------------------------------------
# Main UI Application Class
# ----------------------------------------------------------------------
class SOCDashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("SOC Dashboard: Remote Network Traffic Classification")
        self.geometry("1100x800")
        
        # --- Grid Layout Configuration ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=3) # Main content area
        self.grid_rowconfigure(2, weight=2) # Alerts area

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="🛡️ SOC Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(side="left")

        # --- Fetch Data ---
        telemetry_data = fetch_edge_telemetry()
        traffic_data = fetch_live_traffic_throughput()
        alerts_data = fetch_active_threat_alerts()

        # --- Left Column: Telemetry ---
        self.telemetry_frame = ctk.CTkFrame(self)
        self.telemetry_frame.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.telemetry_frame, text="📡 Edge Hardware Telemetry", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10, padx=10, anchor="w")
        
        self._create_metric_card(self.telemetry_frame, "CPU Load", f"{telemetry_data['cpu_usage']:.1f}%")
        self._create_metric_card(self.telemetry_frame, "RAM Usage", f"{telemetry_data['ram_usage']:.1f}%")
        self._create_metric_card(self.telemetry_frame, "Core Temp", f"{telemetry_data['core_temp']:.1f} °C", 
                                 highlight_temp=telemetry_data['core_temp'] > 70)

        # --- Right Column: Traffic Chart ---
        self.chart_frame = ctk.CTkFrame(self)
        self.chart_frame.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.chart_frame, text="📈 Live Traffic Distribution", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10, padx=10, anchor="w")
        
        self._create_matplotlib_chart(traffic_data)

        # --- Bottom Row: Alerts Drawer ---
        self.alerts_frame = ctk.CTkScrollableFrame(self, label_text="🚨 Active Alert Drawer", label_anchor="w", label_font=ctk.CTkFont(size=18, weight="bold"))
        self.alerts_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="nsew")
        
        for alert in alerts_data:
            self._create_alert_card(alert)

    def _create_metric_card(self, parent, title, value, highlight_temp=False):
        """Helper to create a unified metric card."""
        card = ctk.CTkFrame(parent, fg_color="#2b2b2b", corner_radius=8)
        card.pack(fill="x", padx=15, pady=10)
        
        title_label = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14), text_color="#aaaaaa")
        title_label.pack(anchor="w", padx=15, pady=(10, 0))
        
        value_color = "#e0e0e0"
        if highlight_temp:
            value_color = "#ff7f0e"
            value += " ⚠️"
            
        val_label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=24, weight="bold"), text_color=value_color)
        val_label.pack(anchor="w", padx=15, pady=(0, 10))

    def _create_matplotlib_chart(self, df):
        """Embeds a matplotlib figure into the CustomTkinter frame."""
        # Setup matplotlib styling to match dark theme
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
        fig.patch.set_facecolor('#2b2b2b') # CTk frame background
        ax.set_facecolor('#2b2b2b')
        
        # Plot lines
        ax.plot(df['Timestamp'], df['HTTPS'], label='HTTPS', color='#1f77b4', linewidth=2)
        ax.plot(df['Timestamp'], df['VPN Tunnel'], label='VPN Tunnel', color='#ff7f0e', linewidth=2)
        ax.plot(df['Timestamp'], df['Tor Node'], label='Tor Node', color='#7f7f7f', linewidth=2)
        
        # Formatting
        ax.set_ylabel('Packets/sec')
        ax.tick_params(axis='x', rotation=45)
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.4), ncol=3, frameon=False)
        ax.grid(True, alpha=0.2, linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        fig.tight_layout()

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _create_alert_card(self, alert):
        """Helper to create a rounded alert entry with a button launching a deep-dive window."""
        # Main card container
        card = ctk.CTkFrame(self.alerts_frame, fg_color="#1e1e1e", border_width=1, border_color="#ff7f0e")
        card.pack(fill="x", padx=10, pady=5)
        
        # Header container (Title + Toggle Button)
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=10)
        
        header_text = f"[{alert['timestamp']}] {alert['type']} detected from IP: {alert['source_ip']} (AI Confidence: {alert['confidence']*100:.1f}%)"
        title_label = ctk.CTkLabel(header_frame, text=header_text, font=ctk.CTkFont(weight="bold"))
        title_label.pack(side="left")
        
        # Function to launch the popup window
        def launch_inspection_window():
            # Create the Toplevel window and pass the specific alert data to it
            AlertDetailsWindow(self, alert)
                
        inspect_btn = ctk.CTkButton(header_frame, text="🔍 Inspect Flow", width=120, height=28, 
                                   fg_color="#005b96", hover_color="#003f69",
                                   command=launch_inspection_window)
        inspect_btn.pack(side="right")


if __name__ == "__main__":
    app = SOCDashboardApp()
    app.mainloop()
