# Speech Text Pipeline

speech_text_pipeline is a Python package that allows you to process audio files for automatic speech recognition (ASR), speaker diarization, and speaker matching. The package is designed to handle both cases with regular transcription with diarization and cases with transcription, diarization with speaker identification  where one speaker’s identity is known and provided via an additional audio sample.

## Installation

### Prerequisites

Install the following dependencies before install speech_text_pipeline:

- datasets 
- omegaconf 
- pyannote.audio 
- hydra-core
- git+https://github.com/openai/whisper.git
- git+https://github.com/NVIDIA/NeMo.git

### Main Package

Once the prerequisite packages are installed, you can install speech_text_pipeline using pip:

```bash
pip install speech_text_pipeline
```

## Usage

### HF_TOKEN for Speaker Matching

Before using the package you need to have access to 🤗 HuggingFace pyannote/embedding model for speaker matching functionality. Follow steps to get access of the model:

1. Log in to your 🤗 Hugging Face account and visit [pyannote/embedding model](https://huggingface.co/pyannote/embedding).

2. Request for access of the model(if not done already).

3. After getting access, generate your Hugging Face access token (HF_TOKEN) from Access Token tab in your account settings.

4. After generating token you use it in either of the two ways: 

    - CLI login:

    ```bash
    huggingface-cli login
    ```

    Then, input your `HF_TOKEN` when prompted.

    - In Code:

    Pass your `HF_TOKEN` directly to the transcribe function as a parameter:
    ```bash
    import speech_text_pipeline as stp

    result = stp.transcribe(audio="path_to_audio_file.wav", 
                            speaker_audio="path_to_known_speaker_audio.wav", 
                            HF_TOKEN="Your HF_TOKEN")
    ```
Note: The Hugging Face token is only required for the speaker matching functionality.

### Pipeline(anonymous speakers)

This mode generates a transcript with speaker diarization, assigning anonymous labels to speakers(e.g., "Speaker 1", "Speaker 2").

```bash
import speech_text_pipeline as stp

audio_url = "path_to_audio_file.wav"

result = stp.transcribe(audio=audio_url)
```
#### Get diarized transcript with anonymous speakers
```bash
print(result)
```
### Pipeline(named speakers)
```bash
import speech_text_pipeline as stp

audio_url = "path_to_audio_file.wav"

agent_audio_url = "path_to_agent_audio.wav" # Sample of the known speaker

result_with_speaker = stp.transcribe(audio=audio_url, 
                                    speaker_audio=agent_audio_url, 
                                    HF_TOKEN="Your HF_TOKEN") # Passing your geenrated Hugging Face token
```
#### Get diarized transcript with named speaker
```bash
print(result_with_speaker)
```