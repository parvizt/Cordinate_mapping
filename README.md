# Cordinate_mapping
Coordinate Mapping — Well UTM ↔ Lat/Lon A Tkinter-based desktop application for geoscientists and engineers to convert, manage, and visualize well coordinates between Lat/Lon (decimal &amp; DMS) and UTM systems, with Google Maps integration and multiple export formats (CSV, JSON, KML).

# Coordinate Mapping — Well UTM ↔ Lat/Lon

A Python desktop application built with **Tkinter** for converting, managing, and exporting well and point coordinates between **Latitude/Longitude** and **UTM** coordinate systems.  
Designed for geology, oil & gas, surveying, and GIS-related workflows.

---

## Features

- Convert **Lat/Lon ↔ UTM** (WGS84)
- Supports **Decimal Degrees** and **DMS** formats  
  - Example: `30.957, 49.11`
  - Example: `30°57'25.2"N 49°06'37.4"E`
- Automatic UTM zone detection
- Manage multiple wells/points in a table
- Edit points via double-click
- Open points directly in **Google Maps**
- Export data to:
  - CSV
  - JSON
  - KML (Google Earth)
- Import from JSON
- Theme selection (Modern, Classic, Girly, Formal)
- Simple, offline desktop GUI

---

## Screenshots

<img width="1201" height="729" alt="image" src="https://github.com/user-attachments/assets/be29083f-e495-40a1-9f41-7a72fb980cd3" />


---

## Requirements

- Python **3.9+**
- Required library:
  ```bash
  pip install pyproj
