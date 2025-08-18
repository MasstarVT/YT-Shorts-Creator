#!/usr/bin/env python3
"""
Story Manager for Story Video Creator
Helps you create, edit, and manage story files
"""

import os
import sys
from pathlib import Path

def list_stories():
    """List all available story files"""
    stories_dir = Path("stories")
    if not stories_dir.exists():
        print("No stories directory found. Creating one...")
        stories_dir.mkdir()
        return
    
    story_files = list(stories_dir.glob("*.txt"))
    
    if not story_files:
        print("No story files found in the stories/ directory.")
        print("Add .txt files to the stories/ folder to get started.")
        return
    
    print("Available Stories:")
    print("-" * 40)
    
    for i, story_file in enumerate(story_files, 1):
        # Get file size
        size = story_file.stat().st_size
        
        # Read first line as title/preview
        try:
            with open(story_file, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if len(first_line) > 50:
                    first_line = first_line[:47] + "..."
        except:
            first_line = "Unable to read preview"
        
        print(f"{i:2d}. {story_file.name}")
        print(f"    Preview: {first_line}")
        print(f"    Size: {size} bytes")
        print()

def create_new_story():
    """Create a new story file"""
    print("Create New Story")
    print("-" * 20)
    
    title = input("Enter story title: ").strip()
    if not title:
        print("Story title cannot be empty.")
        return
    
    # Create safe filename
    filename = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    filename = filename.replace(' ', '_').lower() + '.txt'
    
    stories_dir = Path("stories")
    stories_dir.mkdir(exist_ok=True)
    
    story_path = stories_dir / filename
    
    if story_path.exists():
        overwrite = input(f"File {filename} already exists. Overwrite? (y/N): ")
        if overwrite.lower() != 'y':
            print("Cancelled.")
            return
    
    print(f"\nCreating story file: {filename}")
    print("Enter your story below. Press Ctrl+Z (Windows) or Ctrl+D (Linux/Mac) when finished:")
    print("-" * 60)
    
    story_content = []
    try:
        while True:
            line = input()
            story_content.append(line)
    except EOFError:
        pass
    
    # Write story to file
    with open(story_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(story_content))
    
    print(f"\nStory saved to: {story_path}")
    print(f"To create a video: python story_video_creator.py \"{story_path}\" backgrounds/ output.mp4")

def preview_story():
    """Preview a story file"""
    list_stories()
    
    stories_dir = Path("stories")
    story_files = list(stories_dir.glob("*.txt"))
    
    if not story_files:
        return
    
    try:
        choice = int(input(f"\nEnter story number (1-{len(story_files)}): "))
        if 1 <= choice <= len(story_files):
            selected_story = story_files[choice - 1]
            
            print(f"\n{selected_story.name}")
            print("=" * len(selected_story.name))
            
            with open(selected_story, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)
            
            print(f"\n[Story length: {len(content)} characters]")
            
            # Ask if user wants to create video
            create_video = input("\nCreate video with this story? (y/N): ")
            if create_video.lower() == 'y':
                output_name = input("Enter output filename (without .mp4): ")
                if not output_name:
                    output_name = selected_story.stem + "_video"
                
                cmd = f'python story_video_creator.py "{selected_story}" backgrounds/ "{output_name}.mp4" --piper-path "piper\\piper\\piper.exe" --voice-model "voices\\en_US-lessac-high.onnx"'
                print(f"\nRun this command to create the video:")
                print(cmd)
                
        else:
            print("Invalid choice.")
    
    except ValueError:
        print("Invalid input. Please enter a number.")

def get_story_stats():
    """Show statistics about all stories"""
    stories_dir = Path("stories")
    story_files = list(stories_dir.glob("*.txt"))
    
    if not story_files:
        print("No stories found.")
        return
    
    total_files = len(story_files)
    total_chars = 0
    total_words = 0
    
    print("Story Statistics")
    print("-" * 40)
    
    for story_file in story_files:
        with open(story_file, 'r', encoding='utf-8') as f:
            content = f.read()
            chars = len(content)
            words = len(content.split())
            
            total_chars += chars
            total_words += words
            
            print(f"{story_file.name}:")
            print(f"  Characters: {chars:,}")
            print(f"  Words: {words:,}")
            print(f"  Est. reading time: {words // 150:.1f} minutes")
            print()
    
    print(f"TOTALS:")
    print(f"  Files: {total_files}")
    print(f"  Characters: {total_chars:,}")
    print(f"  Words: {total_words:,}")
    print(f"  Est. total reading time: {total_words // 150:.1f} minutes")

def main():
    print("=" * 50)
    print("    Story Video Creator - Story Manager")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. List all stories")
        print("2. Create new story")
        print("3. Preview a story")
        print("4. Show story statistics")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            list_stories()
        elif choice == '2':
            create_new_story()
        elif choice == '3':
            preview_story()
        elif choice == '4':
            get_story_stats()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()
