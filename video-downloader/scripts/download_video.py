#!/usr/bin/env python3
"""
YouTube Video Downloader
Downloads videos from YouTube with customizable quality and format options.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

DEFAULT_OUTPUT_DIR = Path.cwd() / "outputs"


def check_yt_dlp():
    """Check if yt-dlp is installed, install if not."""
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("yt-dlp not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)


def get_video_info(url):
    """Get information about the video without downloading."""
    result = subprocess.run(
        ["yt-dlp", "--dump-json", "--no-playlist", url],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def download_video(url, output_path=str(DEFAULT_OUTPUT_DIR), quality="best", format_type="mp4", audio_only=False):
    """Download a YouTube video."""
    check_yt_dlp()
    output_dir = Path(output_path).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = ["yt-dlp"]

    if audio_only:
        cmd.extend([
            "-x",
            "--audio-format",
            "mp3",
            "--audio-quality",
            "0",
        ])
    else:
        if quality == "best":
            format_string = "bestvideo+bestaudio/best"
        elif quality == "worst":
            format_string = "worstvideo+worstaudio/worst"
        else:
            height = quality.replace("p", "")
            format_string = f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"

        cmd.extend([
            "-f",
            format_string,
            "--merge-output-format",
            format_type,
        ])

    cmd.extend([
        "-o",
        str(output_dir / "%(title)s.%(ext)s"),
        "--no-playlist",
    ])

    cmd.append(url)

    print(f"Downloading from: {url}")
    print(f"Quality: {quality}")
    print(f"Format: {'mp3 (audio only)' if audio_only else format_type}")
    print(f"Output: {output_dir}\n")

    try:
        info = get_video_info(url)
        print(f"Title: {info.get('title', 'Unknown')}")
        print(f"Duration: {info.get('duration', 0) // 60}:{info.get('duration', 0) % 60:02d}")
        print(f"Uploader: {info.get('uploader', 'Unknown')}\n")
        subprocess.run(cmd, check=True)
        print("\nDownload complete!")
        return True
    except subprocess.CalledProcessError as error:
        print(f"\nDownload failed: {error}")
        return False
    except Exception as error:
        print(f"\nError: {error}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos with customizable quality and format"
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "-o",
        "--output",
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "-q",
        "--quality",
        default="best",
        choices=["best", "1080p", "720p", "480p", "360p", "worst"],
        help="Video quality (default: best)",
    )
    parser.add_argument(
        "-f",
        "--format",
        default="mp4",
        choices=["mp4", "webm", "mkv"],
        help="Video format (default: mp4)",
    )
    parser.add_argument(
        "-a",
        "--audio-only",
        action="store_true",
        help="Download only audio as MP3",
    )

    args = parser.parse_args()

    success = download_video(
        url=args.url,
        output_path=args.output,
        quality=args.quality,
        format_type=args.format,
        audio_only=args.audio_only,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
