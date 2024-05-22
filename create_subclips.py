import os
from moviepy.editor import VideoFileClip

# Get the directory of the current script
script_directory = os.path.dirname(__file__)

# Load the main video clip
main_clip = VideoFileClip("Dune.mkv")

# Define the duration of each subclip in seconds (5 minutes in this case)
subclip_duration = 300

# Calculate the number of subclips
num_subclips = int(main_clip.duration // subclip_duration)

# Create a subclips folder if it doesn't exist in the script's directory
subclips_folder = os.path.join(script_directory, "subclips")
os.makedirs(subclips_folder, exist_ok=True)

# Create and save subclips
for i in range(num_subclips):
    start_time = i * subclip_duration
    end_time = (i + 1) * subclip_duration

    # Ensure the end time does not exceed the video duration
    if end_time > main_clip.duration:
        end_time = main_clip.duration

    subclip = main_clip.subclip(start_time, end_time)
    subclip_filename = os.path.join(subclips_folder, f"subclip_{i + 1}.mp4")
    subclip.write_videofile(subclip_filename, codec="libx264", fps=25)

print(f"Subclips created and saved to the '{subclips_folder}' folder successfully.")
