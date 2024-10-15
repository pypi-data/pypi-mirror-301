


# DSpeech: A Command-line Speech Processing Toolkit
DSpeech is an advanced command-line toolkit designed for speech processing tasks such as transcription, voice activity detection (VAD), punctuation addition, and emotion classification. It is built on top of state-of-the-art models and provides an easy-to-use interface for handling various speech processing jobs.
## Background
In recent years, the field of speech processing has seen rapid advancements with the development of deep learning techniques. However, many existing solutions are either too complex to set up or lack the flexibility required for different use cases. DSpeech aims to bridge this gap by providing a comprehensive, yet easy-to-use toolkit for speech processing tasks.
## Installation
### Prerequisites
- Python 3.6 or later
- PyTorch 1.7 or later
- torchaudio
- rich
- soundfile
- funasr (A lightweight AutoModel library for speech processing)
### Installation Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/dspeech.git
    cd dspeech
    ```
2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Set the `DSPEECH_HOME` environment variable to the directory where your models are stored:
    ```bash
    export DSPEECH_HOME=/path/to/dspeech/models
    ```
5. Download the necessary models and place them in the `DSPEECH_HOME` directory. You can download the models using the following commands (replace `<model_id>` with the actual model ID):
    ```bash
    export HF_ENDPOINT=https://hf-mirror.com
    huggingface-cli download --resume-download <model_id> --local-dir $DSPEECH_HOME/<model_name>
    ```

6. (Optional) Also you can install Dguard if you want to do the speaker diarization task:
    ```bash
    mkdir my_dguard && cd my_dguard
    git clone https://gitee.com/iint/wespeaker-nuaazs.git && cd wespeaker-nuaazs && pip install . -i https://pypi.tuna.tsinghua.edu.cn/simple && cd ..
    git clone https://gitee.com/iint/silero-vad-nuaazs.git && cd silero-vad-nuaazs && pip install . -i https://pypi.tuna.tsinghua.edu.cn/simple && cd ..
    pip install dguard@git+https://gitee.com/iint/dguard.git -i https://pypi.tuna.tsinghua.edu.cn/simple
    export DGUARD_MODEL_PATH=<path to dguard model home>
    dguard_info
    ```


## Features
DSpeech offers the following functionalities:
- **Transcription**: Convert audio files to text using state-of-the-art speech recognition models.
- **Voice Activity Detection (VAD)**: Detect and segment speech regions in an audio file.
- **Punctuation Addition**: Add punctuation to raw text transcriptions to improve readability.
- **Emotion Classification**: Classify the emotional content of an audio file into various categories.
## Python Demo
To use DSpeech in a Python script, you can import the `STT` class and create an instance with the desired models:

```python
from dspeech.stt import STT
# Initialize the STT handler with the specified models
handler = STT(model_name="paraformer-zh", vad_model="fsmn-vad", punc_model="ct-punc", emo_model="emotion2vec_plus_large")
# Transcribe an audio file
transcription = handler.transcribe_file("audio.wav")
print(transcription)
# Perform VAD on an audio file
vad_result = handler.vad_file("audio.wav")
print(vad_result)
# Add punctuation to a text
punctuation_text = handler.punc_result("this is a test")
print(punctuation_text)
# Perform emotion classification on an audio file
emotion_result = handler.emo_classify_file("audio.wav")
print(emotion_result)
```

## Command-line Interface
DSpeech provides a command-line interface for quick and easy access to its functionalities. To see the available commands, run:
```bash
dspeech help

DSpeech: A Command-line Speech Processing Toolkit
Usage: dspeech  
Commands:
  transcribe  Transcribe an audio file
  vad         Perform VAD on an audio file
  punc        Add punctuation to a text
  emo         Perform emotion classification on an audio file
Options:
  --model      Model name (default: sensevoicesmall)
  --vad-model  VAD model name (default: fsmn-vad)
  --punc-model Punctuation model name (default: ct-punc)
  --emo-model  Emotion model name (default: emotion2vec_plus_large)
  --device     Device to run the models on (default: cuda)
  --file       Audio file path for transcribing, VAD, or emotion classification
  --text       Text to process with punctuation model
  --start      Start time in seconds for processing audio files (default: 0)
  --end        End time in seconds for processing audio files (default: end of file)
  --sample-rate Sample rate of the audio file (default: 16000)
Example: dspeech transcribe --file audio.wav

```

### Usage Examples
- **Transcribe an audio file**:
    ```bash
    dspeech transcribe --file audio.wav
    ```
- **Perform VAD on an audio file**:
    ```bash
    dspeech vad --file audio.wav
    ```
- **Add punctuation to a text**:
    ```bash
    dspeech punc --text "this is a test"
    ```
- **Perform emotion classification on an audio file**:
    ```bash
    dspeech emo --file audio.wav
    ```

## License
DSpeech is licensed under the MIT License. See the LICENSE file for more details.

