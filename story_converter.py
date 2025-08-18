#!/usr/bin/env python3
"""
Story Converter - Convert any text file to TTS-friendly format
Helps clean up existing stories for better TTS narration
"""

import os
import re
import sys
from pathlib import Path

def clean_text_for_tts(text):
    """Clean text to make it more TTS-friendly"""
    
    # Replace common abbreviations
    abbreviations = {
        r'\bDr\.': 'Doctor',
        r'\bMr\.': 'Mister',
        r'\bMrs\.': 'Missus',
        r'\bMs\.': 'Miss',
        r'\bProf\.': 'Professor',
        r'\bSt\.': 'Saint',
        r'\bAve\.': 'Avenue',
        r'\bRd\.': 'Road',
        r'\bBlvd\.': 'Boulevard',
        r'\betc\.': 'etcetera',
        r'\be\.g\.': 'for example',
        r'\bi\.e\.': 'that is',
        r'\bvs\.': 'versus',
        r'\bUSA': 'United States of America',
        r'\bUK': 'United Kingdom',
    }
    
    for abbrev, full in abbreviations.items():
        text = re.sub(abbrev, full, text, flags=re.IGNORECASE)
    
    # Convert numbers to words (basic ones)
    number_words = {
        r'\b0\b': 'zero', r'\b1\b': 'one', r'\b2\b': 'two', r'\b3\b': 'three',
        r'\b4\b': 'four', r'\b5\b': 'five', r'\b6\b': 'six', r'\b7\b': 'seven',
        r'\b8\b': 'eight', r'\b9\b': 'nine', r'\b10\b': 'ten', r'\b11\b': 'eleven',
        r'\b12\b': 'twelve', r'\b13\b': 'thirteen', r'\b14\b': 'fourteen',
        r'\b15\b': 'fifteen', r'\b16\b': 'sixteen', r'\b17\b': 'seventeen',
        r'\b18\b': 'eighteen', r'\b19\b': 'nineteen', r'\b20\b': 'twenty',
        r'\b30\b': 'thirty', r'\b40\b': 'forty', r'\b50\b': 'fifty',
        r'\b60\b': 'sixty', r'\b70\b': 'seventy', r'\b80\b': 'eighty',
        r'\b90\b': 'ninety', r'\b100\b': 'one hundred', r'\b1000\b': 'one thousand'
    }
    
    for num, word in number_words.items():
        text = re.sub(num, word, text)
    
    # Remove or replace problematic characters
    text = re.sub(r'[^\w\s\.,!?;:\'"()-]', '', text)  # Keep only safe characters
    
    # Fix spacing around punctuation
    text = re.sub(r'\s+([.!?])', r'\1', text)  # Remove space before punctuation
    text = re.sub(r'([.!?])\s+', r'\1 ', text)  # Ensure single space after punctuation
    
    # Clean up multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single space
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Clean up paragraph breaks
    
    # Ensure sentences end with proper punctuation
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line and not line[-1] in '.!?':
            line += '.'
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines).strip()

def convert_file(input_file, output_file=None):
    """Convert a text file to TTS-friendly format"""
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        return False
    
    try:
        # Read the original file
        with open(input_file, 'r', encoding='utf-8') as f:
            original_text = f.read()
        
        # Clean the text
        cleaned_text = clean_text_for_tts(original_text)
        
        # Determine output file
        if output_file is None:
            input_path = Path(input_file)
            output_file = f"stories/{input_path.stem}_cleaned.txt"
        
        # Ensure stories directory exists
        os.makedirs("stories", exist_ok=True)
        
        # Write cleaned text
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        
        print(f"✅ Converted: {input_file} -> {output_file}")
        
        # Show statistics
        orig_chars = len(original_text)
        clean_chars = len(cleaned_text)
        print(f"   Original: {orig_chars:,} characters")
        print(f"   Cleaned:  {clean_chars:,} characters")
        print(f"   Est. reading time: {len(cleaned_text.split()) // 150:.1f} minutes")
        
        return True
        
    except Exception as e:
        print(f"Error converting {input_file}: {e}")
        return False

def batch_convert():
    """Convert multiple files at once"""
    print("Batch Converter")
    print("-" * 20)
    
    folder = input("Enter folder path containing text files (or press Enter for current directory): ").strip()
    if not folder:
        folder = "."
    
    if not os.path.exists(folder):
        print(f"Error: Folder not found: {folder}")
        return
    
    # Find all text files
    text_files = []
    for ext in ['*.txt', '*.md', '*.rtf']:
        text_files.extend(Path(folder).glob(ext))
    
    if not text_files:
        print(f"No text files found in: {folder}")
        return
    
    print(f"Found {len(text_files)} text files:")
    for i, file in enumerate(text_files, 1):
        print(f"{i:2d}. {file.name}")
    
    choice = input(f"\nConvert all files? (y/N): ")
    if choice.lower() != 'y':
        return
    
    successful = 0
    for file in text_files:
        if convert_file(str(file)):
            successful += 1
    
    print(f"\n✅ Successfully converted {successful} out of {len(text_files)} files")

def interactive_convert():
    """Interactive single file conversion"""
    print("Single File Converter")
    print("-" * 20)
    
    input_file = input("Enter path to text file: ").strip()
    if not input_file:
        print("No file specified.")
        return
    
    # Remove quotes if present
    input_file = input_file.strip('"\'')
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        return
    
    # Ask for output name
    default_name = Path(input_file).stem + "_cleaned.txt"
    output_name = input(f"Enter output filename (default: {default_name}): ").strip()
    
    if not output_name:
        output_file = f"stories/{default_name}"
    else:
        if not output_name.endswith('.txt'):
            output_name += '.txt'
        output_file = f"stories/{output_name}"
    
    convert_file(input_file, output_file)

def main():
    print("=" * 50)
    print("    Story Video Creator - Story Converter")
    print("=" * 50)
    print("\nThis tool helps convert existing text files to TTS-friendly format.")
    print("It will:")
    print("- Replace abbreviations with full words")
    print("- Convert numbers to words")
    print("- Clean up punctuation and spacing")
    print("- Remove problematic characters")
    
    while True:
        print("\nOptions:")
        print("1. Convert single file")
        print("2. Batch convert multiple files")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            interactive_convert()
        elif choice == '2':
            batch_convert()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-3.")

if __name__ == "__main__":
    main()
