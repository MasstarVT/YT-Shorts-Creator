#!/usr/bin/env python3
"""
Story Video Creator

This program:
1. Reads a story from a text file
2. Uses Piper TTS to generate audio narration
3. Selects a random video file from a specified folder
4. Combines the audio and video to create a final video output

Requirements:
- Piper TTS
- FFmpeg
- moviepy
"""

import os
import sys
import random
import subprocess
import argparse
from pathlib import Path
from typing import Optional
import tempfile
import threading
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

# MoviePy will be imported when needed to avoid early exit on help commands


class StoryVideoCreator:
    def __init__(self, piper_path: str = "piper", voice_model: str = None):
        """
        Initialize the Story Video Creator
        
        Args:
            piper_path: Path to the Piper TTS executable
            voice_model: Path to the Piper voice model (.onnx file)
        """
        self.piper_path = piper_path
        self.voice_model = voice_model
        # Create a temp directory specifically for this instance
        self.temp_dir = tempfile.mkdtemp(prefix="story_video_")
        print(f"Using temp directory: {self.temp_dir}")
        self._current_story_text = None  # Store current story text for subtitles
        self._font_cache = {}  # Cache for loaded fonts
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup temp files"""
        self.cleanup()
        
    def read_story_file(self, story_file: str) -> str:
        """Read the story content from a text file"""
        try:
            with open(story_file, 'r', encoding='utf-8') as f:
                story_content = f.read().strip()
            
            if not story_content:
                raise ValueError("Story file is empty")
                
            print(f"Successfully read story from: {story_file}")
            print(f"Story length: {len(story_content)} characters")
            return story_content
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Story file not found: {story_file}")
        except Exception as e:
            raise Exception(f"Error reading story file: {e}")
    
    def generate_audio_with_piper(self, text: str, output_audio_path: str) -> str:
        """
        Generate audio using Piper TTS
        
        Args:
            text: The text to convert to speech
            output_audio_path: Path where the audio file will be saved
            
        Returns:
            Path to the generated audio file
        """
        try:
            # Try GPU acceleration first, fallback to CPU if it fails
            for use_gpu in [True, False]:
                try:
                    # Prepare Piper command
                    cmd = [self.piper_path]
                    
                    # Add voice model if specified
                    if self.voice_model:
                        cmd.extend(["-m", self.voice_model])
                    
                    # Add GPU acceleration if available and this is the first attempt
                    if use_gpu:
                        cmd.extend(["--cuda"])  # Try GPU acceleration
                    
                    # Add output file
                    cmd.extend(["-f", output_audio_path])
                    
                    print(f"Generating audio with Piper TTS ({'GPU' if use_gpu else 'CPU'})...")
                    print(f"Command: {' '.join(cmd)}")
                    
                    # Run Piper TTS
                    process = subprocess.Popen(
                        cmd,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    stdout, stderr = process.communicate(input=text)
                    
                    if process.returncode == 0 and os.path.exists(output_audio_path):
                        print(f"Audio generated successfully: {output_audio_path}")
                        return output_audio_path
                    elif use_gpu:
                        print("GPU acceleration failed, trying CPU...")
                        continue
                    else:
                        raise Exception(f"Piper TTS failed: {stderr}")
                        
                except Exception as e:
                    if use_gpu:
                        print(f"GPU acceleration failed: {e}, trying CPU...")
                        continue
                    else:
                        raise e
            
            raise Exception("Both GPU and CPU attempts failed")
            
        except Exception as e:
            raise Exception(f"Error generating audio with Piper: {e}")
    
    def select_random_video(self, video_folder: str) -> str:
        """
        Select a random video file from the specified folder
        
        Args:
            video_folder: Path to folder containing video files
            
        Returns:
            Path to the selected video file
        """
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'}
        
        try:
            video_files = []
            for file in os.listdir(video_folder):
                if Path(file).suffix.lower() in video_extensions:
                    video_files.append(os.path.join(video_folder, file))
            
            if not video_files:
                raise ValueError(f"No video files found in folder: {video_folder}")
            
            selected_video = random.choice(video_files)
            print(f"Selected random video: {os.path.basename(selected_video)}")
            return selected_video
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Video folder not found: {video_folder}")
        except Exception as e:
            raise Exception(f"Error selecting random video: {e}")
    
    def create_video_with_audio(self, video_path: str, audio_path: str, output_path: str, add_subtitles: bool = True) -> str:
        """
        Combine video and audio to create final video with optional subtitles
        
        Args:
            video_path: Path to the video file
            audio_path: Path to the audio file
            output_path: Path for the output video
            add_subtitles: Whether to add text subtitles to the video
            
        Returns:
            Path to the created video
        """
        try:
            # Import moviepy here to avoid early exit on help commands
            try:
                from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
                print("MoviePy imported successfully")
            except ImportError as e:
                raise Exception(f"moviepy is required but could not be imported: {e}. Install with: pip install moviepy")
            
            print("Loading video and audio files...")
            
            # Load video clip with optimized settings
            video_clip = VideoFileClip(video_path, audio=False)  # Don't load audio from video
            
            # Load audio clip
            audio_clip = AudioFileClip(audio_path)
            
            # Get durations
            video_duration = video_clip.duration
            audio_duration = audio_clip.duration
            
            print(f"Video duration: {video_duration:.2f} seconds")
            print(f"Audio duration: {audio_duration:.2f} seconds")
            
            print("Processing video timing...")
            # Adjust video to match audio duration
            if video_duration < audio_duration:
                # Loop video if it's shorter than audio
                loops_needed = int(audio_duration / video_duration) + 1
                print(f"Looping video {loops_needed} times to match audio duration")
                video_clip = video_clip.loop(n=loops_needed)
            
            # Cut video to match audio duration
            video_clip = video_clip.subclip(0, audio_duration)
            
            # Set audio to video
            final_video = video_clip.set_audio(audio_clip)
            
            # Add subtitles if requested
            if add_subtitles:
                print("Generating subtitles (this may take a moment)...")
                import time
                start_time = time.time()
                final_video = self.add_subtitles_to_video(final_video, audio_duration)
                subtitle_time = time.time() - start_time
                print(f"Subtitles generated in {subtitle_time:.2f} seconds")
            else:
                print("Skipping subtitle generation for faster processing")
            
            print(f"Creating final video: {output_path}")
            
            # Write the final video with optimized settings
            temp_audio_file = os.path.join(self.temp_dir, 'temp-audio.m4a')
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=temp_audio_file,
                remove_temp=True,
                verbose=False,
                logger=None,
                preset='fast',  # Balanced speed/quality
                threads=4  # Use multiple threads
            )
            
            # Clean up
            video_clip.close()
            audio_clip.close()
            final_video.close()
            
            print(f"Video created successfully: {output_path}")
            return output_path
            
        except Exception as e:
            raise Exception(f"Error creating video: {e}")
    
    def add_subtitles_to_video(self, video_clip, audio_duration: float):
        """
        Add text subtitles to the video using PIL/Pillow for text rendering
        
        Args:
            video_clip: The video clip to add subtitles to
            audio_duration: Duration of the audio/video
            
        Returns:
            Video clip with subtitles
        """
        try:
            from moviepy.editor import ImageClip, CompositeVideoClip
            from PIL import Image, ImageDraw, ImageFont
            import numpy as np
            
            # Get the story text for subtitles
            if not hasattr(self, '_current_story_text'):
                print("Warning: Story text not available for subtitles")
                return video_clip
            
            story_text = self._current_story_text
            
            # Split text into subtitle chunks
            subtitle_chunks = self.create_subtitle_chunks(story_text, audio_duration)
            
            if not subtitle_chunks:
                print("Warning: No subtitle chunks created")
                return video_clip
            
            # Get video dimensions
            video_width, video_height = video_clip.size
            
            # Create image clips for subtitles using multithreading
            subtitle_clips = []
            
            def create_subtitle_clip(chunk_data):
                """Create a single subtitle clip"""
                i, chunk = chunk_data
                try:
                    # Create subtitle image
                    subtitle_img = self.create_subtitle_image(
                        chunk['text'], 
                        video_width, 
                        video_height
                    )
                    
                    if subtitle_img is not None:
                        # Convert PIL image to numpy array
                        subtitle_array = np.array(subtitle_img)
                        
                        # Create ImageClip
                        img_clip = ImageClip(subtitle_array, transparent=True)
                        img_clip = img_clip.set_duration(chunk['duration']).set_start(chunk['start'])
                        
                        return img_clip
                    return None
                    
                except Exception as e:
                    print(f"Warning: Could not create subtitle {i}: {e}")
                    return None
            
            # Use ThreadPoolExecutor for parallel subtitle generation
            max_workers = min(4, len(subtitle_chunks))  # Limit to 4 threads or number of chunks
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all subtitle creation tasks
                future_to_chunk = {
                    executor.submit(create_subtitle_clip, (i, chunk)): i 
                    for i, chunk in enumerate(subtitle_chunks)
                }
                
                # Collect results as they complete
                for future in as_completed(future_to_chunk):
                    clip = future.result()
                    if clip is not None:
                        subtitle_clips.append(clip)
            
            if subtitle_clips:
                # Composite video with subtitles
                final_video = CompositeVideoClip([video_clip] + subtitle_clips)
                print(f"Added {len(subtitle_clips)} subtitle segments using PIL")
                return final_video
            else:
                print("Warning: No subtitle clips could be created")
                return video_clip
            
        except ImportError as e:
            print(f"Warning: PIL/Pillow not available for subtitles: {e}")
            return video_clip
        except Exception as e:
            print(f"Warning: Could not add subtitles: {e}")
            return video_clip
    
    def create_subtitle_image(self, text: str, video_width: int, video_height: int):
        """
        Create a subtitle image using PIL
        Args:
            text: The text to render
            video_width: Width of the video
            video_height: Height of the video
        Returns:
            PIL Image with the subtitle text
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create transparent image
            img = Image.new('RGBA', (video_width, video_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Try to load a font with caching
            font_size = max(24, min(video_width // 25, 48))  # Responsive font size
            font_key = f"font_{font_size}"
            
            if font_key in self._font_cache:
                font = self._font_cache[font_key]
            else:
                try:
                    # Try to use a system font
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    try:
                        # Fallback to different font names
                        font = ImageFont.truetype("Arial.ttf", font_size)
                    except:
                        try:
                            font = ImageFont.truetype("calibri.ttf", font_size)
                        except:
                            # Use default font
                            font = ImageFont.load_default()
                
                # Cache the font for future use
                self._font_cache[font_key] = font
            
            # Wrap text to fit video width
            wrapped_text = self.wrap_text_for_video(text, font, video_width * 0.9)
            
            # Calculate text position
            text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Position text at bottom center
            x = (video_width - text_width) // 2
            y = video_height - text_height - 50  # 50 pixels from bottom
            
            # Draw text with black outline for better visibility
            outline_width = 2
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx != 0 or dy != 0:
                        draw.multiline_text((x + dx, y + dy), wrapped_text, 
                                          font=font, fill=(0, 0, 0, 255), 
                                          align="center")
            
            # Draw main text in white
            draw.multiline_text((x, y), wrapped_text, font=font, 
                              fill=(255, 255, 255, 255), align="center")
            
            return img
            
        except Exception as e:
            print(f"Error creating subtitle image: {e}")
            return None
    
    def wrap_text_for_video(self, text: str, font, max_width: float):
        """
        Wrap text to fit within video width
        
        Args:
            text: Text to wrap
            font: PIL font object
            max_width: Maximum width in pixels
            
        Returns:
            Wrapped text string
        """
        try:
            from PIL import Image, ImageDraw
            
            # Create temporary image for measuring
            temp_img = Image.new('RGB', (1, 1))
            draw = ImageDraw.Draw(temp_img)
            
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = draw.textbbox((0, 0), test_line, font=font)
                width = bbox[2] - bbox[0]
                
                if width <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        # Single word is too long, add it anyway
                        lines.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            return '\n'.join(lines)
            
        except Exception as e:
            print(f"Error wrapping text: {e}")
            return text
    
    def create_subtitle_chunks(self, text: str, total_duration: float):
        """
        Create subtitle chunks with timing
        
        Args:
            text: The full story text
            total_duration: Total duration of the audio
            
        Returns:
            List of subtitle chunks with timing
        """
        # Split text into sentences
        import re
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Calculate timing for each sentence
        chunks = []
        words_per_sentence = [len(sentence.split()) for sentence in sentences]
        total_words = sum(words_per_sentence)
        
        if total_words == 0:
            return chunks
        
        current_time = 0.0
        
        for i, sentence in enumerate(sentences):
            if not sentence.strip():
                continue
                
            # Calculate duration based on word count
            word_count = words_per_sentence[i]
            duration = (word_count / total_words) * total_duration
            
            # Minimum duration of 1 second, maximum of 8 seconds
            duration = max(1.0, min(8.0, duration))
            
            # Split long sentences into multiple chunks
            if len(sentence) > 100:  # If sentence is too long
                words = sentence.split()
                chunk_size = 8  # Words per chunk
                
                for j in range(0, len(words), chunk_size):
                    chunk_words = words[j:j + chunk_size]
                    chunk_text = ' '.join(chunk_words)
                    chunk_duration = (len(chunk_words) / total_words) * total_duration
                    chunk_duration = max(1.5, min(6.0, chunk_duration))
                    
                    chunks.append({
                        'text': chunk_text,
                        'start': current_time,
                        'duration': chunk_duration
                    })
                    
                    current_time += chunk_duration
            else:
                chunks.append({
                    'text': sentence,
                    'start': current_time,
                    'duration': duration
                })
                
                current_time += duration
        
        return chunks
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            print(f"Cleaning up temp directory: {self.temp_dir}")
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except Exception as e:
            print(f"Warning: Could not clean up temp directory: {e}")
    
    def split_video_into_segments(self, video_path: str, segment_duration: int) -> str:
        """
        Split a video into segments of specified duration
        
        Args:
            video_path: Path to the video file to split
            segment_duration: Duration of each segment in seconds
            
        Returns:
            Path to the folder containing the segments
        """
        try:
            from moviepy.editor import VideoFileClip
            
            # Create segments folder
            video_name = Path(video_path).stem
            segments_folder = Path(video_path).parent / f"{video_name}_segments"
            segments_folder.mkdir(exist_ok=True)
            
            print(f"Splitting video into {segment_duration}-second segments...")
            
            # Load the video
            with VideoFileClip(video_path) as video:
                total_duration = video.duration
                num_segments = int(total_duration // segment_duration) + (1 if total_duration % segment_duration > 0 else 0)
                
                print(f"Video duration: {total_duration:.2f} seconds")
                print(f"Creating {num_segments} segments...")
                
                segments_created = []
                
                for i in range(num_segments):
                    start_time = i * segment_duration
                    end_time = min((i + 1) * segment_duration, total_duration)
                    
                    # Skip very short segments (less than 3 seconds)
                    if end_time - start_time < 3:
                        print(f"Skipping segment {i+1} (too short: {end_time - start_time:.2f}s)")
                        continue
                    
                    segment_filename = f"{video_name}_segment_{i+1:02d}.mp4"
                    segment_path = segments_folder / segment_filename
                    
                    print(f"Creating segment {i+1}/{num_segments}: {start_time:.1f}s - {end_time:.1f}s")
                    
                    # Extract segment
                    segment = video.subclip(start_time, end_time)
                    
                    try:
                        segment.write_videofile(
                            str(segment_path),
                            codec='libx264',
                            audio_codec='aac'
                        )
                        segments_created.append(str(segment_path))
                        print(f"✓ Segment {i+1} created successfully")
                    except Exception as segment_error:
                        print(f"✗ Failed to create segment {i+1}: {segment_error}")
                    finally:
                        segment.close()
                
                print(f"\n=== SEGMENTATION COMPLETE ===")
                print(f"Created {len(segments_created)} segments in: {segments_folder}")
                for segment in segments_created:
                    print(f"  - {Path(segment).name}")
                
                return str(segments_folder)
                
        except Exception as e:
            raise Exception(f"Error splitting video into segments: {e}")
    
    def create_story_video(self, story_file: str, video_folder: str, output_file: str, add_subtitles: bool = True, segment_duration: Optional[int] = None) -> str:
        """
        Main method to create a story video
        
        Args:
            story_file: Path to the text file containing the story
            video_folder: Path to folder containing video files
            output_file: Path for the output video file
            add_subtitles: Whether to add text subtitles to the video
            segment_duration: Optional duration in seconds to split video into segments
            
        Returns:
            Path to the created video (or folder containing segments)
        """
        try:
            # Step 1: Read the story
            story_text = self.read_story_file(story_file)
            
            # Store story text for subtitle generation
            self._current_story_text = story_text
            
            # Step 2: Generate audio with Piper TTS
            audio_file = os.path.join(self.temp_dir, "story_audio.wav")
            self.generate_audio_with_piper(story_text, audio_file)
            
            # Step 3: Select random video
            video_file = self.select_random_video(video_folder)
            
            # Step 4: Create final video with subtitles
            final_video_path = self.create_video_with_audio(video_file, audio_file, output_file, add_subtitles)
            
            # Step 5: Split into segments if requested
            if segment_duration:
                return self.split_video_into_segments(final_video_path, segment_duration)
            
            return final_video_path
            
        except Exception as e:
            self.cleanup()
            raise e


def main():
    parser = argparse.ArgumentParser(description="Create videos from story text files using Piper TTS")
    parser.add_argument("story_file", help="Path to the text file containing the story")
    parser.add_argument("video_folder", help="Path to folder containing video files")
    parser.add_argument("output_file", help="Path for the output video file")
    parser.add_argument("--piper-path", default="piper", help="Path to Piper TTS executable")
    parser.add_argument("--voice-model", help="Path to Piper voice model (.onnx file)")
    parser.add_argument("--no-subtitles", action="store_true", help="Disable subtitle generation")
    parser.add_argument("--segment-duration", type=int, help="Split video into segments of specified duration (seconds). Common values: 15, 30, 60")
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.story_file):
        print(f"Error: Story file not found: {args.story_file}")
        sys.exit(1)
    
    if not os.path.exists(args.video_folder):
        print(f"Error: Video folder not found: {args.video_folder}")
        sys.exit(1)
    
    if args.voice_model and not os.path.exists(args.voice_model):
        print(f"Error: Voice model not found: {args.voice_model}")
        sys.exit(1)
    
    # If output file has no directory specified, place it in the output folder
    output_dir = os.path.dirname(args.output_file)
    if not output_dir:
        # No directory specified, use output folder
        output_folder = "output"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        args.output_file = os.path.join(output_folder, args.output_file)
    elif output_dir and not os.path.exists(output_dir):
        # Directory specified but doesn't exist, create it
        os.makedirs(output_dir)
    
    # Create the story video
    with StoryVideoCreator(args.piper_path, args.voice_model) as creator:
        try:
            print("=== Story Video Creator ===")
            print(f"Story file: {args.story_file}")
            print(f"Video folder: {args.video_folder}")
            print(f"Output file: {args.output_file}")
            print(f"Subtitles: {'Disabled' if args.no_subtitles else 'Enabled'}")
            if args.segment_duration:
                print(f"Segment duration: {args.segment_duration} seconds")
            print()
            
            result = creator.create_story_video(
                args.story_file, 
                args.video_folder, 
                args.output_file,
                add_subtitles=not args.no_subtitles,
                segment_duration=args.segment_duration
            )
            
            print()
            print("=== SUCCESS ===")
            if args.segment_duration:
                print(f"Story video segments created successfully in: {result}")
            else:
                print(f"Story video created successfully: {result}")
            
        except Exception as e:
            print()
            print("=== ERROR ===")
            print(f"Failed to create story video: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
