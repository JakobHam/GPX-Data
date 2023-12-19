import os
import random
import datetime
import gpxpy

def add_random_timestamps(gpx_file):
    gpx = gpxpy.parse(gpx_file)
    
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                # Add a random timestamp within a specific range
                random_time = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))
                point.time = random_time

    return gpx

def combine_gpx_files(folder_path, output_file):
    combined_gpx = gpxpy.gpx.GPX()

    for filename in os.listdir(folder_path):
        if filename.endswith(".gpx"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                gpx = add_random_timestamps(file.read())
                combined_gpx.tracks.extend(gpx.tracks)

    return combined_gpx

def split_and_save_gpx(gpx, num_files, output_folder):
    tracks = gpx.tracks
    num_tracks = len(tracks)
    tracks_per_file = num_tracks // num_files

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for i in range(num_files):
        start_idx = i * tracks_per_file
        end_idx = start_idx + tracks_per_file

        # Create a new GPX object for each part
        part_gpx = gpxpy.gpx.GPX()
        part_gpx.tracks.extend(tracks[start_idx:end_idx])

        # Save the part to a file
        part_filename = os.path.join(output_folder, f"part_{i + 1}.gpx")
        with open(part_filename, "w") as part_file:
            part_file.write(part_gpx.to_xml())

if __name__ == "__main__":
    input_folder = "/Users/jakobsmac/Public/python_script"
    output_file = "/Users/jakobsmac/Public/python_script/combined.gpx"
    output_folder = "/Users/jakobsmac/Public/python_script/output_parts"
    num_output_files = 10  # Change this to the desired number of output files

    combined_gpx = combine_gpx_files(input_folder, output_file)
    split_and_save_gpx(combined_gpx, num_output_files, output_folder)
