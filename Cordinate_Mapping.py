#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AI BROTHERS TOOLS - PROPRIETARY SOFTWARE
Version: 2.0.5 Pro
Copyright © 2026 AI Brothers Tools - All Rights Reserved
================================================================================

PROPRIETARY AND CONFIDENTIAL

This software and its source code are the exclusive property of AI Brothers Tools.

⚠️ WARNING:
- Unauthorized copying, distribution, or use is strictly prohibited.
- Reverse engineering or decompiling is illegal.
- This code contains proprietary algorithms and trade secrets.
- Violators will be prosecuted to the maximum extent of the law.

📧 Contact: info@aibrotherstools.ir
🌐 Website: https://aibrotherstools.ir

================================================================================
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import math
import os
import sys
import webbrowser
import tempfile
import hashlib
import datetime
from datetime import timedelta
import threading
import time

# Try importing PIL and qrcode
try:
    from PIL import Image, ImageTk
    import qrcode
    HAS_FANCY_LIBS = True
except ImportError:
    HAS_FANCY_LIBS = False

# ============================================================
#  SECURITY & CONFIGURATION
# ============================================================

LICENSE_HASH =[
    "a4de2cff63569134c857fbe45f6cfdbebec2ff11cc54b5eb228f0bba79bbeaf6",
    "67c45db67539ac3719ae825af6134e2c063bc9f6eb19e24a8a04830e00c79341",
    "732cfbd556aa4fcd1baa38ba67e365983c82b3010c2ccb84f19db337d26c6b9d",
    "f01e6cbd8e2d8f60fe79890126b35e2356765f19ac956d5235433ede249d94d7",
    "015df875f12bc0a22fe3cb7781e910f60730e85dc26478146b23adee1df1f6d8",
    "15d4a0fd5fab170194e3f151b07e895e45d103e5fa98c22769f52a004226ed24",
    "e2382169f932679f2e8e4e2a6f46b3dc9d480bbbd03723b950e6d09c655631b4",
    "58ee51384e7e930c835583931563ee688807bac80e2b6a94f6371f81a02ff5d4",
    "7c26c0cc57414ecbfdf7b9d0b6c635f9c023e5f8e9bd6c02e26e7cb1622132a6",
    "74650e3da99199ce678834ec9147ebbac3a328af1f38b60e8e31c534095ffd92",
]
CONFIG_FILE = "app_config.dat"
TRIAL_DAYS = 3

# ============================================================
#  MATH & GEOMETRY FUNCTIONS (CORE LOGIC)
# ============================================================

def parse_dms(dms_str):
    """Parses DMS string (e.g. 35°41'21") to decimal degrees."""
    try:
        if isinstance(dms_str, (float, int)):
            return float(dms_str)
        dms_str = str(dms_str).strip()
        try:
            return float(dms_str)
        except ValueError:
            pass
        dms_str = dms_str.replace("''", '"').strip()
        parts = dms_str.replace('°', ' ').replace("'", ' ').replace('"', ' ').split()
        deg = float(parts[0])
        mn = float(parts[1]) if len(parts) > 1 else 0
        sec = float(parts[2]) if len(parts) > 2 else 0
        return deg + mn / 60 + sec / 3600
    except:
        return None

def decimal_to_dms(deg):
    """Converts decimal degrees to DMS string."""
    try:
        d = int(deg)
        m = int((deg - d) * 60)
        s = (deg - d - m/60) * 3600
        return f"{d}°{m}'{s:.2f}\""
    except:
        return "0°0'0.00\""

def latlon_to_utm(lat, lon, zone_number=39):
    try:
        a = 6378137
        f = 1 / 298.257223563
        k0 = 0.9996
        phi = math.radians(lat)
        lam = math.radians(lon)
        lam0 = math.radians((zone_number - 1) * 6 - 180 + 3)
        e = math.sqrt(2 * f - f ** 2)
        ep2 = e ** 2 / (1 - e ** 2)
        N = a / math.sqrt(1 - e ** 2 * math.sin(phi) ** 2)
        T = math.tan(phi) ** 2
        C = ep2 * math.cos(phi) ** 2
        A = (lam - lam0) * math.cos(phi)
        M = a * ((1 - e**2/4 - 3*e**4/64 - 5*e**6/256) * phi -
                 (3*e**2/8 + 3*e**4/32 + 45*e**6/1024) * math.sin(2*phi) +
                 (15*e**4/256 + 45*e**6/1024) * math.sin(4*phi) -
                 (35*e**6/3072) * math.sin(6*phi))
        x = 500000 + k0 * N * (A + (1 - T + C) * A**3 / 6 + (5 - 18 * T + T**2 + 72 * C - 58 * ep2) * A**5 / 120)
        y = k0 * (M + N * math.tan(phi) * (A**2 / 2 + (5 - T + 9 * C + 4 * C**2) * A**4 / 24 + (61 - 58 * T + T**2 + 600 * C - 330 * ep2) * A**6 / 720))
        return x, y, zone_number, 'N' 
    except:
        return 0, 0, zone_number, 'N'

def utm_to_latlon(easting, northing, zone_number, zone_letter='N'):
    try:
        k0 = 0.9996
        a = 6378137
        f = 1 / 298.257223563
        e = math.sqrt(2 * f - f ** 2)
        e1sq = e ** 2 / (1 - e ** 2)
        x = easting - 500000
        y = northing
        m = y / k0
        mu = m / (a * (1 - e**2/4 - 3*e**4/64 - 5*e**6/256))
        e1 = (1 - math.sqrt(1 - e**2)) / (1 + math.sqrt(1 - e**2))
        phi1 = mu + (3*e1/2 - 27*e1**3/32) * math.sin(2*mu) + (21*e1**2/16 - 55*e1**4/32) * math.sin(4*mu) + (151*e1**3/96) * math.sin(6*mu)
        n1 = a / math.sqrt(1 - e**2 * math.sin(phi1)**2)
        t1 = math.tan(phi1)**2
        c1 = e1sq * math.cos(phi1)**2
        r1 = a * (1 - e**2) / math.pow(1 - e**2 * math.sin(phi1)**2, 1.5)
        d = x / (n1 * k0)
        lat = phi1 - (n1 * math.tan(phi1) / r1) * (d**2 / 2 - (5 + 3 * t1 + 10 * c1 - 4 * c1**2 - 9 * e1sq) * d**4 / 24 + (61 + 90 * t1 + 298 * c1 + 45 * t1**2 - 252 * e1sq - 3 * c1**2) * d**6 / 720)
        lat = math.degrees(lat)
        lon = (d - (1 + 2 * t1 + c1) * d**3 / 6 + (5 - 2 * c1 + 28 * t1 - 3 * c1**2 + 8 * e1sq + 24 * t1**2) * d**5 / 120) / math.cos(phi1)
        lon = math.degrees(lon) + ((zone_number - 1) * 6 - 180 + 3)
        return lat, lon
    except:
        return 0, 0

# ============================================================
#  MAIN APPLICATION CLASS
# ============================================================

class CoordinateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coordinate Mapping v1.5 Pro - Ultimate Edition")
        self.root.geometry("1150x850")
        
        # --- Variables ---
        self.points = []
        self.base_font_size = 10
        self.current_theme = "Official"
        self.logo_img_ref = None 
        self.is_activated = False
        self.trial_remaining = 0
        
        # --- Styles ---
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # --- Themes Definition ---
        self.themes = {
            "Official": {"bg": "#ECF0F1", "fg": "#2C3E50", "btn_primary": "#2980B9", "btn_success": "#27AE60", "btn_danger": "#C0392B", "header": "#2C3E50"},
            "Girly 🌸": {"bg": "#FFF0F5", "fg": "#880E4F", "btn_primary": "#FF69B4", "btn_success": "#FFB6C1", "btn_danger": "#DB7093", "header": "#FF1493"},
            "Colorful": {"bg": "#FFFFFF", "fg": "#333333", "btn_primary": "#FF5733", "btn_success": "#C70039", "btn_danger": "#900C3F", "header": "#FFC300"},
            "Gray": {"bg": "#BDC3C7", "fg": "#000000", "btn_primary": "#7F8C8D", "btn_success": "#95A5A6", "btn_danger": "#2C3E50", "header": "#34495E"},
            "Classic": {"bg": "#F0F0F0", "fg": "#000000", "btn_primary": "#000080", "btn_success": "#008000", "btn_danger": "#800000", "header": "#000080"},
        }

        # --- License Check ---
        self.check_license_status()

        # --- UI Build ---
        self.setup_ui()
        self.apply_theme("Official")
        self.update_app_font()
        self.log_operation("Application Started.")
        
        if not self.is_activated:
            self.log_operation(f"Trial Version: {self.trial_remaining} days remaining.")
            if self.trial_remaining <= 0:
                self.lock_application()

    # ----------------------------------------------------------------
    # LICENSE & SECURITY LOGIC
    # ----------------------------------------------------------------
    def check_license_status(self):
        """Checks trial status and activation."""
        current_date = datetime.datetime.now()
        
        if not os.path.exists(CONFIG_FILE):
            # First run, initialize config
            data = {
                "start_date": current_date.isoformat(),
                "activated": False
            }
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f)
            self.is_activated = False
            self.trial_remaining = TRIAL_DAYS
        else:
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                
                if data.get("activated", False):
                    self.is_activated = True
                    self.trial_remaining = 9999
                else:
                    self.is_activated = False
                    start_date = datetime.datetime.fromisoformat(data["start_date"])
                    elapsed = (current_date - start_date).days
                    self.trial_remaining = TRIAL_DAYS - elapsed
            except:
                # Corrupt config, reset (security risk handled by simple overwrite for this scope)
                self.is_activated = False
                self.trial_remaining = 0

    def register_product(self):
        key = self.license_entry.get().strip()
        hashed_key = hashlib.sha256(key.encode()).hexdigest()
        
        if hashed_key in LICENSE_HASH:  # <-- تنها تغییر: == به in تبدیل شد
            self.is_activated = True
            # Update Config
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                data["activated"] = True
                with open(CONFIG_FILE, "w") as f:
                    json.dump(data, f)
                
                messagebox.showinfo("Success", "Product Activated Successfully!\nThank you for supporting AI Brothers Tools.")
                self.log_operation("Product Activated.")
                
                # If locked, unlock
                if hasattr(self, 'lock_frame') and self.lock_frame.winfo_ismapped():
                    self.unlock_application()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Could not save license: {e}")
        else:
            messagebox.showerror("Error", "Invalid License Key.")
            self.log_operation("Failed Activation Attempt.")


    def lock_application(self):
        """Hides the main app and shows the lock screen."""
        self.notebook.pack_forget()
        
        self.lock_frame = tk.Frame(self.root, bg="#2C3E50")
        self.lock_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(self.lock_frame, text="🔒 LICENSE EXPIRED", font=("Segoe UI", 30, "bold"), fg="#E74C3C", bg="#2C3E50").pack(pady=(100, 20))
        tk.Label(self.lock_frame, text="Your 3-day trial has ended.", font=("Segoe UI", 16), fg="white", bg="#2C3E50").pack(pady=10)
        tk.Label(self.lock_frame, text="Please enter your license key to continue.", font=("Segoe UI", 12), fg="#BDC3C7", bg="#2C3E50").pack(pady=5)
        
        input_frame = tk.Frame(self.lock_frame, bg="#2C3E50")
        input_frame.pack(pady=30)
        
        tk.Label(input_frame, text="License Key:", fg="white", bg="#2C3E50").pack(side=tk.LEFT, padx=5)
        self.license_entry = tk.Entry(input_frame, width=30, show="*")
        self.license_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(input_frame, text="Unlock", bg="#27AE60", fg="white", font=("Arial", 10, "bold"),
                  command=self.register_product).pack(side=tk.LEFT, padx=10)
                  
        tk.Button(self.lock_frame, text="Exit", bg="#C0392B", fg="white", width=20, command=self.root.quit).pack(pady=50)

    def unlock_application(self):
        """Removes lock screen and shows main app."""
        self.lock_frame.destroy()
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X) # Repack logging

    # ----------------------------------------------------------------
    # UI SETUP
    # ----------------------------------------------------------------
    def setup_ui(self):
        # --- Header ---
        self.header_frame = tk.Frame(self.root, height=60)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        self.header_frame.pack_propagate(False)

        # --- LOGO IMPLEMENTATION ---
        logo_path = r"C:\Users\parviztajdari\VSCODE_PROJECT\FINAL_CODES\1\logo\logo.ico"
        if HAS_FANCY_LIBS and os.path.exists(logo_path):
            try:
                pil_image = Image.open(logo_path)
                pil_image = pil_image.resize((45, 45), Image.Resampling.LANCZOS)
                self.logo_img_ref = ImageTk.PhotoImage(pil_image)
                tk.Label(self.header_frame, image=self.logo_img_ref, bg="#2C3E50").pack(side=tk.LEFT, padx=(10, 0), pady=5)
            except Exception as e:
                print(f"Could not load logo: {e}")

        # Title & Join Us
        self.title_label = tk.Label(self.header_frame, text="🌍 Coordinate Mapping v1.5", font=("Segoe UI", 14, "bold"), fg="white")
        self.title_label.pack(side=tk.LEFT, padx=15)
        
        # CHANGED: Join Us Button Blue and Link
        tk.Button(self.header_frame, text="🤝 Join Us", bg="#2980B9", fg="white", font=("Arial", 9, "bold"),
                  command=lambda: webbrowser.open("https://aibrotherstools.ir")).pack(side=tk.LEFT, padx=5)

        # Controls
        controls_frame = tk.Frame(self.header_frame, bg=self.header_frame['bg'])
        controls_frame.pack(side=tk.RIGHT, padx=10)
        self.controls_frame = controls_frame

        # License Field (Header) for manual activation before expiry
        if not self.is_activated:
            reg_frame = tk.Frame(controls_frame, bg=self.header_frame['bg'])
            reg_frame.pack(side=tk.LEFT, padx=10)
            self.license_entry = tk.Entry(reg_frame, width=15, show="*") # Re-used variable, carefully
            self.license_entry.pack(side=tk.LEFT)
            tk.Button(reg_frame, text="🔑 Activate", bg="#F1C40F", fg="black", font=("Arial", 8),
                      command=self.register_product).pack(side=tk.LEFT, padx=2)

        tk.Label(controls_frame, text="Theme:", fg="white", bg=self.themes["Official"]["header"]).pack(side=tk.LEFT, padx=2)
        self.theme_var = tk.StringVar(value="Official")
        theme_combo = ttk.Combobox(controls_frame, textvariable=self.theme_var, values=list(self.themes.keys()), state="readonly", width=10)
        theme_combo.pack(side=tk.LEFT, padx=5)
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_theme(self.theme_var.get()))

        tk.Button(controls_frame, text="A-", width=3, bg="#E74C3C", fg="white", font=("Arial", 8, "bold"),
                  command=lambda: self.change_zoom(-1)).pack(side=tk.LEFT, padx=2)
        tk.Button(controls_frame, text="A+", width=3, bg="#27AE60", fg="white", font=("Arial", 8, "bold"),
                  command=lambda: self.change_zoom(1)).pack(side=tk.LEFT, padx=2)

        tk.Button(self.header_frame, text="ℹ️ Info", bg="#3498DB", fg="white", command=self.show_app_info).pack(side=tk.RIGHT, padx=5, pady=10)
        # CHANGED: License text to Proprietary
        tk.Button(self.header_frame, text="📜 License", bg="#D35400", fg="white", command=self.show_license).pack(side=tk.RIGHT, padx=5, pady=10)
        # CHANGED: Exit button Red
        tk.Button(self.header_frame, text="❌ Exit", bg="#C0392B", fg="white", command=self.root.quit).pack(side=tk.RIGHT, padx=5, pady=10)

        # --- Tabs ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tab_main = tk.Frame(self.notebook)
        self.tab_convert = tk.Frame(self.notebook)
        self.tab_calc = tk.Frame(self.notebook)
        self.tab_petrel = tk.Frame(self.notebook)
        self.tab_arcgis = tk.Frame(self.notebook)
        self.tab_download = tk.Frame(self.notebook)

        self.notebook.add(self.tab_main, text="🏠 Main")
        self.notebook.add(self.tab_convert, text="🔄 Convert")
        self.notebook.add(self.tab_calc, text="📐 Calculations")
        self.notebook.add(self.tab_petrel, text="🛢️ Petrel Export")
        self.notebook.add(self.tab_arcgis, text="🗺️ ArcGIS Export")
        self.notebook.add(self.tab_download, text="📥 Download & Tools")

        # Setup Tab Contents
        self.setup_main_tab()
        self.setup_convert_tab()
        self.setup_calculations_tab()
        self.setup_petrel_tab()
        self.setup_arcgis_tab()
        self.setup_download_tab()

        # --- Logging & Status Bar ---
        self.setup_status_bar()

    def setup_status_bar(self):
        self.status_frame = tk.Frame(self.root, height=100, bg="#ECF0F1")
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Log Text Area
        lbl_log = tk.Label(self.status_frame, text="📋 Operation Log:", font=("Segoe UI", 9, "bold"), bg="#ECF0F1")
        lbl_log.pack(anchor="w", padx=5)
        
        self.log_text = tk.Text(self.status_frame, height=4, font=("Consolas", 8), state='disabled', bg="white")
        self.log_text.pack(fill=tk.X, padx=5, pady=2)
        
        # System Info Bar
        sys_info = tk.Frame(self.status_frame, bg="#BDC3C7")
        sys_info.pack(fill=tk.X)
        
        tk.Label(sys_info, text=f"📅 Date: {datetime.date.today()}", bg="#BDC3C7").pack(side=tk.LEFT, padx=10)
        tk.Label(sys_info, text="⚙️ Recommended System: RAM 8GB+ | CPU Core i5+", bg="#BDC3C7", fg="#2C3E50", font=("Arial", 9, "bold")).pack(side=tk.RIGHT, padx=10)

    def log_operation(self, message):
        """Logs message to the bottom text widget."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        full_msg = f"[{timestamp}] {message}\n"
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, full_msg)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    # ----------------------------------------------------------------
    # 1. MAIN TAB
    # ----------------------------------------------------------------
    def setup_main_tab(self):
        main_frame = tk.Frame(self.tab_main)
        main_frame.pack(fill=tk.BOTH, expand=True)

        top_panel = tk.Frame(main_frame)
        top_panel.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        input_frame = tk.LabelFrame(top_panel, text="📍 Input Coordinates")
        input_frame.pack(fill=tk.X, pady=5)
        
        grid_frame = tk.Frame(input_frame)
        grid_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(grid_frame, text="Point Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(grid_frame, width=25)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(grid_frame, text="Latitude (DMS):").grid(row=1, column=0, sticky="w")
        self.lat_entry = tk.Entry(grid_frame, width=25)
        self.lat_entry.grid(row=1, column=1, padx=5, pady=2)
        self.lat_entry.insert(0, "e.g. 35°41'21\"")

        tk.Label(grid_frame, text="Longitude (DMS):").grid(row=2, column=0, sticky="w")
        self.lon_entry = tk.Entry(grid_frame, width=25)
        self.lon_entry.grid(row=2, column=1, padx=5, pady=2)
        self.lon_entry.insert(0, "e.g. 51°25'23\"")

        tk.Label(grid_frame, text="Zone (WGS84):").grid(row=3, column=0, sticky="w")
        self.zone_entry = tk.Entry(grid_frame, width=25)
        self.zone_entry.grid(row=3, column=1, padx=5, pady=2)
        self.zone_entry.insert(0, "39")

        tk.Button(grid_frame, text="➕ Add Point", bg="#27AE60", fg="white", width=20,
                  command=self.add_point).grid(row=4, column=0, columnspan=2, pady=10)

        tools_panel = tk.Frame(input_frame)
        tools_panel.pack(side=tk.RIGHT, padx=20, pady=10, anchor="e")

        tk.Button(tools_panel, text="📱 Generate QR", bg="#8E44AD", fg="white", width=20,
                  command=self.generate_qr_code).pack(fill=tk.X, pady=(0, 5))
        
        tk.Button(tools_panel, text="🌏 Google Earth", bg="#2980B9", fg="white", width=20,
                  command=self.open_in_google_earth).pack(fill=tk.X, pady=2)

        tk.Button(tools_panel, text="📍 Google Map", bg="#E67E22", fg="white", width=20,
                  command=self.open_in_google_maps).pack(fill=tk.X, pady=2)
        
        middle_panel = tk.Frame(main_frame)
        middle_panel.pack(fill=tk.X, padx=10)

        json_frame = tk.LabelFrame(middle_panel, text="💾 Project (JSON)")
        json_frame.pack(fill=tk.X, pady=5)
        btn_config = {'padx': 2, 'pady': 5, 'side': tk.LEFT, 'expand': True, 'fill': tk.X}
        
        # ADDED/CONFIRMED: Reset, Load, Save
        tk.Button(json_frame, text="💾 Save", bg="#16A085", fg="white", command=self.save_json).pack(**btn_config)
        tk.Button(json_frame, text="📂 Load", bg="#2980B9", fg="white", command=self.load_json).pack(**btn_config)
        tk.Button(json_frame, text="🔄 Reset", bg="#C0392B", fg="white", command=self.reset_all).pack(**btn_config)

        excel_frame = tk.LabelFrame(middle_panel, text="📊 Excel Tools")
        excel_frame.pack(fill=tk.X, pady=5)
        tk.Button(excel_frame, text="📄 Create & Open Template", bg="#8E44AD", fg="white",
                  command=self.create_excel_template).pack(side=tk.LEFT, padx=2, pady=5, expand=True, fill=tk.X)
        tk.Button(excel_frame, text="📥 Load Excel", bg="#E67E22", fg="white",
                  command=self.import_excel).pack(side=tk.LEFT, padx=2, pady=5, expand=True, fill=tk.X)

        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        cols = ('Name', 'Lat', 'Lon', 'Easting', 'Northing', 'Zone')
        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80)
        
        sb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

    # ----------------------------------------------------------------
    # 2. CONVERT TAB
    # ----------------------------------------------------------------
    def setup_convert_tab(self):
        container = tk.Frame(self.tab_convert)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        frame_dms = tk.LabelFrame(container, text="➡️ DMS to UTM")
        frame_dms.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        tk.Label(frame_dms, text="Lat (DMS):").pack(pady=5)
        self.conv_lat = tk.Entry(frame_dms, width=25); self.conv_lat.pack()
        tk.Label(frame_dms, text="Lon (DMS):").pack(pady=5)
        self.conv_lon = tk.Entry(frame_dms, width=25); self.conv_lon.pack()
        
        tk.Button(frame_dms, text="Convert ⬇️", bg="#2980B9", fg="white", command=self.do_convert_dms_utm).pack(pady=10)
        self.res_utm = tk.Text(frame_dms, height=4, width=30); self.res_utm.pack(pady=5)

        frame_utm = tk.LabelFrame(container, text="➡️ UTM to DMS")
        frame_utm.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        input_box = tk.Frame(frame_utm)
        input_box.pack(pady=15)
        tk.Label(input_box, text="East:").grid(row=0, column=0)
        self.conv_east = tk.Entry(input_box, width=12); self.conv_east.grid(row=0, column=1, padx=2)
        tk.Label(input_box, text="North:").grid(row=0, column=2)
        self.conv_north = tk.Entry(input_box, width=12); self.conv_north.grid(row=0, column=3, padx=2)
        tk.Label(input_box, text="Zone:").grid(row=0, column=4)
        self.conv_znum = tk.Entry(input_box, width=4); self.conv_znum.grid(row=0, column=5)
        self.conv_zlet = tk.Entry(input_box, width=4); self.conv_zlet.grid(row=0, column=6)
        self.conv_zlet.insert(0, "N")

        tk.Button(frame_utm, text="Convert ⬇️", bg="#8E44AD", fg="white", command=self.do_convert_utm_dms).pack(pady=10)
        self.res_dms = tk.Text(frame_utm, height=4, width=30); self.res_dms.pack(pady=5)

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

    # ----------------------------------------------------------------
    # 3. CALCULATIONS TAB
    # ----------------------------------------------------------------
    def setup_calculations_tab(self):
        frame = tk.Frame(self.tab_calc)
        frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        tk.Label(frame, text="📐 Geometric Analysis", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(frame, text="Calculates distances between points (Km) and Area (Km²).\nDraws polygons based on points in Main Tab.", font=("Arial", 12)).pack(pady=10)
        
        tk.Button(frame, text="🖥️ Open Visualizer Window", font=("Arial", 14, "bold"),
                  bg="#27AE60", fg="white", height=3, width=30,
                  command=self.open_calculation_window).pack(pady=30)

    def open_calculation_window(self):
        self.log_operation("Opening Calculation Visualizer.")
        if len(self.points) < 3:
            messagebox.showwarning("Oops!", "Please add at least 3 points in the Main Tab first!")
            return
            
        win = tk.Toplevel(self.root)
        win.title("📐 Visualization Result")
        win.geometry("1100x800")
        win.configure(bg="white")
        
        canvas_width = 1050
        canvas_height = 650
        canvas = tk.Canvas(win, bg="#ECF0F1", width=canvas_width, height=canvas_height)
        canvas.pack(pady=15)
        
        x_coords = [p['easting'] for p in self.points]
        y_coords = [p['northing'] for p in self.points]
        
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        
        range_x = max_x - min_x
        range_y = max_y - min_y
        
        if range_x == 0: range_x = 1
        if range_y == 0: range_y = 1
        
        padding = 80
        draw_width = canvas_width - (2 * padding)
        draw_height = canvas_height - (2 * padding)
        
        scale_x = draw_width / range_x
        scale_y = draw_height / range_y
        final_scale = min(scale_x, scale_y)
        
        center_x_data = (min_x + max_x) / 2
        center_y_data = (min_y + max_y) / 2
        center_x_canvas = canvas_width / 2
        center_y_canvas = canvas_height / 2
        
        screen_pts = []
        for p in self.points:
            sx = center_x_canvas + (p['easting'] - center_x_data) * final_scale
            sy = center_y_canvas - (p['northing'] - center_y_data) * final_scale
            screen_pts.append({'x': sx, 'y': sy, 'real_e': p['easting'], 'real_n': p['northing'], 'name': p['name']})

        total_dist_km = 0
        area_sum = 0
        num = len(screen_pts)
        
        for i in range(num):
            p1 = screen_pts[i]
            p2 = screen_pts[(i + 1) % num] 
            
            canvas.create_line(p1['x'], p1['y'], p2['x'], p2['y'], fill="blue", width=2, arrow=tk.LAST)
            
            dist_m = math.sqrt((p2['real_e'] - p1['real_e'])**2 + (p2['real_n'] - p1['real_n'])**2)
            dist_km = dist_m / 1000.0
            total_dist_km += dist_km
            
            area_sum += (p1['real_e'] * p2['real_n']) - (p2['real_e'] * p1['real_n'])
            
            mid_x = (p1['x'] + p2['x']) / 2
            mid_y = (p1['y'] + p2['y']) / 2
            text_str = f"{dist_km:.2f} km"
            
            canvas.create_rectangle(mid_x - 35, mid_y - 10, mid_x + 35, mid_y + 10, fill="white", outline="")
            canvas.create_text(mid_x, mid_y, text=text_str, fill="#C0392B", font=("Arial", 9, "bold"))

        for p in screen_pts:
            canvas.create_oval(p['x']-6, p['y']-6, p['x']+6, p['y']+6, fill="red", outline="black", width=2)
            canvas.create_text(p['x'], p['y']-20, text=p['name'], font=("Arial", 11, "bold"), fill="black")
            
        final_area_m2 = 0.5 * abs(area_sum)
        final_area_km2 = final_area_m2 / 1_000_000.0
        
        avg_sx = sum(p['x'] for p in screen_pts) / num
        avg_sy = sum(p['y'] for p in screen_pts) / num
        
        canvas.create_text(avg_sx, avg_sy, text=f"AREA:\n{final_area_km2:.3f} km²", 
                           font=("Arial", 14, "bold"), fill="#27AE60", justify=tk.CENTER)

        stats_frame = tk.Frame(win, bg="white")
        stats_frame.pack(fill=tk.X, pady=10)
        tk.Label(stats_frame, text=f"Total Perimeter: {total_dist_km:.3f} km", 
                 font=("Segoe UI", 16, "bold"), fg="#2980B9", bg="white").pack()
        tk.Label(stats_frame, text="* Shape is automatically closed (Last Point → First Point).", 
                 font=("Segoe UI", 9), fg="gray", bg="white").pack()

    # ----------------------------------------------------------------
    # 4. PETREL TAB
    # ----------------------------------------------------------------
    def setup_petrel_tab(self):
        frame = tk.LabelFrame(self.tab_petrel, text="🛢️ Petrel Well Export", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Export points as Well Heads compatible with Petrel.", font=("Arial", 12)).pack(pady=10)
        tk.Label(frame, text="Format: [Name] [X-Coord] [Y-Coord] [KB=0] [TD=0]", fg="gray").pack()
        tk.Button(frame, text="📄 Export Petrel Well Heads", bg="#D35400", fg="white", font=("Arial", 12, "bold"),
                  command=self.export_petrel_wells, height=2, width=25).pack(pady=20)

    # ----------------------------------------------------------------
    # 5. ARCGIS TAB
    # ----------------------------------------------------------------
    def setup_arcgis_tab(self):
        frame = tk.Frame(self.tab_arcgis)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        lbl = tk.LabelFrame(frame, text="🗺️ Export to GIS Formats", padx=10, pady=10)
        lbl.pack(fill=tk.X)
        btn_box = tk.Frame(lbl)
        btn_box.pack(pady=10)
        tk.Button(btn_box, text="📄 Shapefile (SHP)", bg="#27AE60", fg="white", width=15, command=lambda: messagebox.showinfo("Info", "SHP requires GDAL library.")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_box, text="🌎 Google KML", bg="#2980B9", fg="white", width=15, command=self.export_kml).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_box, text="🔢 CSV (Points)", bg="#F39C12", fg="white", width=15, command=self.export_csv).pack(side=tk.LEFT, padx=5)
        info_frame = tk.Frame(frame, bg="#F9E79F", pady=10)
        info_frame.pack(fill=tk.X, pady=20)
        tk.Label(info_frame, text="ℹ️ GIS Info:", bg="#F9E79F", font=("Arial", 10, "bold")).pack()
        tk.Label(info_frame, text="• CSV: Universal format, loadable in ArcGIS/QGIS as XY Data.\n• KML: Directly opens in Google Earth.\n• Use UTM Zone 39N for Iran projects.", bg="#F9E79F", justify=tk.LEFT).pack()

    # ----------------------------------------------------------------
    # 6. DOWNLOAD TAB
    # ----------------------------------------------------------------
    def setup_download_tab(self):
        frame = tk.Frame(self.tab_download)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        links_frame = tk.LabelFrame(frame, text="🔗 Download Links")
        links_frame.pack(fill=tk.X, pady=10)
        dl_btns = [
            ("🌍 Download Google Earth Pro", "https://www.google.com/earth/versions/#earth-pro", "#4285F4"),
            ("🗺️ Download ArcGIS Pro (Trial)", "https://www.esri.com/en-us/arcgis/products/arcgis-pro/trial", "#2C3E50"),
            ("🛢️ Petrel Information", "https://www.software.slb.com/products/petrel", "#E67E22")
        ]
        for text, url, color in dl_btns:
            tk.Button(links_frame, text=text, fg="white", bg=color, width=40,
                      command=lambda u=url: webbrowser.open(u)).pack(pady=5)
        check_frame = tk.LabelFrame(frame, text="🔍 System Check")
        check_frame.pack(fill=tk.X, pady=10)
        tk.Label(check_frame, text="Check if GIS software is installed on this PC:").pack(pady=5)
        tk.Button(check_frame, text="🕵️ Run Software Check", bg="#8E44AD", fg="white",
                  command=self.check_installed_software).pack(pady=10)
        self.check_result = tk.Label(check_frame, text="", fg="blue")
        self.check_result.pack(pady=5)

    # ============================================================
    # HELPER METHODS
    # ============================================================
    
    def change_zoom(self, direction):
        self.base_font_size += direction
        if self.base_font_size < 8: self.base_font_size = 8
        if self.base_font_size > 16: self.base_font_size = 16
        self.update_app_font()

    def update_app_font(self):
        default_font = ("Segoe UI", self.base_font_size)
        self.style.configure(".", font=default_font)
        self.style.configure("Treeview.Heading", font=("Segoe UI", self.base_font_size, "bold"))
        self.root.option_add("*Font", default_font)
    
    def apply_theme(self, theme_name):
        colors = self.themes[theme_name]
        self.root.configure(bg=colors["bg"])
        self.header_frame.configure(bg=colors["header"])
        self.controls_frame.configure(bg=colors["header"])
        self.title_label.configure(bg=colors["header"])
        self.style.configure('TFrame', background=colors["bg"])
        self.style.configure('TLabel', background=colors["bg"], foreground=colors["fg"])
        self.style.configure('TLabelframe', background=colors["bg"], foreground=colors["fg"])
        self.style.configure('TLabelframe.Label', background=colors["bg"], foreground=colors["fg"])
        self.log_operation(f"Theme changed to {theme_name}")

    def add_point(self):
        try:
            name = self.name_entry.get()
            lat = parse_dms(self.lat_entry.get())
            lon = parse_dms(self.lon_entry.get())
            zone = int(self.zone_entry.get())
            if lat is None or lon is None: raise ValueError("Invalid DMS")
            x, y, z, L = latlon_to_utm(lat, lon, zone)
            pt = {'name': name, 'lat': lat, 'lon': lon, 'easting': x, 'northing': y, 'zone': f"{z}{L}"}
            self.points.append(pt)
            self.tree.insert('', 'end', values=(name, f"{lat:.5f}", f"{lon:.5f}", f"{x:.2f}", f"{y:.2f}", f"{z}{L}"))
            self.log_operation(f"Point Added: {name}")
            messagebox.showinfo("Success", "Point Added!")
        except Exception as e:
            self.log_operation(f"Error Adding Point: {e}")
            messagebox.showerror("Error", f"Check inputs! {e}")

    def open_in_google_earth(self):
        if not self.points:
            messagebox.showwarning("Warning", "No points to show!")
            return
        try:
            kml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'
            for p in self.points:
                kml_content += f'<Placemark><name>{p["name"]}</name><Point><coordinates>{p["lon"]},{p["lat"]},0</coordinates></Point></Placemark>\n'
            kml_content += '</Document></kml>'
            fd, path = tempfile.mkstemp(suffix=".kml")
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(kml_content)
            self.log_operation("Opening Google Earth...")
            os.startfile(path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Google Earth: {e}")

    def open_in_google_maps(self):
        if not self.points:
            messagebox.showwarning("Warning", "No points to show!")
            return
        url = "https://www.google.com/maps/dir/"
        for i, p in enumerate(self.points):
            url += f"{p['lat']},{p['lon']}/"
            if i >= 9: break 
        self.log_operation("Opening Google Maps...")
        webbrowser.open(url)

    def generate_qr_code(self):
        if not HAS_FANCY_LIBS:
            messagebox.showerror("Missing Libraries", "Please install 'qrcode' and 'pillow':\npip install qrcode pillow")
            return
        if not self.points:
            messagebox.showwarning("Warning", "No points to generate QR for!")
            return
        url = "https://www.google.com/maps/dir/"
        for i, p in enumerate(self.points):
            url += f"{p['lat']},{p['lon']}/"
            if i >= 8: break
        try:
            qr = qrcode.QRCode(box_size=10, border=4)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            top = tk.Toplevel(self.root)
            top.title("📱 Scan to View on Map")
            top.geometry("450x500")
            margin_frame = tk.Frame(top, bg="#ECF0F1", padx=30, pady=30)
            margin_frame.pack(expand=True, fill=tk.BOTH)
            tk.Label(margin_frame, text="Scan with mobile camera:", font=("Arial", 11, "bold"), bg="#ECF0F1").pack(pady=(0, 10))
            self.tk_qr = ImageTk.PhotoImage(img)
            tk.Label(margin_frame, image=self.tk_qr, bg="white", relief="solid", bd=1).pack()
            tk.Label(margin_frame, text="Opens Google Maps with your points.", fg="gray", bg="#ECF0F1").pack(pady=10)
            self.log_operation("QR Code Generated.")
        except Exception as e:
            messagebox.showerror("Error", f"QR Generation failed: {e}")

    def save_json(self):
        f = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
        if f:
            with open(f, 'w') as file: json.dump(self.points, file)
            self.log_operation("Project Saved (JSON).")
            messagebox.showinfo("Saved", "Project saved.")

    def load_json(self):
        f = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if f:
            with open(f, 'r') as file: self.points = json.load(file)
            for item in self.tree.get_children(): self.tree.delete(item)
            for p in self.points:
                 self.tree.insert('', 'end', values=(p['name'], f"{p['lat']:.5f}", f"{p['lon']:.5f}", f"{p['easting']:.2f}", f"{p['northing']:.2f}", p['zone']))
            self.log_operation("Project Loaded (JSON).")
            messagebox.showinfo("Loaded", "Project loaded.")

    def reset_all(self):
        if messagebox.askyesno("Reset", "Clear all data?"):
            self.points = []
            for item in self.tree.get_children(): self.tree.delete(item)
            self.log_operation("Data Reset.")

    def create_excel_template(self):
        try:
            import openpyxl
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(['Name', 'Lat_DMS', 'Lon_DMS'])
            ws.append(['Point1', "35°41'21\"", "51°25'23\""])
            f = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile="Template.xlsx")
            if f:
                wb.save(f)
                self.log_operation("Excel Template Created.")
                try: os.startfile(f)
                except: messagebox.showinfo("Saved", "Template saved.")
        except ImportError:
            messagebox.showerror("Error", "Install openpyxl: pip install openpyxl")

    def import_excel(self):
        try:
            import openpyxl
        except ImportError:
            messagebox.showerror("Error", "Library 'openpyxl' is missing.\nInstall it using: pip install openpyxl")
            return
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if not file_path: return
        try:
            wb = openpyxl.load_workbook(file_path, data_only=True)
            sheet = wb.active
            try: current_zone = int(self.zone_entry.get())
            except: current_zone = 39
            count = 0
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if not row or len(row) < 3 or row[0] is None: continue
                name = str(row[0])
                lat_val = parse_dms(row[1])
                lon_val = parse_dms(row[2])
                if lat_val is None or lon_val is None: continue
                x, y, z, L = latlon_to_utm(lat_val, lon_val, current_zone)
                pt = {'name': name, 'lat': lat_val, 'lon': lon_val, 'easting': x, 'northing': y, 'zone': f"{z}{L}"}
                self.points.append(pt)
                self.tree.insert('', 'end', values=(name, f"{lat_val:.5f}", f"{lon_val:.5f}", f"{x:.2f}", f"{y:.2f}", f"{z}{L}"))
                count += 1
            self.log_operation(f"Imported {count} points from Excel.")
            messagebox.showinfo("Success", f"Successfully imported {count} points from Excel.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read Excel file:\n{e}")

    def do_convert_dms_utm(self):
        try:
            l = parse_dms(self.conv_lat.get())
            n = parse_dms(self.conv_lon.get())
            x, y, z, let = latlon_to_utm(l, n)
            self.res_utm.delete("1.0", tk.END)
            self.res_utm.insert("1.0", f"E: {x:.2f}\nN: {y:.2f}\nZone: {z}{let}")
        except: self.res_utm.insert("1.0", "Error")

    def do_convert_utm_dms(self):
        try:
            e = float(self.conv_east.get())
            n = float(self.conv_north.get())
            zn = int(self.conv_znum.get())
            lat, lon = utm_to_latlon(e, n, zn)
            self.res_dms.delete("1.0", tk.END)
            self.res_dms.insert("1.0", f"Lat: {decimal_to_dms(lat)}\nLon: {decimal_to_dms(lon)}")
        except: self.res_dms.insert("1.0", "Error")

    def export_petrel_wells(self):
        if not self.points: return
        f = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Petrel Well Heads","*.txt")])
        if f:
            with open(f, 'w') as file:
                file.write("Name X Y KB TD\n")
                for p in self.points:
                    file.write(f"{p['name']} {p['easting']:.2f} {p['northing']:.2f} 0 0\n")
            self.log_operation("Exported Petrel Well Heads.")
            messagebox.showinfo("Success", "Exported for Petrel!")

    def export_csv(self):
        if not self.points: return
        f = filedialog.asksaveasfilename(defaultextension=".csv")
        if f:
            with open(f, 'w', newline='') as csvfile:
                w = csv.writer(csvfile)
                w.writerow(['Name', 'Lat', 'Lon', 'X', 'Y', 'Zone'])
                for p in self.points:
                    w.writerow([p['name'], p['lat'], p['lon'], p['easting'], p['northing'], p['zone']])
            self.log_operation("Exported CSV.")
            messagebox.showinfo("Done", "CSV Saved.")
            
    def export_kml(self):
        if not self.points: return
        f = filedialog.asksaveasfilename(defaultextension=".kml")
        if f:
            kml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'
            for p in self.points:
                kml_content += f'<Placemark><name>{p["name"]}</name><Point><coordinates>{p["lon"]},{p["lat"]},0</coordinates></Point></Placemark>\n'
            kml_content += '</Document></kml>'
            with open(f, "w") as file: file.write(kml_content)
            self.log_operation("Exported KML.")
            messagebox.showinfo("Done", "KML Saved.")

    def check_installed_software(self):
        paths = {
            "Google Earth": r"C:\Program Files\Google\Google Earth Pro\client\googleearth.exe",
            "ArcGIS Pro": r"C:\Program Files\ArcGIS\Pro\bin\ArcGISPro.exe",
            "Petrel": r"C:\Program Files\Schlumberger\Petrel\Petrel.exe"
        }
        res = "Results:\n"
        for name, path in paths.items():
            status = "✅ Found" if os.path.exists(path) else "❌ Not Found (Standard Path)"
            res += f"{name}: {status}\n"
        self.check_result.config(text=res)

    # CHANGED: Updated Info text
    def show_app_info(self):
        info_text = (
            "Coordinate Mapping v9.0 Pro\n"
            "Developed by: AI Brothers Tools\n\n"
            "This application is a professional tool for Geomatics and Petroleum Engineering.\n"
            "Features:\n"
            "- Convert Lat/Lon to UTM and vice versa.\n"
            "- Visualize shapes, calculate Area & Perimeter.\n"
            "- Export to Petrel, ArcGIS (Shape/CSV), and Google Earth.\n"
            "- Direct integration with Google Maps/Earth.\n\n"
            "System Requirements:\n"
            "RAM: 4GB minimum (8GB Recommended)\n"
            "CPU: Intel Core i5 or equivalent\n\n"
            "Support: info@aibrotherstools.ir"
        )
        messagebox.showinfo("Application Information", info_text)

    # CHANGED: Updated License text to Proprietary
    def show_license(self):
        license_text = (
            "PROPRIETARY SOFTWARE LICENSE AGREEMENT\n\n"
            "This software is the exclusive property of AI Brothers Tools.\n\n"
            "1. GRANT OF LICENSE: AI Brothers Tools grants you a non-exclusive, "
            "non-transferable license to use this software solely for your internal business purposes.\n\n"
            "2. RESTRICTIONS: You may not reverse engineer, decompile, or disassemble the software. "
            "You may not distribute, rent, lease, or sub-license the software.\n\n"
            "3. OWNERSHIP: All title, ownership rights, and intellectual property rights in and to the "
            "software remain with AI Brothers Tools.\n\n"
            "4. TERMINATION: This license is effective until terminated. Your rights under this license "
            "will terminate automatically without notice if you fail to comply with any term(s).\n\n"
            "Copyright © 2026 AI Brothers Tools. All Rights Reserved."
        )
        messagebox.showwarning("PROPRIETARY LICENSE", license_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = CoordinateApp(root)
    root.mainloop()

