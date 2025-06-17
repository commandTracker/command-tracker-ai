import ffmpeg
import io
from config.constants import MESSAGES

def insert_subtitle_to_video(video_bytes, subtitle_path):
    try:
        input_video = ffmpeg.input("pipe:0")

        output, _ = (
            input_video
            .filter("subtitles", subtitle_path)
            .output("pipe:1",
                    vcodec="libvpx-vp9",
                    acodec="libvorbis",
                    format="webm")
            .run(input=video_bytes, capture_stdout=True)
        )

        return io.BytesIO(output)

    except:
        raise RuntimeError(MESSAGES.ERROR.FAILED_INSERT_SUBTITLE)
