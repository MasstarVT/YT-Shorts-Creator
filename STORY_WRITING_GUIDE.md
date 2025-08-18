# Story Writing Guide for TTS Videos

## 📖 **How to Write Stories for Your Video Creator**

### **📁 Where to Put Your Stories**
- Save all story files in the `stories/` folder
- Use `.txt` format (plain text files)
- Name files descriptively: `my_adventure.txt`, `funny_story.txt`, etc.

### **✍️ Writing Tips for TTS (Text-to-Speech)**

#### **1. Use Simple, Clear Language**
- **Good**: "Sarah walked slowly down the old, creaky stairs."
- **Avoid**: "Sarah descended the antiquated, dilapidated staircase."

#### **2. Write Natural Dialogue**
- Use contractions: "don't", "can't", "won't"
- Include natural pauses with commas and periods
- **Good**: "I can't believe it," she whispered. "This is amazing."

#### **3. Include Natural Pacing**
- Use periods for full stops
- Use commas for brief pauses
- Use paragraph breaks for longer pauses
- **Example**:
  ```
  Emma opened the door slowly.
  
  Inside, she found something incredible.
  ```

#### **4. Avoid Complex Formatting**
- No special characters: @, #, %, &, etc.
- No abbreviations: write "Doctor" not "Dr."
- No numbers: write "twenty-five" not "25"
- Spell out everything: "Mister Smith" not "Mr. Smith"

#### **5. Consider Audio Length**
- **Short stories**: 150-300 words (1-2 minutes)
- **Medium stories**: 300-600 words (2-4 minutes)
- **Long stories**: 600+ words (4+ minutes)

### **📝 Story Structure Templates**

#### **Adventure Story Template**
```
[Character] was [doing something ordinary] when [unexpected event].

[Character] decided to [take action]. [Describe the journey/challenge].

[Obstacles and difficulties]. [How character overcomes them].

[Resolution and what character learned].
```

#### **Mystery Story Template**
```
[Something strange happens]. [Character investigates].

[Clues are discovered]. [Red herrings and false leads].

[The truth is revealed]. [Surprising but logical explanation].

[Resolution and character's reaction].
```

#### **Fantasy Story Template**
```
[Character in ordinary world]. [Discovery of magical element].

[Character enters magical situation]. [Rules of magic explained].

[Challenge using magic]. [Character learns important lesson].

[Return to ordinary world, changed].
```

### **🎯 Example Story Formats**

#### **Children's Story (150 words)**
```
The Little Robot's Big Day

Beep was the smallest robot in the factory. Every day, he watched the big robots do important work while he could only sweep floors.

One morning, the factory's main computer broke down. All the big robots stopped working. The humans looked worried.

But Beep was so small, he could crawl inside the computer through a tiny opening. He found a loose wire and connected it back.

Suddenly, all the lights came back on. The big robots started working again. Everyone cheered for Beep.

From that day on, Beep knew that being small was actually his superpower. Sometimes the smallest helpers can make the biggest difference.
```

#### **Adult Story (400 words)**
```
The Time Traveler's Café

Margaret had run the corner café for thirty years, serving the same regular customers coffee and pastries every morning. She thought she knew everyone in the neighborhood.

Then a strange man in an old-fashioned coat began visiting every Tuesday at exactly nine-fifteen. He always ordered black coffee and a plain croissant, paid with exact change, and left no tip.

What puzzled Margaret was that he seemed to know things before they happened. He would smile sadly when Mrs. Henderson ordered her usual before she announced her husband's passing the next week. He would nod knowingly when young Tom discussed his job interview before Tom even mentioned applying.

One Tuesday, Margaret decided to ask him directly. "Excuse me," she said, refilling his coffee. "I hope you don't mind me asking, but how do you always seem to know what's going to happen?"

The man looked up with kind but tired eyes. "I've been visiting this café for a very long time," he said quietly. "Longer than you might believe."

"But I've only seen you for a few months," Margaret replied.

He smiled gently. "Time doesn't always move the way we think it does. I come here because this place, your kindness, it's been a constant in many different versions of this week."

Margaret stared at him, not quite understanding but somehow believing. "Are you from the future?"

"I'm from many futures," he said, standing and placing exact change on the table. "And in every one of them, your café is the brightest spot in this neighborhood. Thank you for that."

He walked to the door, then turned back. "Tomorrow, wear the blue dress. Trust me."

The next morning, Margaret wore her blue dress. A famous food critic, who happened to love that particular shade of blue, visited her café and wrote a glowing review that changed her life forever.

She never saw the strange man again, but every Tuesday at nine-fifteen, she set out an extra cup of black coffee and a plain croissant, just in case.
```

### **🔧 Tools to Help You**

#### **Use the Story Manager**
```bash
python story_manager.py
```
This tool helps you:
- Create new stories with guided prompts
- Preview existing stories
- See statistics about your stories
- Generate video commands

#### **Test Your Stories**
```bash
# Test with Piper TTS only (no video)
echo "Your story text here" | piper\piper\piper.exe -m voices\en_US-lessac-high.onnx -f test.wav
```

### **📋 Pre-Writing Checklist**

Before writing your story, ask yourself:
- [ ] Who is my main character?
- [ ] What is the main event or conflict?
- [ ] How will it be resolved?
- [ ] What is the lesson or message?
- [ ] Is the language simple and clear?
- [ ] Will this sound good when spoken aloud?

### **🎬 Creating Videos from Your Stories**

Once your story is written:

1. **Save** your story as a `.txt` file in the `stories/` folder
2. **Add background videos** to the `backgrounds/` folder
3. **Create your video**:
   ```bash
   python story_video_creator.py "stories/your_story.txt" backgrounds/ "your_video.mp4" --piper-path "piper\piper\piper.exe" --voice-model "voices\en_US-lessac-high.onnx"
   ```

### **💡 Pro Tips**

- **Read aloud**: Read your story out loud before converting to check flow
- **Keep paragraphs short**: Easier for TTS to handle
- **Use active voice**: "Sarah opened the door" vs "The door was opened by Sarah"
- **Test different lengths**: See what works best for your content
- **Consider your audience**: Adjust complexity and themes accordingly

Start with the example stories in the `stories/` folder, then create your own masterpieces!
