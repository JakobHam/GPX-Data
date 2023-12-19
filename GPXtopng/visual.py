import os
import gpxpy
import matplotlib.pyplot as plt

def plot_gpx_folder(folder_path):
    plt.figure(figsize=(10, 6))
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.gpx'):
            gpx_file_path = os.path.join(folder_path, filename)
            plot_gpx_file(gpx_file_path)

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('GPX Files Visualization')
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def plot_gpx_file(gpx_file_path):
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                lats = [point.latitude for point in segment.points]
                lons = [point.longitude for point in segment.points]
                plt.scatter(lons, lats, label=gpx_file_path, alpha=0.7)

if __name__ == "__main__":
    folder_path = "/Users/jakobsmac/Public/python_script/source"
    plot_gpx_folder(folder_path)
