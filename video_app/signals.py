import os
import subprocess
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Video


@receiver(post_save, sender=Video)
def convert_video_to_hls(sender, instance, created, **kwargs):
    if not created or not instance.video:
        return

    video_id = instance.id
    input_path = instance.video.path
    resolutions = ['480p', '720p', '1080p']
    media_root = settings.MEDIA_ROOT

    for res in resolutions:
        output_dir = os.path.join(media_root, f"hls/{video_id}/{res}")
        os.makedirs(output_dir, exist_ok=True)

        subprocess.call([
            "ffmpeg", "-i", input_path,
            "-vf", f"scale=-2:{res.replace('p', '')}",
            "-profile:v", "baseline", "-level", "3.0",
            "-start_number", "0", "-hls_time", "10", "-hls_list_size", "0",
            "-hls_segment_filename", f"{output_dir}/%03d.ts",
            f"{output_dir}/index.m3u8"
        ])

    thumbnail_path = os.path.join(media_root, f"thumbnails/{video_id}.jpg")
    os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)

    subprocess.call([
        "ffmpeg", "-ss", "00:00:05", "-i", input_path,
        "-frames:v", "1", "-q:v", "2", "-update", "1", thumbnail_path
    ])

    instance.thumbnail.name = f"thumbnails/{video_id}.jpg"
    instance.save(update_fields=["thumbnail"])
