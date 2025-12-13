# Copyright 2025 Parviz tajdari
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import webbrowser, os, json, csv, re
from pyproj import Transformer

# ============================
# DMS / Decimal Parsing
# ============================
# Regular expression to capture Degrees / Minutes / Seconds and hemisphere
dms_regex = re.compile(
    r"""(?P<deg>-?\d+)[°\s]\s*(?P<min>\d+)?['\s]?\s*(?P<sec>[\d\.]+)?["]?\s*(?P<hem>[NnSsEeWw])?"""
)

def dms_to_decimal(d, m=0, s=0, hem=None):
    # Convert DMS components to decimal degrees, applying hemisphere sign if present
    val = abs(float(d)) + float(m or 0)/60 + float(s or 0)/3600
    if str(d).startswith('-'): val = -val
    if hem:
        hem = hem.upper()
        if hem in ('S','W'): val = -abs(val)
    return val

def parse_single_dms(token):
    # Try direct float parse first, otherwise attempt DMS regex conversion
    token = token.strip()
    try:
        return float(token)
    except:
        pass
    m = dms_regex.search(token)
    if not m:
        raise ValueError(f"Cannot parse coordinate token: {token}")
    return dms_to_decimal(m.group('deg'), m.group('min') or 0, m.group('sec') or 0, m.group('hem'))

def parse_latlon_input(text):
    # Accepts many input formats: "30°57'25.2\"N 49°06'37.4\"E", "30.957,49.11", "30.957 49.11"
    text = text.strip()
    # If both NS and EW letters present, split at the NS marker boundary
    if re.search(r'[NSns]', text) and re.search(r'[EWew]', text):
        m = re.search(r'([NSns])', text)
        n_pos = m.end()
        part1 = text[:n_pos].strip()
        part2 = text[n_pos:].strip().strip(',').strip()
        return parse_single_dms(part1), parse_single_dms(part2)
    # Comma separated decimal
    if ',' in text:
        a,b = text.split(',',1)
        return parse_single_dms(a), parse_single_dms(b)
    # Space separated
    parts = text.split()
    if len(parts) >= 2:
        return parse_single_dms(parts[0]), parse_single_dms(parts[1])
    raise ValueError("Cannot determine lat/lon pair from input")

# ============================
# UTM <-> Lat/Lon Conversion
# ============================
def latlon_to_utm(lat, lon):
    # Convert latitude/longitude (decimal degrees) to UTM easting/northing and zone string
    lat = float(lat); lon = float(lon)
    zone_number = int((lon + 180)//6) + 1
    is_north = lat >= 0
    proj = f"+proj=utm +zone={zone_number} +{'north' if is_north else 'south'} +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    transformer = Transformer.from_crs("epsg:4326", proj, always_xy=True)
    e, n = transformer.transform(lon, lat)
    z = 'N' if is_north else 'S'
    return round(e,3), round(n,3), f"{zone_number}{z}"

def utm_to_latlon(easting, northing, zone):
    # Convert UTM easting,northing,zone to latitude/longitude (decimal degrees)
    z = str(zone).strip()
    if z[-1].isalpha():
        zone_num = int(z[:-1]); hemi = z[-1].upper()
    else:
        zone_num = int(z); hemi = 'N'
    is_north = (hemi == 'N')
    proj = f"+proj=utm +zone={zone_num} +{'north' if is_north else 'south'} +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    transformer = Transformer.from_crs(proj, "epsg:4326", always_xy=True)
    lon, lat = transformer.transform(float(easting), float(northing))
    return round(lat,8), round(lon,8)

# ============================
# Logo + Join Us + Exit Button
# ============================
def add_top_right_logo(root, logo_path=" "):
    """
    Create a small top-right frame that contains:
      - Red Exit button (far right)
      - Blue 'Join Us' button with link
      - Optional logo image (if the path exists)
    The layout uses side='right' packing so that the first packed appears at the far right.
    """
    logo_frame = tk.Frame(root)
    # Place the frame at the top area; use pack with fill="x" so it spans the width
    logo_frame.pack(fill="x", padx=5, pady=5, anchor="ne")

    # Exit button: red, placed at the far right
    exit_btn = tk.Button(
        logo_frame, text="Exit",
        fg="white", bg="#d9534f",  # Bootstrap 'danger' red
        activebackground="#c9302c",
        command=root.destroy
    )
    # Pack exit button first so it appears at the extreme right when using side="right"
    exit_btn.pack(side="right", padx=5)

    # Join Us button: blue and opens the project's site
    join_btn = tk.Button(
        logo_frame, text="Join Us",
        fg="white", bg="#007bff",
        activebackground="#0069d9",
        command=lambda: webbrowser.open("https://jolly-babka-a57fa8.netlify.app/#home")
    )
    join_btn.pack(side="right", padx=5)

    # Optional logo image: display to the left of the buttons if file exists
    if os.path.exists(logo_path):
        try:
            logo_img = tk.PhotoImage(file=logo_path)
            # downscale image if too large (subsample)
            logo_img = logo_img.subsample(2, 2)
            logo_lbl = tk.Label(logo_frame, image=logo_img)
            logo_lbl.image = logo_img  # keep reference
            logo_lbl.pack(side="right", padx=5)
        except Exception:
            # If image cannot be loaded, silently skip (do not break application)
            pass

# ============================
# Main App Class
# ============================
class WellMapApp:
    def __init__(self, root):
        # Core window setup
        self.root = root
        root.title("Coordinate Mapping — Well UTM ↔ Lat/Lon")
        root.geometry("1150x720")

        # Application title label
        tk.Label(root, text="Coordinate Mapping", font=("Arial Black", 28), fg="black").pack(pady=10)

        # Theme definitions and selection UI
        self.themes = {
            "Modern": {"bg":"#f0f2f5", "fg":"#000"},
            "Classic": {"bg":"#fffaf0", "fg":"#000"},
            "Girly": {"bg":"#ffe6f2", "fg":"#000"},
            "Formal": {"bg":"#d9d9d9", "fg":"#000"}
        }
        self.theme_var = tk.StringVar(value="Modern")
        theme_frame = ttk.Frame(root); theme_frame.pack(pady=5)
        ttk.Label(theme_frame,text="Select Theme:").pack(side="left", padx=5)
        ttk.Combobox(theme_frame,textvariable=self.theme_var,values=list(self.themes.keys()),state="readonly",width=12).pack(side="left")
        ttk.Button(theme_frame,text="Apply Theme",command=self.apply_theme).pack(side="left", padx=5)

        # Add top-right logo, Join Us and Exit button using user's VSCode path
        add_top_right_logo(root, "Final_codes_30-11-2025/Cordinate_Mapping/logo_22.png")

        # Input Frame for Lat/Lon and UTM
        frm = ttk.LabelFrame(root, text="Input (Lat/Lon OR Easting+Northing+Zone)")
        frm.pack(fill="x", padx=8, pady=6)

        ttk.Label(frm, text="Well Name").grid(row=0,column=0,padx=6,pady=6,sticky="e")
        self.name_ent = ttk.Entry(frm, width=22); self.name_ent.grid(row=0,column=1,padx=6,pady=6,sticky="w")
        self.name_ent.insert(0,"Well-A1")

        ttk.Label(frm,text="Lat/Lon (DMS/decimal)").grid(row=0,column=2,padx=6,pady=6,sticky="e")
        self.latlon_ent = ttk.Entry(frm,width=36); self.latlon_ent.grid(row=0,column=3,padx=6,pady=6,sticky="w")
        self._set_placeholder(self.latlon_ent,'30°57\'25.2"N 49°06\'37.4"E')

        ttk.Label(frm,text="Easting (UTM)").grid(row=1,column=0,padx=6,pady=6,sticky="e")
        self.e_ent = ttk.Entry(frm,width=20); self.e_ent.grid(row=1,column=1,padx=6,pady=6,sticky="w")
        self._set_placeholder(self.e_ent,"500000.00")

        ttk.Label(frm,text="Northing (UTM)").grid(row=1,column=2,padx=6,pady=6,sticky="e")
        self.n_ent = ttk.Entry(frm,width=20); self.n_ent.grid(row=1,column=3,padx=6,pady=6,sticky="w")
        self._set_placeholder(self.n_ent,"3420000.00")

        ttk.Label(frm,text="Zone (e.g., 39N)").grid(row=1,column=4,padx=6,pady=6,sticky="e")
        self.zone_ent = ttk.Entry(frm,width=10); self.zone_ent.grid(row=1,column=5,padx=6,pady=6,sticky="w")
        self.zone_ent.insert(0,"39N")

        ttk.Button(frm,text="Add / Convert",command=self.add_point).grid(row=0,column=5,padx=8,pady=6)
        ttk.Button(frm,text="Import JSON",command=self.import_json).grid(row=1,column=6,padx=6,pady=6)

        # Treeview to list points
        cols = ("Name","Latitude","Longitude","Easting","Northing","Zone")
        self.tree = ttk.Treeview(root,columns=cols,show="headings",selectmode="extended")
        for c in cols:
            self.tree.heading(c,text=c)
            self.tree.column(c,width=150,anchor="center")
        self.tree.pack(fill="both",expand=True,padx=8,pady=6)
        vsb = ttk.Scrollbar(self.tree.master,orient="vertical",command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set); vsb.pack(side="right",fill="y")
        self.tree.bind("<Double-1>",self.on_double_click)

        # Buttons frame: actions for selected rows and exports
        btns = ttk.Frame(root); btns.pack(fill="x", padx=8, pady=6)
        ttk.Button(btns,text="Edit Selected",command=self.edit_selected).pack(side="left", padx=6)
        ttk.Button(btns,text="Delete Selected",command=self.delete_selected).pack(side="left", padx=6)
        ttk.Button(btns,text="Copy Selected Google Maps Link",command=self.copy_link).pack(side="left", padx=6)
        ttk.Button(btns,text="Open Selected in Google Maps",command=self.open_selected).pack(side="left", padx=6)
        ttk.Button(btns,text="Open ALL in Google Maps",command=self.open_all).pack(side="left", padx=6)
        ttk.Button(btns,text="Export CSV",command=self.export_csv).pack(side="left", padx=6)
        ttk.Button(btns,text="Export JSON",command=self.export_json).pack(side="left", padx=6)
        ttk.Button(btns,text="Export KML",command=self.export_kml).pack(side="left", padx=6)
        ttk.Button(btns,text="Reset",command=self.reset_all).pack(side="left", padx=6)
        ttk.Button(btns,text="Exit",command=root.destroy).pack(side="right", padx=6)

        # Status bar at bottom
        self.status = tk.StringVar(value="Ready")
        ttk.Label(root,textvariable=self.status,relief="sunken",anchor="w").pack(fill="x",side="bottom")

        # Apply default theme settings
        self.apply_theme()

    # ============================
    # Theme application
    # ============================
    def apply_theme(self):
        theme = self.themes.get(self.theme_var.get(),{})
        bg = theme.get("bg","#f0f0f0")
        fg = theme.get("fg","#000")
        self.root.configure(bg=bg)
        # Attempt to configure common child widgets; safe-guard with try/except
        for child in self.root.winfo_children():
            try:
                child.configure(bg=bg, fg=fg)
            except:
                pass

    # ============================
    # Placeholder Helper for Entry widgets
    # ============================
    def _set_placeholder(self,entry,text):
        entry.insert(0,text)
        def on_focus_in(event,w=entry,t=text):
            if w.get()==t: w.delete(0,tk.END)
        def on_focus_out(event,w=entry,t=text):
            if w.get().strip()=="": w.delete(0,tk.END); w.insert(0,t)
        entry.bind("<FocusIn>",on_focus_in)
        entry.bind("<FocusOut>",on_focus_out)

    # ============================
    # Add / Edit / Delete Points
    # ============================
    def add_point(self):
        name = self.name_ent.get().strip()
        latlon_txt = self.latlon_ent.get().strip()
        e_txt = self.e_ent.get().strip()
        n_txt = self.n_ent.get().strip()
        zone_txt = self.zone_ent.get().strip()
        lat = lon = None
        try:
            if latlon_txt and latlon_txt != '30°57\'25.2"N 49°06\'37.4"E':
                lat, lon = parse_latlon_input(latlon_txt)
            elif e_txt and n_txt and zone_txt:
                lat, lon = utm_to_latlon(e_txt, n_txt, zone_txt)
            else:
                messagebox.showwarning("Input","Enter Lat/Lon OR UTM+Zone")
                return
        except Exception as ex:
            messagebox.showerror("Parse error",f"{ex}")
            return
        try:
            easting, northing, zone_out = latlon_to_utm(lat, lon)
        except Exception as ex:
            messagebox.showerror("Conversion error",f"{ex}")
            return
        if not name:
            messagebox.showwarning("Name required","Enter Well Name")
            return
        self.tree.insert("", "end", values=(name,round(lat,8),round(lon,8),easting,northing,zone_out))
        self.status.set(f"Added: {name}")

    def edit_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info","Select a row to edit")
            return
        for item in sel:
            self.on_double_click_fake(item)

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info","Select rows to delete")
            return
        for item in sel:
            self.tree.delete(item)
        self.status.set(f"Deleted {len(sel)} row(s)")

    # ============================
    # Double-click Editing
    # ============================
    def on_double_click(self,event):
        item = self.tree.identify_row(event.y)
        if item:
            self.on_double_click_fake(item)

    def on_double_click_fake(self,item):
        vals = list(self.tree.item(item,"values"))
        new_name = simpledialog.askstring("Edit Well Name","Well Name:",initialvalue=vals[0])
        if new_name:
            vals[0] = new_name
        new_latlon = simpledialog.askstring("Edit Lat/Lon","Lat,Lon:",initialvalue=f"{vals[1]},{vals[2]}")
        if new_latlon:
            try:
                lat,lon = parse_latlon_input(new_latlon)
                e,n,z = latlon_to_utm(lat,lon)
            except:
                pass
            else:
                vals[1] = round(lat,8); vals[2] = round(lon,8); vals[3] = e; vals[4] = n; vals[5] = z
        self.tree.item(item,values=vals)
        self.status.set("Edited row")

    # ============================
    # Google Maps helpers
    # ============================
    def _get_latlon_from_item(self,item):
        vals = self.tree.item(item,"values")
        try:
            return float(vals[1]), float(vals[2])
        except:
            return None, None

    def copy_link(self):
        sel = self.tree.selection()
        if not sel: return
        latlon = self._get_latlon_from_item(sel[0])
        if latlon[0] is None: return
        link = f"https://www.google.com/maps/search/?api=1&query={latlon[0]},{latlon[1]}"
        self.root.clipboard_clear(); self.root.clipboard_append(link)
        self.status.set("Link copied")

    def open_selected(self):
        sel = self.tree.selection(); pts = []
        for item in sel:
            latlon = self._get_latlon_from_item(item)
            if latlon[0]:
                pts.append(f"{latlon[0]},{latlon[1]}")
        if pts:
            webbrowser.open("https://www.google.com/maps/dir/" + "/".join(pts))
            self.status.set("Opened selected points")

    def open_all(self):
        pts = []
        for it in self.tree.get_children():
            latlon = self._get_latlon_from_item(it)
            if latlon[0]:
                pts.append(f"{latlon[0]},{latlon[1]}")
        if pts:
            webbrowser.open("https://www.google.com/maps/dir/" + "/".join(pts))
            self.status.set("Opened all points")

    # ============================
    # Export / Import functions
    # ============================
    def export_csv(self):
        rows = [self.tree.item(it,"values") for it in self.tree.get_children()]
        if not rows: return
        fn = filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV","*.csv")])
        if not fn: return
        header = ["Name","Latitude","Longitude","Easting","Northing","Zone"]
        with open(fn,"w",newline="",encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(header); [w.writerow(r) for r in rows]
        self.status.set(f"CSV exported: {os.path.basename(fn)}")

    def export_json(self):
        data = [{"Name":vals[0],"Latitude":vals[1],"Longitude":vals[2],"Easting":vals[3],"Northing":vals[4],"Zone":vals[5]} for vals in [self.tree.item(it,"values") for it in self.tree.get_children()]]
        if not data: return
        fn = filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("JSON","*.json")])
        if not fn: return
        with open(fn,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=2)
        self.status.set(f"JSON exported: {os.path.basename(fn)}")

    def import_json(self):
        fn = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if not fn: return
        with open(fn,"r",encoding="utf-8") as f:
            data = json.load(f)
        for rec in data:
            try:
                name = rec.get("Name","Well")
                lat = rec.get("Latitude"); lon = rec.get("Longitude")
                e = rec.get("Easting"); n = rec.get("Northing"); z = rec.get("Zone")
                self.tree.insert("", "end", values=(name,lat,lon,e,n,z))
            except:
                continue
        self.status.set(f"Imported {len(data)} items from JSON")

    def export_kml(self):
        kml_tpl = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"><Document>{}</Document></kml>"""
        placemarks = ""
        for it in self.tree.get_children():
            vals = self.tree.item(it,"values")
            placemarks += f"<Placemark><name>{vals[0]}</name><Point><coordinates>{vals[2]},{vals[1]},0</coordinates></Point></Placemark>\n"
        if not placemarks: return
        fn = filedialog.asksaveasfilename(defaultextension=".kml",filetypes=[("KML","*.kml")])
        if not fn: return
        with open(fn,"w",encoding="utf-8") as f:
            f.write(kml_tpl.format(placemarks))
        self.status.set(f"KML exported: {os.path.basename(fn)}")

    # ============================
    # Reset All
    # ============================
    def reset_all(self):
        for it in self.tree.get_children():
            self.tree.delete(it)
        self.status.set("All data cleared")

# ============================
# Run App
# ============================
if __name__=="__main__":
    root = tk.Tk()
    app = WellMapApp(root)
    root.mainloop()
