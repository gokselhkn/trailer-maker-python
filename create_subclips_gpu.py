import os
import subprocess
from moviepy.editor import VideoFileClip

# Define the path to your FFmpeg binary
ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"

# Get the directory of the current script
script_directory = os.path.dirname(__file__)

# Load the main video clip to get its duration
main_clip_path = os.path.join(script_directory, "Dune.mkv")
main_clip = VideoFileClip(main_clip_path)
main_duration = main_clip.duration
main_clip.close()

# Define the duration of each subclip in seconds (5 minutes in this case)
subclip_duration = 300

# Calculate the number of subclips
num_subclips = int(main_duration // subclip_duration)

# Create a subclips folder if it doesn't exist in the script's directory
subclips_folder = os.path.join(script_directory, "subclips")
os.makedirs(subclips_folder, exist_ok=True)


# Function to format time in HH:MM:SS.mmm
def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hrs:02}:{mins:02}:{secs:06.3f}"


# Function to create subclips using FFmpeg
def create_subclip(start_time, end_time, subclip_filename):
    ffmpeg_command = [
        ffmpeg_path,
        "-i",
        main_clip_path,
        "-ss",
        format_time(start_time),
        "-to",
        format_time(end_time),
        "-c",
        "copy",  # Copy codec to preserve original quality
        "-y",
        subclip_filename,
    ]

    print("Running command:", " ".join(ffmpeg_command))  # Debugging line

    try:
        result = subprocess.run(
            ffmpeg_command, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE
        )
        print(f"FFmpeg output: {result.stdout.decode()}")  # Debugging line
    except subprocess.CalledProcessError as e:
        print(f"Error with segment processing: {e.stderr.decode()}")


# Create and save subclips
for i in range(num_subclips + 1):  # +1 to include the last segment if not exact
    start_time = i * subclip_duration
    end_time = (i + 1) * subclip_duration

    # Ensure the end time does not exceed the video duration
    if end_time > main_duration:
        end_time = main_duration

    subclip_filename = os.path.join(subclips_folder, f"subclip_{i + 1}.mp4")
    create_subclip(start_time, end_time, subclip_filename)

print(f"Subclips created and saved to the '{subclips_folder}' folder successfully.")
