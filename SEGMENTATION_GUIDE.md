# Video Segmentation Guide

## What is Video Segmentation?

The video segmentation feature allows you to automatically split your story videos into shorter clips of specified duration. This is perfect for creating content for social media platforms with time limits.

## How It Works

1. **Create Full Video**: First, the program creates your complete story video as usual
2. **Split into Segments**: Then, it automatically splits the video into segments of your chosen duration
3. **Save Segments**: All segments are saved in a dedicated folder

## Common Use Cases

### Social Media Platforms
- **TikTok/Instagram Reels**: 15-30 second segments
- **YouTube Shorts**: 30-60 second segments
- **Twitter Videos**: 30-45 second segments
- **LinkedIn**: 30-60 second segments

### Accessibility
- Break long stories into digestible chunks
- Create cliffhangers and series content
- Easier to share specific parts

## Usage

### Command Line
```bash
# 15-second segments (TikTok/Reels)
python story_video_creator.py story.txt backgrounds/ output.mp4 --segment-duration 15

# 30-second segments (General social media)
python story_video_creator.py story.txt backgrounds/ output.mp4 --segment-duration 30

# 60-second segments (YouTube Shorts)
python story_video_creator.py story.txt backgrounds/ output.mp4 --segment-duration 60
```

### GUI
1. Open the Story Video Creator GUI
2. Select your story and settings as usual
3. Check "Split video into segments"
4. Choose your desired segment duration from the dropdown
5. Click "Create Video"

## Output Structure

When segmentation is enabled:
```
output/
├── your_video.mp4                    # Original full video
└── your_video_segments/              # Segments folder
    ├── your_video_segment_01.mp4     # First segment
    ├── your_video_segment_02.mp4     # Second segment
    ├── your_video_segment_03.mp4     # Third segment
    └── ...                           # Additional segments
```

## Important Notes

- **Minimum Segment Length**: Segments shorter than 3 seconds are automatically skipped
- **Original Video**: The complete video is always created first, then segmented
- **Subtitles**: If subtitles are enabled, they're included in all segments
- **Quality**: Segments maintain the same quality as the original video
- **Format**: All segments are saved as MP4 files with H.264 encoding

## Tips for Best Results

1. **Choose Appropriate Duration**: Consider your target platform's optimal video length
2. **Story Length**: Longer stories will create more segments
3. **Content Breaks**: Natural pauses in speech work well for segment boundaries
4. **Batch Processing**: You can segment multiple stories using different duration settings

## Troubleshooting

**Some segments fail to create**: This is normal due to MoviePy's internal processing. The successfully created segments are still usable.

**Segments too short**: Increase the segment duration or use a longer story.

**Quality issues**: Segments maintain the same quality as the original video, so ensure your source video and audio are high quality.

## Examples

### TikTok Content Creation
```bash
python story_video_creator.py "stories/funny_story.txt" backgrounds/ "tiktok_content.mp4" --segment-duration 15
```
Result: Creates 15-second clips perfect for TikTok posting

### YouTube Shorts Series
```bash
python story_video_creator.py "stories/long_adventure.txt" backgrounds/ "youtube_shorts.mp4" --segment-duration 60
```
Result: Creates 60-second episodes for a YouTube Shorts series

### Instagram Story Series
```bash
python story_video_creator.py "stories/tutorial.txt" backgrounds/ "insta_story.mp4" --segment-duration 30
```
Result: Creates 30-second segments perfect for Instagram Story sequences
