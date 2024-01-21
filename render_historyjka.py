import argparse

from historyjki_roblox.resource_manager import ResourceReadFailed
from historyjki_roblox.video.video_builder import VideoBuilder

parser = argparse.ArgumentParser(
    description="Historyjka renderer",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "story",
    help="Story filename (if in 'stories' directory), or a full path to the story",
)
parser.add_argument("--vertical", action="store_true", help="Render vertical video")
parser.add_argument(
    "-o", "--output", default=None, help="Output video name. Random value if None"
)


if __name__ == "__main__":
    args = parser.parse_args()
    video_builder = VideoBuilder()
    try:
        video_builder.build_video_from_json(
            args.story, is_video_horizontal=not args.vertical
        )
        path = video_builder.save(args.output)
    except ResourceReadFailed as exe:
        print(f"Failed to read a resource: {exe}")
    except Exception as exe:
        print(f"Video builder failed: {exe}")
