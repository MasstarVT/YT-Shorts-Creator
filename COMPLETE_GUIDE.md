# Story Video Creator - Complete Guide

## Overview
The Story Video Creator is a Python program that automatically creates engaging videos by:
1. Reading text stories from files
2. Converting text to speech using Piper TTS
3. Combining the narration with random background videos
4. Producing professional-looking story videos

## Quick Start

### 1. Setup
```bash
# Clone or download the project
cd "YT Sorts Creater"

# Create virtual environment (recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate    # Linux/Mac

# Install dependencies
pip install moviepy
```

### 2. Install Piper TTS
- **Automatic**: Run `python setup.py` to download Piper TTS and voice models
- **Manual**: Download from [Piper TTS Releases](https://github.com/rhasspy/piper/releases)

### 3. Prepare Content
```bash
# Add background videos to the backgrounds folder
mkdir backgrounds
# Copy your MP4, AVI, MOV files to backgrounds/

# Create or use the sample story
# Edit sample_story.txt or create your own
```

### 4. Create Video
```bash
# Basic usage
python story_video_creator.py sample_story.txt backgrounds/ my_video.mp4

# With custom Piper settings
python story_video_creator.py sample_story.txt backgrounds/ my_video.mp4 --piper-path "piper/piper.exe" --voice-model "voices/en_US-lessac-high.onnx"

# Or use the Windows batch file
run_story_creator.bat sample_story.txt backgrounds/ my_video.mp4
```

## Detailed Setup Instructions

### Installing Piper TTS

#### Windows (Automatic)
```bash
python setup.py
```
This will:
- Download Piper TTS for Windows
- Download a high-quality English voice model
- Create a configuration file with paths

#### Manual Installation
1. Go to [Piper TTS Releases](https://github.com/rhasspy/piper/releases)
2. Download the appropriate version for your OS
3. Extract to a `piper` folder in your project
4. Download voice models from [Piper Voices](https://github.com/rhasspy/piper/blob/master/VOICES.md)

### Voice Models
Popular English voices:
- `en_US-lessac-high.onnx` - Natural female voice
- `en_US-ryan-high.onnx` - Natural male voice
- `en_GB-alba-medium.onnx` - British accent

Download from: https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0

## Usage Examples

### Command Line

#### Basic Example
```bash
python story_video_creator.py "my_story.txt" "backgrounds/" "output_video.mp4"
```

#### With Custom Settings
```bash
python story_video_creator.py "story.txt" "videos/" "final.mp4" \
  --piper-path "C:/Tools/piper/piper.exe" \
  --voice-model "C:/Tools/piper/voices/en_US-lessac-high.onnx"
```

### Programmatic Usage
```python
from story_video_creator import StoryVideoCreator

# Initialize
creator = StoryVideoCreator(
    piper_path="piper/piper.exe",
    voice_model="voices/en_US-lessac-high.onnx"
)

# Create video
try:
    result = creator.create_story_video(
        story_file="my_story.txt",
        video_folder="backgrounds/",
        output_file="my_video.mp4"
    )
    print(f"Video created: {result}")
finally:
    creator.cleanup()
```

## File Organization

### Recommended Structure
```
YT Sorts Creater/
├── story_video_creator.py     # Main program
├── setup.py                   # Automatic setup script
├── requirements.txt           # Python dependencies
├── sample_story.txt          # Example story
├── backgrounds/              # Background videos folder
│   ├── nature_video.mp4
│   ├── abstract_animation.avi
│   └── scenic_loop.mov
├── stories/                  # Your story files
│   ├── adventure.txt
│   ├── mystery.txt
│   └── comedy.txt
├── piper/                    # Piper TTS (after setup)
│   ├── piper.exe
│   └── piper
├── voices/                   # Voice models
│   ├── en_US-lessac-high.onnx
│   └── en_US-ryan-high.onnx
└── output/                   # Generated videos
    ├── adventure_video.mp4
    └── mystery_video.mp4
```

## Advanced Features

### Multiple Voice Support
```bash
# Use different voices for different stories
python story_video_creator.py story1.txt backgrounds/ output1.mp4 --voice-model "voices/female_voice.onnx"
python story_video_creator.py story2.txt backgrounds/ output2.mp4 --voice-model "voices/male_voice.onnx"
```

### Batch Processing
Create a batch script to process multiple stories:

```python
# batch_process.py
import os
from story_video_creator import StoryVideoCreator

stories = ["story1.txt", "story2.txt", "story3.txt"]
creator = StoryVideoCreator()

for story in stories:
    output = f"output_{os.path.splitext(story)[0]}.mp4"
    try:
        creator.create_story_video(story, "backgrounds/", output)
        print(f"Completed: {output}")
    except Exception as e:
        print(f"Failed {story}: {e}")

creator.cleanup()
```

## Troubleshooting

### Common Issues and Solutions

#### 1. "piper command not found"
**Problem**: Piper TTS is not installed or not in PATH
**Solutions**:
- Run the automatic setup: `python setup.py`
- Download Piper manually and use `--piper-path`
- Add Piper to your system PATH

#### 2. "No video files found in folder"
**Problem**: Background videos folder is empty or has unsupported formats
**Solutions**:
- Add video files to the backgrounds folder
- Supported formats: MP4, AVI, MOV, MKV, FLV, WMV, WebM
- Check folder path is correct

#### 3. "Import moviepy could not be resolved"
**Problem**: MoviePy is not installed
**Solutions**:
- Install with: `pip install moviepy`
- Activate virtual environment first
- Install FFmpeg if needed

#### 4. Audio/Video Sync Issues
**Problem**: Audio and video don't match properly
**Solutions**:
- The program automatically handles duration matching
- Ensure video files are not corrupted
- Use high-quality background videos

#### 5. Voice Model Errors
**Problem**: Voice model file not found or corrupted
**Solutions**:
- Download voice models from official sources
- Verify file paths are correct
- Use the `--voice-model` parameter with full path

### Performance Optimization

#### For Faster Processing
- Use shorter background videos (they'll be looped anyway)
- Use compressed video formats (MP4 with H.264)
- Keep story text reasonable length
- Use SSD storage for temporary files

#### For Better Quality
- Use high-quality voice models (high.onnx files)
- Use high-resolution background videos
- Ensure good audio quality settings in Piper

## Configuration

### Environment Variables
You can set environment variables instead of using command-line arguments:

```bash
# Windows
set PIPER_PATH=C:\Tools\piper\piper.exe
set PIPER_VOICE=C:\Tools\piper\voices\en_US-lessac-high.onnx

# Linux/Mac
export PIPER_PATH=/usr/local/bin/piper
export PIPER_VOICE=/usr/local/share/piper/voices/en_US-lessac-high.onnx
```

### Config File
The setup script creates a `config.txt` with recommended paths:
```
PIPER_PATH=piper/piper.exe
VOICE_MODEL=voices/en_US-lessac-high.onnx
```

## Best Practices

### Story Writing Tips
- Keep paragraphs reasonable length for better pacing
- Use clear, simple language for TTS
- Avoid special characters that might confuse TTS
- Include natural pauses with periods and commas

### Video Selection
- Use videos that loop well
- Avoid videos with loud original audio
- Choose content that matches your story theme
- Consider using royalty-free background videos

### Output Settings
- Use `.mp4` extension for best compatibility
- Consider your target platform requirements
- Test with different voice models for best results

## API Reference

### StoryVideoCreator Class

#### Constructor
```python
StoryVideoCreator(piper_path="piper", voice_model=None)
```
- `piper_path`: Path to Piper TTS executable
- `voice_model`: Path to voice model file (.onnx)

#### Methods

##### create_story_video()
```python
create_story_video(story_file, video_folder, output_file) -> str
```
Main method to create a complete story video.

##### read_story_file()
```python
read_story_file(story_file) -> str
```
Read and validate story text from file.

##### generate_audio_with_piper()
```python
generate_audio_with_piper(text, output_audio_path) -> str
```
Convert text to speech using Piper TTS.

##### select_random_video()
```python
select_random_video(video_folder) -> str
```
Choose a random video from the folder.

##### create_video_with_audio()
```python
create_video_with_audio(video_path, audio_path, output_path) -> str
```
Combine video and audio into final output.

##### cleanup()
```python
cleanup()
```
Clean up temporary files.

## Contributing

Feel free to contribute improvements:
- Add support for more TTS engines
- Implement video effects
- Add subtitle generation
- Create GUI interface
- Improve error handling

## License

This project is open source. Use and modify as needed.
