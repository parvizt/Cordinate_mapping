
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

<img width="1201" height="729" alt="image" src="https://github.com/user-attachments/assets/be29083f-e495-40a1-9f41-7a72fb980cd3" />


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
