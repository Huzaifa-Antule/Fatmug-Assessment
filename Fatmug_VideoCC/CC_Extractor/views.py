from django.shortcuts import render,redirect,get_object_or_404
from django.http import request,JsonResponse
from .subtitles_extractor import extract_subtitles
from django.conf import settings
from .models import Video,Subtitle
import webvtt
import os
import mimetypes

# Create your views here.
def Home(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        video_file = request.FILES.get('video_file')

        # Check if file is uploaded and if it's a valid video
        if not video_file:
            message = "Please upload a video file."
            return render(request, 'home.html', {'message': message})

        mime_type, _ = mimetypes.guess_type(video_file.name)
        if not mime_type or not mime_type.startswith('video'):
            message = "Invalid file type. Please upload a valid video file."
            return render(request, 'home.html', {'message': message})

        # Save the video file to the database
        try:
            video = Video.objects.create(title=title, video_file=video_file)
        except Exception as e:
            message = f"Failed to upload video. Error: {e}"
            return render(request, 'home.html', {'message': message})

        try:
            # Extract subtitles using the custom function
            subtitle_files = extract_subtitles(video)

            # If subtitles are successfully extracted, show a success message
            message = "Subtitles extracted successfully!"
            return render(request, 'home.html', {'message': message, 'subtitle_files': subtitle_files})

        except Exception as e:
            message = f"An error occurred during subtitle extraction: {e}"
            return render(request, 'home.html', {'message': message})

    return render(request, 'home.html')

def Search_Functionality(request,id):
    # Get the video object based on video_id
    video = get_object_or_404(Video, pk=id)
    subtitles = []  # List to hold all subtitle captions

    # Loop through all subtitles for this video
    for subtitle in video.subtitles.all():
        vtt_file = subtitle.subtitle_file.path  # Get the actual file path of the VTT file
        for caption in webvtt.read(vtt_file):  # Read the VTT file
            # Append all subtitles to the list
            subtitles.append({
                'start': caption.start,  # Start time of the subtitle
                'text': caption.text     # The subtitle text
            })
    # Render the template with video and subtitle data
    return render(request, 'search.html', {
        'video': video,
        'subtitles': subtitles,  # Pass the subtitles to the template
    })

def Video_Detail(request):
    video_id = request.GET.get('video_id')  # Get video_id from query params
    video = None
    subtitles = []

    if video_id:
        # Fetch and display the details of a specific video
        video = get_object_or_404(Video, pk=video_id)
        subtitles = [
            {'start': caption.start, 'text': caption.text}
            for subtitle in video.subtitles.all()
            for caption in webvtt.read(subtitle.subtitle_file.path)
        ]

    # List all videos
    videos = Video.objects.all()[::-1]

    return render(request, 'video_detail.html', {
        'videos': videos,
        'video': video,
        'subtitles': subtitles,
    })