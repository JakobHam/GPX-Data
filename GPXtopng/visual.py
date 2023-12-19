import os
import gpxpy
import folium
from folium import plugins

def plot_gpx_folder(folder_path, map_filename="map.html"):
    bounds = [[54, 18], [58, 1]]
    m = folium.Map(location=[56, 10], zoom_start=7, max_bounds=True, min_lat=bounds[0][0], max_lat=bounds[1][0], min_lon=bounds[0][1], max_lon=bounds[1][1])
    marker_cluster = plugins.MarkerCluster().add_to(m)
    total_points = 0
    total_lat = 0
    total_lon = 0

    for filename in os.listdir(folder_path):
        if filename.endswith('.gpx'):
            gpx_file_path = os.path.join(folder_path, filename)
            marker_cluster, total_lat, total_lon, total_points = plot_gpx_file(gpx_file_path, m, marker_cluster, total_lat, total_lon, total_points)

    if total_points > 0:
        average_lat = total_lat / total_points
        average_lon = total_lon / total_points
        m.location = [average_lat, average_lon]  # Set the new center for the map
        m.zoom_start = 12  # Set the new zoom level

        m.save(map_filename)
        print(f"Map saved as {map_filename}")
    else:
        print("No valid coordinates found in GPX files.")

def plot_gpx_file(gpx_file_path, map_obj, marker_cluster, total_lat, total_lon, total_points):
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                lats = [point.latitude for point in segment.points]
                lons = [point.longitude for point in segment.points]
                total_lat += sum(lats)
                total_lon += sum(lons)
                total_points += len(lats)
                marker_cluster = plot_points_on_map(lats, lons, map_obj, marker_cluster)

    return marker_cluster, total_lat, total_lon, total_points

def plot_points_on_map(lats, lons, map_obj, marker_cluster):
    for lat, lon in zip(lats, lons):
        folium.Marker(location=[lat, lon]).add_to(marker_cluster)

    return marker_cluster

if __name__ == "__main__":
    folder_path = "/Users/jakobsmac/Public/python_script/source"
    plot_gpx_folder(folder_path)
