import os
import concurrent.futures
import subprocess
from moviepy.editor import VideoFileClip

# Define the path to your FFmpeg binary
ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"

# Get the directory of the current script
script_directory = os.path.dirname(__file__)


def get_video_duration(file_path):
    """Retrieve the duration of the video using MoviePy."""
    clip = VideoFileClip(file_path)
    duration = clip.duration
    clip.close()
    return duration


# Function to format time in HH:MM:SS.mmm
def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hrs:02}:{mins:02}:{secs:06.3f}"


def process_segment(subclip_path, subclip_name, segment_duration, j, segment_folder):
    segment_start = j * segment_duration
    segment_end = segment_start + segment_duration

    # Ensure the end time does not exceed the subclip duration
    duration = get_video_duration(subclip_path)
    if segment_end > duration:
        segment_end = duration

    segment_filename = os.path.join(
        segment_folder, f"{subclip_name}_segment_{j + 1}.mp4"
    )

    # Use ffmpeg for copying streams without re-encoding to preserve quality
    ffmpeg_command = [
        ffmpeg_path,
        "-i",
        subclip_path,
        "-ss",
        format_time(segment_start),
        "-to",
        format_time(segment_end),
        "-c",
        "copy",
        "-y",
        segment_filename,
    ]

    print("Running command:", " ".join(ffmpeg_command))  # Debugging line

    try:
        result = subprocess.run(
            ffmpeg_command, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE
        )
        print(
            f"FFmpeg output for segment {j + 1}: {result.stdout.decode()}"
        )  # Debugging line
        print(
            f"FFmpeg error (if any) for segment {j + 1}: {result.stderr.decode()}"
        )  # Debugging line
    except subprocess.CalledProcessError as e:
        print(f"Error with segment processing {j + 1}: {e.stderr.decode()}")


def process_subclip(subclip_file, subclips_folder, segment_duration):
    subclip_name = os.path.splitext(subclip_file)[0]
    subclip_folder = os.path.join(subclips_folder, subclip_name)
    os.makedirs(subclip_folder, exist_ok=True)
    subclip_path = os.path.join(subclips_folder, subclip_file)

    # Get the duration of the video
    duration = get_video_duration(subclip_path)
    num_segments = int(duration // segment_duration)

    # Use all available CPU cores for processing segments
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                process_segment,
                subclip_path,
                subclip_name,
                segment_duration,
                j,
                subclip_folder,
            )
            for j in range(
                num_segments + 1
            )  # +1 to include the last segment if not exact
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error occurred: {e}")


if __name__ == "__main__":
    segment_duration = 3
    subclips_folder = os.path.join(script_directory, "subclips")
    subclip_files = [
        file
        for file in os.listdir(subclips_folder)
        if file.endswith((".mp4", ".mkv", ".avi", ".mov"))
    ]

    for subclip_file in subclip_files:
        process_subclip(subclip_file, subclips_folder, segment_duration)

    print(
        f"Segments created and saved in their respective subfolders within the '{subclips_folder}' folder successfully."
    )
