from yta_general_utils.file.filename import sanitize_filename
from moviepy.editor import AudioFileClip, VideoFileClip
from pathlib import Path


def is_file(filename):
    """
    Checks if the provided 'filename' is an existing and
    valid file. It returns True if yes or False if not.
    """
    filename = sanitize_filename(filename)
    filename = Path(filename)

    return filename.exists() and filename.is_file()

def is_folder(filename):
    """
    Checks if the provided 'filename' is an existing and
    valid folder. It returns True if yes or False if not.
    """
    filename = sanitize_filename(filename)
    filename = Path(filename)

    return filename.exists() and filename.is_dir()

def file_exists(filename):
    """
    Checks if the provided 'filename' file or folder exist. It
    returns True if existing or False if not. 
    """
    filename = sanitize_filename(filename)

    return Path(filename).exists()

def file_is_audio_file(filename):
    """
    Checks if the provided 'filename' is an audio file by
    trying to instantiate it as a moviepy AudioFileClip.
    """
    try:
        AudioFileClip(filename)
    except:
        return False
    
    return True

def file_is_video_file(filename):
    """
    Checks if the provided 'filename' is a video file by
    trying to instantiate it as a moviepy VideoFileClip.
    """
    try:
        VideoFileClip(filename)
    except:
        return False
    
    return True