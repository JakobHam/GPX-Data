import os
import gpxpy
import folium
from folium import plugins

def plot_gpx_folder(folder_path, map_filename="map.html"):
    m = folium.Map(location=[0, 0], zoom_start=10)  # Initialize the map
    total_points = 0
    total_lat = 0
    total_lon = 0

    for filename in os.listdir(folder_path):
        if filename.endswith('.gpx'):
            gpx_file_path = os.path.join(folder_path, filename)
            total_lat, total_lon, total_points = plot_gpx_file(gpx_file_path, m, total_lat, total_lon, total_points)

    if total_points > 0:
        average_lat = total_lat / total_points
        average_lon = total_lon / total_points
        m = folium.Map(location=[average_lat, average_lon], zoom_start=12)

        for filename in os.listdir(folder_path):
            if filename.endswith('.gpx'):
                gpx_file_path = os.path.join(folder_path, filename)
                plot_gpx_file(gpx_file_path, m, total_lat, total_lon, total_points)

        m.save(map_filename)
        print(f"Map saved as {map_filename}")
    else:
        print("No valid coordinates found in GPX files.")

def plot_gpx_file(gpx_file_path, map_obj, total_lat, total_lon, total_points):
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                lats = [point.latitude for point in segment.points]
                lons = [point.longitude for point in segment.points]
                total_lat += sum(lats)
                total_lon += sum(lons)
                total_points += len(lats)
                plot_points_on_map(lats, lons, map_obj)

    return total_lat, total_lon, total_points

def plot_points_on_map(lats, lons, map_obj):
    for lat, lon in zip(lats, lons):
        folium.CircleMarker(location=[lat, lon], radius=3, color='blue').add_to(map_obj)

if __name__ == "__main__":
    folder_path = "/Users/jakobsmac/Public/python_script/source"
    plot_gpx_folder(folder_path)
