#!/usr/bin/env python3
"""
Example usage of the Story Video Creator
This script demonstrates how to use the StoryVideoCreator class programmatically
"""

import os
from story_video_creator import StoryVideoCreator

def example_usage():
    """Example of how to use the StoryVideoCreator class"""
    
    # Configuration
    story_file = "sample_story.txt"
    video_folder = "backgrounds"  # You need to create this folder and add videos
    output_file = "example_output.mp4"
    
    # Optional: specify custom Piper path and voice model
    piper_path = "piper"  # or full path like "C:/piper/piper.exe"
    voice_model = None    # or path like "voices/en_US-lessac-high.onnx"
    
    # Create the video creator instance
    creator = StoryVideoCreator(piper_path=piper_path, voice_model=voice_model)
    
    try:
        print("Creating story video...")
        
        # Check if files exist
        if not os.path.exists(story_file):
            print(f"Error: Story file not found: {story_file}")
            return
        
        if not os.path.exists(video_folder):
            print(f"Error: Video folder not found: {video_folder}")
            print("Please create a 'backgrounds' folder and add some video files")
            return
        
        # Create the video
        result = creator.create_story_video(story_file, video_folder, output_file)
        
        print(f"Success! Video created: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Clean up temporary files
        creator.cleanup()

def create_test_structure():
    """Create the basic folder structure for testing"""
    
    # Create backgrounds folder
    backgrounds_dir = "backgrounds"
    if not os.path.exists(backgrounds_dir):
        os.makedirs(backgrounds_dir)
        print(f"Created {backgrounds_dir} folder")
        print("Please add some video files (mp4, avi, mov, etc.) to this folder")
    else:
        print(f"{backgrounds_dir} folder already exists")
    
    # Check for story file
    if os.path.exists("sample_story.txt"):
        print("sample_story.txt is ready")
    else:
        print("sample_story.txt not found")
    
    print()
    print("To get started:")
    print("1. Add video files to the 'backgrounds' folder")
    print("2. Run: python example_usage.py")
    print("   Or: python story_video_creator.py sample_story.txt backgrounds/ output.mp4")

if __name__ == "__main__":
    print("=== Story Video Creator Example ===")
    print()
    
    # Create test structure
    create_test_structure()
    
    print()
    
    # Ask user if they want to run the example
    response = input("Do you want to run the example now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        example_usage()
    else:
        print("Example cancelled. Run this script again when you're ready!")
