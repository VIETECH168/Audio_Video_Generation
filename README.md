
# Video Processing Pipeline

## Overview

This project provides a comprehensive pipeline to process videos by extracting audio, converting speech to text, translating text into Vietnamese, and integrating the translated audio back into the original video. The final output is an edited video with a Vietnamese voice-over.

## Features

- Extract audio from video files.
- Transcribe audio to text using silence detection.
- Translate English text to Vietnamese.
- Convert Vietnamese text to audio.
- Integrate new audio back into the original video.
- Handle multiple video formats (e.g., .mp4, .avi, .mov).

## Directory Structure

```
.
├── Input Video/                # Folder containing input video files
├── Output Video/               # Folder for output files
│   ├── audio/                  # Folder for generated audio files
│   ├── transcript/             # Folder for generated transcripts
│   └── edited/                 # Folder for edited videos
├── function/                   # Folder containing utility functions
├── main.py                     # Main script for the pipeline
└── README.md                   # Documentation file
```

## Requirements

- Python 3.8 or later

### Libraries:
- os
- moviepy
- speech_recognition
- gtts

Custom functions (included in `function/`)

Install dependencies with:

```
pip install moviepy speechrecognition gtts
```

## Usage

### 1. Prepare Input Files

Place your video files in the `Input Video/` directory.

Supported formats: `.mp4`, `.avi`, `.mov`.

### 2. Run the Pipeline

Execute the main script:

```
python main.py
```

### 3. Output Files

- **Transcripts**: Located in `Output Video/transcript/`.

  - `<video_name>_english.txt` for English transcripts.
  - `<video_name>_vietnamese.txt` for Vietnamese translations.

- **Audio**: Located in `Output Video/audio/`.

  - `<video_name>_audio.mp3` for Vietnamese voice-over.

- **Edited Video**: Located in `Output Video/`.

  - `<video_name>_edited.mp4` is the final video with integrated Vietnamese audio.

### Example Workflow

- **Input Video**: `Input Video/Self-Healing Metal.mp4`
- **Output Transcripts**:
  - `Output Video/transcript/Self-Healing Metal_english.txt`
  - `Output Video/transcript/Self-Healing Metal_vietnamese.txt`
- **Generated Audio**: `Output Video/audio/Self-Healing Metal_audio.mp3`
- **Final Video**: `Output Video/Self-Healing Metal_edited.mp4`

## Error Handling

- If the `Input Video/` folder does not exist, the program will prompt an error.
- Unsupported file formats will be skipped.
- Missing transcript files will raise a `FileNotFoundError`.

## Future Enhancements

- Support for additional languages.
- Improved error handling and logging.
- Enhanced transcription accuracy with advanced models.
- Integration with cloud-based translation APIs for better results.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

Developed by [VieAI]
