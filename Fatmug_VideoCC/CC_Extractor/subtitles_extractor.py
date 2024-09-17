import subprocess
import os
from django.conf import settings
from .models import Subtitle

def extract_subtitles(video):
    subtitle_files = []
    try:
        # Create subtitles directory within MEDIA_ROOT
        subtitles_dir = os.path.join(settings.MEDIA_ROOT, 'subtitles')
        os.makedirs(subtitles_dir, exist_ok=True)
        
        # Run ffprobe to get subtitle streams
        result = subprocess.run(
            ['ffprobe', '-loglevel', 'error', '-select_streams', 's',
             '-show_entries', 'stream=index:stream_tags=language', 
             '-of', 'csv=p=0', video.video_file.path],
            capture_output=True, text=True, check=True
        )

        # Process ffprobe output
        for line in result.stdout.strip().splitlines():
            if ',' in line:
                idx, lang = line.split(',')
                if not lang:  # Handle missing language
                    lang = "unknown"
            else:
                idx = line
                lang = "unknown"  # Default language if not provided
            
            # Define subtitle file path within the media directory
            subtitle_file_name = f"{video.title}_{lang}_{idx}.vtt"
            subtitle_file_path = os.path.join(subtitles_dir, subtitle_file_name)

            # Prepare and run ffmpeg command to extract subtitles
            ffmpeg_command = [
                'ffmpeg', '-nostdin', '-y', '-hide_banner', '-loglevel', 'quiet',
                '-i', video.video_file.path,
                '-map', f'0:{idx}', subtitle_file_path
            ]
            subprocess.run(ffmpeg_command, check=True)

            # Save subtitle file to the database
            subtitle = Subtitle.objects.create(
                video=video,
                subtitle_file=os.path.join('subtitles', subtitle_file_name),  # Store relative path
                language=lang
            )
            subtitle_files.append(subtitle.subtitle_file)

        # Check if the video file is in .mkv format
        if video.video_file.path.endswith('.mkv'):
            # Define the new .mp4 file path within MEDIA_ROOT
            mkv_path = video.video_file.path
            mp4_file_name = video.video_file.name.replace('.mkv', '.mp4')
            mp4_file_path = os.path.join(settings.MEDIA_ROOT, mp4_file_name)

            # Convert .mkv to .mp4 using ffmpeg
            convert_command = ['ffmpeg', '-i', video.video_file.path, '-c', 'copy', mp4_file_path]
            subprocess.run(convert_command, check=True)

            # Update the video file path to the .mp4 file in the database
            video.video_file.name = mp4_file_name  # Update the relative path in the database
            video.save()
            
            if os.path.exists(mkv_path):
                os.remove(mkv_path)

    except subprocess.CalledProcessError as e:
        print(f"Error processing {video.video_file.path}: {e}")

    return subtitle_files
