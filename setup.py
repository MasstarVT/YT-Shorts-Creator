#!/usr/bin/env python3
"""
Setup script for Story Video Creator
Downloads and sets up Piper TTS automatically
"""

import os
import sys
import urllib.request
import zipfile
import platform
from pathlib import Path

def download_file(url, filename):
    """Download a file with progress indication"""
    print(f"Downloading {filename}...")
    
    def progress_hook(block_num, block_size, total_size):
        if total_size > 0:
            percent = min(100, (block_num * block_size * 100) // total_size)
            print(f"\rProgress: {percent}%", end="", flush=True)
    
    urllib.request.urlretrieve(url, filename, progress_hook)
    print()  # New line after progress

def setup_piper_windows():
    """Setup Piper TTS for Windows"""
    print("Setting up Piper TTS for Windows...")
    
    # Create piper directory
    piper_dir = Path("piper")
    piper_dir.mkdir(exist_ok=True)
    
    # Download Piper for Windows
    piper_url = "https://github.com/rhasspy/piper/releases/latest/download/piper_windows_amd64.zip"
    piper_zip = "piper_windows.zip"
    
    try:
        download_file(piper_url, piper_zip)
        
        # Extract Piper
        print("Extracting Piper TTS...")
        with zipfile.ZipFile(piper_zip, 'r') as zip_ref:
            zip_ref.extractall(piper_dir)
        
        # Clean up
        os.remove(piper_zip)
        
        print("Piper TTS installed successfully!")
        return str(piper_dir / "piper.exe")
        
    except Exception as e:
        print(f"Error downloading Piper: {e}")
        return None

def setup_piper_linux():
    """Setup Piper TTS for Linux"""
    print("Setting up Piper TTS for Linux...")
    
    # Create piper directory
    piper_dir = Path("piper")
    piper_dir.mkdir(exist_ok=True)
    
    # Download Piper for Linux
    piper_url = "https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz"
    piper_tar = "piper_linux.tar.gz"
    
    try:
        download_file(piper_url, piper_tar)
        
        # Extract Piper
        print("Extracting Piper TTS...")
        import tarfile
        with tarfile.open(piper_tar, 'r:gz') as tar_ref:
            tar_ref.extractall(piper_dir)
        
        # Clean up
        os.remove(piper_tar)
        
        # Make executable
        piper_exe = piper_dir / "piper" / "piper"
        if piper_exe.exists():
            os.chmod(piper_exe, 0o755)
        
        print("Piper TTS installed successfully!")
        return str(piper_exe)
        
    except Exception as e:
        print(f"Error downloading Piper: {e}")
        return None

def download_voice_model():
    """Download a sample voice model"""
    print("\nDownloading sample voice model...")
    
    voices_dir = Path("voices")
    voices_dir.mkdir(exist_ok=True)
    
    # Download a high-quality English voice
    voice_url = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/high/en_US-lessac-high.onnx"
    voice_config_url = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/high/en_US-lessac-high.onnx.json"
    
    voice_file = voices_dir / "en_US-lessac-high.onnx"
    config_file = voices_dir / "en_US-lessac-high.onnx.json"
    
    try:
        download_file(voice_url, str(voice_file))
        download_file(voice_config_url, str(config_file))
        
        print("Voice model downloaded successfully!")
        return str(voice_file)
        
    except Exception as e:
        print(f"Error downloading voice model: {e}")
        return None

def install_python_dependencies():
    """Install required Python packages"""
    print("Installing Python dependencies...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Python dependencies installed successfully!")
            return True
        else:
            print(f"Error installing dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error installing Python dependencies: {e}")
        return False

def create_config_file(piper_path, voice_model):
    """Create a configuration file"""
    config_content = f"""# Story Video Creator Configuration
# Edit these paths as needed

PIPER_PATH={piper_path}
VOICE_MODEL={voice_model}

# Example usage:
# python story_video_creator.py sample_story.txt backgrounds/ output.mp4 --piper-path "{piper_path}" --voice-model "{voice_model}"
"""
    
    with open("config.txt", "w") as f:
        f.write(config_content)
    
    print("Configuration file created: config.txt")

def main():
    print("=== Story Video Creator Setup ===")
    print()
    
    # Install Python dependencies
    if not install_python_dependencies():
        print("Setup failed at Python dependencies")
        return
    
    # Detect OS and setup Piper
    system = platform.system().lower()
    
    if system == "windows":
        piper_path = setup_piper_windows()
    elif system == "linux":
        piper_path = setup_piper_linux()
    else:
        print(f"Unsupported OS: {system}")
        print("Please manually install Piper TTS from: https://github.com/rhasspy/piper")
        return
    
    if not piper_path:
        print("Setup failed at Piper TTS installation")
        return
    
    # Download voice model
    voice_model = download_voice_model()
    
    if not voice_model:
        print("Setup failed at voice model download")
        return
    
    # Create config file
    create_config_file(piper_path, voice_model)
    
    print()
    print("=== Setup Complete! ===")
    print(f"Piper TTS: {piper_path}")
    print(f"Voice Model: {voice_model}")
    print()
    print("Next steps:")
    print("1. Create a 'backgrounds' folder and add video files")
    print("2. Run: python story_video_creator.py sample_story.txt backgrounds/ my_video.mp4")
    print("   Or use the paths from config.txt with --piper-path and --voice-model arguments")

if __name__ == "__main__":
    main()
