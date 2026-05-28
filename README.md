
## Coordinate Mapping — Well UTM ↔ Lat/Lon
Coordinate Mapping — Well UTM ↔ Lat/Lon A Tkinter-based desktop application for geoscientists and engineers to convert, manage, and visualize well coordinates between Lat/Lon (decimal &amp; DMS) and UTM systems, with Google Maps integration and multiple export formats (CSV, JSON, KML).


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

<img width="1362" height="1116" alt="1" src="https://github.com/user-attachments/assets/185b8ca7-a1e7-40ae-8ce7-7806dd6dea5c" />
<img width="1366" height="1116" alt="5" src="https://github.com/user-attachments/assets/e1c47d3d-0542-4dfb-aac3-989826ac71e0" />
<img width="1365" height="1116" alt="4" src="https://github.com/user-attachments/assets/d1b3f434-1096-48e8-a47c-ac469874ce6c" />
<img width="1207" height="1116" alt="3" src="https://github.com/user-attachments/assets/835cbe31-b90f-4501-af17-181bb65af2c0" />
<img width="1366" height="1116" alt="2" src="https://github.com/user-attachments/assets/524b25de-6e86-45ca-a156-6079c91ed208" />
<img width="1366" height="1116" alt="6" src="https://github.com/user-attachments/assets/6186265c-cab8-47c8-805c-2f31591e0ad4" />




---

## Requirements

- Python **3.9+**
- Required library:
  ```bash
  pip install pyproj

## How to Run  
python well_coordinate_mapping.py

## Input Examples
Latitude / Longitude
30°57'25.2"N 49°06'37.4"E
30.957, 49.11
30.957 49.11

## UTM
Easting: 500000
Northing: 3420000
Zone: 39N

## Exports
CSV – Excel, Power BI, databases
JSON – Data exchange and automation
KML – Google Earth visualization

## Google Maps Integration
Copy Google Maps link for selected points
Open selected points as a route
Open all points at once in Google Maps

## Author
Parviz Tajdari
Geologist | Python Developer | Geospatial Tools
GitHub: https://github.com/parvizt

## Notes
Intended for engineering and geological workflows
Uses WGS84 datum
Offline, lightweight, suitable for field laptops

## Future Improvements
DXF export
Batch import from CSV
Map preview inside the app
Well trajectory support
