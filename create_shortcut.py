#!/usr/bin/env python3
"""
Desktop Shortcut Creator for Story Video Creator GUI
"""

import os
import sys
from pathlib import Path

def create_windows_shortcut():
    """Create a Windows desktop shortcut"""
    try:
        import win32com.client
        
        desktop = Path.home() / "Desktop"
        shortcut_path = desktop / "Story Video Creator.lnk"
        
        target = Path.cwd() / "launch_gui.bat"
        icon_path = Path.cwd() / "story_video_gui.py"
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.Targetpath = str(target)
        shortcut.WorkingDirectory = str(Path.cwd())
        shortcut.IconLocation = str(icon_path)
        shortcut.Description = "Story Video Creator - Create narrated videos from text stories"
        shortcut.save()
        
        print(f"✅ Desktop shortcut created: {shortcut_path}")
        return True
        
    except ImportError:
        print("❌ pywin32 not available. Creating batch file instead...")
        return False
    except Exception as e:
        print(f"❌ Error creating shortcut: {e}")
        return False

def create_simple_launcher():
    """Create a simple launcher script"""
    desktop = Path.home() / "Desktop"
    launcher_path = desktop / "Story Video Creator.bat"
    
    current_dir = Path.cwd()
    
    launcher_content = f'''@echo off
cd /d "{current_dir}"
call launch_gui.bat
'''
    
    try:
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
        
        print(f"✅ Launcher created: {launcher_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating launcher: {e}")
        return False

def main():
    print("🔗 Creating Desktop Shortcut for Story Video Creator")
    print("=" * 50)
    
    if sys.platform == "win32":
        # Try to create a proper shortcut first
        if not create_windows_shortcut():
            # Fall back to simple batch file
            create_simple_launcher()
    else:
        print("⚠️  Desktop shortcut creation is currently only supported on Windows")
        print("You can manually create a shortcut to launch_gui.bat")
    
    print()
    print("To start the application:")
    print("1. Double-click the desktop shortcut (if created)")
    print("2. Or run: python story_video_gui.py")
    print("3. Or run: launch_gui.bat")

if __name__ == "__main__":
    main()
