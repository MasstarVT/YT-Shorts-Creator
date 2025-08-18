#!/usr/bin/env python3
"""
Story Video Creator GUI
A user-friendly graphical interface for creating story videos with TTS
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import subprocess
import threading
from pathlib import Path

# Add the directory containing story_video_creator.py to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from story_video_creator import StoryVideoCreator


class StoryVideoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Story Video Creator - GUI")
        self.root.geometry("800x700")
        
        # Variables
        self.story_file_var = tk.StringVar()
        self.video_folder_var = tk.StringVar(value="backgrounds")
        self.output_file_var = tk.StringVar()
        self.piper_path_var = tk.StringVar(value="piper\\piper\\piper.exe")
        self.voice_model_var = tk.StringVar(value="voices\\en_US-lessac-high.onnx")
        self.progress_var = tk.StringVar(value="Ready to create videos!")
        self.add_subtitles_var = tk.BooleanVar(value=True)  # Subtitles enabled by default
        self.segment_video_var = tk.BooleanVar(value=False)  # Segmentation disabled by default
        self.segment_duration_var = tk.StringVar(value="30")  # Default 30 seconds
        self.estimated_duration_var = tk.StringVar(value="Select a story to see estimated duration")
        
        # Add trace to story file variable to update duration estimate
        self.story_file_var.trace_add("write", self.update_duration_estimate)
        self.segment_video_var.trace_add("write", self.update_duration_estimate)
        self.segment_duration_var.trace_add("write", self.update_duration_estimate)
        
        # Create GUI
        self.create_widgets()
        self.setup_defaults()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Main title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        title_label = ttk.Label(title_frame, text="🎬 Story Video Creator", 
                               font=("Arial", 16, "bold"))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Transform your stories into engaging videos with AI narration",
                                  font=("Arial", 10), foreground="gray")
        subtitle_label.pack()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tab 1: Basic Creation
        self.create_basic_tab()
        
        # Tab 2: Story Manager
        self.create_story_tab()
        
        # Tab 3: Settings
        self.create_settings_tab()
        
        # Progress and status
        self.create_status_area()
        
    def create_basic_tab(self):
        """Create the basic video creation tab"""
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text="Create Video")
        
        # Story file selection
        story_group = ttk.LabelFrame(basic_frame, text="1. Select Story", padding=10)
        story_group.pack(fill=tk.X, padx=10, pady=5)
        
        story_frame = ttk.Frame(story_group)
        story_frame.pack(fill=tk.X)
        
        ttk.Entry(story_frame, textvariable=self.story_file_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(story_frame, text="Browse", command=self.browse_story_file).pack(side=tk.RIGHT, padx=(5,0))
        ttk.Button(story_frame, text="Stories Folder", command=self.open_stories_folder).pack(side=tk.RIGHT, padx=(5,0))
        
        # Quick story selection
        quick_frame = ttk.Frame(story_group)
        quick_frame.pack(fill=tk.X, pady=(5,0))
        
        ttk.Label(quick_frame, text="Quick Select:").pack(side=tk.LEFT)
        self.story_combo = ttk.Combobox(quick_frame, state="readonly", width=40)
        self.story_combo.pack(side=tk.LEFT, padx=(5,0), fill=tk.X, expand=True)
        self.story_combo.bind("<<ComboboxSelected>>", self.on_story_selected)
        ttk.Button(quick_frame, text="Refresh", command=self.refresh_stories).pack(side=tk.RIGHT, padx=(5,0))
        
        # Duration estimate
        duration_frame = ttk.Frame(story_group)
        duration_frame.pack(fill=tk.X, pady=(5,0))
        
        ttk.Label(duration_frame, text="📊 Estimated Duration:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        self.duration_label = ttk.Label(duration_frame, textvariable=self.estimated_duration_var, 
                                       font=("Arial", 9), foreground="blue")
        self.duration_label.pack(side=tk.LEFT, padx=(5,0))
        
        # Video folder selection
        video_group = ttk.LabelFrame(basic_frame, text="2. Background Videos Folder", padding=10)
        video_group.pack(fill=tk.X, padx=10, pady=5)
        
        video_frame = ttk.Frame(video_group)
        video_frame.pack(fill=tk.X)
        
        ttk.Entry(video_frame, textvariable=self.video_folder_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(video_frame, text="Browse", command=self.browse_video_folder).pack(side=tk.RIGHT, padx=(5,0))
        
        # Output file selection
        output_group = ttk.LabelFrame(basic_frame, text="3. Output Video", padding=10)
        output_group.pack(fill=tk.X, padx=10, pady=5)
        
        output_frame = ttk.Frame(output_group)
        output_frame.pack(fill=tk.X)
        
        ttk.Entry(output_frame, textvariable=self.output_file_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse", command=self.browse_output_file).pack(side=tk.RIGHT, padx=(5,0))
        
        # Subtitle options
        subtitle_group = ttk.LabelFrame(basic_frame, text="4. Subtitle Options", padding=10)
        subtitle_group.pack(fill=tk.X, padx=10, pady=5)
        
        subtitle_frame = ttk.Frame(subtitle_group)
        subtitle_frame.pack(fill=tk.X)
        
        self.subtitle_check = ttk.Checkbutton(subtitle_frame, 
                                            text="Add white text subtitles to video", 
                                            variable=self.add_subtitles_var)
        self.subtitle_check.pack(side=tk.LEFT)
        
        ttk.Label(subtitle_frame, text="(Recommended for better accessibility)", 
                 font=("Arial", 8), foreground="gray").pack(side=tk.LEFT, padx=(10,0))
        
        # Segmentation options
        segment_group = ttk.LabelFrame(basic_frame, text="5. Video Segmentation", padding=10)
        segment_group.pack(fill=tk.X, padx=10, pady=5)
        
        segment_frame = ttk.Frame(segment_group)
        segment_frame.pack(fill=tk.X)
        
        self.segment_check = ttk.Checkbutton(segment_frame, 
                                           text="Split video into segments", 
                                           variable=self.segment_video_var,
                                           command=self.toggle_segment_options)
        self.segment_check.pack(side=tk.LEFT)
        
        # Duration selection frame (initially disabled)
        self.duration_frame = ttk.Frame(segment_group)
        self.duration_frame.pack(fill=tk.X, pady=(5,0))
        
        ttk.Label(self.duration_frame, text="Segment duration:").pack(side=tk.LEFT)
        
        duration_options = ["15", "30", "45", "60", "90", "120"]
        self.duration_combo = ttk.Combobox(self.duration_frame, textvariable=self.segment_duration_var, 
                                         values=duration_options, state="readonly", width=10)
        self.duration_combo.pack(side=tk.LEFT, padx=(5,0))
        self.duration_combo.bind("<<ComboboxSelected>>", self.update_duration_estimate)
        
        ttk.Label(self.duration_frame, text="seconds", font=("Arial", 8), foreground="gray").pack(side=tk.LEFT, padx=(5,0))
        ttk.Label(self.duration_frame, text="(Perfect for short social media clips)", 
                 font=("Arial", 8), foreground="gray").pack(side=tk.LEFT, padx=(10,0))
        
        # Initially disable duration options
        self.toggle_segment_options()
        
        # Create video button
        button_frame = ttk.Frame(basic_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_button = ttk.Button(button_frame, text="🎬 Create Video", 
                                       command=self.create_video, style="Accent.TButton")
        self.create_button.pack(side=tk.LEFT, padx=(0,5))
        
        ttk.Button(button_frame, text="Preview Audio Only", 
                  command=self.preview_audio).pack(side=tk.LEFT, padx=(5,0))
        
        # Info label
        info_label = ttk.Label(basic_frame, 
                              text="💡 Tip: Use the Story Manager tab to create and edit stories easily!",
                              font=("Arial", 9), foreground="gray")
        info_label.pack(pady=(0,5))
        
    def estimate_video_duration(self, text: str) -> tuple:
        """
        Estimate video duration based on text length and reading speed
        
        Args:
            text: The story text to analyze
            
        Returns:
            tuple: (duration_seconds, word_count, character_count)
        """
        # Clean the text and count words
        clean_text = text.strip()
        if not clean_text:
            return 0, 0, 0
            
        # Count words (split by whitespace and filter empty strings)
        words = [word for word in clean_text.split() if word.strip()]
        word_count = len(words)
        character_count = len(clean_text)
        
        # Average reading speed for TTS is about 150-180 words per minute
        # We'll use 160 WPM as a middle ground
        words_per_minute = 160
        
        # Calculate duration in seconds
        duration_seconds = (word_count / words_per_minute) * 60
        
        return duration_seconds, word_count, character_count
    
    def format_duration(self, seconds: float) -> str:
        """Format duration in seconds to a readable string"""
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f} minutes ({seconds:.0f} seconds)"
        else:
            hours = seconds / 3600
            minutes = (seconds % 3600) / 60
            return f"{hours:.1f} hours ({minutes:.0f} minutes)"
    
    def update_duration_estimate(self, *args):
        """Update the duration estimate when story file changes"""
        try:
            story_file = self.story_file_var.get()
            if not story_file or not os.path.exists(story_file):
                self.estimated_duration_var.set("Select a valid story to see estimated duration")
                return
            
            # Read the story file
            with open(story_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Calculate estimates
            duration, word_count, char_count = self.estimate_video_duration(text)
            
            if duration > 0:
                duration_str = self.format_duration(duration)
                segments_info = ""
                
                # Add segment information if segmentation is enabled
                if self.segment_video_var.get():
                    try:
                        segment_duration = int(self.segment_duration_var.get())
                        num_segments = max(1, int(duration / segment_duration))
                        if duration % segment_duration > 3:  # Only count if remainder > 3 seconds
                            num_segments += 1
                        segments_info = f" → {num_segments} segments of {segment_duration}s each"
                    except:
                        pass
                
                self.estimated_duration_var.set(f"{duration_str} | {word_count} words{segments_info}")
            else:
                self.estimated_duration_var.set("Story appears to be empty")
                
        except Exception as e:
            self.estimated_duration_var.set(f"Error reading story: {str(e)[:50]}...")
    
    def toggle_segment_options(self):
        """Enable/disable segment duration options based on checkbox"""
        state = "normal" if self.segment_video_var.get() else "disabled"
        
        # Enable/disable all widgets in duration frame
        for widget in self.duration_frame.winfo_children():
            if hasattr(widget, 'configure'):
                try:
                    widget.configure(state=state)
                except:
                    pass  # Some widgets might not support state configuration
        
        # Update duration estimate when segmentation is toggled
        self.update_duration_estimate()
    
    def browse_story_file(self):
        """Browse for story file"""
        filename = filedialog.askopenfilename(
            title="Select Story File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.story_file_var.set(filename)
    
    def browse_video_folder(self):
        """Browse for video folder"""
        folder = filedialog.askdirectory(title="Select Background Videos Folder")
        if folder:
            self.video_folder_var.set(folder)
    
    def browse_output_file(self):
        """Browse for output file"""
        filename = filedialog.asksaveasfilename(
            title="Save Video As",
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        if filename:
            self.output_file_var.set(filename)
    
    def open_stories_folder(self):
        """Open the stories folder"""
        stories_folder = Path("stories")
        if not stories_folder.exists():
            stories_folder.mkdir()
        
        if sys.platform == "win32":
            os.startfile(stories_folder)
        elif sys.platform == "darwin":
            subprocess.run(["open", str(stories_folder)])
        else:
            subprocess.run(["xdg-open", str(stories_folder)])
    
    def refresh_stories(self):
        """Refresh the stories dropdown"""
        stories_dir = Path("stories")
        if stories_dir.exists():
            stories = [f.name for f in stories_dir.glob("*.txt")]
            self.story_combo['values'] = stories
    
    def on_story_selected(self, event=None):
        """Handle story selection from dropdown"""
        selected = self.story_combo.get()
        if selected:
            story_path = Path("stories") / selected
            self.story_file_var.set(str(story_path))
            
            # Auto-generate output filename
            if not self.output_file_var.get():
                output_name = f"output/{story_path.stem}_video.mp4"
                self.output_file_var.set(output_name)
    
    def create_story_tab(self):
        """Create the story management tab"""
        story_frame = ttk.Frame(self.notebook)
        self.notebook.add(story_frame, text="Story Manager")
        
        # Instructions
        instructions = ttk.Label(story_frame, 
                                text="📝 Manage your story files. Create new stories or edit existing ones.",
                                font=("Arial", 10))
        instructions.pack(pady=10)
        
        # Story list
        list_frame = ttk.LabelFrame(story_frame, text="Available Stories", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # List with scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.story_listbox = tk.Listbox(list_container, yscrollcommand=scrollbar.set)
        self.story_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.story_listbox.yview)
        
        # Buttons
        button_frame = ttk.Frame(story_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="📄 New Story", command=self.new_story).pack(side=tk.LEFT, padx=(0,5))
        ttk.Button(button_frame, text="✏️ Edit Selected", command=self.edit_story).pack(side=tk.LEFT, padx=(5,5))
        ttk.Button(button_frame, text="🔄 Refresh", command=self.refresh_story_list).pack(side=tk.LEFT, padx=(5,5))
        ttk.Button(button_frame, text="📁 Open Stories Folder", command=self.open_stories_folder).pack(side=tk.LEFT, padx=(5,0))
        
        # Load stories
        self.refresh_story_list()
    
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Piper settings
        piper_group = ttk.LabelFrame(settings_frame, text="Piper TTS Settings", padding=10)
        piper_group.pack(fill=tk.X, padx=10, pady=5)
        
        # Piper path
        piper_frame = ttk.Frame(piper_group)
        piper_frame.pack(fill=tk.X, pady=(0,5))
        
        ttk.Label(piper_frame, text="Piper Executable:").pack(anchor=tk.W)
        path_frame = ttk.Frame(piper_frame)
        path_frame.pack(fill=tk.X, pady=(2,0))
        
        ttk.Entry(path_frame, textvariable=self.piper_path_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(path_frame, text="Browse", command=self.browse_piper_path).pack(side=tk.RIGHT, padx=(5,0))
        
        # Voice model
        voice_frame = ttk.Frame(piper_group)
        voice_frame.pack(fill=tk.X)
        
        ttk.Label(voice_frame, text="Voice Model:").pack(anchor=tk.W)
        model_frame = ttk.Frame(voice_frame)
        model_frame.pack(fill=tk.X, pady=(2,0))
        
        ttk.Entry(model_frame, textvariable=self.voice_model_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(model_frame, text="Browse", command=self.browse_voice_model).pack(side=tk.RIGHT, padx=(5,0))
        
        # Help section
        help_group = ttk.LabelFrame(settings_frame, text="Help & Information", padding=10)
        help_group.pack(fill=tk.X, padx=10, pady=5)
        
        help_text = tk.Text(help_group, height=15, wrap=tk.WORD)
        help_text.pack(fill=tk.BOTH, expand=True)
        
        help_content = """
🎬 Story Video Creator Help

GETTING STARTED:
1. Place your story text files in the 'stories' folder
2. Place background videos in the 'backgrounds' folder
3. Select a story and configure settings
4. Click 'Create Video' to generate your video

SUPPORTED VIDEO FORMATS:
- MP4, AVI, MOV, MKV, FLV, WMV, WebM

STORY FORMAT:
- Plain text files (.txt)
- UTF-8 encoding recommended
- No special formatting required

FEATURES:
- AI-powered text-to-speech narration
- Automatic subtitle generation
- Video segmentation for social media
- Multiple voice models available

TIPS:
- Longer stories = longer videos
- Use segmentation for social media posts
- Enable subtitles for better accessibility
- Check estimated duration before creating

For more information, check the README.md file.
"""
        
        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)
    
    def create_status_area(self):
        """Create status and progress area"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(0,5))
        
        # Status label
        status_label = ttk.Label(status_frame, textvariable=self.progress_var)
        status_label.pack()
    
    def setup_defaults(self):
        """Setup default values"""
        self.refresh_stories()
        
        # Set default output folder
        if not self.output_file_var.get():
            self.output_file_var.set("output/my_story_video.mp4")
    
    def create_video(self):
        """Create the story video"""
        # Validate inputs
        if not self.story_file_var.get():
            messagebox.showerror("Error", "Please select a story file")
            return
        
        if not self.video_folder_var.get():
            messagebox.showerror("Error", "Please select a video folder")
            return
        
        if not self.output_file_var.get():
            messagebox.showerror("Error", "Please specify an output file")
            return
        
        # Disable the create button
        self.create_button.config(state="disabled")
        self.progress_bar.start()
        self.progress_var.set("Creating video... This may take several minutes.")
        
        # Run in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self._create_video_thread)
        thread.daemon = True
        thread.start()
    
    def _create_video_thread(self):
        """Create video in separate thread"""
        try:
            # Create output directory
            output_path = Path(self.output_file_var.get())
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Determine segment duration
            segment_duration = None
            if self.segment_video_var.get():
                try:
                    segment_duration = int(self.segment_duration_var.get())
                except ValueError:
                    segment_duration = 30  # Default fallback
            
            # Create video
            creator = StoryVideoCreator(self.piper_path_var.get(), self.voice_model_var.get())
            
            result = creator.create_story_video(
                self.story_file_var.get(),
                self.video_folder_var.get(),
                self.output_file_var.get(),
                add_subtitles=self.add_subtitles_var.get(),
                segment_duration=segment_duration
            )
            
            # Update UI in main thread
            self.root.after(0, self._video_creation_success, result, segment_duration)
            
        except Exception as e:
            # Update UI in main thread
            self.root.after(0, self._video_creation_error, str(e))
    
    def _video_creation_success(self, result, segment_duration):
        """Handle successful video creation"""
        self.progress_bar.stop()
        self.progress_var.set("Video created successfully!")
        self.create_button.config(state="normal")
        
        # Success message with options
        if segment_duration:
            # Segmented video
            response = messagebox.askyesnocancel(
                "Success!", 
                f"Video segments created successfully in: {result}\n\nWould you like to:\nYes - Open segments folder\nNo - Open output folder\nCancel - Do nothing"
            )
            
            if response is True:  # Yes - open segments folder
                if sys.platform == "win32":
                    os.startfile(result)
                elif sys.platform == "darwin":
                    subprocess.run(["open", result])
                else:
                    subprocess.run(["xdg-open", result])
            elif response is False:  # No - open output folder
                output_folder = str(Path(result).parent)
                if sys.platform == "win32":
                    os.startfile(output_folder)
                elif sys.platform == "darwin":
                    subprocess.run(["open", output_folder])
                else:
                    subprocess.run(["xdg-open", output_folder])
        else:
            # Single video
            response = messagebox.askyesnocancel(
                "Success!", 
                f"Video created successfully: {result}\n\nWould you like to:\nYes - Open the video\nNo - Open output folder\nCancel - Do nothing"
            )
            
            if response is True:  # Yes - open video
                if sys.platform == "win32":
                    os.startfile(result)
                elif sys.platform == "darwin":
                    subprocess.run(["open", result])
                else:
                    subprocess.run(["xdg-open", result])
            elif response is False:  # No - open folder
                folder = str(Path(result).parent)
                if sys.platform == "win32":
                    os.startfile(folder)
                elif sys.platform == "darwin":
                    subprocess.run(["open", folder])
                else:
                    subprocess.run(["xdg-open", folder])
    
    def _video_creation_error(self, error_message):
        """Handle video creation error"""
        self.progress_bar.stop()
        self.progress_var.set("Error creating video")
        self.create_button.config(state="normal")
        
        messagebox.showerror("Error", f"Failed to create video:\n{error_message}")
    
    def preview_audio(self):
        """Preview the audio without creating video"""
        if not self.story_file_var.get():
            messagebox.showerror("Error", "Please select a story file first")
            return
        
        try:
            # Generate audio preview
            creator = StoryVideoCreator(self.piper_path_var.get(), self.voice_model_var.get())
            story_text = creator.read_story_file(self.story_file_var.get())
            
            # Create temporary audio file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_audio_path = temp_file.name
            
            creator.generate_audio_with_piper(story_text, temp_audio_path)
            
            # Play the audio
            if sys.platform == "win32":
                os.startfile(temp_audio_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", temp_audio_path])
            else:
                subprocess.run(["xdg-open", temp_audio_path])
            
            messagebox.showinfo("Audio Preview", f"Audio preview generated and opened.\nTemporary file: {temp_audio_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate audio preview:\n{e}")
    
    def browse_piper_path(self):
        """Browse for Piper executable"""
        filename = filedialog.askopenfilename(
            title="Select Piper Executable",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if filename:
            self.piper_path_var.set(filename)
    
    def browse_voice_model(self):
        """Browse for voice model file"""
        filename = filedialog.askopenfilename(
            title="Select Voice Model",
            filetypes=[("ONNX files", "*.onnx"), ("All files", "*.*")]
        )
        if filename:
            self.voice_model_var.set(filename)
    
    def new_story(self):
        """Create a new story"""
        # Simple story creation dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Story")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Story name
        name_frame = ttk.Frame(dialog)
        name_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(name_frame, text="Story Name:").pack(anchor=tk.W)
        name_var = tk.StringVar()
        ttk.Entry(name_frame, textvariable=name_var).pack(fill=tk.X, pady=(2,0))
        
        # Story content
        content_frame = ttk.Frame(dialog)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        ttk.Label(content_frame, text="Story Content:").pack(anchor=tk.W)
        
        text_frame = ttk.Frame(content_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(2,0))
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        story_text = tk.Text(text_frame, yscrollcommand=scrollbar.set, wrap=tk.WORD)
        story_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=story_text.yview)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        def save_story():
            name = name_var.get().strip()
            content = story_text.get("1.0", tk.END).strip()
            
            if not name:
                messagebox.showerror("Error", "Please enter a story name")
                return
            
            if not content:
                messagebox.showerror("Error", "Please enter story content")
                return
            
            # Create stories directory if it doesn't exist
            stories_dir = Path("stories")
            stories_dir.mkdir(exist_ok=True)
            
            # Save story file
            story_file = stories_dir / f"{name}.txt"
            try:
                with open(story_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                messagebox.showinfo("Success", f"Story saved as {story_file}")
                self.refresh_story_list()
                self.refresh_stories()
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save story: {e}")
        
        ttk.Button(button_frame, text="💾 Save Story", command=save_story).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="❌ Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=(5,0))
    
    def edit_story(self):
        """Edit selected story"""
        selection = self.story_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a story to edit")
            return
        
        story_name = self.story_listbox.get(selection[0])
        story_path = Path("stories") / story_name
        
        if not story_path.exists():
            messagebox.showerror("Error", f"Story file not found: {story_path}")
            return
        
        # Open story in default text editor
        if sys.platform == "win32":
            os.startfile(story_path)
        elif sys.platform == "darwin":
            subprocess.run(["open", story_path])
        else:
            subprocess.run(["xdg-open", story_path])
    
    def refresh_story_list(self):
        """Refresh the story list"""
        self.story_listbox.delete(0, tk.END)
        stories_dir = Path("stories")
        if stories_dir.exists():
            for story_file in stories_dir.glob("*.txt"):
                self.story_listbox.insert(tk.END, story_file.name)


def main():
    root = tk.Tk()
    app = StoryVideoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
