import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from faster_whisper import WhisperModel

model_size = "medium.en"
model = WhisperModel(
    model_size,
    device="cuda",
    compute_type="float16",
    download_root=os.path.join(os.path.dirname(__file__), "./models/download")
)

segments, info = model.transcribe("./output.wav", beam_size=7)
transcription = ' '.join(segment.text for segment in segments)

print(transcription)
