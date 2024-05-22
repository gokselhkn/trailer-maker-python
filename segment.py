import os
from moviepy.editor import VideoFileClip

# Get the directory of the current script
script_directory = os.path.dirname(__file__)

# Define the duration of each segment in seconds
segment_duration = 3

# Find all existing subclips in the subclips folder
subclips_folder = os.path.join(script_directory, "subclips")
subclip_files = [file for file in os.listdir(subclips_folder) if file.endswith(".mp4")]

# Iterate over each existing subclip
for subclip_file in subclip_files:
    # Create a subfolder for this subclip
    subclip_name = os.path.splitext(subclip_file)[0]
    subclip_folder = os.path.join(subclips_folder, subclip_name)
    os.makedirs(subclip_folder, exist_ok=True)

    # Load the subclip
    subclip_path = os.path.join(subclips_folder, subclip_file)
    subclip = VideoFileClip(subclip_path)

    # Calculate the number of segments in this subclip
    num_segments = int(subclip.duration // segment_duration)

    # Create and save each segment
    for j in range(num_segments):
        segment_start = j * segment_duration
        segment_end = (j + 1) * segment_duration

        # Ensure the end time does not exceed the subclip duration
        if segment_end > subclip.duration:
            segment_end = subclip.duration

        # Extract the segment
        segment = subclip.subclip(segment_start, segment_end)

        # Construct the segment filename including subclip name
        segment_filename = os.path.join(
            subclip_folder, f"{subclip_name}_segment_{j + 1}.mp4"
        )

        # Save the segment
        segment.write_videofile(segment_filename, codec="libx264", fps=25)

    # Close the subclip
    subclip.close()

print(
    f"Segments created and saved in their respective subfolders within the '{subclips_folder}' folder successfully."
)
