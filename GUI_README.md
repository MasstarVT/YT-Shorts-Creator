# Story Video Creator GUI

🎬 **A User-Friendly Graphical Interface for Creating Story Videos**

## 🚀 Quick Start

### **Launch the GUI**
```bash
# Method 1: Double-click the launcher
launch_gui.bat

# Method 2: Command line
python story_video_gui.py

# Method 3: With virtual environment
.\.venv\Scripts\Activate.ps1; python story_video_gui.py
```

### **Create Your First Video**
1. **Launch the GUI** using one of the methods above
2. **Select a story** from the dropdown or browse for a file
3. **Choose background videos** folder (defaults to `backgrounds/`)
4. **Set output filename** (or let it auto-generate)
5. **Click "Create Video"** and wait for completion!

## 📱 GUI Features

### **🎬 Create Video Tab**
- **Story Selection**: Browse files or select from dropdown
- **Quick Access**: Direct buttons to open stories and backgrounds folders
- **Auto-naming**: Automatically generates output filenames
- **Progress Tracking**: Real-time progress bar and status updates
- **Preview Options**: Test audio before creating full video

### **📚 Manage Stories Tab**
- **Story List**: View all available stories with previews
- **Built-in Editor**: Create and edit stories directly in the GUI
- **Story Management**: Create, edit, delete stories with confirmation
- **Live Preview**: See story content and statistics
- **Character Counter**: Track story length and estimated reading time

### **⚙️ Settings Tab**
- **TTS Configuration**: Set Piper path and voice model
- **Quick Testing**: Test TTS with sample audio
- **Folder Management**: Quick access to all project folders
- **System Information**: Check if all components are working
- **Auto-detection**: Automatically finds installed components

## 🎯 GUI Components Guide

### **Main Interface**

#### **Story Selection**
```
Story File: [Browse] [Stories Folder]
Quick Select: [Dropdown] [Refresh]
```
- **Browse**: Select any `.txt` file from anywhere
- **Stories Folder**: Opens the `stories/` directory
- **Quick Select**: Choose from existing stories
- **Auto-complete**: Automatically sets output filename

#### **Video Settings**
```
Background Videos: [Browse] [Open Folder]
Output File: [Browse]
```
- **Background Videos**: Folder containing your video files
- **Output File**: Where to save the final video
- **Smart Defaults**: Uses `backgrounds/` and `output/` folders

#### **Action Buttons**
- **🎬 Create Video**: Main video creation button
- **Preview Audio Only**: Generate just the TTS audio
- **Progress Bar**: Shows creation progress

### **Story Management**

#### **Story List**
- **Double-click**: Select story for main creation
- **Preview Pane**: See story content and statistics
- **Management Buttons**: Create, Edit, Delete stories

#### **Story Editor**
```
Title: [Story Name]
Content: [Large text area]
[Save] [Cancel]
Status: Characters: 1234 | Words: 567 | Est. time: 3.8 min
```
- **Real-time Stats**: Character/word count and estimated reading time
- **Auto-save Names**: Converts titles to safe filenames
- **Validation**: Ensures title and content are provided

### **Settings Panel**

#### **Piper TTS Settings**
```
Piper Executable: [path] [Browse]
Voice Model: [path] [Browse]
[Test TTS]
```
- **Auto-detection**: Finds Piper in default locations
- **Test Function**: Generates sample audio to verify setup
- **Voice Models**: Supports all Piper `.onnx` voice files

#### **System Information**
```
✅ Piper TTS: Found at piper\piper\piper.exe
✅ Voice Model: Found at voices\en_US-lessac-high.onnx
✅ MoviePy: Available
✅ Stories folder: 5 files
✅ Backgrounds folder: 2 files
✅ Output folder: 3 files
```

## 🔧 Advanced Features

### **Threading and Progress**
- **Non-blocking Operations**: GUI remains responsive during video creation
- **Real-time Updates**: Progress bar and status messages
- **Error Handling**: Clear error messages with troubleshooting hints

### **Smart File Management**
- **Auto-directory Creation**: Creates missing folders automatically
- **File Validation**: Checks for required files before starting
- **Output Management**: Handles overwrite confirmations

### **Keyboard Shortcuts**
- **Ctrl+S**: Save story (in editor)
- **Enter**: Confirm dialogs
- **Escape**: Cancel operations

## 🎨 Customization

### **Themes and Appearance**
The GUI automatically selects the best available theme:
- **Windows 10/11**: Modern clam theme
- **Other Systems**: Alt theme fallback
- **Custom Styling**: Accent buttons and professional layout

### **Window Management**
- **Resizable Interface**: Minimum 600x500, scales to your screen
- **Tab Organization**: Logical grouping of features
- **Modal Dialogs**: Story editor and confirmations

## 🚀 Tips for Best Experience

### **Story Writing in GUI**
1. **Use the built-in editor** for TTS-optimized writing
2. **Watch the character counter** to gauge video length
3. **Preview audio first** to test narration quality
4. **Save frequently** to avoid losing work

### **Efficient Workflow**
1. **Organize stories** in the stories folder
2. **Prepare background videos** in advance
3. **Use descriptive filenames** for easy organization
4. **Test TTS settings** before bulk creation

### **Troubleshooting**
- **Check System Info**: Settings tab shows component status
- **Test TTS**: Use the test function to verify Piper setup
- **Folder Access**: Use "Open Folder" buttons to verify paths
- **Progress Monitoring**: Watch status messages for details

## 📁 File Organization

### **Recommended Structure**
```
YT Sorts Creater/
├── story_video_gui.py          # Main GUI application
├── launch_gui.bat              # Easy launcher
├── stories/                    # Your story files
│   ├── adventure.txt
│   ├── mystery.txt
│   └── reddit_story.txt
├── backgrounds/                # Background videos
│   ├── minecraft_gameplay.mp4
│   └── subway_surfers.mp4
├── output/                     # Generated videos
│   ├── adventure_video.mp4
│   └── mystery_video.mp4
├── piper/                      # Piper TTS
└── voices/                     # Voice models
```

### **Automatic Folder Creation**
The GUI automatically creates these folders if they don't exist:
- `stories/` - For your text files
- `backgrounds/` - For background videos  
- `output/` - For generated videos

## 🔗 Integration with Command Line

The GUI is fully compatible with the command-line version:
- **Same backend**: Uses the same `StoryVideoCreator` class
- **Same settings**: Piper paths and voice models work in both
- **Same output**: Generated videos are identical
- **File compatibility**: Stories created in GUI work with CLI and vice versa

## 🎯 Getting Started Checklist

- [ ] **Launch GUI**: Run `python story_video_gui.py`
- [ ] **Check Settings**: Verify Piper TTS and voice model paths
- [ ] **Test TTS**: Use the test function to confirm audio works
- [ ] **Add Background Videos**: Copy video files to `backgrounds/` folder
- [ ] **Create/Import Stories**: Use built-in editor or import existing files
- [ ] **Create First Video**: Select story, set output, click Create Video
- [ ] **Verify Output**: Check the generated video in your output folder

The GUI makes it incredibly easy to create professional story videos without any command-line knowledge! 🎥✨
