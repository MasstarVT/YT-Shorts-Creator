# Story Video Creator

A Python program that creates videos by combining story text files with Piper TTS narration and random video backgrounds.

## Features

- Reads story text from any text file
- Uses Piper TTS to generate high-quality speech narration
- Randomly selects background videos from a specified folder
- Automatically adjusts video length to match audio duration
- **NEW: Adds white text subtitles with black outlines for better accessibility**
- **NEW: Split videos into segments for social media (15s, 30s, 60s, etc.)**
- **NEW: Smart duration estimation based on text length and reading speed**
- User-friendly GUI with drag-and-drop functionality
- Creates professional-looking story videos

## Requirements

### Software Dependencies
1. **Python 3.7+**
2. **Piper TTS** - Download from [Piper TTS GitHub](https://github.com/rhasspy/piper)
3. **FFmpeg** - Required by moviepy for video processing

### Python Packages
Install the required packages using:
```bash
pip install -r requirements.txt
```

Or manually install:
```bash
pip install moviepy
```

### Piper TTS Setup

1. Download Piper TTS from the official repository
2. Download a voice model (`.onnx` file) from [Piper voices](https://github.com/rhasspy/piper/blob/master/VOICES.md)
3. Place both the Piper executable and voice model in accessible locations

## Usage

### Basic Usage
```bash
python story_video_creator.py <story_file> <video_folder> <output_file>
```

### With Custom Piper Path and Voice Model
```bash
python story_video_creator.py story.txt videos/ output.mp4 --piper-path "path/to/piper.exe" --voice-model "path/to/voice.onnx"
```

### Disable Subtitles
```bash
python story_video_creator.py story.txt videos/ output.mp4 --no-subtitles
```

### Split Video into Segments
```bash
# Create 30-second segments (perfect for social media)
python story_video_creator.py story.txt videos/ output.mp4 --segment-duration 30

# Create 15-second segments (for TikTok/Instagram Reels)
python story_video_creator.py story.txt videos/ output.mp4 --segment-duration 15

# Create 60-second segments (for YouTube Shorts)
python story_video_creator.py story.txt videos/ output.mp4 --segment-duration 60
```

### Parameters

- `story_file`: Path to the text file containing your story
- `video_folder`: Path to folder containing background video files
- `output_file`: Filename for the output video (will be saved in the `output/` folder automatically)
- `--piper-path`: (Optional) Path to Piper TTS executable (default: "piper")
- `--voice-model`: (Optional) Path to Piper voice model file
- `--no-subtitles`: (Optional) Disable subtitle generation (subtitles enabled by default)
- `--segment-duration`: (Optional) Split video into segments of specified duration (seconds). Common values: 15, 30, 60

**Note**: Output files are automatically saved to the `output/` folder. If you specify just a filename (e.g., `my_video.mp4`), it will be created as `output/my_video.mp4`. To save elsewhere, provide a full path (e.g., `videos/my_video.mp4`).

**Segmentation**: When using `--segment-duration`, the original video is created first, then split into segments. Segments are saved in a folder named `{output_file}_segments/`.

## Example

```bash
# Using the sample story with videos in a "backgrounds" folder
# Output will be saved as output/my_story_video.mp4
python story_video_creator.py sample_story.txt backgrounds/ my_story_video.mp4

# With custom Piper settings
python story_video_creator.py sample_story.txt backgrounds/ my_story_video.mp4 --piper-path "C:/piper/piper.exe" --voice-model "C:/piper/voices/en_US-lessac-high.onnx"

# Create 30-second segments for social media
python story_video_creator.py sample_story.txt backgrounds/ my_story_video.mp4 --segment-duration 30

# To save to a specific location outside the output folder
python story_video_creator.py sample_story.txt backgrounds/ "videos/my_story_video.mp4"
```

## File Structure

```
YT Sorts Creater/
├── story_video_creator.py    # Main program
├── requirements.txt          # Python dependencies
├── sample_story.txt         # Example story file
├── README.md               # This file
├── output/                 # Output videos are saved here
├── backgrounds/            # Folder for background videos (create this)
│   ├── video1.mp4
│   ├── video2.mp4
│   └── ...
└── stories/               # Folder for story files
    ├── story1.txt
    ├── story2.txt
    └── ...
```

## Supported Video Formats

The program supports the following video formats:
- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- FLV (.flv)
- WMV (.wmv)
- WebM (.webm)

## How It Works

1. **Read Story**: The program reads the text content from your story file
2. **Generate Audio**: Piper TTS converts the text to high-quality speech
3. **Select Video**: A random background video is chosen from your video folder
4. **Generate Subtitles**: Text subtitles are automatically created and timed to match the narration
5. **Combine**: The audio, video, and subtitles are combined, with the video looped/trimmed to match the audio duration
6. **Output**: A final MP4 video is created with your story narration and subtitles

## Tips

- Use high-quality background videos for better results
- Keep story files in plain text format (.txt)
- Longer stories will automatically loop shorter background videos
- The program creates temporary files that are automatically cleaned up

## GUI Features

The Story Video Creator includes a user-friendly graphical interface with these features:

### Smart Duration Estimation
- **Real-time Duration Calculation**: See estimated video length before creating
- **Word Count Analysis**: Based on average TTS reading speed (160 WPM)
- **Segment Preview**: Shows how many segments will be created when using segmentation
- **Format**: Displays duration as "X.X minutes (XX seconds) | XXX words"

### Example Duration Display:
```
📊 Estimated Duration: 1.4 minutes (86 seconds) | 229 words → 3 segments of 30s each
```

### Other GUI Features:
- **Story Management**: Create, edit, and manage story files
- **Quick Story Selection**: Dropdown list of available stories
- **Visual Settings**: Easy configuration of all options
- **Progress Tracking**: Real-time progress during video creation
- **Auto-Open Results**: Option to open completed videos or folders

### Launching the GUI:
```bash
python story_video_gui.py
# Or use the batch file:
launch_gui.bat
```

## Troubleshooting

### Common Issues

1. **"piper command not found"**
   - Make sure Piper TTS is installed and in your PATH
   - Use the `--piper-path` argument to specify the full path

2. **"No video files found"**
   - Ensure your video folder contains supported video formats
   - Check that the folder path is correct

3. **"moviepy import error"**
   - Install moviepy: `pip install moviepy`
   - Make sure FFmpeg is installed

4. **Audio/Video sync issues**
   - The program automatically handles duration matching
   - Ensure your video files are not corrupted

## License

This project is open source. Feel free to modify and distribute.
